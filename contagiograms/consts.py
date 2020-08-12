
import matplotlib.font_manager as fm

types_colors = {
    "AT": "dimgrey",
    "RT": "darkorange",
    "OT": "steelblue",
}

fm._rebuild()
fonts = {
    "Default": fm.FontProperties(family=["sans-serif"]),
    "Korean": fm.FontProperties(
        family=["Noto Sans CJK KR", "Noto Sans CJK", "sans-serif"]
    ),
    "Tamil": fm.FontProperties(family=["Noto Sans Tamil", "sans-serif"]),
}

contagiograms = dict(
    example=[
        ("kevät", "fi"),
        ("Carnaval", "pt"),
        ("Lionel Messi", "es"),
        ("#TGIF", "en"),
        ("virus", "fr"),
        ("Brexit", "de"),
    ],
    langs=[
        ("❤", "en"),
        ("Resurrección", "es"),
        ("?", "und"),
        ("eleição", "pt"),
        ("ثورة", "ar"),
        ("@bts_twt", "ko"),
        ("Flüchtling", "de"),
        ("San Valentino", "it"),
        ("карантин", "ru"),
    ],
)

loi = [
    "en",
    "ja",
    "und",
    "es",
    "pt",
    "ar",
    "th",
    "ko",
    "fr",
    "tr",
    "de",
    "it",
]
