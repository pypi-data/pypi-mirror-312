import warnings

import numpy as np

from ..._auxlib._bitlen32_batched import bitlen32_batched
from ..._auxlib._bitlen32_scalar import bitlen32_scalar
from ..._auxlib._bitwise_count64_batched import bitwise_count64_batched
from ..._auxlib._jit import jit


def steady_lookup_ingest_times_batched(
    S: int,
    T: np.ndarray,
    parallel: bool = True,
) -> np.ndarray:
    """Ingest time lookup algorithm for steady curation.

    Parameters
    ----------
    S : int
        Buffer size. Must be a power of two.
    T : np.ndarray
        One-dimensional array of current logical times.
    parallel : bool, default True
        Should numba be applied to parallelize operations?

    Returns
    -------
    np.ndarray
        Ingest time of stored items at buffer sites in index order.

        Two-dimensional array. Each row corresponds to an entry in T. Contains
        S columns, each corresponding to buffer sites.
    """
    assert np.issubdtype(np.asarray(S).dtype, np.integer), S
    assert np.issubdtype(T.dtype, np.integer), T

    if (T < S).any():
        raise ValueError("T < S not supported for batched lookup")

    if parallel:
        if S <= 2**8:  # limit to 2**8 to control jit workload
            return _steady_lookup_ingest_times_batched_jit(
                np.int64(S), T.astype(np.int64)
            )  # cast to make numba happy, improve caching
        else:
            warnings.warn(
                "Falling back to serial processing for S > 256, "
                "to prevent excessive jit workload.",
            )

    return _steady_lookup_ingest_times_batched(S, T)


def _steady_lookup_ingest_times_batched(
    S: int,
    T: np.ndarray,
) -> np.ndarray:
    """Implementation detail for steady_lookup_ingest_times_batched."""
    assert np.logical_and(
        np.asarray(S) > 1,
        bitwise_count64_batched(np.atleast_1d(np.asarray(S)).astype(np.uint64))
        == 1,
    ).all(), S
    # restriction <= 2 ** 52 (bitlen32 precision) might be overly conservative
    assert (np.maximum(S, T) <= 2**52).all()

    s = np.asarray(bitlen32_scalar(S), np.int64) - 1
    t = bitlen32_batched(T).astype(np.int64) - s  # Current epoch

    b = 0  # Bunch physical index (left-to right)
    m_b__ = 1  # Countdown on segments traversed within bunch
    b_star = True  # Have traversed all segments in bunch?
    k_m__ = s + 1  # Countdown on sites traversed within segment

    res = np.empty((T.size, S), dtype=T.dtype)
    for k in range(S):  # Iterate over buffer sites, except unused last one
        # Calculate info about current segment...
        epsilon_w = b == 0  # Correction on segment width if first segment
        # Number of sites in current segment (i.e., segment size)
        w = s - b + epsilon_w
        m = (1 << b) - m_b__  # Calc left-to-right index of current segment
        h_max = t + w - 1  # Max possible hanoi value in segment during epoch

        # Calculate candidate hanoi value...
        h_ = h_max - (h_max + k_m__) % w

        # Decode ingest time of assigned h.v. from segment index g, ...
        # ... i.e., how many instances of that h.v. seen before
        T_bar_k_ = ((2 * m + 1) << h_) - 1  # Guess ingest time
        epsilon_h = (T_bar_k_ >= T) * w  # Correction on h.v. if not yet seen
        h = h_ - epsilon_h  # Corrected true resident h.v.
        T_bar_k = ((2 * m + 1) << h) - 1  # True ingest time
        res[:, k] = T_bar_k

        # Update within-segment state for next site...
        k_m__ = (k_m__ or w) - 1  # Bump to next site within segment

        # Update h for next site...
        # ... only needed if not calculating h fresh every iter [[see above]]
        h_ += 1 - (h_ >= h_max) * w

        # Update within-bunch state for next site...
        m_b__ -= not k_m__  # Bump to next segment within bunch
        b_star = not (m_b__ or k_m__)  # Should bump to next bunch?
        b += b_star  # Do bump to next bunch, if any
        # Set within-bunch segment countdown, if bumping to next bunch
        m_b__ = m_b__ or (1 << (b - 1))

    return res


_steady_lookup_ingest_times_batched_jit = jit(
    nogil=True, nopython=True, parallel=True
)(_steady_lookup_ingest_times_batched)

# lazy loader workaround
lookup_ingest_times_batched = steady_lookup_ingest_times_batched
