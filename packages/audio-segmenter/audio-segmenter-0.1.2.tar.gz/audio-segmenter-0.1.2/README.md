# AudioSegmenter

AudioSegmenter is a powerful Python library for segmenting audio files with flexible options.

## Installation

```bash
pip install audio-segmenter
```

## Usage

### Command Line

```bash
# Time-based segmentation (default)
audio-segmenter input_audio.mp3

# Silence-based segmentation
audio-segmenter input_audio.mp3 -m auto

# Custom segmentation
audio-segmenter input_audio.mp3 \
    -m auto \
    -sr 0.15 \
    -sd 0.3 \
    -min 0.5 \
    -o custom_segments \
    -j custom_metadata.json
```

### Python API

```python
from audio_segmenter import AudioSegmenter

segmenter = AudioSegmenter()
segmenter.segment_audio('input_audio.mp3', method='auto')
```

## Features

- Time-based segmentation
- Silence-based segmentation
- Flexible configuration
- Logging support
- Command-line interface
