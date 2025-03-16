import numpy as np
import matplotlib.pyplot as plt
import adi
import time

# Create PlutoSDR instance
sdr = adi.Pluto('ip:192.168.2.1')  # Replace with your PlutoSDR's IP if necessary

# Configure PlutoSDR
sample_rate = 1e6  # Sample rate in Hz
center_freq = 100e6  # Center frequency in Hz
num_samples = 1024  # Number of samples per frame
fft_size = 1024  # FFT size

sdr.sample_rate = int(sample_rate)
sdr.rx_rf_bandwidth = int(sample_rate)
sdr.rx_lo = int(center_freq)
sdr.rx_buffer_size = num_samples

# Initialize plot
plt.ion()  # Enable interactive mode
fig, ax = plt.subplots()
line, = ax.plot(np.zeros(fft_size))
ax.set_ylim(-100, 0)  # Set y-axis limits for dB scale
ax.set_xlabel("Frequency (Hz)")
ax.set_ylabel("Magnitude (dB)")
ax.set_title("Real-Time Spectrum Analyzer")

# Frequency axis
freq = np.fft.fftshift(np.fft.fftfreq(fft_size, d=1/sample_rate))
ax.set_xlim(freq[0], freq[-1])  # Set x-axis limits to frequency range

# Real-time spectrum analysis
try:
    while True:
        # Capture data
        data = sdr.rx()

        # Perform FFT
        spectrum = np.fft.fftshift(np.fft.fft(data, fft_size))
        spectrum_db = 20 * np.log10(np.abs(spectrum))

        # Update plot
        line.set_ydata(spectrum_db)
        fig.canvas.draw()
        fig.canvas.flush_events()

        # Pause to control update rate
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Stream stopped.")

# Clean up
plt.close()
