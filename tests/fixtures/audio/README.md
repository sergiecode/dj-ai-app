# Test Fixtures - Audio Sample Files
# Author: Sergie Code

This directory contains sample audio files for testing the DJ AI system.

## Sample Files (Not included in repository)

For testing, you can add sample audio files here:

- `sample.mp3` - Sample MP3 file for testing
- `sample.wav` - Sample WAV file for testing
- `sample.flac` - Sample FLAC file for testing
- `sample.m4a` - Sample M4A file for testing

## Generating Test Audio Files

You can generate simple test audio files using Python:

```python
import numpy as np
import soundfile as sf

# Generate a simple sine wave (440 Hz for 5 seconds)
sample_rate = 44100
duration = 5
t = np.linspace(0, duration, int(sample_rate * duration))
audio_data = np.sin(2 * np.pi * 440 * t)

# Save as different formats
sf.write('sample.wav', audio_data, sample_rate)
```

Or use online resources for copyright-free sample audio files for testing.

## Note

Due to file size and copyright considerations, actual audio files are not included in the repository. Tests that require audio files will be skipped if no files are present.
