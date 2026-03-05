# ROCm Dia TTS - All Attempts

This documents every approach tried to get Dia TTS working on AMD ROCm (R9700).

---

## ✅ What WORKED (v1.0)

Using `transformers.pipeline`:

```python
from transformers import pipeline

tts_pipe = pipeline(
    task="text-to-speech",
    model="nari-labs/Dia-1.6B-0626",
    device=0,
    trust_remote_code=True
)

output = tts_pipe("Hello world")
```

**Result**: Working audio, ~18-20 seconds per generation

---

## ❌ What DIDN'T WORK

### Attempt 1: Manual model loading (DiaForConditionalGeneration)
```python
from transformers import DiaForConditionalGeneration

model = DiaForConditionalGeneration.from_pretrained(
    "nari-labs/Dia-1.6B-0626",
    torch_dtype=torch.float16,
    device_map="cuda",
    trust_remote_code=True
)
```
**Problem**: Generated audio codes but couldn't decode them properly. Output was malformed (9 channels, wrong shape).

### Attempt 2: device_map="auto"
```python
model = DiaForConditionalGeneration.from_pretrained(
    "nari-labs/Dia-1.6B-0626",
    device_map="auto"
)
```
**Problem**: Didn't solve the audio decoding issue.

### Attempt 3: torch.compile()
```python
model = DiaForConditionalGeneration.from_pretrained(...)
model = torch.compile(model, mode="max-autotune")
```
**Problem**: Crashed on ROCm.

### Attempt 4: bfloat16
```python
torch_dtype=torch.bfloat16
```
**Problem**: Compatibility issues on ROCm.

### Attempt 5: attn_implementation="sdpa"
```python
model_kwargs={"attn_implementation": "sdpa"}
```
**Problem**: Errors on ROCm.

### Attempt 6: Various audio decoding attempts
- `audio[0, :, 0]` - wrong shape
- `audio.mean(axis=1)` - still malformed  
- `processor.batch_decode()` - wrong API

### Attempt 7: max_new_tokens in pipeline
```python
output = tts_pipe(text, max_new_tokens=256)
```
**Problem**: TextToAudioPipeline doesn't accept max_new_tokens directly.

---

## Key Learnings

1. **Use pipeline abstraction** - It handles the complex decoding internally
2. **ROCm appears as CUDA** - PyTorch sees it as `device=0`
3. **Pipeline > manual** - The abstraction solves many issues
4. **Warmup helps** - First request is slower
5. **Audio format**: 44.1kHz mono WAV, PCM 16-bit

---

## Hardware

- GPU: AMD Radeon AI PRO R9700
- VRAM: 34GB
- Container: rocm/pytorch:latest
