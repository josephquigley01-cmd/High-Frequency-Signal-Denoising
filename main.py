import os
import matplotlib.pyplot as plt
from src.data_loader import fetch_1d_signal
from src.wavelets import denoise_signal_1d

def main():
    ticker = "TSLA"
    
    # 1. Load Data
    raw_signal = fetch_1d_signal(ticker=ticker, period="5d", interval="1m")
    
    # 2. Apply Denoising
    smoothed_signal = denoise_signal_1d(raw_signal, wavelet='db4', level=4)
    
    # 3. Visualize and Save Results
    plt.figure(figsize=(14, 6))
    plt.plot(raw_signal, color='#b0bec5', label=f'{ticker} Original Volatile Signal (Raw Ticks)', alpha=0.9, linewidth=1.5)
    plt.plot(smoothed_signal, color='#1e88e5', label='Denoised Signal (1D DWT)', linewidth=2.5)
    
    plt.title(f"High-Frequency Signal Denoising: {ticker}", fontsize=16, fontweight='bold')
    plt.xlabel("Time (Ticks)", fontsize=12)
    plt.ylabel("Asset Price (USD)", fontsize=12)
    plt.legend(loc="upper left", fontsize=11)
    plt.grid(True, linestyle='--', alpha=0.4)
    plt.tight_layout()
    
    # Save the plot for the README
    os.makedirs('assets', exist_ok=True)
    save_path = 'assets/denoising_plot.png'
    plt.savefig(save_path, dpi=300)
    print(f"[*] Execution complete. Visualization saved to '{save_path}'.")
    plt.show()

if __name__ == "__main__":
    main()