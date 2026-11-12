try:
    from rich.table import Table  # type: ignore[import-not-found]
    from rich.console import Console  # type: ignore[import-not-found]

    console = Console()
except ImportError:
    Table = None
    Console = None
    console = None


# ASS override tags for caption animations
POP = (
    r"\fscx78\fscy78\t(0,110,\fscx104\fscy104)"
    r"\t(110,190,\fscx100\fscy100)"
)
BOUNCE = (
    r"\fscx65\fscy65\t(0,100,\fscx118\fscy118)"
    r"\t(100,190,\fscx100\fscy100)"
)
SOFT = r"\fscx92\fscy92\fad(90,0)\t(0,150,\fscx100\fscy100)"


# Shared defaults for all caption styles
BASE = dict(
    font="Arial",
    size=70,
    bold=True,
    upper=False,
    color="FFFFFF",
    highlight="FFE600",
    highlight_bg=None,
    sweep=False,
    outline_c="000000",
    outline_a=0,
    outline=4.0,
    shadow=1.0,
    border=1,
    glow=None,
    glow_blur=0,
    align=2,
    margin=0.16,
    max_chars=30,
    max_lines=1,
    max_words=4,
    max_dur=4.0,
    fx=POP,
    desc="",
)


STYLES = {
    "classic": {
        **BASE,
        "font": "Arial",
        "size": 70,
        "bold": True,
        "color": "FFFFFF",
        "highlight": "FFFFFF",
        "highlight_bg": "FFE600",
        "outline_c": "000000",
        "outline": 5.0,
        "outline_a": 0,
        "shadow": 1.0,
        "desc": "Bold white text with a thicker clean black outline and a yellow background behind the active word.",
    },
    "impact": {
        **BASE,
        "font": "Impact",
        "size": 76,
        "bold": True,
        "outline": 5.0,
        "shadow": 1.5,
        "highlight": "FFD400",
        "max_words": 3,
        "desc": "Heavy condensed lettering with a strong black edge.",
    },
    "montserrat": {
        **BASE,
        "font": "Montserrat ExtraBold",
        "size": 68,
        "bold": True,
        "outline": 4.0,
        "shadow": 1.2,
        "highlight": "38E879",
        "desc": "Modern geometric bold font with a crisp outline and green highlight.",
    },
    "anton": {
        **BASE,
        "font": "Anton",
        "size": 76,
        "bold": True,
        "outline": 5.0,
        "shadow": 1.5,
        "highlight": "35D7FF",
        "max_words": 3,
        "desc": "Tall, powerful display lettering with a cyan active word.",
    },
    "youtube": {
        **BASE,
        "font": "Montserrat ExtraBold",
        "size": 64,
        "bold": True,
        "border": 3,
        "outline": 4.0,
        "outline_a": 0x20,
        "shadow": 1.5,
        "highlight": "00E676",
        "margin": 0.14,
        "desc": "Strong white captions with a subtle dark edge and green highlight.",
    },
    "tiktok": {
        **BASE,
        "font": "Arial Black",
        "size": 84,
        "bold": True,
        "upper": True,
        "outline": 6.0,
        "shadow": 2.0,
        "max_words": 3,
        "max_chars": 24,
        "margin": 0.20,
        "fx": BOUNCE,
        "desc": "Large uppercase captions with a bounce and yellow highlight.",
    },
    "karaoke": {
        **BASE,
        "font": "Montserrat Bold",
        "size": 70,
        "bold": True,
        "highlight": "FF9500",
        "sweep": True,
        "fx": SOFT,
        "desc": "Bold modern lettering with a smooth orange word-by-word sweep.",
    },
    "neon": {
        **BASE,
        "font": "Arial Black",
        "size": 72,
        "bold": True,
        "highlight": "FF4FD8",
        "outline_c": "00E5FF",
        "outline": 2.5,
        "glow": "00E5FF",
        "glow_blur": 9,
        "max_words": 3,
        "margin": 0.18,
        "desc": "Neon cyan glow with a hot-pink active word.",
    },
    "minimal": {
        **BASE,
        "font": "Inter",
        "size": 58,
        "bold": False,
        "color": "F2F2F2",
        "highlight": "7CF5C0",
        "outline": 2.0,
        "shadow": 1.5,
        "margin": 0.08,
        "fx": SOFT,
        "desc": "Light, simple captions with a soft fade and mint highlight.",
    },
    "cinematic": {
        **BASE,
        "font": "Montserrat SemiBold",
        "size": 62,
        "bold": True,
        "color": "FFF8E8",
        "highlight": "E8C46A",
        "outline": 2.5,
        "outline_a": 30,
        "shadow": 2.0,
        "margin": 0.12,
        "fx": SOFT,
        "desc": "Warm cinematic text with restrained shadow and gold highlight.",
    },
}


def show_styles():
    if Table is None or console is None:
        for name, style in STYLES.items():
            print(f"{name}: {style['desc']}")
        return

    table = Table(
        title="✨ Available Caption Styles ✨",
        header_style="bold cyan",
        border_style="bright_blue",
    )
    table.add_column("Style Name", style="bold green")
    table.add_column("Description", style="white")

    for name, style in STYLES.items():
        table.add_row(name, style["desc"])

    console.print(table)