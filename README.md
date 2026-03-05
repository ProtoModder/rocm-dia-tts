# ROCm Dia TTS 🎤

Fast, high-quality text-to-speech on AMD GPUs.

> **Status**: ✅ Working - ~20 seconds per generation

## What is this?

This lets you run Dia-1.6B TTS on AMD GPUs (like the R9700) using ROCm. No NVIDIA required!

## What You Need

- AMD GPU with ROCm support (Radeon AI PRO R9700, RX 7900 XTX, etc.)
- 16GB+ VRAM recommended
- Linux with ROCm installed

## Super Quick Start

```bash
# 1. Start the container
docker run -d --cap-add=SYS_PTRACE --device=/dev/kfd --device=/dev/dri -p 8000:8000 rocm/pytorch:latest

# 2. Install dependencies
pip install transformers soundfile fastapi uvicorn

# 3. Run the server
python server.py

# 4. Generate speech
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world!"}' \
  --output hello.wav
```

That's it! 🎉

## Using the API

The server runs on port 8000:

```bash
# Basic
curl -X POST http://localhost:8000/generate \
  -d '{"text": "Your text here"}' \
  --output audio.wav

# Longer text
curl -X POST http://localhost:8000/generate \
  -d '{"text": "This is a longer piece of text that will be converted to speech."}' \
  --output output.wav
```

## What We Figured Out

### The Secret Sauce

Don't load the model manually - let the pipeline handle it:

```python
from transformers import pipeline

tts = pipeline(
    task="text-to-speech",
    model="nari-labs/Dia-1.6B-0626",
    device=0,
    trust_remote_code=True
)

output = tts("Your text here")
```

### What Didn't Work

- Loading the model directly (got stuck on decoding)
- Using `device_map`
- Various dtype settings

See [ATTEMPTS.md](./ATTEMPTS.md) if you want all the nerdy details.

## Performance

| Metric | Value |
|--------|-------|
| Speed | ~20 seconds |
| Output | 44.1kHz WAV |
| VRAM | ~8GB |

## Troubleshooting

**Q: It's slow**
> First run is always slower (model loading). Subsequent runs are faster.

**Q: Out of memory**
> Try closing other GPU apps. You need about 8GB free.

**Q: Not working**
> Make sure ROCm is set up properly. Run `rocm-smi` to check.

## Credits

- Model: [nari-labs/Dia-1.6B-0626](https://huggingface.co/nari-labs/Dia-1.6B-0626)
- Built by Nyx on the Void Node
