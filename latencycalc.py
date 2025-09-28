import sounddevice as sd
import numpy as np
import scipy.signal
import csv
import os
import click

def get_supported_samplerates(device_id, input_channels=1, output_channels=1):
    """Query supported sample rates for the device."""
    common_samplerates = [44100, 48000, 88200, 96000, 176400, 192000]
    supported = []
    for sr in common_samplerates:
        try:
            sd.check_output_settings(device=device_id, channels=output_channels, samplerate=sr)
            sd.check_input_settings(device=device_id, channels=input_channels, samplerate=sr)
            supported.append(sr)
        except sd.PortAudioError:
            continue
    return supported if supported else [44100]  # Fallback to 44100 if none supported

def get_supported_blocksizes(device_id, samplerate, input_channels=1, output_channels=1):
    """Query supported block sizes for the device."""
    common_blocksizes = [32, 64, 128, 256, 512, 1024, 2048]
    supported = []
    for bs in common_blocksizes:
        try:
            with sd.Stream(
                device=device_id,
                samplerate=samplerate,
                blocksize=bs,
                channels=(input_channels, output_channels),
                dtype='float32'
            ):
                supported.append(bs)
        except sd.PortAudioError:
            continue
    return supported if supported else [128]  # Fallback to 128 if none supported

def measure_latency(device_id, samplerate=44100, blocksize=128, input_channel=0, output_channel=0):
    """Measure audio latency by sending a pulse and detecting it in the recording."""
    # Parameters
    pulse_duration = 0.001  # 1ms pulse
    recording_duration = 1.0  # 1 second of recording
    samples_per_pulse = int(pulse_duration * samplerate)
    total_samples = int(recording_duration * samplerate)

    # Generate a simple pulse (a short burst of 1s followed by zeros)
    pulse = np.zeros(total_samples, dtype=np.float32)
    pulse[:samples_per_pulse] = 1.0  # Short pulse at the start

    # Buffer to store recorded audio
    recorded = np.zeros(total_samples, dtype=np.float32)

    # Callback function for simultaneous play and record
    def callback(indata, outdata, frames, time, status):
        if status:
            print(f"Status: {status}")
        # Copy specified input channel to recording buffer
        recorded[offset:offset + frames] = indata[:, input_channel] if indata.shape[1] > 1 else indata.squeeze()
        # Play pulse on specified output channel (ensure stereo output if needed)
        outdata.fill(0)  # Clear output buffer
        outdata[:frames, output_channel] = pulse[offset:offset + frames]
        # Update offset
        nonlocal offset
        offset += frames

    # Initialize offset for callback
    offset = 0

    # Get device info to determine channel counts
    device_info = sd.query_devices()[device_id]
    input_channels = min(device_info['max_input_channels'], 2)  # Limit to 2 for simplicity
    output_channels = min(device_info['max_output_channels'], 2)

    # Validate channels
    if input_channel >= input_channels or output_channel >= output_channels:
        return f"Error: Invalid channel selection (Input: {input_channel}, Output: {output_channel})"

    # Set up stream with ASIO device
    try:
        with sd.Stream(
            device=device_id,
            samplerate=samplerate,
            blocksize=blocksize,
            channels=(input_channels, output_channels),
            dtype='float32',
            callback=callback
        ):
            # Wait until recording is done
            sd.sleep(int(recording_duration * 1000))
    except Exception as e:
        return f"Error: {str(e)}"

    # Perform cross-correlation to find the delay
    correlation = scipy.signal.correlate(recorded, pulse, mode='full')
    delay_samples = np.argmax(correlation) - (len(pulse) - 1)
    latency_ms = (delay_samples / samplerate) * 1000

    return f"{latency_ms:.2f} ms"

@click.command()
@click.option('--device-id', type=int, help='Device ID for ASIO device (use -1 to list devices)')
@click.option('--input-channel', type=int, default=0, help='Input channel index (0-based, default 0)')
@click.option('--output-channel', type=int, default=0, help='Output channel index (0-based, default 0)')
@click.option('--csv-export/--no-csv-export', default=True, help='Enable/disable CSV export (default True)')
def main(device_id, input_channel, output_channel, csv_export):
    """Measure audio latency for an ASIO device with specified input/output channels."""
    # List devices if device_id is -1
    if device_id == -1:
        print("Available audio devices:")
        print(sd.query_devices())
        return

    # Find ASIO device if not specified
    if device_id is None:
        for i, dev in enumerate(sd.query_devices()):
            if 'ASIO' in dev['name']:
                device_id = i
                break

    if device_id is None or device_id < 0 or device_id >= len(sd.query_devices()):
        print("Error: No ASIO device found or invalid device ID. Use --device-id -1 to list devices.")
        return

    device_info = sd.query_devices()[device_id]
    print(f"Using device: {device_info['name']}")
    print(f"Max input channels: {device_info['max_input_channels']}")
    print(f"Max output channels: {device_info['max_output_channels']}")

    # Validate channel selection
    if input_channel >= device_info['max_input_channels']:
        print(f"Error: Input channel {input_channel} exceeds max input channels ({device_info['max_input_channels']})")
        return
    if output_channel >= device_info['max_output_channels']:
        print(f"Error: Output channel {output_channel} exceeds max output channels ({device_info['max_output_channels']})")
        return

    # Get driver-reported latencies
    low_input_latency = device_info['default_low_input_latency'] * 1000  # Convert to ms
    high_input_latency = device_info['default_high_input_latency'] * 1000
    low_output_latency = device_info['default_low_output_latency'] * 1000
    high_output_latency = device_info['default_high_output_latency'] * 1000
    print(f"Driver-reported latencies:")
    print(f"  Input: Low = {low_input_latency:.2f} ms, High = {high_input_latency:.2f} ms")
    print(f"  Output: Low = {low_output_latency:.2f} ms, High = {high_output_latency:.2f} ms")

    # Get supported sample rates and block sizes
    input_channels = min(device_info['max_input_channels'], 2)
    output_channels = min(device_info['max_output_channels'], 2)
    samplerates = get_supported_samplerates(device_id, input_channels, output_channels)
    print(f"Supported sample rates: {samplerates}")
    blocksizes = get_supported_blocksizes(device_id, samplerates[0], input_channels, output_channels)
    print(f"Supported block sizes: {blocksizes}")

    # Results list
    results = []

    for sr in samplerates:
        for bs in blocksizes:
            print(f"Testing Sample Rate: {sr} Hz, Block Size: {bs}, Input Channel: {input_channel}, Output Channel: {output_channel}")
            latency = measure_latency(device_id, samplerate=sr, blocksize=bs, input_channel=input_channel, output_channel=output_channel)
            results.append((sr, bs, latency, input_channel, output_channel, low_input_latency, high_input_latency, low_output_latency, high_output_latency))

    # Print results in a table format
    print("\nLatency Measurement Results:")
    print(f"{'Sample Rate (Hz)':<18} {'Block Size':<12} {'Input Ch':<10} {'Output Ch':<10} {'Measured Latency':<15} {'Low In (ms)':<12} {'High In (ms)':<12} {'Low Out (ms)':<12} {'High Out (ms)':<12}")
    print("-" * 110)
    for sr, bs, lat, ic, oc, li, hi, lo, ho in results:
        print(f"{sr:<18} {bs:<12} {ic:<10} {oc:<10} {lat:<15} {li:.2f}:<12} {hi:.2f}:<12} {lo:.2f}:<12} {ho:.2f}:<12}")

    # Export to CSV if enabled
    if csv_export:
        csv_file = "latency_results.csv"
        try:
            with open(csv_file, 'w', newline='') as f:
                writer = csv.writer(f)
                # Write header
                writer.writerow(["Sample Rate (Hz)", "Block Size", "Input Channel", "Output Channel", 
                                "Measured Latency (ms)", "Driver Low Input Latency (ms)", 
                                "Driver High Input Latency (ms)", "Driver Low Output Latency (ms)", 
                                "Driver High Output Latency (ms)"])
                # Write data
                for sr, bs, lat, ic, oc, li, hi, lo, ho in results:
                    # Clean up latency value for CSV (remove 'ms' for numeric values)
                    lat_value = lat.replace(" ms", "") if "ms" in lat else lat
                    writer.writerow([sr, bs, ic, oc, lat_value, f"{li:.2f}", f"{hi:.2f}", f"{lo:.2f}", f"{ho:.2f}"])
            print(f"\nResults exported to {csv_file}")
        except Exception as e:
            print(f"Error exporting to CSV: {e}")

if __name__ == "__main__":
    main()