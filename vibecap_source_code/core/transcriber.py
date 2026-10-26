import time
from rich.console import Console  # type: ignore[import-not-found]
from .utils import run, fail

console = Console()
CHUNK_SEC = 600

def extract_audio(ffmpeg, video, tmp):
    run([ffmpeg, "-y", "-i", str(video), "-map", "0:a:0", "-vn", "-ac", "1", "-ar", "16000",
         "-c:a", "libmp3lame", "-b:a", "48k", "-f", "segment",
         "-segment_time", str(CHUNK_SEC), "-reset_timestamps", "1",
         str(tmp / "part_%03d.mp3")])
    parts = sorted(tmp.glob("part_*.mp3"))
    if not parts:
        fail("No audio track found in this video.")
    return parts

def normalize(data, offset):
    words = []
    for w in data.get("words") or []:
        text = w["word"].strip()
        if text:
            words.append({"word": text, "start": w["start"] + offset, "end": w["end"] + offset})
    if words:
        return words
    for seg in data.get("segments") or []:
        toks = seg["text"].split()
        total = sum(len(t) for t in toks) or 1
        t0, span = seg["start"], seg["end"] - seg["start"]
        for tok in toks:
            d = span * len(tok) / total
            words.append({"word": tok, "start": t0 + offset, "end": t0 + d + offset})
            t0 += d
    return words

def transcribe(client, parts, model, language):
    words = []
    for i, part in enumerate(parts):
        for attempt in range(3):
            try:
                with console.status(f"[cyan]🎙️ Transcribing part {i + 1}/{len(parts)} using Whisper...[/cyan]"):
                    kw = dict(
                        file=(part.name, part.read_bytes()), model=model,
                        response_format="verbose_json",
                        timestamp_granularities=["word", "segment"],
                        temperature=0.0,
                    )
                    if language:
                        kw["language"] = language
                    t = client.audio.transcriptions.create(**kw)
                break
            except Exception as e:
                if attempt == 2:
                    fail(f"Groq request failed: {e}")
                console.print(f"[yellow]⚠️ Retrying... ({e})[/yellow]")
                time.sleep(3 * (attempt + 1))
        data = t.model_dump() if hasattr(t, "model_dump") else dict(t)
        words += normalize(data, i * CHUNK_SEC)
    if not words:
        fail("No speech detected in the audio.")
    return words