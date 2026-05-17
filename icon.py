"""Generate the tray/window icon programmatically using Pillow."""
from PIL import Image, ImageDraw, ImageFont


def make_icon(size: int = 64) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Dark background circle
    draw.ellipse([2, 2, size - 3, size - 3], fill=(30, 30, 40, 255))

    # Green ring
    draw.ellipse([2, 2, size - 3, size - 3], outline=(46, 204, 113, 255), width=max(2, size // 20))

    # "E" text centred
    text = "E"
    font_size = int(size * 0.52)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except OSError:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (size - tw) // 2 - bbox[0]
    y = (size - th) // 2 - bbox[1]
    draw.text((x, y), text, font=font, fill=(46, 204, 113, 255))

    return img
