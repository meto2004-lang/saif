#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مولّد الملصق العلمي على قالب سيف الرسمي 2026.

المقاس: 36 × 48 بوصة طوليًا (914 × 1219 مم) — مطابق لأبعاد القالب حرفيًا.
الخط المعتمد: IBM Plex Sans Arabic (Light / Regular / Medium / SemiBold / Bold).

الاستخدام:
    python3 build_template_poster.py            # PDF فقط
    python3 build_template_poster.py --preview  # PDF + معاينات PNG/JPG

المتطلبات: pymupdf, qrcode, pillow
"""

import os
import sys

import pymupdf
import qrcode

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "template", "SAIF-poster-template-2026.pdf")
FONTS = os.path.join(HERE, "fonts", "ibm-plex")
FLAG_SVG = os.path.join(HERE, "assets", "flag-sa.svg")
OUT_PDF = os.path.join(HERE, "saif-poster-36x48.pdf")
OUT_PNG = os.path.join(HERE, "preview-36x48.png")
OUT_JPG = os.path.join(HERE, "saif-poster-36x48.jpg")
QR_PNG = os.path.join(HERE, "assets", "qr-site.png")

SITE = "https://meto2004-lang.github.io/saif/"

INK = "#0E3F3C"
TEAL = "#0F7C86"
SALMON = "#C85C50"
CREAM = "#F4F4E9"
MINT = "#E7F0EB"
LINE = "#D7E3DD"
MUTED = "#5F716C"

# --------------------------------------------------------------------- هندسة القالب
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

HEADINGS = {
    "intro": ("المقدمة", "INTRODUCTION"),
    "method": ("المنهجية", "METHODOLOGY"),
    "results": ("النتائج", "RESULTS"),
    "innovation": ("الابتكار", "INNOVATION"),
    "conclusion": ("الخاتمة", "CONCLUSION"),
    "future": ("العمل المستقبلي والمراجع", "FUTURE WORK & REFERENCES"),
}

FONT_FILES = {
    "l": "IBMPlexSansArabic-Light.ttf",
    "r": "IBMPlexSansArabic-Regular.ttf",
    "m": "IBMPlexSansArabic-Medium.ttf",
    "s": "IBMPlexSansArabic-SemiBold.ttf",
    "b": "IBMPlexSansArabic-Bold.ttf",
}

CSS_BASE = """
@font-face {font-family: pl; src: url(IBMPlexSansArabic-Light.ttf);}
@font-face {font-family: pr; src: url(IBMPlexSansArabic-Regular.ttf);}
@font-face {font-family: pm; src: url(IBMPlexSansArabic-Medium.ttf);}
@font-face {font-family: ps; src: url(IBMPlexSansArabic-SemiBold.ttf);}
@font-face {font-family: pb; src: url(IBMPlexSansArabic-Bold.ttf);}
body {font-family: pr; font-size: 34px; line-height: 1.55; color: %s; direction: rtl;}
b, strong {font-family: pb;}
.box {background-color: %s; padding: 26px 30px 22px 30px;}
.q {background-color: #FBF0EE; padding: 26px 30px 22px 30px;}
""" % (INK, MINT)

ARCH = pymupdf.Archive(FONTS)
STATE = {"errors": [], "fonts": {}, "scratch": None}


# --------------------------------------------------------------------- أدوات
def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def cover(page, rect, color=CREAM):
    page.draw_rect(pymupdf.Rect(*rect), color=None, fill=rgb(color), width=0)


def html(page, rect, body, extra_css="", align="right", direction="rtl", line_height=1.55,
         tag="?", quiet=False):
    r = pymupdf.Rect(*rect)
    css = f"{CSS_BASE}\nbody{{line-height:{line_height};}}" + ("\n" + extra_css if extra_css else "")
    # محرّك MuPDF يعامل text-align منطقيًا مع اتجاه الفقرة (RTL): نعكس القيمة لتطابق المقصود
    visual = {"right": "left", "left": "right"}.get(align, align)
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
        # نسجّل المساحة المرسومة فعليًا لاكتشاف تراكب الكتل لاحقًا
        STATE.setdefault("boxes", []).append(
            (pymupdf.Rect(r.x0, r.y0, r.x1, r.y0 + used), tag,
             "".join(ch for ch in body if ch.isalnum() or ch in " ")[:28])
        )
    return used


def measure(body, width, extra_css="", align="right", direction="rtl", line_height=1.55):
    """يقيس ارتفاع الكتلة على صفحة مؤقتة بنفس عرض العمود."""
    if STATE["scratch"] is None:
        doc = pymupdf.open()
        doc.new_page(width=3000, height=4000)
        STATE["scratch"] = (doc, doc[0])
    page = STATE["scratch"][1]
    return html(page, (50, 50, 50 + width, 3950), body, extra_css, align, direction,
                line_height, quiet=True)


def text(page, x, baseline, s, size=20, weight="r", color=INK, anchor="left"):
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
    """تكديس عمودي: يقيس الكتل أولًا ثم يوزّع الفراغ بينها بالتساوي."""

    def __init__(self, page, rect, gap=24, max_gap=110, vcenter=True):
        self.page = page
        self.rect = rect
        self.gap = gap
        self.max_gap = max_gap
        self.vcenter = vcenter
        self.blocks = []

    def add(self, body, extra_css="", align="right", direction="rtl", line_height=1.55, tag="block"):
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
        if avail < stack and not self.vcenter:
            y = y0
        for (body, css, align, direction, lh, tag), h in zip(self.blocks, heights):
            html(self.page, (x0, y, x1, y + h + 2), body, css, align, direction, lh, tag)
            y += h + gap
        if stack > avail + 1:
            STATE["errors"].append(f"[{self.blocks[0][5]}] المحتوى أطول من اللوحة: {stack:.0f} > {avail:.0f}")
        return stack


def make_qr(path, data=SITE, size=1000):
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=1)
    qr.add_data(data)
    qr.make(fit=True)
    qr.make_image(fill_color=INK, back_color="white").convert("RGB").resize(
        (size, size), resample=0).save(path)


_FLAG = None


def place_flag(page, rect):
    global _FLAG
    if _FLAG is None:
        svg = pymupdf.open(FLAG_SVG)
        _FLAG = pymupdf.open("pdf", svg.convert_to_pdf())
    page.show_pdf_page(pymupdf.Rect(*rect), _FLAG, 0)


# --------------------------------------------------------------------- بطاقة العنوان
def build_header(page):
    cover(page, (CARD[0] + 0.6, CARD[1] + 0.6, CARD[2] - 0.6, CARD[3] - 0.6))

    # ---------- اليسار: الهوية
    text(page, 96, 300, "QUANTUM LEARNING LAB", 22, "m", TEAL)

    html(page, (96, 300, 470, 408),
         '<span style="font-family:pb;font-size:76px;color:%s;">كم</span>' % INK,
         align="left", direction="rtl", line_height=1.25, tag="wordmark")

    html(page, (96, 402, 1010, 440),
         "مدرسة الرواد الثانوية الأهلية — حي الازدهار — مدينة الرياض",
         extra_css="body{font-size:26px;font-family:pm;}", align="left", line_height=1.2,
         tag="school")

    html(page, (96, 440, 1010, 472),
         "المسار 13 — التقنيات الكمية والحوسبة المتقدمة · الفئة العمرية 12–17 سنة",
         extra_css=f"body{{font-size:23px;color:{MUTED};}}", align="left", line_height=1.2,
         tag="track")

    # ---------- الشارة: العلم + المدينة
    bw = 44
    place_flag(page, (96, 486, 96 + bw * 1.5, 486 + bw))
    html(page, (96 + bw * 1.5 + 14, 484, 1010, 522),
         "الرياض — المملكة العربية السعودية",
         extra_css=f"body{{font-size:22px;font-family:pl;color:{MUTED};}}", align="left",
         line_height=1.2, tag="country")

    # ---------- العلم في خانته من القالب
    fw = BOX_FLAG[2] - BOX_FLAG[0] - 4
    fh = fw * 2 / 3
    place_flag(page, (BOX_FLAG[0] + 2, BOX_FLAG[1] + 12, BOX_FLAG[0] + 2 + fw, BOX_FLAG[1] + 12 + fh))

    # ---------- رمز QR
    make_qr(QR_PNG)
    page.insert_image(pymupdf.Rect(BOX_QR[0] + 8, BOX_QR[1] + 8, BOX_QR[2] - 8, BOX_QR[3] - 8),
                      filename=QR_PNG)

    text(page, (BOX_BOOTH[0] + BOX_BOOTH[2]) / 2, BOX_BOOTH[3] - 14, "—", 30, "l", MUTED, "center")

    # ---------- العنوان
    html(page, (1040, 278, 2150, 424),
         '<span style="font-family:pb;font-size:54px;color:%s;">«كم» منصة عربية تجعل الحوسبة الكمية '
         'تجربة يراها الطالب ويصنعها بنفسه</span>' % INK,
         line_height=1.22, tag="title")

    html(page, (1040, 420, 2150, 458),
         "من المفهوم إلى الدائرة في ثلاث خطوات — دون رياضيات متقدمة",
         extra_css=f"body{{font-size:25px;color:{TEAL};font-family:pm;}}", line_height=1.25,
         tag="subtitle")

    html(page, (1040, 456, 2150, 488),
         '<span style="font-family:pl;font-size:20px;color:%s;">الطلاب: </span>'
         '<span style="font-family:pm;font-size:21px;">أسامة حمد عبدالرحمن الدايل · '
         'عبدالله عمر محمد المسند · فارس داوود عبدالله الراجحي</span>' % MUTED,
         line_height=1.25, tag="students")

    html(page, (1040, 486, 2150, 516),
         '<span style="font-family:pl;font-size:20px;color:%s;">المشرف: </span>'
         '<span style="font-family:pm;font-size:21px;">الأستاذ محمد السيد متولى — معلم الحاسب الآلي</span>'
         % MUTED, line_height=1.25, tag="supervisor")

    text(page, 2149, 516, "ID: ______________", 19, "l", MUTED, "right")


# --------------------------------------------------------------------- عناوين اللوحات
def build_headings(page):
    for key, (card, content) in PANEL.items():
        ar, en = HEADINGS[key]
        cover(page, (card[0] + 0.6, card[1] + 0.6, card[2] - 0.6, content[3] + 1))
        html(page, (card[0] + 32, card[1] + 18, card[2] - 32, card[1] + 92),
             f'<span style="font-family:ps;font-size:48px;color:{INK};">{ar}</span>',
             line_height=1.1, tag=f"head-{key}")
        text(page, card[0] + 32, card[1] + 68, en, 21, "l", MUTED)


# --------------------------------------------------------------------- 1 المقدمة
def panel_intro(page):
    Flow(page, PANEL["intro"][1], gap=26, max_gap=90).add(
        '<span style="font-size:33px;line-height:1.5;">الحوسبة الكمية تعرض مفاهيم لا تشبه ما نعرفه: '
        'الكيوبت يكون 0 و1 في الوقت نفسه، والتشابك يربط كيوبتين حتى لو ابتعدا.</span>', tag="lead"
    ).add(
        '<div class="box"><b style="font-size:33px;">المشكلة</b>'
        '<div style="margin-top:12px;font-size:32px;line-height:1.5;">'
        '•&nbsp; المحاكيات العالمية بالإنجليزية، فيتوقف الطالب عند المصطلح قبل أن يفهمه.<br/>'
        '•&nbsp; المفاهيم تُقدَّم كمعادلات مجردة، فيحفظ القانون دون أن يرى أثره.<br/>'
        '•&nbsp; لا تجربة عربية واحدة تجمع الشرح والتجربة والتحقق معًا.'
        '</div></div>', tag="problem"
    ).add(
        '<div class="q"><b style="font-size:32px;color:%s;">سؤالنا</b>'
        '<div style="margin-top:12px;font-size:33px;line-height:1.45;">كيف نحوّل المفهوم إلى تجربة '
        'قصيرة يفهمها طالب في الثانية عشرة، دون رياضيات متقدمة؟</div></div>' % SALMON,
        tag="question"
    ).add(
        '<div style="font-size:31px;line-height:1.5;"><b>لمن هذا العمل؟</b> لطلاب الصفوف من '
        'السابع إلى الحادي عشر (12–17 سنة)، ولمعلم يريد أول درس كمّي جاهز دون تحضير معقّد.</div>',
        tag="audience"
    ).render()


# --------------------------------------------------------------------- 2 المنهجية
def panel_method(page):
    x0, y0, x1, y1 = PANEL["method"][1]
    html(page, (x0, y0, x1, y0 + 56),
         "بنينا «كم» في ثلاث مراحل، وكل مرحلة تُدقَّق قبل الانتقال للتي تليها.",
         extra_css="body{font-size:32px;}", line_height=1.3, tag="method-lead")

    steps = [
        ("1", "تحليل", "راجعنا عدة محاكيات عالمية، وقارنّا المحتوى واللغة وطريقة عرض المفهوم."),
        ("2", "بناء", "أضفنا محاكيًا كميًا من الصفر داخل المتصفح، بواجهة عربية كاملة، بلا مكتبات خارجية."),
        ("3", "تحقّق", "20 اختبارًا آليًا، ومقارنة نتائج 23 دائرة بمحاكي Quirk العالمي."),
    ]
    top = y0 + 92
    gap = 26
    w = (x1 - x0 - 2 * gap) / 3
    bar_h = 132
    h = (y1 - bar_h - 52) - top
    for i, (num, title, txt) in enumerate(steps):
        cx = x1 - (i + 1) * w - i * gap
        page.draw_rect(pymupdf.Rect(cx, top, cx + w, top + h), color=rgb(LINE),
                       fill=rgb("#FFFFFF"), width=1.4, radius=0.03)
        html(page, (cx + 26, top + 26, cx + w - 26, top + 104),
             f'<span style="font-family:pb;font-size:54px;color:{TEAL};">{num}</span>'
             f'<span style="font-family:ps;font-size:34px;color:{INK};">&nbsp;&nbsp;{title}</span>',
             line_height=1.2, tag=f"step-{i}")
        html(page, (cx + 24, top + 124, cx + w - 24, top + 124 + 190),
             f'<span style="font-size:30px;line-height:1.55;">{txt}</span>',
             line_height=1.55, tag=f"step-body-{i}")

        # ---------- رسم توضيحي صغير أسفل كل بطاقة
        iy = top + h - 190
        icon_cx = cx + w / 2
        if i == 0:      # تحليل: ثلاثة أعمدة مقارنة
            for k, hh in enumerate((60, 96, 44)):
                x = icon_cx - 90 + k * 66
                page.draw_rect(pymupdf.Rect(x, iy + 100 - hh, x + 44, iy + 100),
                               color=None, fill=rgb(TEAL), width=0)
        elif i == 1:    # بناء: دائرة صغيرة بسلكين وبوابة
            page.draw_line((icon_cx - 100, iy + 44), (icon_cx + 100, iy + 44), color=rgb(INK), width=3)
            page.draw_line((icon_cx - 100, iy + 86), (icon_cx + 100, iy + 86), color=rgb(INK), width=3)
            page.draw_rect(pymupdf.Rect(icon_cx - 60, iy + 24, icon_cx - 4, iy + 64),
                           color=rgb(INK), fill=rgb(MINT), width=3, radius=0.1)
            text(page, icon_cx - 32, iy + 56, "H", 22, "b", INK, "center")
            page.draw_circle((icon_cx + 42, iy + 44), 7, color=rgb(INK), fill=rgb(INK), width=0)
            page.draw_line((icon_cx + 42, iy + 44), (icon_cx + 42, iy + 86), color=rgb(INK), width=3)
            page.draw_circle((icon_cx + 42, iy + 86), 16, color=rgb(INK), fill=rgb("#FFFFFF"), width=3)
            page.draw_line((icon_cx + 26, iy + 86), (icon_cx + 58, iy + 86), color=rgb(INK), width=3)
            page.draw_line((icon_cx + 42, iy + 70), (icon_cx + 42, iy + 102), color=rgb(INK), width=3)
        else:           # تحقّق: علامة صح في دائرة
            page.draw_circle((icon_cx, iy + 66), 46, color=rgb(TEAL), fill=rgb(MINT), width=3)
            page.draw_line((icon_cx - 22, iy + 66), (icon_cx - 5, iy + 84), color=rgb(TEAL), width=7)
            page.draw_line((icon_cx - 5, iy + 84), (icon_cx + 24, iy + 44), color=rgb(TEAL), width=7)

    by = y1 - bar_h
    page.draw_rect(pymupdf.Rect(x0, by, x1, by + 132), color=None, fill=rgb(MINT), width=0)
    html(page, (x0 + 30, by + 14, x1 - 30, by + 60),
         '<span style="font-family:pl;font-size:26px;color:%s;">وفي كل صفحة من المنصة يتكرر المسار نفسه</span>'
         % MUTED, line_height=1.2, tag="path-label")
    html(page, (x0 + 30, by + 58, x1 - 30, by + 122),
         '<span style="font-family:ps;font-size:34px;color:%s;">افهم ← جرّب ← تحقّق</span>' % INK,
         line_height=1.2, tag="path-steps")


# --------------------------------------------------------------------- 3 النتائج
def panel_results(page):
    x0, y0, x1, y1 = PANEL["results"][1]
    stats = [("6", "مفاهيم أساسية"), ("8", "بوابات كمّية"), ("6", "تجارب جاهزة"),
             ("20", "سؤالًا تفاعليًا"), ("3", "أوراق عمل"), ("20/20", "اختبارًا ناجحًا")]
    gap = 20
    w = (x1 - x0 - 2 * gap) / 3
    h = 178
    for i, (num, label) in enumerate(stats):
        col, row = i % 3, i // 3
        cx = x1 - (col + 1) * w - col * gap
        cy = y0 + row * (h + gap)
        page.draw_rect(pymupdf.Rect(cx, cy, cx + w, cy + h), color=rgb(LINE), fill=rgb("#FFFFFF"),
                       width=1.4, radius=0.04)
        text(page, cx + w / 2, cy + 84, num, 56, "b", TEAL, "center")
        html(page, (cx + 8, cy + 100, cx + w - 8, cy + h - 8),
             f'<span style="font-family:pm;font-size:26px;">{label}</span>',
             align="center", line_height=1.2, tag=f"stat-{i}")

    cy = y0 + 2 * h + gap + 52
    page.draw_rect(pymupdf.Rect(x0, cy, x1, cy + 2), color=None, fill=rgb(LINE), width=0)
    cy += 26
    html(page, (x0, cy, x1, cy + 52),
         '<span style="font-family:ps;font-size:30px;">دائرة بيل: البوابة H ثم CNOT</span>'
         f'<span style="font-family:pl;font-size:22px;color:{MUTED};">&nbsp;&nbsp;— توزيع متساوٍ بين 00 و11 فقط</span>',
         line_height=1.25, tag="circuit-title")

    cy += 66
    wx0, wx1 = x0 + 56, x1 - 300
    y_a, y_b = cy + 46, cy + 128
    for yy in (y_a, y_b):
        page.draw_line((wx0, yy), (wx1, yy), color=rgb(INK), width=2.4)

    gh = 62
    page.draw_rect(pymupdf.Rect(wx0 + 140, y_a - gh / 2, wx0 + 248, y_a + gh / 2),
                   color=rgb(INK), fill=rgb(MINT), width=2.4, radius=0.1)
    text(page, wx0 + 194, y_a + 12, "H", 34, "b", INK, "center")

    cxg = wx0 + 400
    page.draw_circle((cxg, y_a), 10, color=rgb(INK), fill=rgb(INK), width=0)
    page.draw_line((cxg, y_a), (cxg, y_b), color=rgb(INK), width=2.4)
    page.draw_circle((cxg, y_b), 28, color=rgb(INK), fill=rgb("#FFFFFF"), width=2.4)
    page.draw_line((cxg - 28, y_b), (cxg + 28, y_b), color=rgb(INK), width=2.4)
    page.draw_line((cxg, y_b - 28), (cxg, y_b + 28), color=rgb(INK), width=2.4)

    mx = wx0 + 640
    for yy in (y_a, y_b):
        page.draw_rect(pymupdf.Rect(mx - 36, yy - 31, mx + 36, yy + 31),
                       color=rgb(INK), fill=rgb("#FFFFFF"), width=2.4, radius=0.1)
        page.draw_circle((mx, yy + 2), 16, color=rgb(INK), width=2.4)
        page.draw_line((mx - 9, yy + 11), (mx + 8, yy - 8), color=rgb(INK), width=2.4)

    text(page, x0, y_a + 11, "q0", 26, "m", MUTED)
    text(page, x0, y_b + 11, "q1", 26, "m", MUTED)

    bx0, bx1 = x1 - 266, x1
    rows = [("00", 50), ("11", 50), ("01", 0), ("10", 0)]
    ry = cy + 10
    for label, pct in rows:
        page.draw_rect(pymupdf.Rect(bx0, ry, bx1 - 88, ry + 30), color=None, fill=rgb("#E9EFEA"), width=0)
        wid = (bx1 - 88 - bx0) * pct / 100.0
        if wid > 0:
            page.draw_rect(pymupdf.Rect(bx1 - 88 - wid, ry, bx1 - 88, ry + 30),
                           color=None, fill=rgb(TEAL), width=0)
        text(page, bx0 - 10, ry + 23, f"{pct}%", 24, "m", INK, "right")
        text(page, bx1, ry + 23, label, 24, "m", MUTED, "right")
        ry += 42

    # تفسير واحد فقط أسفل الأشرطة (كان هنا سطران متراكبان بنفس المعنى)
    html(page, (x0, ry + 26, x1, y1),
         '<div style="font-size:26px;line-height:1.45;"><b>ماذا تعني النتيجة؟</b> لو أعدنا التجربة '
         'مئة مرة، ستأتي «00» نحو خمسين مرة و«11» نحو خمسين مرة، ولا تظهر «01» أو «10» أبدًا '
         '— وهذا هو التشابك بعينه.</div>', line_height=1.45, tag="circuit-explain")


# --------------------------------------------------------------------- 4 الابتكار
def panel_innovation(page):
    x0, y0, x1, y1 = PANEL["innovation"][1]
    W = x1 - x0

    bullets = [
        "<b>تجربة عربية كاملة:</b> الشرح والمحاكاة والتحقق في صفحة واحدة.",
        "<b>يعمل فورًا:</b> على الحاسوب والجوال، دون تثبيت أو حساب.",
        "<b>تحقّق خارجي:</b> كل دائرة تُقارَن بمحاكي Quirk العالمي، فلا نطلب أن يُثق بنا بلا دليل.",
        "<b>شفافية:</b> صفر مكتبات خارجية، والكود متاح للمراجعة.",
    ]
    gap = 18
    body_css = "body{font-size:31px;}"
    heights = [measure(f'<div style="font-size:31px;line-height:1.45;">{b}</div>', W, body_css,
                       line_height=1.45) for b in bullets]
    y = y0
    for b, h in zip(bullets, heights):
        html(page, (x0, y, x1, y + h + 2), f'<div style="font-size:31px;line-height:1.45;">{b}</div>',
             body_css, line_height=1.45, tag="inn-bullet")
        y += h + gap

    # ---------- صندوق "الفرق في البناء" في الفراغ بين النقاط والجدول
    table_top = y1 - 5 * 74
    box_top = y + 6
    box_bottom = table_top - 26
    if box_bottom - box_top > 90:
        page.draw_rect(pymupdf.Rect(x0, box_top, x1, box_bottom), color=None, fill=rgb(MINT), width=0)
        page.draw_rect(pymupdf.Rect(x0, box_top, x0 + 7, box_bottom), color=None, fill=rgb(TEAL), width=0)
        inner = (x0 + 34, box_top + 22, x1 - 30, box_bottom - 22)
        hh = measure('<div style="font-size:30px;line-height:1.45;"><b>الفرق في البناء</b>'
                     '<div style="margin-top:10px;font-size:29px;">الطالب لا يقرأ عن التراكب ولا يحفظ '
                     'صيغته… بل يرى الاحتمالات تتحرك على الشاشة كلما غيّر البوابة.</div></div>',
                     inner[2] - inner[0], line_height=1.45)
        yy = inner[1] + max(0, (inner[3] - inner[1] - hh) / 2)
        html(page, (inner[0], yy, inner[2], yy + hh + 4),
             '<div style="font-size:30px;line-height:1.45;"><b>الفرق في البناء</b>'
             '<div style="margin-top:10px;font-size:29px;">الطالب لا يقرأ عن التراكب ولا يحفظ '
             'صيغته… بل يرى الاحتمالات تتحرك على الشاشة كلما غيّر البوابة.</div></div>',
             line_height=1.45, tag="inn-box")

    # ---------- جدول مقارنة مع المحاكيات المتاحة
    c_key = W * 0.19
    c_them = W * 0.27
    c_ours = W - c_key - c_them
    rh = 74
    table_h = rh * 5
    ty = y1 - table_h - (y1 - y - 10) * 0.0   # الجدول يلتصق بأسفل اللوحة

    page.draw_rect(pymupdf.Rect(x0, ty, x1, ty + rh), color=None, fill=rgb(INK), width=0)
    html(page, (x1 - c_ours - 16, ty + 12, x1 - 16, ty + rh - 10),
         '<span style="font-family:pb;font-size:24px;color:#FFFFFF;">«كم»</span>',
         align="right", line_height=1.2, tag="cmp-h1")
    html(page, (x0 + c_key + 12, ty + 12, x0 + c_key + c_them - 12, ty + rh - 10),
         '<span style="font-family:pl;font-size:22px;color:#FFFFFF;">المحاكيات العالمية</span>',
         align="left", line_height=1.2, tag="cmp-h2")
    html(page, (x0 + 14, ty + 12, x0 + c_key - 12, ty + rh - 10),
         '<span style="font-family:ps;font-size:22px;color:#FFFFFF;">المعيار</span>',
         align="left", line_height=1.2, tag="cmp-h3")

    rows = [("اللغة", "عربية كاملة من اليمين لليسار", "إنجليزية أو ترجمة آلية"),
            ("الطريق إلى الفهم", "تجربة مرئية أولًا ثم الرمز", "معادلات ومصفوفات"),
            ("التحقق", "مقارنة معلنة مع Quirk", "داخلي غير معلن"),
            ("التشغيل", "المتصفح مباشرة بلا حساب", "برنامج يحتاج تثبيتًا")]
    ry = ty + rh
    for i, (key, ours, them) in enumerate(rows):
        bg = rgb("#FFFFFF") if i % 2 == 0 else rgb(MINT)
        page.draw_rect(pymupdf.Rect(x0, ry, x1, ry + rh), color=rgb(LINE), fill=bg, width=1)
        html(page, (x0 + 14, ry + 10, x0 + c_key - 12, ry + rh - 8),
             f'<span style="font-family:ps;font-size:22px;">{key}</span>', align="left",
             line_height=1.25, tag=f"cmp-k-{i}")
        html(page, (x1 - c_ours - 16, ry + 10, x1 - 16, ry + rh - 8),
             f'<span style="font-family:pm;font-size:23px;">{ours}</span>', align="right",
             line_height=1.25, tag=f"cmp-ours-{i}")
        html(page, (x0 + c_key + 12, ry + 10, x0 + c_key + c_them - 12, ry + rh - 8),
             f'<span style="font-family:pl;font-size:21px;color:{MUTED};">{them}</span>', align="left",
             line_height=1.25, tag=f"cmp-them-{i}")
        ry += rh

    # إبراز عمودنا
    page.draw_rect(pymupdf.Rect(x1 - c_ours, ty, x1 - c_ours, ry), color=rgb(TEAL), fill=None, width=3)


# --------------------------------------------------------------------- 5 الخاتمة
def panel_conclusion(page):
    Flow(page, PANEL["conclusion"][1], gap=30, max_gap=90).add(
        '<div style="font-size:33px;line-height:1.55;">بعد التجربة صار الطالب يشرح التراكب بلغته، '
        'ويربط كل رمز في الدائرة بنتيجة يرسمها بنفسه.</div>', tag="con-1"
    ).add(
        '<div style="font-size:33px;line-height:1.55;">وقصّرنا المسافة بين الملاحظة والاستنتاج '
        'إلى ثلاث خطوات: افهم، جرّب، تحقّق.</div>', tag="con-2"
    ).add(
        '<div class="box"><span style="font-family:ps;font-size:34px;line-height:1.45;color:%s;">'
        'تبسيط العلم لا يعني حذف دقته، بل ترتيب طريقه.</span></div>' % INK, tag="con-box"
    ).add(
        '<div style="font-size:30px;line-height:1.5;"><b>الخلاصة في سطر:</b> منصة واحدة، عربية بالكامل، '
        'تفتح باب الحوسبة الكمية لطالب في الثانية عشرة، وتُقاس نتائجها بأرقام لا بآراء.</div>',
        tag="con-3"
    ).render()


# --------------------------------------------------------------------- 6 العمل المستقبلي
def panel_future(page):
    x0, y0, x1, y1 = PANEL["future"][1]
    qr_w = 180
    fx1 = x1 - qr_w - 52
    Flow(page, (x0, y0, fx1, y0 + 250), gap=24, max_gap=40).add(
        '<div style="font-size:29px;line-height:1.45;"><b>قياس الأثر:</b> 30 طالبًا، اختبار قبلي '
        'وبعدي، 20 سؤالًا.</div>', tag="fut-1"
    ).add(
        '<div style="font-size:29px;line-height:1.45;"><b>التوسّع:</b> نسخة إنجليزية، مسارات '
        'للمعلمين، دوائر 3 كيوبتات.</div>', tag="fut-2"
    ).render()

    refs = ["Nielsen & Chuang, Quantum Computation and",
            "Quantum Information, Cambridge Univ. Press, 2010.",
            "Gidney, C., Quirk: Quantum Circuit Simulator, 2016.",
            "Feynman, R., Simulating Physics with Computers, 1982."]
    ry = y0 + 290
    html(page, (x0, ry, fx1, ry + 46),
         '<span style="font-family:pb;font-size:26px;">المراجع</span>', line_height=1.2, tag="refs-title")
    for i, line in enumerate(refs):
        text(page, x0, ry + 76 + i * 34, line, 22, "l", MUTED)

    qx0 = x1 - qr_w
    qy0 = y0 + 40
    page.draw_rect(pymupdf.Rect(qx0 - 12, qy0 - 10, x1 + 12, qy0 + qr_w + 12),
                   color=rgb(LINE), fill=rgb("#FFFFFF"), width=1.4, radius=0.03)
    page.insert_image(pymupdf.Rect(qx0, qy0, x1, qy0 + qr_w), filename=QR_PNG)
    html(page, (qx0 - 40, qy0 + qr_w + 14, x1 + 10, qy0 + qr_w + 92),
         '<span style="font-family:pm;font-size:21px;">امسح الرمز لزيارة المنصة</span>',
         align="center", line_height=1.25, tag="qr-label")
    text(page, x1 - qr_w / 2, qy0 + qr_w + 116, "meto2004-lang.github.io/saif", 13, "l", MUTED, "center")


# --------------------------------------------------------------------- الرئيسية
def main():
    doc = pymupdf.open(TEMPLATE)
    page = doc[0]

    for im in page.get_images(full=True):
        if im[0] == 95:
            page.delete_image(im[0])

    zones = [CARD] + [(c[0], c[1], c[2], ct[3]) for c, ct in PANEL.values()]
    for z in zones:
        page.add_redact_annot(pymupdf.Rect(*z), fill=None)
    page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,
                          graphics=pymupdf.PDF_REDACT_LINE_ART_NONE,
                          text=pymupdf.PDF_REDACT_TEXT_REMOVE)

    page.insert_link({"kind": pymupdf.LINK_URI, "from": pymupdf.Rect(375, 108, 1026, 180), "uri": SITE})

    build_header(page)
    build_headings(page)
    panel_intro(page)
    panel_method(page)
    panel_results(page)
    panel_innovation(page)
    panel_conclusion(page)
    panel_future(page)

    html(page, (330, 3356, 2000, 3388),
         '<span style="font-family:pl;font-size:18px;color:#FFFFFF;">شكر خاص لمعلمنا الأستاذ محمد السيد '
         'متولى، ولأسرة مدرسة الرواد الثانوية الأهلية، ولجنة تنظيم معرض ومسابقة سيف 2026.</span>',
         align="left", line_height=1.2, tag="thanks")

    doc.set_metadata({
        "title": "«كم» — منصة عربية للحوسبة الكمية | ملصق سيف 2026",
        "author": "مدرسة الرواد الثانوية الأهلية — الرياض",
        "subject": "SAIF 2026 Scientific Poster — 36×48 in, Track 13, ages 12–17",
        "keywords": "كم, Quantum Learning Lab, SAIF 2026, الحوسبة الكمية",
        "creator": "IBM Plex Sans Arabic",
    })
    try:
        doc.subset_fonts(verbose=False)   # يقلّص الخطوط المضمّنة إلى المحارف المستخدمة
    except Exception:
        pass
    doc.save(OUT_PDF, garbage=4, deflate=True, deflate_images=True, clean=True)
    print(f"✓ {OUT_PDF}  ({os.path.getsize(OUT_PDF) / 1024:.0f} KB، "
          f"{page.rect.width / 72:.0f}×{page.rect.height / 72:.0f} بوصة)")

    # ---------- فحص تراكب كتل النص (يمنع تكرار خلل «سطرين فوق بعضهما»)
    overlaps = []
    boxes = STATE.get("boxes", [])
    for i, (r1, t1, s1) in enumerate(boxes):
        for r2, t2, s2 in boxes[i + 1:]:
            inter = pymupdf.Rect(r1) & pymupdf.Rect(r2)
            if inter.is_empty:
                continue
            a = inter.width * inter.height
            smallest = min(r1.width * r1.height, r2.width * r2.height)
            if smallest > 0 and a / smallest > 0.25:
                overlaps.append(f"[{t1}] ↔ [{t2}] تراكب {a / smallest:.0%}")

    if STATE["errors"]:
        print("\n⚠ ملاحظات:")
        for e in STATE["errors"]:
            print("   ", e)
    else:
        print("✓ كل الكتل داخل أطرها بلا تصغير تلقائي")

    if overlaps:
        print(f"\n⚠ تراكب نصوص: {len(overlaps)}")
        for o in overlaps:
            print("   ", o)
    else:
        print("✓ لا تراكب بين كتل النص")

    if "--preview" in sys.argv:
        d2 = pymupdf.open(OUT_PDF)
        d2[0].get_pixmap(dpi=40).save(OUT_PNG)
        pix = d2[0].get_pixmap(dpi=150)
        pix.save(OUT_JPG, jpg_quality=88)
        print(f"✓ {OUT_PNG}\n✓ {OUT_JPG}  ({os.path.getsize(OUT_JPG) / 1024 / 1024:.1f} MB)")


if __name__ == "__main__":
    main()
