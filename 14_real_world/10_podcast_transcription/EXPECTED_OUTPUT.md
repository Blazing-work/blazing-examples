# Expected Output

## Running

```bash
python flow.py
```

## Requirements

This example requires external services configured:
- `OPENAI_API_KEY` for OpenAI Whisper transcription
- `ffmpeg` and `ffprobe` installed on the system:
  - macOS: `brew install ffmpeg`
  - Ubuntu: `apt-get install ffmpeg`

Start infrastructure: `docker-compose up -d`

## Output

```
INFO - TranscriptionService - Audio duration: 47m 23s
INFO - TranscriptionService - Split into 5 chunks (10m each)
INFO - TranscriptionService - Transcribing chunk 1/5...
INFO - TranscriptionService - Transcribing chunk 2/5...
INFO - TranscriptionService - Transcribing chunk 3/5...
INFO - TranscriptionService - Transcribing chunk 4/5...
INFO - TranscriptionService - Transcribing chunk 5/5...
INFO - TranscriptionService - Merged transcript: 6,842 words
{"duration_s": 2843, "chunks": 5, "word_count": 6842, "transcript": "Welcome to the show..."}
```

## Notes

- Audio duration and chunk count depend on the input audio file length
- Transcription uses Semaphore(3) for parallel processing — max 3 concurrent Whisper API calls
- Each chunk is split at 10-minute boundaries (well under the 25MB Whisper API file size limit)
- Transcript text will vary with the actual audio content
- OpenAI API costs apply per minute of audio transcribed
