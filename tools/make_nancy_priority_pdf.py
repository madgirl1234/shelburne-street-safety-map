from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "output" / "pdf"
OUT_DIR.mkdir(parents=True, exist_ok=True)
PDF_PATH = OUT_DIR / "Shelburne_Three_Priority_Safety_Areas.pdf"


W, H = letter
M = 0.45 * inch
INK = colors.HexColor("#18212f")
MUTED = colors.HexColor("#5b6472")
RED = colors.HexColor("#991b1b")
RED_LIGHT = colors.HexColor("#fee2e2")
TEAL = colors.HexColor("#0f7a8a")
GREEN = colors.HexColor("#16784f")
PAPER = colors.HexColor("#fffaf2")
LINE = colors.HexColor("#d8cfc0")
BLUE = colors.HexColor("#2563eb")
ORANGE = colors.HexColor("#d8791d")


def wrap_text(c, text, x, y, max_width, font="Helvetica", size=9, leading=11, color=MUTED):
    c.setFont(font, size)
    c.setFillColor(color)
    words = text.split()
    lines = []
    current = []
    for word in words:
        candidate = " ".join(current + [word])
        if c.stringWidth(candidate, font, size) <= max_width:
            current.append(word)
        else:
            if current:
                lines.append(" ".join(current))
            current = [word]
    if current:
        lines.append(" ".join(current))
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y


def pill(c, x, y, w, h, text, stroke=GREEN, fill=colors.white, text_color=GREEN):
    c.setStrokeColor(stroke)
    c.setFillColor(fill)
    c.setLineWidth(1.4)
    c.roundRect(x, y, w, h, h / 2, stroke=1, fill=1)
    c.setFillColor(text_color)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(x + w / 2, y + h / 2 - 3, text)


def stat_box(c, x, y, w, h, value, label):
    c.setStrokeColor(LINE)
    c.setFillColor(colors.white)
    c.roundRect(x, y, w, h, 8, stroke=1, fill=1)
    c.setFillColor(RED)
    size = 20
    while c.stringWidth(value, "Helvetica-Bold", size) > w - 20 and size > 14:
        size -= 1
    c.setFont("Helvetica-Bold", size)
    c.drawString(x + 10, y + h - 25, value)
    wrap_text(c, label, x + 10, y + h - 39, w - 20, size=7.7, leading=9)


def crash_bubble(c, x, y, r, label):
    c.setFillColor(colors.Color(0.65, 0.08, 0.08, alpha=0.72))
    c.setStrokeColor(RED)
    c.setLineWidth(1.5)
    c.circle(x, y, r, stroke=1, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(x, y - 3, label)


def draw_shelburne_map(c, x, y, w, h):
    c.setFillColor(colors.HexColor("#f3f6f0"))
    c.setStrokeColor(LINE)
    c.roundRect(x, y, w, h, 10, stroke=1, fill=1)

    # Parks / green area
    c.setFillColor(colors.HexColor("#b9e4a8"))
    c.roundRect(x + 12, y + 14, w - 24, 34, 10, stroke=0, fill=1)

    # Roads
    c.setStrokeColor(colors.white)
    c.setLineWidth(12)
    c.line(x + 18, y + 70, x + w - 18, y + 70)  # Shelburne
    c.line(x + w * 0.25, y + 22, x + w * 0.25, y + h - 18)  # Courtland
    c.line(x + w * 0.64, y + 22, x + w * 0.64, y + h - 18)  # Warrensville
    c.setStrokeColor(colors.HexColor("#cbd5e1"))
    c.setLineWidth(1)
    c.line(x + 18, y + 70, x + w - 18, y + 70)
    c.line(x + w * 0.25, y + 22, x + w * 0.25, y + h - 18)
    c.line(x + w * 0.64, y + 22, x + w * 0.64, y + h - 18)

    # Highlighted sections
    c.setStrokeColor(TEAL)
    c.setLineWidth(7)
    c.line(x + 18, y + 70, x + w * 0.64, y + 70)
    c.setStrokeColor(GREEN)
    c.line(x + w * 0.64, y + 70, x + w - 18, y + 70)
    crash_bubble(c, x + w * 0.42, y + 70, 18, "40")
    crash_bubble(c, x + w * 0.81, y + 70, 13, "16")

    pill(c, x + 16, y + h - 28, 60, 18, "Shelburne", stroke=TEAL, text_color=TEAL)
    pill(c, x + w * 0.64 - 22, y + h - 28, 72, 18, "Warrensville", stroke=GREEN, text_color=GREEN)


def draw_fairmount_map(c, x, y, w, h):
    c.setFillColor(colors.HexColor("#f4f1e8"))
    c.setStrokeColor(LINE)
    c.roundRect(x, y, w, h, 10, stroke=1, fill=1)
    c.setFillColor(colors.HexColor("#cdeebd"))
    c.roundRect(x + 10, y + 12, w - 20, 28, 10, stroke=0, fill=1)

    c.setStrokeColor(colors.white)
    c.setLineWidth(13)
    c.line(x + 12, y + h * 0.54, x + w - 12, y + h * 0.54)  # Fairmount
    c.line(x + w * 0.56, y + 16, x + w * 0.56, y + h - 16)  # Warrensville
    c.setStrokeColor(colors.HexColor("#d0d7de"))
    c.setLineWidth(1)
    c.line(x + 12, y + h * 0.54, x + w - 12, y + h * 0.54)
    c.line(x + w * 0.56, y + 16, x + w * 0.56, y + h - 16)

    c.setStrokeColor(RED)
    c.setLineWidth(7)
    c.line(x + 16, y + h * 0.54, x + w - 16, y + h * 0.54)
    crash_bubble(c, x + w * 0.56, y + h * 0.54, 22, "74")
    crash_bubble(c, x + w * 0.56, y + 33, 18, "55")
    pill(c, x + w * 0.56 - 32, y + h * 0.54 + 29, 78, 18, "Circle area", stroke=RED, text_color=RED)
    pill(c, x + 18, y + h - 28, 72, 18, "Fairmount", stroke=RED, text_color=RED)


def draw_shaker_map(c, x, y, w, h):
    c.setFillColor(colors.HexColor("#eef6f1"))
    c.setStrokeColor(LINE)
    c.roundRect(x, y, w, h, 10, stroke=1, fill=1)
    c.setFillColor(colors.HexColor("#b9e4a8"))
    c.roundRect(x + 12, y + 12, w - 24, 30, 10, stroke=0, fill=1)

    c.setStrokeColor(colors.white)
    c.setLineWidth(13)
    c.line(x + 12, y + 55, x + w - 12, y + 55)  # Shaker
    c.line(x + w * 0.42, y + 16, x + w * 0.42, y + h - 16)  # Warrensville
    c.setStrokeColor(colors.HexColor("#d0d7de"))
    c.setLineWidth(1)
    c.line(x + 12, y + 55, x + w - 12, y + 55)
    c.line(x + w * 0.42, y + 16, x + w * 0.42, y + h - 16)

    c.setStrokeColor(RED)
    c.setLineWidth(7)
    c.line(x + 12, y + 55, x + w - 12, y + 55)
    crash_bubble(c, x + w * 0.42, y + 55, 22, "61")
    pill(c, x + 16, y + h - 28, 58, 18, "Shaker", stroke=RED, text_color=RED)
    pill(c, x + w * 0.52, y + 22, 38, 18, "MID", stroke=BLUE, text_color=BLUE)
    pill(c, x + w * 0.52, y + 46, 34, 18, "LIB", stroke=ORANGE, text_color=ORANGE)
    pill(c, x + w * 0.75, y + 22, 28, 18, "US", stroke=TEAL, text_color=TEAL)


def panel(c, x, y, w, h, title, subtitle, stats, draw_map, note):
    c.setFillColor(colors.white)
    c.setStrokeColor(LINE)
    c.roundRect(x, y, w, h, 12, stroke=1, fill=1)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 13.5)
    c.drawString(x + 13, y + h - 22, title)
    wrap_text(c, subtitle, x + 13, y + h - 37, w - 26, font="Helvetica", size=8.5, leading=10, color=MUTED)

    map_h = 96
    map_w = w * 0.47
    draw_map(c, x + 13, y + h - 158, map_w, map_h)

    stat_x = x + 28 + map_w
    stat_y = y + h - 112
    gap = 7
    box_w = (w - map_w - 45 - gap * (len(stats) - 1)) / len(stats)
    for i, (value, label) in enumerate(stats):
        stat_box(c, stat_x + i * (box_w + gap), stat_y, box_w, 50, value, label)

    wrap_text(c, note, x + 13, y + 17, w - 26, font="Helvetica", size=8.5, leading=10, color=INK)


def build():
    c = canvas.Canvas(str(PDF_PATH), pagesize=letter)
    c.setTitle("Shelburne Street Safety - Three Priority Areas")

    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, stroke=0, fill=1)

    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(M, H - 42, "Three Priority Safety Areas")
    c.setFont("Helvetica", 10)
    c.setFillColor(MUTED)
    c.drawString(M, H - 58, "Shelburne Street Safety Map summary for quick review")

    c.setFillColor(RED_LIGHT)
    c.setStrokeColor(RED)
    c.roundRect(W - M - 176, H - 66, 176, 32, 8, stroke=1, fill=1)
    c.setFillColor(RED)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(W - M - 88, H - 48, "2021-2025 crash records")

    panel_w = W - 2 * M
    panel_h = 186
    y1 = H - 82 - panel_h
    y2 = y1 - panel_h - 12
    y3 = y2 - panel_h - 12

    panel(
        c,
        M,
        y1,
        panel_w,
        panel_h,
        "1. Shelburne cut-through",
        "Crash burden is higher on the residential cut-through section closer to Warrensville, Courtland, and North Park.",
        [("40", "to Warrensville crashes"), ("16", "injured on that section"), ("16 / 8", "crashes / injured after Warrensville")],
        draw_shelburne_map,
        "Use this as the clearest comparison: Shelburne to Warrensville has 40 crashes / 16 injured, while Shelburne after Warrensville to Green has 16 crashes / 8 injured.",
    )

    panel(
        c,
        M,
        y2,
        panel_w,
        panel_h,
        "2. Fairmount Circle / Fairmount Blvd",
        "High-crash everyday destination area near CVS, food, Fairmount Circle, and future Trader Joe's.",
        [("74 / 16", "Circle area crashes / injured"), ("55 / 26", "Fairmount + Warrensville"), ("160 / 53", "Fairmount corridor total")],
        draw_fairmount_map,
        "This is not only a traffic location. It is an errand and family destination area where walking and biking should be practical.",
    )

    panel(
        c,
        M,
        y3,
        panel_w,
        panel_h,
        "3. Shaker / Warrensville by school + library",
        "Major crossing area next to Shaker Middle, Bertram Woods Library, University School, transit, and fields.",
        [("61 / 25", "Warrensville + Shaker"), ("113 / 44", "school/library corridor"), ("0", "Chesterton comparison crashes")],
        draw_shaker_map,
        "This area is a school, library, transit, and field access concern, not just an arterial traffic issue.",
    )

    footer_y = 28
    c.setFillColor(colors.white)
    c.setStrokeColor(LINE)
    c.roundRect(M, footer_y, W - 2 * M, 34, 8, stroke=1, fill=1)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(M + 11, footer_y + 20, "Specific ask:")
    c.setFont("Helvetica", 9)
    c.drawString(M + 75, footer_y + 20, "Who is the right staff person, committee, or process to review these three areas as a corridor safety / traffic-calming issue?")
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 7.5)
    c.drawString(M + 11, footer_y + 8, "Source: Ohio public crash records, 2021-2025. Interactive map: https://madgirl1234.github.io/shelburne-street-safety-map/")

    c.save()
    print(PDF_PATH)


if __name__ == "__main__":
    build()
