# Clipped

## Description
By default, this program will generate two WAV sound files: `sine.wav` and `clipped.wav`.

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
Run the provided script to set up and/or activate a Python environment. Use the command below to execute the script; notice that it starts with a period. This allows the activation of the Python environment to update the terminal used to execute the script.
```bash
. ./env-setup.bash
```
If the directory hasn't been initialized then the environment will be created, activated, and the required packages will be installed. If the directory was initialized previously, then 

### Running the Program
Use the following command to execute the program:
```bash
python3 clipped.py
```
Configuration options are available as well (can also be seen by using `python3 clipped.py -h`):
```bash
usage: python3 clipped.py [options]

options:
  -h, --help            show this help message and exit
  -q, --quiet           Prevent the clipped audio from playing.
  -f, --frequency FREQUENCY
                        Set the frequency. [default: 440]
  -s, --samplerate SAMPLERATE
                        Set the samplerate. [default: 48000]
  -v, --verbose         Print more information about the generated audio.
  --sine-amp-scale SINE_AMP_SCALE
                        Scale the maximum amplitude. Value must be between 0 and 1. [default: 0.25]
  --clip-amp-scale CLIP_AMP_SCALE
                        Scale the maximum amplitude for the clipped audio. Value must be between 0 and 1. [default: 0.5]
  --clip-threshold CLIP_THRESHOLD
                        Set the maximum threshold for the clipped audio. Value must be between 0 and 1. [default: 0.25]
```

## My Story
I started this project by finding the [documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.wavfile.write.html) for SciPy's `scipy.io.wavfile` API. There they have a code example for generating a sine wave and writing that data to a file. Aside from changing the samplerate and frequency, this was essentially all that was needed to satisfy the first part of the assignment. After that I copy-pasted that code and changed the amplitude modified to 0.5 from 0.25 for the second part of the assignment. The missing piece to this part was the fact I needed to "clip" any sample that exceeded the range -8192..8192, to it's nearest maximum value.

The "clipping" process was straight-forward enough. I knew that what I needed to do was a prime use case for performing a mapping operation, where a provided function is applied to each item of an iterable that may, or may not, alter it. Since I was using `NDArray` collections from NumPy, I needed to use the internet to make sure I wasn't missing an inherent ability of an `NDArray` or helper function specific to NumPy that would help me with this task. I didn't find anything, so I went with the AI-suggested code that suggested using Python's `map` function and then casting it to a `list` and, finally, back to an `NDArray`. Really, with this part working, I had completed the second part of this assignment. As suggested, I even confirmed that the audio was "clipped" by using the Linux application Audacity to review the waveform that was stored in the file.

Lastly, I just needed to output the raw "clipped" audio data to the sound system of the machine this program is being run on. As recommended, I used the `sounddevice` Python library which worked out-of-the-box for me, easy-peasy.

At this point, I felt that I had successfully completed the minimum requirements of the assignment... but I decided to continue developing the program into a more full-fledged experince.

### Further Development Efforts

> **NOTE:** I'm realizing now that I probably took this assignment way too far. The intent for giving us such a significant amount of time to work on it was to ensure that we identify and resolve any issuses with our development environments _before_ going on to more involved assignments. Thankfully, I made sure to have the default values of the program fulfill the original requirements, so no arguments are required. Feel free to ignore this section.

To start with, I saw a lot of duplicate code that I wanted to consolidate but, I also saw an opportunity to use a minute amount of functional programming that I recently picked up in my CS358 class. I noticed that no matter which signal I was going to generate, I always started with a base sine wave that was comprised of a frequency, a sample rate, and the maximum amplitude possible. My function then returns a function that handles determining the actual maximum amplitude the waveform will have and generating the dataset. I used this same trick in a couple other places as well.

After this refactoring, I moved on to making the program configurable through arguments, including a verbose mode and a way to disable auto-playing the clipped audio. This effort got me to refresh my understanding of the capabilities of the `ArgumentParser`, which is extremely helpful and also generates a clean "help" menu as well. Even while typing this out an revisited my way of handling the validation of my "scaling" arguments only to discover (through a Google AI search result) that I can provide a validation function when defining a new argument. This helped clean up my implementation quite a bit. 

### What's Next?
I can't think of much else to do with this program that I haven't already done aside from a small testsuite and, perhaps, attempting to ensure that it's as cross-platform friendly as possible which seems like it would be _even more_ overkill.