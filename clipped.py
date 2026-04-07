#!/usr/bin/python3
# Author: Max Janisse
import argparse
import numpy as np
from scipy.io.wavfile import write
import sounddevice as sd
import math

sine_filename = "sine.wav"
clipped_filename = "clipped.wav"

amp = np.iinfo(np.int16)

def validate_scale(value):
    """
    Validation function used by the ArgumentParser to ensure the value is a float and is between 0 and 1

    Args:
        value (Unknown): The value provided by the user through the command-line
    
    Returns:
        The validated float value to use
    
    Raises:
        ValueError: When argument is not a float value or if it is not between 0 and 1
    """
    scale = float(value)
    if scale <= 0 or scale > 1:
        raise ValueError(f"*** invalid scale {scale}, should be between 0 and 1")
    return scale

def clip(scale):
    """
    Function that provides a function that can be used as a filter

    Args:
        scale (float): The decimal value to clip the sample size by.

    Returns:
        Function used to filter 
    """
    max = amp.max*scale
    min = amp.min*scale
    def f(value):
        """
        Nested function used to map 

        Args:
            value (float): The value to evaluate
        
        Returns:
            Float value
        """
        if value > max: return max
        if value < min: return min
        return value
    return f

def sine_wave(freq, samples, max_amp):
    """
    Set up a Sine wave

    Args:
        freq (float): The frequency
        samples (NDArray): The samples
        max_amp (int): The maximum amplitude

    Returns:
        Function that takes a scale value as an argument and generates a sine wave
    """
    return lambda scale: np.array((max_amp * scale) * np.sin(2. * np.pi * freq * samples)).astype(np.int16)

def clipped_sine_data(scale):
    """
    Set up a Sine wave where the amplitudes will be clipped if they exceed the threshold defined by the `scale` argument

    Args:
        scale (float): The decimal value used to determine the clipping threshold

    Returns:
        Function that takes in the base sine wave data and returns the clipped form of the data
    """
    return lambda data: np.array(list(map(clip(scale), data))).astype(np.int16)

def main(args):
    freq = args.frequency
    sine_amp_scale = args.sine_amp_scale
    clip_amp_scale = args.clip_amp_scale
    clip_threshold = args.clip_threshold
    samplerate = args.samplerate
    samples = np.linspace(0., 1., samplerate)

    set_amp_scale = sine_wave(freq, samples, amp.max)

    print(f"Generated {freq}Hz @ {samplerate} samples/second sine wave")

    sine_wave_data = set_amp_scale(sine_amp_scale)

    if args.verbose:
        print(f"  -> Amplitude range {math.ceil(amp.min*sine_amp_scale)}..{math.ceil(amp.max*sine_amp_scale)}")
    
    write(sine_filename, samplerate, sine_wave_data)
    print(f"Wrote sine signal to file '{sine_filename}'")
    
    sine_wave_data = set_amp_scale(clip_amp_scale)
    clip_sine_wave = clipped_sine_data(clip_threshold)

    if args.verbose:
        print(f"  -> Amplitude range {math.ceil(amp.min*clip_amp_scale)}..{math.ceil(amp.max*clip_amp_scale)}")
        print(f"  -> Signal clipped at {math.ceil(amp.min*clip_threshold)}..{math.ceil(amp.max*clip_threshold)}")
    
    clipped_wave_data = clip_sine_wave(sine_wave_data)

    write(clipped_filename, samplerate, clipped_wave_data)
    print(f"Wrote clipped signal to file '{clipped_filename}'")

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
    parser.add_argument("-f", "--frequency", default=440, type=int, help="Set the frequency. [default: %(default)s]")
    parser.add_argument("-s", "--samplerate", default=48000, type=int, help="Set the samplerate. [default: %(default)s]")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print more information about the generated audio.")
    parser.add_argument("--sine-amp-scale", default=0.25, type=validate_scale, help="Scale the maximum amplitude. Value must be between 0 and 1. [default: %(default)s]")
    parser.add_argument("--clip-amp-scale", default=0.5, type=validate_scale, help="Scale the maximum amplitude for the clipped audio. Value must be between 0 and 1. [default: %(default)s]")
    parser.add_argument("--clip-threshold", default=0.25, type=validate_scale, help="Set the maximum threshold for the clipped audio. Value must be between 0 and 1. [default: %(default)s]")
    main(parser.parse_args())