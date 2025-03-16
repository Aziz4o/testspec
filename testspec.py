import numpy as np
import matplotlib.pyplot as plt
import adi

# Parameters
sample_rate = 1e6  # Sample rate in Hz
center_freq = 100e6  # Center frequency in Hz
num_samples = 1024  # Number of samples to capture
fft_size = 1024  # FFT size

# Create PlutoSDR instance
sdr = adi.Pluto()

# Configure PlutoSDR
sdr.sample_rate = int(sample_rate)
sdr.rx_rf_bandwidth = int(sample_rate)
sdr.rx_lo = int(center_freq)
sdr.rx_buffer_size = num_samples

# Capture data
data = sdr.rx()

# Perform FFT
spectrum = np.fft.fftshift(np.fft.fft(data, fft_size))
freq = np.fft.fftshift(np.fft.fftfreq(fft_size, d=1/sample_rate))

# Plot the spectrum
plt.figure()
plt.plot(freq, 20 * np.log10(np.abs(spectrum)))
plt.title("Spectrum Analyzer")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude (dB)")
plt.grid()
plt.show()
