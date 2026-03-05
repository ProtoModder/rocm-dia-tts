#!/bin/bash
# Quick test for Dia TTS

TEXT="${1:-Hello world, this is a test of the Dia text to speech system.}"
OUTPUT="${2:-test.wav}"
HOST="${3:-localhost:8000}"

echo "Generating TTS..."
echo "Text: $TEXT"
echo "Output: $OUTPUT"

curl -X POST "http://$HOST/generate" \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"$TEXT\"}" \
  --output "$OUTPUT"

if [ -f "$OUTPUT" ]; then
    echo "✅ Saved to $OUTPUT"
    ls -lh "$OUTPUT"
else
    echo "❌ Failed"
fi
