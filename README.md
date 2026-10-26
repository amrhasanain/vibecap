# VibeCap

Auto caption maker ✨. Powered by Groq Whisper for transcription and FFmpeg for audio extraction and caption rendering.

VibeCap is a Python script, not a standalone executable. Run it with `python vibecap.py` from the project folder.

## Requirements

- Python 3
- Git, to clone the repository
- A Groq API key
- A recent FFmpeg installation with both `ffmpeg` and `ffprobe` available on `PATH`

Check that FFmpeg is available in PowerShell:

```powershell
ffmpeg -version
ffprobe -version
```

## Fast use

```powershell
git clone https://github.com/amrhasanain/vibecap
cd vibecap
python -m pip install -r requirements.txt
python vibecap.py
```

## Installation

```powershell
git clone https://github.com/amrhasanain/vibecap
cd vibecap
python -m pip install -r requirements.txt
```

## Groq API key

On the first run, VibeCap prompts for your Groq API key and saves it locally in your user configuration folder. You can also save it from PowerShell with:

```powershell
python vibecap.py --key YOUR_GROQ_API_KEY
```

## Usage

Run the script without arguments to open the interactive wizard:

```powershell
python vibecap.py
```

To see the available command-line options:

```powershell
python vibecap.py --help
```

Caption a video in Arabic with the minimal style:

```powershell
python vibecap.py "input.mp4" --lang ar --style minimal --model turbo
```

Create only an SRT subtitle file:

```powershell
python vibecap.py "input.mp4" --lang ar --srt-only
```

Choose a different output path, font, or subtitle position:

```powershell
python vibecap.py "input.mp4" --lang en --style classic --output "output.mp4" --font "Arial" --position bottom
```


## Options

| Option | Description |
| --- | --- |
| `input` | Video file path. Optional when using the interactive wizard. |
| `-k`, `--key` | Save a Groq API key. |
| `-l`, `--lang` | Language code such as `ar` or `en`; use `auto` for automatic detection. |
| `-s`, `--style` | Caption style: `classic`, `youtube`, `tiktok`, `karaoke`, `neon`, or `minimal`. |
| `-m`, `--model` | Transcription model: `turbo` or `large`. |
| `-o`, `--output` | Output video path. Defaults to `<input>_captioned.mp4`. |
| `--font` | Override the caption font name. |
| `--fonts-dir` | Folder containing additional font files. |
| `--position` | Caption position: `top`, `middle`, or `bottom`. |
| `--srt-only` | Create the SRT file without rendering captions onto a video. |
| `--list-styles` | List available caption styles. |
| `-h`, `--help` | Show all command-line options. |

## Troubleshooting

- **`ffmpeg` or `ffprobe` not found:** Install FFmpeg and add its `bin` folder to `PATH`, then open a new PowerShell window.
- **Captions are not rendered:** Check `ffmpeg -version` and make sure a recent FFmpeg build is being used.
- **No speech detected:** Confirm that the video has an audio track and that the selected language is correct, or try `--lang auto`.
- **API request failed:** Check that the Groq API key is valid and that the computer has an internet connection.

## License

Copyright 2026 Amr Mohamed Hasanain.

Licensed under the [Apache License 2.0](LICENSE).