"""
Mathematical Utilities

Common mathematical functions and calculations for economic modeling.
"""

import numpy as np
from typing import List, Union, Optional
import logging

logger = logging.getLogger(__name__)


def moving_average(data: List[float], window: int) -> List[float]:
    """
    Calculate moving average with specified window size.
    
    Args:
        data: Input data series
        window: Window size for moving average
        
    Returns:
        List of moving averages
    """
    if window <= 0:
        raise ValueError("Window size must be positive")
    
    if len(data) < window:
        logger.warning(f"Data length ({len(data)}) is less than window size ({window})")
        return [np.mean(data)] * len(data)
    
    result = []
    for i in range(len(data)):
        if i < window - 1:
            # For early periods, use available data
            result.append(np.mean(data[:i+1]))
        else:
            # Calculate moving average for full window
            result.append(np.mean(data[i-window+1:i+1]))
    
    return result


def exponential_decay(initial_value: float, decay_rate: float, periods: int) -> List[float]:
    """
    Calculate exponential decay series.
    
    Args:
        initial_value: Starting value
        decay_rate: Decay rate per period (0 < decay_rate < 1)
        periods: Number of periods
        
    Returns:
        List of decayed values
    """
    if not 0 < decay_rate < 1:
        raise ValueError("Decay rate must be between 0 and 1")
    
    return [initial_value * (decay_rate ** t) for t in range(periods)]


def compound_growth(initial_value: float, growth_rate: float, periods: int) -> List[float]:
    """
    Calculate compound growth series.
    
    Args:
        initial_value: Starting value
        growth_rate: Growth rate per period
        periods: Number of periods
        
    Returns:
        List of compounded values
    """
    return [initial_value * ((1 + growth_rate) ** t) for t in range(periods)]


def calculate_statistics(data: List[float]) -> dict:
    """
    Calculate descriptive statistics for a data series.
    
    Args:
        data: Input data series
        
    Returns:
        Dictionary with statistical measures
    """
    if not data:
        return {}
    
    np_data = np.array(data)
    
    return {
        'mean': float(np.mean(np_data)),
        'median': float(np.median(np_data)),
        'std': float(np.std(np_data)),
        'min': float(np.min(np_data)),
        'max': float(np.max(np_data)),
        'q25': float(np.percentile(np_data, 25)),
        'q75': float(np.percentile(np_data, 75)),
        'range': float(np.max(np_data) - np.min(np_data)),
        'count': len(data)
    }


def normalize_series(data: List[float], method: str = 'minmax') -> List[float]:
    """
    Normalize a data series.
    
    Args:
        data: Input data series
        method: Normalization method ('minmax' or 'zscore')
        
    Returns:
        Normalized data series
    """
    if not data:
        return []
    
    np_data = np.array(data)
    
    if method == 'minmax':
        min_val = np.min(np_data)
        max_val = np.max(np_data)
        if max_val == min_val:
            return [0.0] * len(data)
        return ((np_data - min_val) / (max_val - min_val)).tolist()
    
    elif method == 'zscore':
        mean_val = np.mean(np_data)
        std_val = np.std(np_data)
        if std_val == 0:
            return [0.0] * len(data)
        return ((np_data - mean_val) / std_val).tolist()
    
    else:
        raise ValueError(f"Unknown normalization method: {method}")


def interpolate_missing(data: List[Optional[float]], method: str = 'linear') -> List[float]:
    """
    Interpolate missing values in a data series.
    
    Args:
        data: Input data with possible None values
        method: Interpolation method ('linear', 'forward_fill', 'backward_fill')
        
    Returns:
        Data series with interpolated values
    """
    if not data:
        return []
    
    # Convert to numpy array, handling None values
    valid_indices = [i for i, x in enumerate(data) if x is not None]
    valid_values = [data[i] for i in valid_indices]
    
    if not valid_values:
        raise ValueError("No valid values found for interpolation")
    
    result = data.copy()
    
    if method == 'linear':
        # Linear interpolation
        for i in range(len(data)):
            if data[i] is None:
                # Find surrounding valid values
                prev_idx = None
                next_idx = None
                
                for j in range(i-1, -1, -1):
                    if data[j] is not None:
                        prev_idx = j
                        break
                
                for j in range(i+1, len(data)):
                    if data[j] is not None:
                        next_idx = j
                        break
                
                if prev_idx is not None and next_idx is not None:
                    # Interpolate between two points
                    weight = (i - prev_idx) / (next_idx - prev_idx)
                    result[i] = data[prev_idx] + weight * (data[next_idx] - data[prev_idx])
                elif prev_idx is not None:
                    # Use previous value
                    result[i] = data[prev_idx]
                elif next_idx is not None:
                    # Use next value
                    result[i] = data[next_idx]
    
    elif method == 'forward_fill':
        last_valid = None
        for i in range(len(data)):
            if data[i] is not None:
                last_valid = data[i]
            elif last_valid is not None:
                result[i] = last_valid
    
    elif method == 'backward_fill':
        next_valid = None
        for i in range(len(data)-1, -1, -1):
            if data[i] is not None:
                next_valid = data[i]
            elif next_valid is not None:
                result[i] = next_valid
    
    else:
        raise ValueError(f"Unknown interpolation method: {method}")
    
    # Handle any remaining None values
    for i in range(len(result)):
        if result[i] is None:
            result[i] = valid_values[0] if valid_values else 0.0
    
    return result 