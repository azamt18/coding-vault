"""Draws the extension icon (a white Ş on a green rounded square) at every size Chrome needs."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
GREEN = (11, 122, 92, 255)
OUT = Path(__file__).resolve().parent.parent / "public" / "icon"

def draw(size: int) -> Image.Image:
    scale = 8  # draw large, then shrink for smooth edges
    big = size * scale
    image = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    canvas = ImageDraw.Draw(image)
    canvas.rounded_rectangle((0, 0, big - 1, big - 1), radius=big // 5, fill=GREEN)
    font = ImageFont.truetype(FONT, int(big * 0.62))
    left, top, right, bottom = canvas.textbbox((0, 0), "Ş", font=font)
    x = (big - (right - left)) / 2 - left
    y = (big - (bottom - top)) / 2 - top
    canvas.text((x, y), "Ş", font=font, fill="white")
    return image.resize((size, size), Image.LANCZOS)

OUT.mkdir(parents=True, exist_ok=True)
for size in (16, 32, 48, 96, 128):
    draw(size).save(OUT / f"{size}.png")
print("icons written to", OUT)
