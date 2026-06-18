from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "output" / "pdf"
OUT_DIR.mkdir(parents=True, exist_ok=True)

SHOT_SHELBURNE = Path("/var/folders/jn/lf78l6md42g9lbb7vsfkv9lc0000gn/T/codex-clipboard-29adc0d5-07e5-4985-8ff9-6701235122e1.png")
SHOT_SHAKER = Path("/var/folders/jn/lf78l6md42g9lbb7vsfkv9lc0000gn/T/codex-clipboard-5d3501ff-4c49-4810-a22f-fedf515daa2d.png")

PNG_PATH = OUT_DIR / "Shelburne_Actual_Map_Views_For_Nancy.png"
PDF_PATH = OUT_DIR / "Shelburne_Actual_Map_Views_For_Nancy.pdf"

INK = (24, 33, 47)
MUTED = (86, 96, 111)
RED = (153, 27, 27)
TEAL = (15, 118, 110)
GREEN = (21, 128, 61)
PAPER = (255, 250, 242)
WHITE = (255, 255, 255)
LINE = (216, 207, 192)
PALE_RED = (254, 242, 242)


def font(size, bold=False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


FONT_TITLE = font(46, True)
FONT_H2 = font(29, True)
FONT_BODY = font(22)
FONT_BODY_BOLD = font(22, True)
FONT_SMALL = font(18)
FONT_STAT = font(30, True)


def wrapped_lines(draw, text, max_width, font_obj):
    words = text.split()
    lines = []
    current = []
    for word in words:
        candidate = " ".join(current + [word])
        if not current or draw.textbbox((0, 0), candidate, font=font_obj)[2] <= max_width:
            current.append(word)
        else:
            lines.append(" ".join(current))
            current = [word]
    if current:
        lines.append(" ".join(current))
    return lines


def draw_wrapped(draw, text, xy, max_width, font_obj, fill=INK, gap=7):
    x, y = xy
    for line in wrapped_lines(draw, text, max_width, font_obj):
        draw.text((x, y), line, fill=fill, font=font_obj)
        y += font_obj.size + gap
    return y


def fit_cover(img, width, height):
    scale = max(width / img.width, height / img.height)
    resized = img.resize((int(img.width * scale), int(img.height * scale)), Image.Resampling.LANCZOS)
    left = max(0, (resized.width - width) // 2)
    top = max(0, (resized.height - height) // 2)
    return resized.crop((left, top, left + width, top + height))


def map_crop(source, box, size):
    cropped = source.crop(box)
    return fit_cover(cropped, *size)


def round_rect(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def stat_card(draw, box, value, label):
    round_rect(draw, box, 16, PALE_RED, RED, 2)
    x1, y1, x2, _ = box
    draw.text((x1 + 18, y1 + 14), value, fill=RED, font=FONT_STAT)
    draw_wrapped(draw, label, (x1 + 18, y1 + 50), x2 - x1 - 36, FONT_SMALL, fill=INK, gap=2)


def bullet(draw, x, y, text, max_width):
    draw.ellipse((x, y + 9, x + 9, y + 18), fill=TEAL)
    return draw_wrapped(draw, text, (x + 22, y), max_width, FONT_BODY, fill=INK, gap=6)


def make_panel(number, title, bullets, stats, source, crop_box, color=TEAL):
    panel_w, panel_h = 1600, 780
    margin = 28
    text_w = 515
    map_x = margin + text_w + 28
    map_w = panel_w - map_x - margin
    map_h = panel_h - 2 * margin

    img = Image.new("RGB", (panel_w, panel_h), PAPER)
    draw = ImageDraw.Draw(img)
    round_rect(draw, (16, 16, panel_w - 16, panel_h - 16), 22, WHITE, LINE, 3)

    y = 42
    draw.text((48, y), f"{number}. {title}", fill=INK, font=FONT_H2)
    y += 55

    for value, label in stats:
        stat_card(draw, (48, y, 48 + text_w, y + 92), value, label)
        y += 108

    y += 4
    for item in bullets:
        y = bullet(draw, 52, y, item, text_w - 28)
        y += 18

    map_img = map_crop(source, crop_box, (map_w, map_h))
    img.paste(map_img, (map_x, margin))
    draw.rounded_rectangle((map_x, margin, map_x + map_w, margin + map_h), radius=18, outline=LINE, width=3)
    draw.rectangle((map_x, margin, map_x + 12, margin + map_h), fill=color)
    return img


def make_outputs():
    shelburne = Image.open(SHOT_SHELBURNE).convert("RGB")
    shaker = Image.open(SHOT_SHAKER).convert("RGB")

    panels = [
        make_panel(
            "1",
            "Shelburne cut-through",
            [
                "Largest Shelburne residential-street concern.",
                "This is the segment to ask staff to evaluate first.",
                "Compare with the lower-count section east of Warrensville.",
            ],
            [
                ("40", "crashes between Shelburne / Eaton-Fairmount and Warrensville"),
                ("16", "people injured on this Shelburne segment"),
                ("16 vs 40", "crashes east of Warrensville vs this core segment"),
            ],
            shelburne,
            (710, 210, 2048, 890),
            TEAL,
        ),
        make_panel(
            "2",
            "Fairmount Circle / Fairmount Blvd",
            [
                "Everyday destination area: pharmacy, food, restaurants, and future Trader Joe's.",
                "Crash burden is concentrated around places families walk to.",
                "Useful ask: focused crossing and circle safety review.",
            ],
            [
                ("74", "crashes in the Fairmount Circle area"),
                ("16", "people injured in the Fairmount Circle area"),
                ("160", "broader Fairmount corridor crashes"),
            ],
            shelburne,
            (1635, 150, 2090, 725),
            RED,
        ),
        make_panel(
            "3",
            "Shaker / Warrensville school area",
            [
                "School, library, athletic fields, transit, and crossings overlap here.",
                "Affects Shaker Middle, Bertram Woods Library, and University School access.",
                "Useful ask: school-zone crossing review and interim protections.",
            ],
            [
                ("61", "crashes at Warrensville + Shaker"),
                ("25", "people injured at Warrensville + Shaker"),
                ("0", "tracked crashes on Chesterton comparison route"),
            ],
            shaker,
            (690, 540, 2050, 990),
            GREEN,
        ),
    ]

    header_h = 150
    gap = 22
    footer_h = 96
    out_w = 1600
    out_h = header_h + len(panels) * 780 + (len(panels) - 1) * gap + footer_h
    out = Image.new("RGB", (out_w, out_h), PAPER)
    draw = ImageDraw.Draw(out)
    draw.text((42, 34), "Three Priority Safety Areas", fill=INK, font=FONT_TITLE)
    draw.text((44, 90), "Actual map views with the key numbers pulled out for quick review", fill=MUTED, font=FONT_BODY)

    y = header_h
    for panel in panels:
        out.paste(panel, (0, y))
        y += panel.height + gap

    round_rect(draw, (42, out_h - 72, out_w - 42, out_h - 22), 16, WHITE, LINE, 2)
    draw.text((66, out_h - 57), "Specific ask:", fill=INK, font=FONT_BODY_BOLD)
    draw.text((220, out_h - 56), "Who is the right staff person, committee, or process to review these three areas?", fill=INK, font=FONT_BODY)
    out.save(PNG_PATH)

    page_w, page_h = landscape(letter)
    c = canvas.Canvas(str(PDF_PATH), pagesize=(page_w, page_h))
    c.setTitle("Shelburne actual map views for quick review")
    for panel in panels:
        tmp = OUT_DIR / "_actual_map_panel.png"
        panel.save(tmp)
        c.setFillColorRGB(*(v / 255 for v in PAPER))
        c.rect(0, 0, page_w, page_h, fill=1, stroke=0)
        c.drawImage(str(tmp), 0.22 * inch, 0.18 * inch, width=page_w - 0.44 * inch, height=page_h - 0.36 * inch, preserveAspectRatio=True, anchor="c")
        c.showPage()
        tmp.unlink(missing_ok=True)
    c.save()


if __name__ == "__main__":
    make_outputs()
    print(PNG_PATH)
    print(PDF_PATH)
