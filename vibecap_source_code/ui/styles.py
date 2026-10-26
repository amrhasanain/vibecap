try:
    from rich.table import Table  # type: ignore[import-not-found]
    from rich.console import Console  # type: ignore[import-not-found]
    console = Console()
except ImportError:
    Table = None
    Console = None
    console = None

POP = "\\fscx78\\fscy78\\t(0,110,\\fscx104\\fscy104)\\t(110,190,\\fscx100\\fscy100)"
BOUNCE = "\\fscx65\\fscy65\\t(0,100,\\fscx118\\fscy118)\\t(100,190,\\fscx100\\fscy100)"
SOFT = "\\fscx92\\fscy92\\fad(90,0)\\t(0,150,\\fscx100\\fscy100)"

BASE = dict(
    font="Arial", size=70, bold=True, upper=False,
    color="FFFFFF", highlight="FFE600", sweep=False,
    outline_c="000000", outline_a=0, outline=4.0, shadow=0.0, border=1,
    glow=None, glow_blur=0, align=2, margin=0.16,
    max_chars=30, max_lines=1, max_words=4, max_dur=4.0, fx=POP, desc="",
)

STYLES = {
    "classic": {**BASE, "desc": "White bold text, black outline, active word turns yellow. 4 words."},
    "youtube": {**BASE, "size": 64, "border": 3, "outline": 10, "outline_a": 0x59, "highlight": "00E676", "margin": 0.14, "desc": "Dark rounded-look box, active word turns green. 4 words."},
    "tiktok": {**BASE, "size": 88, "upper": True, "outline": 6, "max_words": 3, "max_chars": 24, "margin": 0.20, "fx": BOUNCE, "desc": "Huge uppercase, bounce-in, yellow active word. 3 words."},
    "karaoke": {**BASE, "size": 72, "highlight": "FF9500", "sweep": True, "fx": SOFT, "desc": "Orange colour sweeps smoothly across each word. 4 words."},
    "neon": {**BASE, "size": 74, "highlight": "FF4FD8", "outline_c": "00E5FF", "outline": 2.5, "glow": "00E5FF", "glow_blur": 9, "max_words": 3, "margin": 0.18, "desc": "Real neon glow (cyan), active word turns hot pink. 3 words."},
    "minimal": {**BASE, "size": 58, "bold": False, "color": "F2F2F2", "highlight": "7CF5C0", "outline": 2.0, "shadow": 1.5, "margin": 0.08, "fx": SOFT, "desc": "Light and elegant, soft fade-in, mint active word. 4 words."},
}

def show_styles():
    t = Table(title="✨ Available Caption Styles ✨", header_style="bold cyan", border_style="bright_blue")
    t.add_column("Style Name", style="bold green")
    t.add_column("Description", style="white")
    for name, s in STYLES.items():
        t.add_row(name, s["desc"])
    console.print(t)