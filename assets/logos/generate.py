#!/usr/bin/env python3
"""Generate SearchingBinary logo PNGs in all sizes and variants."""

from PIL import Image, ImageDraw, ImageFont
import os

DIR = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = os.path.join(DIR, "font", "InstrumentSerif-Regular.ttf")

# Brand colors
NAVY = (10, 22, 40)
GOLD = (200, 164, 94)
CREAM = (250, 248, 244)
WHITE = (255, 255, 255)
TRANSPARENT = (0, 0, 0, 0)

def load_font(size):
    return ImageFont.truetype(FONT_PATH, size)

def draw_full_logo(w, h, bg_color, text_color, gold_color, transparent_bg=False):
    """Draw full 'SearchingBinary' wordmark."""
    if transparent_bg:
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    else:
        img = Image.new("RGBA", (w, h), bg_color + (255,) if len(bg_color) == 3 else bg_color)

    draw = ImageDraw.Draw(img)
    font_size = int(h * 0.36)
    font = load_font(font_size)

    text1 = "Searching"
    text2 = "Binary"

    bbox1 = draw.textbbox((0, 0), text1, font=font)
    bbox2 = draw.textbbox((0, 0), text2, font=font)
    w1 = bbox1[2] - bbox1[0]
    w2 = bbox2[2] - bbox2[0]
    total_w = w1 + w2

    x_start = (w - total_w) // 2
    y = (h - font_size) // 2 - int(font_size * 0.08)

    tc = text_color + (255,) if len(text_color) == 3 else text_color
    gc = gold_color + (255,) if len(gold_color) == 3 else gold_color

    draw.text((x_start, y), text1, fill=tc, font=font)
    draw.text((x_start + w1, y), text2, fill=gc, font=font)

    return img

def draw_icon(size, bg_color, text_color, gold_color, rounded=True):
    """Draw SB monogram icon."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Rounded rectangle background
    if rounded:
        r = int(size * 0.18)
        draw.rounded_rectangle([0, 0, size-1, size-1], radius=r,
                                fill=bg_color + (255,) if len(bg_color) == 3 else bg_color)
    else:
        draw.rectangle([0, 0, size-1, size-1],
                       fill=bg_color + (255,) if len(bg_color) == 3 else bg_color)

    font_size = int(size * 0.42)
    font = load_font(font_size)

    s_text = "S"
    b_text = "B"

    bbox_s = draw.textbbox((0, 0), s_text, font=font)
    bbox_b = draw.textbbox((0, 0), b_text, font=font)
    ws = bbox_s[2] - bbox_s[0]
    wb = bbox_b[2] - bbox_b[0]
    gap = int(size * 0.01)
    total = ws + gap + wb

    x_start = (size - total) // 2
    y = (size - font_size) // 2 - int(font_size * 0.08)

    tc = text_color + (255,) if len(text_color) == 3 else text_color
    gc = gold_color + (255,) if len(gold_color) == 3 else gold_color

    draw.text((x_start, y), s_text, fill=tc, font=font)
    draw.text((x_start + ws + gap, y), b_text, fill=gc, font=font)

    return img

def draw_favicon(size):
    """Draw small favicon with SB on navy background."""
    img = Image.new("RGBA", (size, size), NAVY + (255,))
    draw = ImageDraw.Draw(img)

    font_size = int(size * 0.55)
    font = load_font(font_size)

    s_text = "S"
    b_text = "B"

    bbox_s = draw.textbbox((0, 0), s_text, font=font)
    bbox_b = draw.textbbox((0, 0), b_text, font=font)
    ws = bbox_s[2] - bbox_s[0]
    wb = bbox_b[2] - bbox_b[0]
    total = ws + wb

    x_start = (size - total) // 2
    y = (size - font_size) // 2 - int(font_size * 0.1)

    draw.text((x_start, y), s_text, fill=CREAM + (255,), font=font)
    draw.text((x_start + ws, y), b_text, fill=GOLD + (255,), font=font)

    return img

def draw_og_image():
    """Draw Open Graph social share image 1200x630."""
    w, h = 1200, 630
    img = Image.new("RGBA", (w, h), NAVY + (255,))
    draw = ImageDraw.Draw(img)

    # Subtle circle accents
    circle_color = (200, 164, 94, 20)
    draw.ellipse([w*0.75, h*0.05, w*0.75+400, h*0.05+400], outline=circle_color, width=1)
    draw.ellipse([w*0.02, h*0.6, w*0.02+300, h*0.6+300], outline=circle_color, width=1)

    # Gold line
    gold_line_color = GOLD + (100,)
    line_y = int(h * 0.49)
    draw.rectangle([int(w*0.35), line_y, int(w*0.65), line_y+1], fill=gold_line_color)

    # Company name
    name_size = int(h * 0.13)
    name_font = load_font(name_size)

    text1 = "Searching"
    text2 = "Binary"
    bbox1 = draw.textbbox((0, 0), text1, font=name_font)
    bbox2 = draw.textbbox((0, 0), text2, font=name_font)
    w1 = bbox1[2] - bbox1[0]
    w2 = bbox2[2] - bbox2[0]
    total_w = w1 + w2
    x_start = (w - total_w) // 2
    y_name = int(h * 0.3)

    draw.text((x_start, y_name), text1, fill=CREAM + (255,), font=name_font)
    draw.text((x_start + w1, y_name), text2, fill=GOLD + (255,), font=name_font)

    # Tagline
    tag_size = int(h * 0.035)
    tag_font = load_font(tag_size)
    tagline = "Investment  |  Business Advisory  |  AI Consultancy  |  QA Consultancy"
    tag_bbox = draw.textbbox((0, 0), tagline, font=tag_font)
    tag_w = tag_bbox[2] - tag_bbox[0]
    draw.text(((w - tag_w) // 2, int(h * 0.56)), tagline, fill=CREAM + (130,), font=tag_font)

    return img

def save(img, filename):
    """Save image to logos directory."""
    path = os.path.join(DIR, filename)
    img.save(path, "PNG", optimize=True)
    size_kb = os.path.getsize(path) / 1024
    print(f"  {filename:45s} {img.size[0]:>5d}x{img.size[1]:<5d} ({size_kb:.1f} KB)")

def main():
    print("Generating SearchingBinary logos...\n")

    # ── FULL LOGOS ──
    full_sizes = [(1600, 400), (800, 200), (400, 100)]
    full_variants = [
        ("dark", NAVY, CREAM, GOLD, False),
        ("light", CREAM, NAVY, GOLD, False),
        ("white", WHITE, NAVY, GOLD, False),
        ("transparent", None, NAVY, GOLD, True),
    ]

    print("Full Logo Wordmarks:")
    for name, bg, text, gold, transp in full_variants:
        for w, h in full_sizes:
            img = draw_full_logo(w, h, bg or (0,0,0), text, gold, transparent_bg=transp)
            save(img, f"logo-full-{name}-{w}x{h}.png")

    # ── ICON / MONOGRAM ──
    icon_sizes = [1024, 512, 256, 180, 128, 64]
    icon_variants = [
        ("dark", NAVY, CREAM, GOLD),
        ("light", CREAM, NAVY, GOLD),
        ("white", WHITE, NAVY, GOLD),
    ]

    print("\nIcon Monograms (SB):")
    for name, bg, text, gold in icon_variants:
        for size in icon_sizes:
            img = draw_icon(size, bg, text, gold)
            save(img, f"icon-{name}-{size}x{size}.png")

    # ── FAVICONS ──
    print("\nFavicons:")
    for size in [48, 32, 16]:
        img = draw_favicon(size)
        save(img, f"favicon-{size}x{size}.png")

    # ── OG IMAGE ──
    print("\nOpen Graph:")
    img = draw_og_image()
    save(img, "og-image-1200x630.png")

    # ── APPLE TOUCH ICON ──
    print("\nApple Touch Icon:")
    img = draw_icon(180, NAVY, CREAM, GOLD, rounded=False)
    save(img, "apple-touch-icon-180x180.png")

    # ── FAVICON.ICO (multi-size) ──
    print("\nFavicon ICO (multi-size):")
    ico_16 = draw_favicon(16).convert("RGBA")
    ico_32 = draw_favicon(32).convert("RGBA")
    ico_48 = draw_favicon(48).convert("RGBA")
    ico_path = os.path.join(DIR, "..", "..", "favicon.ico")
    ico_16.save(ico_path, format="ICO", sizes=[(16,16), (32,32), (48,48)],
                append_images=[ico_32, ico_48])
    print(f"  {'../../favicon.ico':45s} multi-size ICO")

    total = len(full_sizes) * len(full_variants) + len(icon_sizes) * len(icon_variants) + 3 + 1 + 1 + 1
    print(f"\nDone! Generated {total} PNG files + 1 ICO file.")

if __name__ == "__main__":
    main()
