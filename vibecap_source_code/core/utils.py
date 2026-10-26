import shutil
import subprocess
import sys
import json
from pathlib import Path
from rich.console import Console  # type: ignore[import-not-found]
import os
import shlex

console = Console()

def fail(msg):
    console.print(f"[bold red]❌ Error:[/bold red] {msg}")
    sys.exit(1)

def find_tool(name):
    exe = name + (".exe" if sys.platform.startswith("win") else "")
    for base in (Path(__file__).resolve().parent.parent.parent, Path.cwd()):
        for p in (base / "ffmpeg" / exe, base / exe):
            if p.exists():
                return str(p)
    found = shutil.which(name)
    if not found:
        fail(f"{name} not found. Install FFmpeg or put it in ./ffmpeg/")
    return found

def run(cmd, cwd=None):
    command = [str(arg) for arg in cmd]
    shell_command = (
        subprocess.list2cmdline(command)
        if os.name == "nt"
        else " ".join(shlex.quote(arg) for arg in command)
    )

    previous_dir = None
    try:
        if cwd is not None:
            previous_dir = os.getcwd()
            os.chdir(cwd)
        status = os.system(shell_command)
    finally:
        if previous_dir is not None:
            os.chdir(previous_dir)

    exit_code = status if os.name == "nt" else os.waitstatus_to_exitcode(status)
    if exit_code != 0:
        fail("FFmpeg execution failed.")
    return exit_code

def video_size(ffprobe, path):
    try:
        out = subprocess.check_output([
            ffprobe, "-v", "error", "-select_streams", "v:0",
            "-show_streams", "-of", "json", str(path)],
            text=True, stderr=subprocess.DEVNULL)
        st = json.loads(out)["streams"][0]
        w, h = int(st["width"]), int(st["height"])
        rot = st.get("tags", {}).get("rotate")
        if rot is None:
            rot = next((d["rotation"] for d in st.get("side_data_list", []) if "rotation" in d), 0)
        return (h, w) if abs(int(float(rot))) in (90, 270) else (w, h)
    except Exception:
        return 1920, 1080

def path_tool(name: str) -> str:
    """Check FFmpeg on PATH via the system shell and return its command name."""
    filename = name + (".exe" if os.name == "nt" else "")

    # Prefer the WinGet link directory if it is available on Windows PATH.
    if os.name == "nt":
        local_app_data = os.environ.get("LOCALAPPDATA")
        if local_app_data:
            winget_dir = Path(local_app_data) / "Microsoft" / "WinGet" / "Links"
            if (winget_dir / filename).is_file():
                os.environ["PATH"] = str(winget_dir) + os.pathsep + os.environ.get("PATH", "")

    redirect = " >NUL 2>&1" if os.name == "nt" else " >/dev/null 2>&1"
    if os.system(filename + " -version" + redirect) == 0:
        return filename

    raise FileNotFoundError(
        f"{filename} not found on PATH. Install FFmpeg and add its bin folder to PATH."
    )