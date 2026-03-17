from __future__ import annotations

from typing import Iterable

import numpy as np


def summarize_event_window(returns: Iterable[float]) -> dict:
    arr = np.array(list(returns), dtype=float)
    if arr.size == 0:
        raise ValueError('returns cannot be empty')
    curve = np.cumprod(1 + arr)
    drawdown = curve / np.maximum.accumulate(curve) - 1
    cum = np.prod(1 + arr) - 1
    return {
        'mean_return': float(np.mean(arr)),
        'median_return': float(np.median(arr)),
        'win_rate': float(np.mean(arr > 0)),
        'volatility': float(np.std(arr)),
        'max_drawdown': float(np.min(drawdown)),
        'cumulative_return': float(cum),
        'p10': float(np.percentile(arr, 10)),
        'p90': float(np.percentile(arr, 90)),
    }
