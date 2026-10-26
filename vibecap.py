import argparse
import tempfile
import os
from pathlib import Path
from rich.console import Console  # type: ignore[import-not-found]
from rich.prompt import Prompt # type: ignore[import-not-found]

from vibecap_source_code.core.config import get_api_key, save_api_key
from vibecap_source_code.ui.styles import STYLES, show_styles, BASE
from vibecap_source_code.ui.banner import ASCII_BANNER
from vibecap_source_code.core.utils import path_tool, fail, video_size, run
from vibecap_source_code.core.transcriber import extract_audio, transcribe
from vibecap_source_code.generator.subtitles import make_captions, write_srt, write_ass, fit_chars

VERSION = "1.0.0"


console = Console()

MODELS = {
    "turbo": "whisper-large-v3-turbo",
    "large": "whisper-large-v3",
}

def wizard(args):
    console.print(ASCII_BANNER)
    console.print("[bold green]✨ Welcome to the interactive wizard! Let's make some magic.\n[/bold green]")
    path = Prompt.ask("[cyan]📁 Drag & drop your video file here[/cyan]").strip().strip("\"'")
    args.input = path
    args.lang = Prompt.ask("[cyan]🌐 Language code (ar / en / fr ... or auto)[/cyan]", default="auto")
    show_styles()
    args.style = Prompt.ask("[cyan]🎨 Choose a caption style[/cyan]", choices=list(STYLES), default="classic")
    args.model = Prompt.ask("[cyan]🚀 Choose quality model[/cyan]", choices=list(MODELS), default="turbo")
    return args

def main():
    ap = argparse.ArgumentParser(prog="vibecap", description="Auto captions with Groq Whisper & FFmpeg.")
    ap.add_argument("input", nargs="?", help="video file path")
    ap.add_argument("-k", "--key", default=None, help="Save Groq API Key (e.g. vibecap -key mykey)")
    ap.add_argument("-l", "--lang", default=None, help="language code (ar, en, ...) or 'auto'")
    ap.add_argument("-s", "--style", default=None, choices=list(STYLES), help="caption style")
    ap.add_argument("-m", "--model", default="turbo", help="turbo | large")
    ap.add_argument("-o", "--output", default=None, help="output video path")
    ap.add_argument("--font", default=None, help="override font name (e.g. Cairo, Tajawal)")
    ap.add_argument("--fonts-dir", default=None, help="folder with extra font files")
    ap.add_argument("--position", choices=["top", "middle", "bottom"], default=None)
    ap.add_argument("--srt-only", action="store_true", help="only create the .srt file")
    ap.add_argument("--list-styles", action="store_true", help="show available styles")
    ap.add_argument("-v", "--version", action="version", version=f"VibeCap {VERSION}")
    args = ap.parse_args()

    api_key = get_api_key(args.key)

    if args.key and not args.input:
        console.print("[green]✔ API key saved successfully to JSON![/green]")
        return

    if not api_key:
        console.print(ASCII_BANNER)
        console.print("[yellow]⚠️ No Groq API Key found in JSON config![/yellow]")
        api_key = Prompt.ask("[cyan]🔑 Please enter your Groq API Key (Paste is enabled)[/cyan]").strip()
        if not api_key:
            fail("API Key is required!")
        save_api_key(api_key)
        console.print("[green]✔ API key saved successfully![/green]")

    if args.list_styles:
        console.print(ASCII_BANNER)
        show_styles()
        return

    if not args.input:
        args = wizard(args)

    video = Path(args.input.strip("\"'")).expanduser().resolve()
    if not video.exists():
        fail(f"File not found: {video}")

    console.print(ASCII_BANNER)

    lang = None if (args.lang or "auto").lower() == "auto" else args.lang.lower()
    style_name = args.style or "classic"
    p = STYLES[style_name]
    model = MODELS.get(args.model, args.model)
    out = Path(args.output).resolve() if args.output else video.with_name(video.stem + "_captioned.mp4")
    srt_path = out.with_suffix(".srt")

    try:
        from groq import Groq # type: ignore[import-not-found]
    except ImportError:
        fail("Missing package. Run: pip install groq rich")

    ffmpeg = path_tool("ffmpeg")
    ffprobe = path_tool("ffprobe")
    client = Groq(api_key=api_key)

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)

        with console.status("[cyan]🎵 Extracting audio from video...[/cyan]"):
            parts = extract_audio(ffmpeg, video, tmp)

        words = transcribe(client, parts, model, lang)

        srt_p = {**BASE, "max_words": 0, "max_lines": 2, "max_chars": 42, "max_dur": 6.0}
        write_srt(make_captions(words, srt_p), srt_path, srt_p)
        console.print(f"[green]✔ Subtitles saved:[/green] {srt_path}")

        if args.srt_only:
            return

        size = video_size(ffprobe, video)
        p_fit = {**p, "max_chars": fit_chars(p, size)}
        caps = make_captions(words, p_fit)
        write_ass(caps, tmp / "captions.ass", p_fit, size, font=args.font, position=args.position)

        vf = "ass=captions.ass"
        if args.fonts_dir:
            fd = Path(args.fonts_dir).resolve().as_posix().replace(":", "\\:")
            vf += f":fontsdir={fd}"

        with console.status(f"[cyan]🔥 Burning '{style_name}' captions into video...[/cyan]"):
            run([ffmpeg, "-y", "-i", str(video), "-vf", vf,
                 "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                 "-c:a", "copy", "-movflags", "+faststart", str(out)], cwd=td)

    console.print(f"\n[bold green3]🎉 Done! Successfully saved to:[/bold green3] [cyan]{out}[/cyan]\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️ Cancelled by user.[/yellow]")
