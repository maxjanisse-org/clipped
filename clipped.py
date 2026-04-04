#!/usr/bin/python3
import argparse
import numpy as np
from scipy.io.wavfile import write
import sounddevice as sd
import math

sine_filename = "sine.wav"
clipped_filename = "clipped.wav"

amp = np.iinfo(np.int16)

def clip(ratio):
    """
    Curried function

    Args:
        ratio (float): The decimal value to clip the sample size by.

    Returns:
        Function used to filter 

    Raises:
        Exception: If ratio <= 0 or ratio > 1
    """
    if ratio <= 0 or ratio > 1:
        raise Exception(f"*** invalid ratio {ratio}, should be between 0 and 1")
    max = amp.max*ratio
    min = amp.min*ratio
    def f(value):
        """
        Nested function used to map 

        Args:
            value (float): The value 
        
        Returns:
            Float value
        """
        if value > max: return max
        if value < min: return min
        return value
    return f

def sine_wave(freq, samples, max_amp):
    """
    Set up a Sine Wave

    Args:
        freq (float): The frequency
        samples (NDArray): The samples
        max_amp (int): The maximum amplitude

    Returns:
        Function 
    """
    return lambda factor: np.array((max_amp * factor) * np.sin(2. * np.pi * freq * samples)).astype(np.int16)

def clipped_sine_data(factor):
    """


    Args:
        factor (float): The decimal value to limit

    Returns:
        Function
    """
    return lambda data: np.array(list(map(clip(factor), data))).astype(np.int16)

def main(args):
    freq = args.frequency
    samplerate = args.samplerate
    samples = np.linspace(0., 1., samplerate)

    set_max_amp = sine_wave(freq, samples, amp.max)

    print(f"Generated {freq}Hz @ {samplerate} samples/second sine wave")

    sine_wave_data = set_max_amp(0.25)

    if args.verbose:
        print(f"  -> Amplitude range {math.ceil(amp.min*0.25)}..{math.ceil(amp.max*0.25)}")
    
    write(sine_filename, samplerate, sine_wave_data)
    print(f"Generated sine signal in file: {sine_filename}...")
    
    sine_wave_data = set_max_amp(0.5)
    clip_sine_wave = clipped_sine_data(0.25)

    if args.verbose:
        print(f"  -> Amplitude range {math.ceil(amp.min*0.5)}..{math.ceil(amp.max*0.5)}")
        print(f"  -> Signal clipped at {math.ceil(amp.min*0.25)}..{math.ceil(amp.max*0.25)}")
    
    clipped_wave_data = clip_sine_wave(sine_wave_data)

    write(clipped_filename, samplerate, clipped_wave_data)
    print(f"Generated clipped signal in file: {clipped_filename}...")

    if not args.quiet:
        print("Playing clipped signal...")
        sd.play(sine_wave_data, samplerate)
        sd.wait()
        print("Playback complete, exiting...")
    else:
        print("Playback skipped, exiting...")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="clipped.py",
        usage="python3 %(prog)s [options]"
    )
    parser.add_argument("-q", "--quiet", action="store_true", help="Prevent the clipped audio from playing.")
    parser.add_argument("-f", "--frequency", default=440, type=int, help="Set the frequency.")
    parser.add_argument("-s", "--samplerate", default=48000, type=int, help="Set the samplerate.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print more information about the generated audio.")
    main(parser.parse_args())