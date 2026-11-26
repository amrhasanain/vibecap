
<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://groq.com/"><img src="https://img.shields.io/badge/Groq%20Whisper-F55036?style=flat" alt="Groq Whisper"></a>
  <a href="https://ffmpeg.org/"><img src="https://img.shields.io/badge/FFmpeg-007808?style=flat&logo=ffmpeg&logoColor=white" alt="FFmpeg"></a>
  <a href="https://github.com/amrhasanain/vibecap"><img src="https://img.shields.io/badge/Arabic-16A34A?style=flat" alt="Arabic"></a>
  <a href="https://github.com/amrhasanain/vibecap"><img src="https://img.shields.io/badge/English-2563EB?style=flat" alt="English"></a>
  <a href="https://github.com/amrhasanain/vibecap"><img src="https://img.shields.io/badge/SRT%20Export-475569?style=flat" alt="SRT Export"></a>
</p>


<h1 align="center">VibeCap</h1>

<p align="center">
  Auto caption maker ✨. Powered by Groq Whisper for transcription and FFmpeg for audio extraction and caption rendering.
</p>


---

VibeCap is a Python script, not a standalone executable. Run it with `vibecap` from the project folder.

## Requirements

- `Python 3`
- `Git` to clone the repository, or you can use `pip` instead
- A Groq API key
- A recent FFmpeg installation with both `ffmpeg` and `ffprobe` available on `PATH`

Check that FFmpeg is available in PowerShell:

```powershell
ffmpeg -version
ffprobe -version
```


## Installation
### With git:
```powershell
git clone https://github.com/amrhasanain/vibecap
cd vibecap
python -m pip install -e .
```

### With pip:

```powershell
python -m pip install vibecap
```


## Groq API key

On the first run, VibeCap prompts for your Groq API key and saves it locally in your user configuration folder. You can also save it from PowerShell with:

```powershell
vibecap --key YOUR_GROQ_API_KEY
```

## Usage

Run the script without arguments to open the interactive wizard:

```powershell
vibecap
```

To see the available command-line options:

```powershell
vibecap --help
```

Caption a video in Arabic with the minimal style:

```powershell
vibecap "input.mp4" --lang ar --style minimal --model turbo
```

Create only an SRT subtitle file:

```powershell
vibecap "input.mp4" --lang ar --srt-only
```

Choose a different output path, font, or subtitle position:

```powershell
vibecap "input.mp4" --lang en --style classic --output "output.mp4" --font "Arial" --position bottom
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
