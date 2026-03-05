# ROCm Dia TTS Server

Optimized Dia-1.6B TTS server for AMD ROCm (Radeon AI PRO R9700).

## Hardware

- **GPU**: AMD Radeon AI PRO R9700
- **VRAM**: 34GB

## Requirements

- ROCm-enabled PyTorch
- Docker with ROCm support
- transformers
- soundfile
- fastapi
- uvicorn

## Quick Start

```bash
# Build or use ROCm container
docker run -d --cap-add=SYS_PTRACE --device=/dev/kfd --device=/dev/dri -p 8000:8000 rocm/pytorch:latest

# Install dependencies
pip install transformers soundfile fastapi uvicorn

# Run server
python server.py
```

## The Fix

The key insight is using `transformers.pipeline` instead of manually loading the model:

```python
from transformers import pipeline

# This works on ROCm
tts_pipe = pipeline(
    task="text-to-speech",
    model="nari-labs/Dia-1.6B-0626",
    device=0,  # ROCm appears as CUDA device
    trust_remote_code=True
)

# Generate
output = tts_pipe("Hello world")
```

## What DIDN'T Work

- Manual model loading with `DiaForConditionalGeneration.from_pretrained()`
- `device_map="cuda"`
- `torch.compile()`
- Various dtype configurations

## Performance

- ~18-20 seconds per generation
- 44.1kHz mono output
- FP16 inference

## Notes

- ROCm shows up as CUDA device in PyTorch
- Use pipeline abstraction, not manual loading
- Warmup the model on first request for better performance
