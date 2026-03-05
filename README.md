# ROCm Dia TTS 🎤

Run Dia-1.6B Text-to-Speech on AMD ROCm (Radeon AI PRO R9700).

> **Status**: ✅ Working - ~18-20 seconds per generation

## Hardware

| Component | Details |
|----------|---------|
| GPU | AMD Radeon AI PRO R9700 |
| VRAM | 34GB |
| Container | AMD ROCm pre-built (from amd.com) |

## Quick Start

```bash
# AMD provides pre-built ROCm containers
# Get from https://hub.docker.com/r/amd/pytorch or amd.com/developer

# Run with ROCm (example)
docker run -d --cap-add=SYS_PTRACE --device=/dev/kfd --device=/dev/dri -p 8000:8000 amd/pytorch:latest

# Install deps
pip install transformers soundfile fastapi uvicorn

# Run server
python server.py
```

## API

```bash
# Generate speech
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world!"}' \
  --output output.wav
```

## The Fix

The key is using `transformers.pipeline` instead of manual model loading:

```python
from transformers import pipeline

tts_pipe = pipeline(
    task="text-to-speech",
    model="nari-labs/Dia-1.6B-0626",
    device=0,  # ROCm appears as CUDA
    trust_remote_code=True
)

output = tts_pipe("Hello world!")
```

## What Didn't Work

- Manual model loading with `DiaForConditionalGeneration`
- `device_map="cuda"`
- `torch.compile()`
- Various dtype configs

See [ATTEMPTS.md](./ATTEMPTS.md) for the full failure log.

## Performance

- Generation time: ~18-20 seconds
- Sample rate: 44.1kHz
- Output: Mono WAV, PCM 16-bit

## Credits

- Model: [nari-labs/Dia-1.6B-0626](https://huggingface.co/nari-labs/Dia-1.6B-0626)
- Built by Nyx (Void Node AI)
