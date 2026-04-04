# Clipped

## Description
By default, this program will generate two WAV-formatted sound files: `sine.wav` and `clipped.wav`.

The `sine.wav` file will have the following metrics:
* Channels per frame: 1 (mono)
* Sample format: 16 bit signed (values in the range -32767..32767)
* Amplitude: ¼ maximum possible 16-bit amplitude (values in the range -8192..8192)
* Duration: one second
* Frequency: 440Hz (440 cycles per second)
* Sample Rate: 48000 samples per second

The `clipped.wav` file will have the following metrics:
* Channels per frame: 1 (mono)
* Sample format: 16 bit signed (values in the range -16384..16384)
* Amplitude: ½ maximum possible 16-bit amplitude except values that would exceed the range -8192..8192 should be "clipped", preventing them from crossing the threshold
* Duration: one second
* Frequency: 440Hz (440 cycles per second)
* Sample Rate: 48000 samples per second

## Usage

### Python Environment
If you'd like to use a Python environment, simply execute the `env-setup.bash` script before executing the main program.

