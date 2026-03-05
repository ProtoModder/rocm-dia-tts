import os
os.environ["HF_HOME"] = "/app/models"

import torch
import numpy as np
import soundfile as sf
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse
from transformers import pipeline
import uvicorn

app = FastAPI(title="Dia TTS API")

MODEL_ID = "nari-labs/Dia-1.6B-0626"

# Device selection
device = 0 if torch.cuda.is_available() else -1
print("GPU available:", torch.cuda.is_available())
print(f"Loading {MODEL_ID} pipeline onto device {device}...")

# Load Dia pipeline
tts_pipe = pipeline(
    task="text-to-speech",
    model=MODEL_ID,
    device=device,
    trust_remote_code=True
)
print("Dia pipeline loaded. Ready for generation.")

# Warmup
print("Warming up...")
_ = tts_pipe("warmup")
print("Ready!")

class TTSRequest(BaseModel):
    text: str

@app.post("/generate")
async def generate_audio(request: TTSRequest):
    text = request.text.strip()
    if not text:
        return {"error": "Empty text input."}
    
    print("Generating audio for:", text[:60], "...")
    output = tts_pipe(text)
    
    audio = np.array(output["audio"])
    sample_rate = output["sampling_rate"]

    # Flatten if batched
    if audio.ndim > 1:
        audio = audio.squeeze()

    # Normalize waveform to [-1,1]
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val

    save_path = "/app/workspace/output.wav"
    sf.write(save_path, audio, sample_rate, subtype="PCM_16")

    return FileResponse(save_path, media_type="audio/wav")

@app.get("/health")
def health():
    return {"status": "ok", "device": "cuda" if torch.cuda.is_available() else "cpu"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
