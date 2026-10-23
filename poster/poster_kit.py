#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
poster_kit — الأدوات المشتركة لمولّدَي الملصق (العربي والإنجليزي).

يحتوي: الألوان، هندسة القالب الرسمي، الخطوط، وأدوات الرسم العربي/اللاتيني
الدقيقة فوق محرّك MuPDF. لا يحتوي أي محتوى نصي — المحتوى في ملفَي البناء.

ملاحظات مهمّة عن محرّك MuPDF (تحقّقت منها تجريبيًا):
  * insert_htmlbox يفشل بصمت ويعيد -1 إذا كان الإطار أقصر من سطر واحد.
  * text-align تُطبَّق على الجهة المعاكسة (left ⟶ يمين، right ⟶ يسار)،
    لذلك تُعكس القيمة داخل html()، ومعامل align يعني الجهة الفيزيائية.
"""

import os

import pymupdf
import qrcode

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "template", "SAIF-poster-template-2026.pdf")
FONTS = os.path.join(HERE, "fonts", "ibm-plex")
FLAG_SVG = os.path.join(HERE, "assets", "flag-sa.svg")
QR_PNG = os.path.join(HERE, "assets", "qr-site.png")

SITE = "https://meto2004-lang.github.io/saif/"

# --------------------------------------------------------------------- الهوية اللونية
INK = "#0E3F3C"
TEAL = "#0F7C86"
SALMON = "#C85C50"
CREAM = "#F4F4E9"
MINT = "#E7F0EB"
LINE = "#D7E3DD"
MUTED = "#5F716C"
WHITE = "#FFFFFF"

# --------------------------------------------------------------------- هندسة القالب (نقطة)
CARD = (63.5, 268.1, 2528.5, 524.2)
BOX_QR = (2200.4, 300.7, 2273.1, 373.4)
BOX_BOOTH = (2299.8, 300.7, 2372.5, 373.4)
BOX_FLAG = (2399.2, 300.7, 2502.8, 373.4)

PANEL = {
    "intro": ((63.5, 582.2, 1056.0, 1563.0), (96.8, 702.2, 1026.0, 1530.7)),
    "method": ((1116.0, 582.2, 2528.1, 1563.0), (1146.8, 702.2, 2502.8, 1530.7)),
    "results": ((63.5, 1620.9, 1398.0, 2601.7), (96.8, 1743.3, 1359.0, 2571.8)),
    "innovation": ((1461.0, 1620.9, 2528.1, 2601.7), (1497.5, 1740.3, 2490.0, 2568.8)),
    "conclusion": ((63.5, 2659.7, 1398.0, 3327.0), (96.8, 2780.9, 1359.0, 3294.0)),
    "future": ((1461.0, 2659.7, 2528.1, 3327.0), (1497.5, 2779.1, 2490.0, 3292.1)),
}

FONT_FILES = {
    "l": "IBMPlexSansArabic-Light.ttf",
    "r": "IBMPlexSansArabic-Regular.ttf",
    "m": "IBMPlexSansArabic-Medium.ttf",
    "s": "IBMPlexSansArabic-SemiBold.ttf",
    "b": "IBMPlexSansArabic-Bold.ttf",
}

ARCH = pymupdf.Archive(FONTS)
STATE = {"errors": [], "overlaps": [], "fonts": {}, "scratch": None, "boxes": []}

# اتجاه المستند: "rtl" للعربي، "ltr" للإنجليزي
DIR = "rtl"


def set_direction(direction):
    """يضبط اتجاه المستند الافتراضي (rtl / ltr)."""
    global DIR
    DIR = direction


def css_base():
    return """
@font-face {font-family: pl; src: url(IBMPlexSansArabic-Light.ttf);}
@font-face {font-family: pr; src: url(IBMPlexSansArabic-Regular.ttf);}
@font-face {font-family: pm; src: url(IBMPlexSansArabic-Medium.ttf);}
@font-face {font-family: ps; src: url(IBMPlexSansArabic-SemiBold.ttf);}
@font-face {font-family: pb; src: url(IBMPlexSansArabic-Bold.ttf);}
body {font-family: pr; font-size: 34px; line-height: 1.55; color: %s; direction: %s;}
b, strong {font-family: pb;}
.box {background-color: %s; padding: 26px 30px 22px 30px;}
.q {background-color: #FBF0EE; padding: 26px 30px 22px 30px;}
""" % (INK, DIR, MINT)


# --------------------------------------------------------------------- أدوات
def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def cover(page, rect, color=CREAM):
    page.draw_rect(pymupdf.Rect(*rect), color=None, fill=rgb(color), width=0)


def html(page, rect, body, extra_css="", align="right", direction=None, line_height=1.55,
         tag="?", quiet=False):
    """يرسم كتلة نص ويعيد ارتفاعها الفعلي. align = الجهة الفيزيائية المقصودة."""
    direction = direction or DIR
    r = pymupdf.Rect(*rect)
    css = f"{css_base()}\nbody{{line-height:{line_height};}}" + ("\n" + extra_css if extra_css else "")
    # MuPDF يعكس text-align في سياق RTL فقط (تحقّقت تجريبيًا):
    #   rtl + left  ⟶ يمين / rtl + right ⟶ يسار
    #   ltr + left  ⟶ يسار / ltr + right ⟶ يمين (سلوك CSS الطبيعي)
    # التصحيح يعتمد على اتجاه المستند (body) لا على اتجاه الكتلة
    visual = {"right": "left", "left": "right"}.get(align, align) if DIR == "rtl" else align
    spare, scale = page.insert_htmlbox(
        r, f'<div dir="{direction}" style="text-align:{visual};">{body}</div>',
        css=css, archive=ARCH, scale_low=1
    )
    if spare < 0:
        if not quiet:
            STATE["errors"].append(f"[{tag}] فشل الرسم: الإطار {r.height:.0f}pt أقصر من النص")
        return 0
    used = r.height - spare
    if scale < 0.999 and not quiet:
        STATE["errors"].append(f"[{tag}] صُغِّر تلقائيًا ×{scale:.2f}")
    if not quiet:
        STATE["boxes"].append((pymupdf.Rect(r.x0, r.y0, r.x1, r.y0 + used), tag))
    return used


def measure(body, width, extra_css="", align="right", direction=None, line_height=1.55):
    """يقيس ارتفاع الكتلة على صفحة مؤقتة بنفس العرض."""
    if STATE["scratch"] is None:
        doc = pymupdf.open()
        doc.new_page(width=3000, height=4000)
        STATE["scratch"] = (doc, doc[0])
    page = STATE["scratch"][1]
    return html(page, (50, 50, 50 + width, 3950), body, extra_css, align,
                direction or DIR, line_height, quiet=True)


def text(page, x, baseline, s, size=20, weight="r", color=INK, anchor="left"):
    """نص لاتيني/أرقام بدقة (لا يحتاج تشكيلًا)."""
    if weight not in STATE["fonts"]:
        path = os.path.join(FONTS, FONT_FILES[weight])
        name = f"plex-{weight}"
        page.insert_font(fontname=name, fontfile=path)
        STATE["fonts"][weight] = (name, pymupdf.Font(fontfile=path))
    name, fnt = STATE["fonts"][weight]
    w = fnt.text_length(s, size)
    if anchor == "right":
        x -= w
    elif anchor == "center":
        x -= w / 2
    page.insert_text((x, baseline), s, fontsize=size, fontname=name, color=rgb(color))
    return w


class Flow:
    """تكديس عمودي يقيس الكتل أولًا ثم يوزّع الفراغ بينها."""

    def __init__(self, page, rect, gap=24, max_gap=110, vcenter=True):
        self.page = page
        self.rect = rect
        self.gap = gap
        self.max_gap = max_gap
        self.vcenter = vcenter
        self.blocks = []

    def add(self, body, extra_css="", align="right", direction=None, line_height=1.55, tag="block"):
        self.blocks.append((body, extra_css, align, direction, line_height, tag))
        return self

    def render(self):
        x0, y0, x1, y1 = self.rect
        width = x1 - x0
        heights = [measure(b[0], width, b[1], b[2], b[3], b[4]) for b in self.blocks]
        total = sum(heights)
        n = len(self.blocks)
        avail = y1 - y0
        gap = self.gap
        if n > 1 and avail > total:
            gap = min(self.max_gap, self.gap + (avail - total - self.gap * (n - 1)) / (n - 1))
            gap = max(self.gap, gap)
        stack = total + gap * (n - 1)
        y = y0 + (avail - stack) / 2 if (self.vcenter and avail > stack) else y0
        for (body, css, align, direction, lh, tag), h in zip(self.blocks, heights):
            html(self.page, (x0, y, x1, y + h + 2), body, css, align, direction, lh, tag)
            y += h + gap
        if stack > avail + 1:
            STATE["errors"].append(f"[{self.blocks[0][5]}] المحتوى أطول من اللوحة: {stack:.0f} > {avail:.0f}")
        return stack


def make_qr(path=QR_PNG, data=SITE, size=1000):
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=1)
    qr.add_data(data)
    qr.make(fit=True)
    qr.make_image(fill_color=INK, back_color="white").convert("RGB").resize(
        (size, size), resample=0).save(path)


_FLAG = None


def place_flag(page, rect):
    """العلم السعودي متجهيًا: SVG ← PDF بمحرّك MuPDF."""
    global _FLAG
    if _FLAG is None:
        svg = pymupdf.open(FLAG_SVG)
        _FLAG = pymupdf.open("pdf", svg.convert_to_pdf())
    page.show_pdf_page(pymupdf.Rect(*rect), _FLAG, 0)


def col_x(x0, x1, i, w, gap):
    """موضع العمود رقم i من الجهة البادئة: اليمين في RTL واليسار في LTR."""
    if DIR == "rtl":
        return x1 - (i + 1) * w - i * gap
    return x0 + i * (w + gap)


# --------------------------------------------------------------------- الفحص والبناء
def check_overlaps():
    ov = []
    boxes = STATE["boxes"]
    for i, (r1, t1) in enumerate(boxes):
        for r2, t2 in boxes[i + 1:]:
            inter = pymupdf.Rect(r1) & pymupdf.Rect(r2)
            if inter.is_empty:
                continue
            a = inter.width * inter.height
            smallest = min(r1.width * r1.height, r2.width * r2.height)
            if smallest > 0 and a / smallest > 0.25:
                ov.append(f"[{t1}] ↔ [{t2}] تراكب {a / smallest:.0%}")
    return ov


def prepare_page(doc):
    """يحذف مؤشر الفأرة ونصوص القالب المؤقتة ويضيف رابط التحميل."""
    page = doc[0]
    for im in page.get_images(full=True):
        if im[0] == 95:                      # مؤشر الفأرة الملتقط سهوًا في القالب
            page.delete_image(im[0])

    zones = [CARD] + [(c[0], c[1], c[2], ct[3]) for c, ct in PANEL.values()]
    for z in zones:
        page.add_redact_annot(pymupdf.Rect(*z), fill=None)
    page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,
                          graphics=pymupdf.PDF_REDACT_LINE_ART_NONE,
                          text=pymupdf.PDF_REDACT_TEXT_REMOVE)

    page.insert_link({"kind": pymupdf.LINK_URI, "from": pymupdf.Rect(375, 108, 1026, 180), "uri": SITE})
    return page


def save(doc, page, out_pdf, out_png=None, out_jpg=None, preview=False, lang="ar"):
    try:
        doc.subset_fonts(verbose=False)
    except Exception:
        pass
    doc.save(out_pdf, garbage=4, deflate=True, deflate_images=True, clean=True)
    print(f"✓ {out_pdf}  ({os.path.getsize(out_pdf) / 1024:.0f} KB، "
          f"{page.rect.width / 72:.0f}×{page.rect.height / 72:.0f} بوصة)")

    if STATE["errors"]:
        print("\n⚠ ملاحظات:")
        for e in STATE["errors"]:
            print("   ", e)
    else:
        print("✓ كل الكتل داخل أطرها بلا تصغير تلقائي")

    ov = check_overlaps()
    if ov:
        print(f"\n⚠ تراكب نصوص: {len(ov)}")
        for o in ov:
            print("   ", o)
    else:
        print("✓ لا تراكب بين كتل النص")

    if preview and out_png:
        d2 = pymupdf.open(out_pdf)
        d2[0].get_pixmap(dpi=40).save(out_png)
        print(f"✓ {out_png}")
        if out_jpg:
            d2[0].get_pixmap(dpi=150).save(out_jpg, jpg_quality=88)
            print(f"✓ {out_jpg}  ({os.path.getsize(out_jpg) / 1024 / 1024:.1f} MB)")
    return ov
