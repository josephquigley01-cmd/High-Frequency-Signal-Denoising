import numpy as np
import pywt
from typing import List

def denoise_signal_1d(signal: np.ndarray, wavelet: str = 'db4', level: int = 4) -> np.ndarray:
    """
    Applies 1D Discrete Wavelet Transform (DWT) to filter high-frequency noise
    out of a 1D data stream using Soft Thresholding.
    
    Args:
        signal (np.ndarray): The raw 1D time-series data.
        wavelet (str): The wavelet basis to use (e.g., 'db4', 'haar', 'sym8').
        level (int): The number of decomposition levels.
        
    Returns:
        np.ndarray: The reconstructed, denoised 1D signal.
    """
    print(f"[*] Decomposing signal using 1D DWT (Wavelet: {wavelet}, Level: {level})...")
    
    # Step 1: Decompose the 1D signal into Approximation and Detail coefficients
    coeffs: List[np.ndarray] = pywt.wavedec(signal, wavelet, mode='per', level=level)
    
    # Step 2: Calculate Universal Threshold using Median Absolute Deviation (MAD)
    # The noise variance is estimated from the finest detail coefficients (last element)
    sigma = np.median(np.abs(coeffs[-1] - np.median(coeffs[-1]))) / 0.6745
    threshold = sigma * np.sqrt(2 * np.log(len(signal)))
    
    print(f"[*] Applying soft thresholding (Universal Threshold: {threshold:.4f})...")
    # Step 3: Apply Soft Thresholding to the Detail Coefficients (sub-bands)
    # The Approximation band (coeffs[0]) is kept intact to preserve macro trends
    thresholded_coeffs = [coeffs[0]]
    for cD in coeffs[1:]:
        thresholded_coeffs.append(pywt.threshold(cD, value=threshold, mode='soft'))
        
    # Step 4: Reconstruct the clean signal using 1D Inverse DWT
    print("[*] Reconstructing clean signal via Inverse DWT...")
    clean_signal = pywt.waverec(thresholded_coeffs, wavelet, mode='per')
    
    # Ensure reconstructed array strictly matches the original length
    return clean_signal[:len(signal)]