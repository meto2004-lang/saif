#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مولّد الملصق العلمي لمشروع «كم» — معرض ومسابقة سيف 2026
=======================================================
يُنتج ملفات PDF متجهية بمقاسات A1 و A2 و A3 من تصميم واحد مرسوم على A2.

    python3 build_poster.py          # الثلاثة
    python3 build_poster.py A2       # مقاس واحد

المتطلبات: reportlab, arabic-reshaper, python-bidi, qrcode
الخطوط في مجلد fonts/ (Tajawal, Orbitron, DejaVu مُجزّأ لرموز الرياضيات)
"""

import math
import os
import sys
from io import BytesIO

import arabic_reshaper
import qrcode
from bidi.algorithm import get_display
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.pdfgen.canvas import Canvas

HERE = os.path.dirname(os.path.abspath(__file__))
MM = 72.0 / 25.4
PT2MM = 25.4 / 72.0

DESIGN_W, DESIGN_H = 420.0, 594.0          # A2 عمودي
SIZES = {"A1": (594.0, 841.0), "A2": (420.0, 594.0), "A3": (297.0, 420.0)}

URL = "https://meto2004-lang.github.io/saif/"

# ------------------------------------------------------------------ الألوان
NAVY = HexColor("#0A0E27")
NAVY_2 = HexColor("#1A1150")
NAVY_3 = HexColor("#11173C")
INK = HexColor("#0B1030")
INK_2 = HexColor("#3E4866")
INK_3 = HexColor("#6B7492")
CYAN = HexColor("#0E7490")
CYAN_BR = HexColor("#0891B2")
CYAN_L = HexColor("#67E8F9")
PURPLE = HexColor("#5B21B6")
PURPLE_L = HexColor("#8B5CF6")
AMBER = HexColor("#B45309")
AMBER_L = HexColor("#F59E0B")
AMBER_BG = HexColor("#FFF8EC")
AMBER_LN = HexColor("#F3D9AE")
AMBER_TX = HexColor("#7C3E06")
GREEN = HexColor("#047857")
WHITE = HexColor("#FFFFFF")
PANEL = HexColor("#F6F8FF")
LINE = HexColor("#D5DCF0")
MUTED = HexColor("#A6B0CE")
TRACK = HexColor("#E7ECF9")

# ------------------------------------------------------------------ الخطوط
FONTS = {
    "Taj": "Tajawal-Regular.ttf",
    "Taj-B": "Tajawal-Bold.ttf",
    "Taj-Blk": "Tajawal-Black.ttf",
    "Orb": "Orbitron-Medium.ttf",
    "Orb-B": "Orbitron-Bold.ttf",
    "Math": "DejaVuSans-math.ttf",
}
for _name, _file in FONTS.items():
    pdfmetrics.registerFont(TTFont(_name, os.path.join(HERE, "fonts", _file)))

_shape_cache = {}


def AR(txt):
    """تشكيل الحروف العربية + ترتيب ثنائي الاتجاه (RTL)."""
    if txt not in _shape_cache:
        _shape_cache[txt] = get_display(arabic_reshaper.reshape(txt))
    return _shape_cache[txt]


def tw(txt, font, size, shape=True):
    """عرض نص بالملّيمتر."""
    return pdfmetrics.stringWidth(AR(txt) if shape else txt, font, size) * PT2MM


def wrap(txt, font, size, width_mm):
    lines, cur = [], ""
    for word in txt.split(" "):
        cand = (cur + " " + word).strip()
        if not cur or tw(cand, font, size) <= width_mm:
            cur = cand
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


class Doc:
    """قماش بوحدات الملّيمتر، إحداثيات y من أعلى الصفحة."""

    def __init__(self, c, w_mm, h_mm):
        self.c, self.W, self.H = c, w_mm, h_mm

    def X(self, x):
        return x * MM

    def Y(self, y):
        return (self.H - y) * MM

    def rect(self, x, y, w_, h_, r=0, fill=None, stroke=None, lw=0.35, dash=None):
        c = self.c
        c.saveState()
        if fill is not None:
            c.setFillColor(fill)
        if stroke is not None:
            c.setStrokeColor(stroke)
            c.setLineWidth(lw)
        if dash:
            c.setDash(dash)
        c.roundRect(self.X(x), self.Y(y + h_), w_ * MM, h_ * MM, r * MM,
                    stroke=1 if stroke is not None else 0,
                    fill=1 if fill is not None else 0)
        c.restoreState()

    def line(self, x1, y1, x2, y2, color=LINE, lw=0.35, dash=None):
        c = self.c
        c.saveState()
        c.setStrokeColor(color)
        c.setLineWidth(lw)
        if dash:
            c.setDash(dash)
        c.line(self.X(x1), self.Y(y1), self.X(x2), self.Y(y2))
        c.restoreState()

    def text(self, x, y, txt, font="Taj", size=15, color=INK, align="right",
             shape=True, charspace=0, opacity=1):
        c = self.c
        c.saveState()
        c.setFillColor(color)
        if opacity < 1:
            c.setFillAlpha(opacity)
        t = AR(txt) if shape else txt
        if charspace:
            to = c.beginText()
            to.setFont(font, size)
            to.setCharSpace(charspace)
            width = c.stringWidth(t, font, size) + charspace * max(0, len(t) - 1)
            if align == "right":
                to.setTextOrigin(self.X(x) - width, self.Y(y))
            elif align == "left":
                to.setTextOrigin(self.X(x), self.Y(y))
            else:
                to.setTextOrigin(self.X(x) - width / 2.0, self.Y(y))
            to.textOut(t)
            c.drawText(to)
        else:
            c.setFont(font, size)
            if align == "right":
                c.drawRightString(self.X(x), self.Y(y), t)
            elif align == "left":
                c.drawString(self.X(x), self.Y(y), t)
            else:
                c.drawCentredString(self.X(x), self.Y(y), t)
        c.restoreState()

    def gradient_rect(self, x, y, w_, h_, c1, c2, r=0):
        c = self.c
        c.saveState()
        p = c.beginPath()
        p.roundRect(self.X(x), self.Y(y + h_), w_ * MM, h_ * MM, r * MM)
        c.clipPath(p, stroke=0, fill=0)
        c.linearGradient(self.X(x), self.Y(y + h_), self.X(x + w_), self.Y(y), (c1, c2), extend=True)
        c.restoreState()

    def circle(self, cx, cy, r, fill=None, stroke=None, lw=0.4, opacity=1):
        c = self.c
        c.saveState()
        if opacity < 1:
            c.setFillAlpha(opacity)
            c.setStrokeAlpha(opacity)
        if fill is not None:
            c.setFillColor(fill)
        if stroke is not None:
            c.setStrokeColor(stroke)
            c.setLineWidth(lw)
        c.circle(self.X(cx), self.Y(cy), r * MM,
                 stroke=1 if stroke is not None else 0,
                 fill=1 if fill is not None else 0)
        c.restoreState()

    def ellipse(self, cx, cy, rx, ry, stroke=LINE, lw=0.4, opacity=1, rotate=0):
        c = self.c
        c.saveState()
        if opacity < 1:
            c.setStrokeAlpha(opacity)
        c.setStrokeColor(stroke)
        c.setLineWidth(lw)
        if rotate:
            c.translate(self.X(cx), self.Y(cy))
            c.rotate(rotate)
            c.ellipse(-rx * MM, -ry * MM, rx * MM, ry * MM)
        else:
            c.ellipse(self.X(cx - rx), self.Y(cy + ry), self.X(cx + rx), self.Y(cy - ry))
        c.restoreState()

    def arrow(self, x1, y1, x2, y2, color=INK_2, lw=0.6, head=2.0):
        c = self.c
        self.line(x1, y1, x2, y2, color, lw)
        ang = math.atan2(-(y2 - y1), (x2 - x1))
        for s in (+1, -1):
            a = ang + s * math.radians(26)
            c.saveState()
            c.setStrokeColor(color)
            c.setLineWidth(lw)
            c.line(self.X(x2), self.Y(y2),
                   self.X(x2 - head * math.cos(a)), self.Y(y2 + head * math.sin(a)))
            c.restoreState()


def draw_qr(d, x, y, size_mm, url, fg=NAVY):
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=1, border=0)
    qr.add_data(url)
    qr.make(fit=True)
    m = qr.get_matrix()
    n = len(m)
    pad = 1.8
    d.rect(x - pad, y - pad, size_mm + 2 * pad, size_mm + 2 * pad, r=1.4, fill=WHITE)
    cell = size_mm / n
    c = d.c
    c.saveState()
    c.setFillColor(fg)
    for r_ in range(n):
        for col in range(n):
            if m[r_][col]:
                c.rect(d.X(x + col * cell), d.Y(y + (r_ + 1) * cell), cell * MM, cell * MM,
                       stroke=0, fill=1)
    c.restoreState()


class Panel:
    """لوحة قابلة للقياس: تُجمع عناصرها أولًا ثم تُرسم بارتفاع محسوب."""

    PAD = 6.4

    def __init__(self, d, x, y, w_, num, title, accent=CYAN, sub=None):
        self.d, self.x, self.y, self.w = d, x, y, w_
        self.num, self.title, self.accent, self.sub = num, title, accent, sub
        self.ops = []
        self.cur = self.PAD + 9.6 + (6.0 if sub else 0.0)

    # ------------------------------------------------ عناصر
    def op(self, h, fn):
        self.ops.append((self.cur, fn))
        self.cur += h

    def gap(self, h):
        self.cur += h

    def para(self, txt, size=15, leading=23, color=INK_2, font="Taj", after=1.2):
        lines = wrap(txt, font, size, self.w - 2 * self.PAD)
        lh = leading * PT2MM
        h = len(lines) * lh + after
        base = size * 0.80 * PT2MM
        x_right = self.x + self.w - self.PAD
        d = self.d

        def fn(c, oy):
            for i, ln in enumerate(lines):
                d.text(x_right, oy + base + i * lh, ln, font, size, color)
        self.op(h, fn)

    def bullets(self, items, size=14.4, leading=21.5, color=INK_2, marker=CYAN_BR, after=1.4):
        lh = leading * PT2MM
        base = size * 0.80 * PT2MM
        prepared = [wrap(it, "Taj", size, self.w - 2 * self.PAD - 5.2) for it in items]
        h = sum(len(p) * lh + after for p in prepared)
        x_text = self.x + self.w - self.PAD - 5.2
        x_dot = self.x + self.w - self.PAD - 1.9
        d = self.d

        def fn(c, oy):
            y = oy
            for lines in prepared:
                d.circle(x_dot, y + base - 1.5, 0.95, fill=marker)
                for i, ln in enumerate(lines):
                    d.text(x_text, y + base + i * lh, ln, "Taj", size, color)
                y += len(lines) * lh + after
        self.op(h, fn)

    def chips(self, items, size=13.4, gap=2.8, row_gap=3.0, ch=8.6, after=2.0):
        avail = self.w - 2 * self.PAD
        rows, cur, cur_w = [], [], 0.0
        for it in items:
            cw = tw(it, "Taj-B", size) + 9.0
            if cur and cur_w + gap + cw > avail:
                rows.append(cur)
                cur, cur_w = [], 0.0
            cur.append((it, cw))
            cur_w += (gap if cur_w else 0) + cw
        if cur:
            rows.append(cur)
        h = len(rows) * (ch + row_gap) + after
        d = self.d

        def fn(c, oy):
            y = oy
            for row in rows:
                xr = self.x + self.w - self.PAD
                for txt, cw in row:
                    d.rect(xr - cw, y, cw, ch, r=4.3, fill=WHITE, stroke=LINE, lw=0.3)
                    d.text(xr - cw / 2, y + ch / 2 + 1.5, txt, "Taj-B", size, INK, align="center")
                    xr -= cw + gap
                y += ch + row_gap
        self.op(h, fn)

    def custom(self, h, fn, after=0.0):
        self.op(h + after, fn)

    # ------------------------------------------------ الرسم
    @property
    def height(self):
        return self.cur + self.PAD

    def draw(self):
        d = self.d
        d.rect(self.x, self.y, self.w, self.height, r=4.6, fill=PANEL, stroke=LINE, lw=0.35)
        d.rect(self.x + self.w - 1.6, self.y + 0.6, 1.6, self.height - 1.2, r=0.8, fill=self.accent)
        d.text(self.x + self.w - self.PAD, self.y + self.PAD + 4.8,
               self.num, "Math", 12.0, self.accent, shape=False)
        d.text(self.x + self.w - self.PAD - 9.8, self.y + self.PAD + 5.2,
               self.title, "Taj-Blk", 19.4, INK)
        if self.sub:
            d.text(self.x + self.w - self.PAD, self.y + self.PAD + 11.6,
                   self.sub, "Taj", 11.4, INK_3)
        for off, fn in self.ops:
            fn(d.c, self.y + off)


# ------------------------------------------------------------------ الترويسة
def header(d):
    hh = 128.0
    d.gradient_rect(0, 0, d.W, hh, NAVY, NAVY_2)

    # زخرفة: مدارات ذرّة خلف الشعار (علامة مائية خفيفة)
    ox, oy = 246.0, 60.0
    for ang, op in ((0, .26), (60, .18), (120, .13)):
        d.ellipse(ox, oy, 40, 14, stroke=CYAN_L, lw=0.45, opacity=op, rotate=ang)
    d.circle(ox, oy, 3.2, fill=CYAN_L, opacity=.55)
    d.circle(ox, oy, 8.0, stroke=CYAN_L, lw=0.3, opacity=.22)

    # بيانات المعرض (يسار)
    bx = 30.0
    badge = "معرض ومسابقة سيف 2026"
    bw = tw(badge, "Taj-B", 14.6) + 13
    d.rect(bx, 19.0, bw, 11.8, r=5.9, stroke=AMBER_L, lw=0.8)
    d.text(bx + bw / 2, 27.0, badge, "Taj-B", 14.6, AMBER_L, align="center")
    d.text(bx, 44.0, "الرياض  ·  24-26 نوفمبر 2026", "Taj-B", 15.8, WHITE, align="left")
    d.text(bx, 56.5, "المسار 13 — التقنيات الكمية والحوسبة المتقدمة", "Taj", 12.8, MUTED, align="left")
    d.text(bx, 68.0, "الفئة المستهدفة: طلاب 12–17 سنة", "Taj-B", 12.8, CYAN_L, align="left")

    # العنوان (يمين)
    xr = d.W - 26
    d.text(xr, 60, "كم", "Taj-Blk", 94, WHITE)
    d.text(xr - 78, 38, "QUANTUM LEARNING LAB", "Orb-B", 12.4, CYAN_L, shape=False, charspace=1.8)
    d.text(xr, 84, "منصّة عربية تجعل الحوسبة الكمية تجربة", "Taj-B", 21.6, WHITE)
    d.text(xr, 104, "يراها الطالب ويصنعها بنفسه داخل المتصفّح", "Taj-B", 21.6, WHITE)

    # شريط المدرسة والفريق
    sy = 112.0
    d.rect(0, sy, d.W, 16.0, fill=NAVY_3)
    d.line(0, sy, d.W, sy, HexColor("#2A3170"), 0.4)
    yb = sy + 10.6
    d.text(xr, yb, "مدرسة الرواد الثانوية الأهلية — حي الازدهار، الرياض", "Taj-B", 13.4, WHITE)
    d.text(xr - 172, yb, "أسامة الدايل · عبدالله المسند · فارس الراجحي", "Taj", 12.6, MUTED)
    d.text(bx, yb, "بإشراف الأستاذ محمد السيد متولى", "Taj", 12.6, MUTED, align="left")
    return hh


# ------------------------------------------------------------------ اللوحات
def panel_problem(d, x, y, w_):
    p = Panel(d, x, y, w_, "01", "المشكلة والسؤال", accent=AMBER)
    p.para("تُقدَّم الحوسبة الكمية غالبًا كمعادلات مجردة، فيحفظ الطالب المصطلح ولا يرى أثره. "
           "ومعظم المحاكيات العالمية بالإنجليزية، وواجهتها معقدة على المبتدئ.", size=15.0, leading=23.5)

    q = ("السؤال التصميمي: كيف نحوّل كل مفهوم كمي إلى تجربة قصيرة "
         "يفهمها طالب في الثانية عشرة دون رياضيات متقدمة؟")
    lines = wrap(q, "Taj-B", 14.4, w_ - 2 * Panel.PAD - 9)
    lh = 21.5 * PT2MM
    h = len(lines) * lh + 7.4

    def fn(c, oy):
        d.rect(p.x + Panel.PAD, oy, p.w - 2 * Panel.PAD, h - 1.4, r=3.4,
               fill=AMBER_BG, stroke=AMBER_LN, lw=0.4)
        for i, ln in enumerate(lines):
            d.text(p.x + p.w - Panel.PAD - 4.6, oy + 5.4 + i * lh, ln, "Taj-B", 14.4, AMBER_TX)
    p.custom(h, fn)
    return p


def panel_solution(d, x, y, w_):
    p = Panel(d, x, y, w_, "02", "الفكرة في ثلاث خطوات", accent=CYAN)
    steps = [("افهم", "بطاقة مفهوم مبسّطة"), ("جرّب", "دائرة تُشغَّل فعليًا"), ("تحقّق", "نشاط واختبار فوري")]
    sh = 20.4

    def fn(c, oy):
        bw = (p.w - 2 * Panel.PAD - 2 * 5.0) / 3
        for i, (t, sub) in enumerate(steps):
            bx = p.x + p.w - Panel.PAD - (i + 1) * bw - i * 5.0
            d.rect(bx, oy, bw, sh, r=3.4, fill=WHITE, stroke=LINE, lw=0.35)
            d.rect(bx + 0.7, oy, bw - 1.4, 1.2, r=0.6, fill=CYAN_BR)
            d.text(bx + bw / 2, oy + 8.2, t, "Taj-Blk", 15.8, INK, align="center")
            d.text(bx + bw / 2, oy + 14.6, sub, "Taj", 11.0, INK_3, align="center")
            if i < 2:
                d.arrow(bx - 1.4, oy + sh / 2, bx - 4.6, oy + sh / 2, CYAN_BR, 0.6, 1.5)
    p.custom(sh + 4.6, fn)
    p.bullets([
        "شرح عربي مبسّط مع المصطلح الإنجليزي المقابل",
        "محاكي Quirk يعمل داخل الصفحة بضغطة واحدة",
        "مساعد تعليمي وأوراق عمل جاهزة للمعلّم",
    ], size=14.2, leading=21.0)
    return p


def panel_content(d, x, y, w_):
    p = Panel(d, x, y, w_, "03", "ماذا يحتوي الموقع؟", accent=PURPLE)
    p.chips(["6 مفاهيم", "8 بوابات", "6 تجارب", "5 دوائر جاهزة",
             "4 أنشطة", "20 سؤالًا", "3 أوراق عمل", "10 أسئلة تقويم"])
    p.para("من الكيوبت إلى حالة GHZ في مسار واحد متصل. المحتوى كله ثنائي اللغة "
           "(عربي/إنجليزي) ويعمل على الجوّال والسبورة.", size=13.6, leading=20.0)
    return p


def panel_method(d, x, y, w_):
    p = Panel(d, x, y, w_, "04", "المنهجية", sub="بحث قائم على التصميم — دورات قصيرة", accent=GREEN)
    rows = [
        ("تحليل", "مراجعة المفاهيم والمحاكيات المتاحة وتحديد الفجوة."),
        ("تطوير", "كتابة المحتوى ثم بناء محاكٍ محلي وربط كل مفهوم بدائرة."),
        ("تحقّق", "20 اختبارًا آليًا للمحاكي والتحقق من 23 دائرة في Quirk."),
    ]
    rh = 15.6

    def fn(c, oy):
        yy = oy
        for i, (tag, txt) in enumerate(rows):
            d.circle(p.x + p.w - Panel.PAD - 3.4, yy + 4.4, 3.4, fill=WHITE, stroke=GREEN, lw=0.5)
            d.text(p.x + p.w - Panel.PAD - 3.4, yy + 5.7, str(i + 1), "Math", 9.0, GREEN, align="center", shape=False)
            d.text(p.x + p.w - Panel.PAD - 9.6, yy + 3.6, tag, "Taj-B", 13.8, INK)
            lines = wrap(txt, "Taj", 13.0, p.w - 2 * Panel.PAD - 11.0)
            for j, ln in enumerate(lines[:2]):
                d.text(p.x + p.w - Panel.PAD - 9.6, yy + 9.4 + j * 5.3, ln, "Taj", 13.0, INK_2)
            yy += rh
    p.custom(len(rows) * rh, fn)
    return p


def panel_science(d, x, y, w_):
    p = Panel(d, x, y, w_, "05", "الأساس العلمي", accent=CYAN)
    formulas = [
        ("الكيوبت", "|ψ⟩ = α|0⟩ + β|1⟩", "|α|² + |β|² = 1"),
        ("التراكب", "H|0⟩ = (|0⟩ + |1⟩)/√2", "H|1⟩ = (|0⟩ − |1⟩)/√2"),
        ("التشابك", "H + CNOT ⇒ (|00⟩ + |11⟩)/√2", "Φ⁻ = (|00⟩ − |11⟩)/√2"),
        ("القياس", "P(0) = |α|²", "P(1) = |β|²"),
    ]
    rh = 19.0
    h = len(formulas) * rh + 1

    def fn(c, oy):
        yy = oy
        for label, expr, note in formulas:
            d.text(p.x + p.w - Panel.PAD, yy + 4.6, label, "Taj-B", 13.6, CYAN)
            d.text(p.x + p.w - Panel.PAD, yy + 10.4, expr, "Math", 14.2, INK, shape=False)
            d.text(p.x + p.w - Panel.PAD, yy + 16.2, note, "Math", 11.4, INK_3, shape=False)
            yy += rh
    p.custom(h, fn)

    # كرة بلوخ
    bh = 46.0

    def bloch(c, oy):
        cx, cy, R = p.x + 38.0, oy + 22.0, 19.0
        d.circle(cx, cy, R, stroke=HexColor("#C3CDE9"), lw=0.5)
        d.ellipse(cx, cy, R, R * 0.34, stroke=HexColor("#B9C4E6"), lw=0.4)
        d.line(cx, cy - R - 2.4, cx, cy + R + 2.4, HexColor("#C9D2EC"), 0.35)
        d.line(cx - R - 2.4, cy, cx + R + 2.4, cy, HexColor("#C9D2EC"), 0.35)
        d.arrow(cx, cy, cx + 12.4, cy - 12.4, AMBER, 1.0, 2.3)
        d.circle(cx + 12.4, cy - 12.4, 1.5, fill=AMBER)
        d.text(cx + 1.6, cy - 2.2, "|ψ⟩", "Math", 11.0, AMBER, align="left", shape=False)
        d.text(cx, cy - R - 5.4, "|0⟩", "Math", 10.4, INK_3, align="center", shape=False)
        d.text(cx, cy + R + 7.2, "|1⟩", "Math", 10.4, INK_3, align="center", shape=False)
        d.text(cx + 6.0, cy + 2.4, "x", "Math", 8.4, MUTED, align="left", shape=False)
    p.custom(bh, bloch)
    p.para("كرة بلوخ: تمثيل بصري لحالة الكيوبت؛ القياس ينهار بالحالة إلى أحد القطبين.",
           size=12.4, leading=18.0)
    return p


def panel_bell(d, x, y, w_):
    p = Panel(d, x, y, w_, "06", "من الفكرة إلى الدائرة", accent=PURPLE)
    ch = 32.0

    def circ(c, oy):
        x0 = p.x + 30.0
        x1 = p.x + p.w - Panel.PAD - 6
        y0, y1 = oy + 8.0, oy + 22.0
        d.text(x0 - 4, y0 + 2.0, "q0", "Math", 9.8, INK_3, shape=False)
        d.text(x0 - 4, y1 + 2.0, "q1", "Math", 9.8, INK_3, shape=False)
        d.line(x0, y0, x1, y0, HexColor("#9FB0DA"), 0.6)
        d.line(x0, y1, x1, y1, HexColor("#9FB0DA"), 0.6)
        hx = x0 + 14
        d.rect(hx, y0 - 4.6, 9.2, 9.2, r=1.5, fill=PURPLE)
        d.text(hx + 4.6, y0 + 1.9, "H", "Orb-B", 10.2, WHITE, align="center", shape=False)
        cxx = hx + 20
        d.circle(cxx, y0, 1.7, fill=INK)
        d.line(cxx, y0, cxx, y1, INK, 0.7)
        d.rect(cxx - 4.6, y1 - 4.6, 9.2, 9.2, r=1.5, stroke=INK, lw=0.7)
        d.text(cxx, y1 + 2.0, "X", "Orb-B", 10.2, INK, align="center", shape=False)
        for yy in (y0, y1):
            mx = x1 - 13
            d.rect(mx, yy - 4.6, 9.6, 9.2, r=1.5, fill=WHITE, stroke=INK, lw=0.7)
            d.c.saveState()
            d.c.setStrokeColor(INK)
            d.c.setLineWidth(0.7)
            # arc(x1, y1, x2, y2) = المستطيل المحيط (أسفل-يسار ثم أعلى-يمين)
            d.c.arc(d.X(mx + 1.4), d.Y(yy + 3.2), d.X(mx + 8.2), d.Y(yy - 3.2), 200, 140)
            d.c.restoreState()
            d.line(mx + 4.8, yy + 3.2, mx + 7.4, yy - 2.6, INK, 0.7)
        d.text(x1 + 2.0, y1 + 1.6, "M", "Math", 8.6, MUTED, align="left", shape=False)
    p.custom(ch, circ)

    rows = [("00", 50, CYAN_BR), ("11", 50, PURPLE_L), ("01", 0, TRACK), ("10", 0, TRACK)]
    bh = len(rows) * 7.4 + 3

    def bars(c, oy):
        track_w = p.w - 2 * Panel.PAD - 34
        xr = p.x + p.w - Panel.PAD
        yy = oy
        for lab, pct, col in rows:
            d.text(xr, yy + 4.4, lab, "Math", 10.6, INK, shape=False)
            d.rect(xr - 13 - track_w, yy + 0.7, track_w, 4.8, r=2.4, fill=TRACK)
            if pct:
                fw = track_w * pct / 100.0
                d.rect(xr - 13 - fw, yy + 0.7, fw, 4.8, r=2.4, fill=col)
            d.text(xr - 13 - track_w - 2.2, yy + 4.4, f"{pct}%", "Math", 10.2, INK_2,
                   align="right", shape=False)
            yy += 7.4
    p.custom(bh, bars)
    p.para("لا تظهر 01 أو 10 أبدًا: الكيوبتان يتصرّفان كوحدة واحدة متشابكة.",
           size=12.8, leading=19.0)
    return p


def panel_verify(d, x, y, w_):
    p = Panel(d, x, y, w_, "07", "التحقق التقني", accent=GREEN)
    rows = [
        ("اختبارات صحة المحاكي الكمّي", "20 / 20", GREEN),
        ("دوائر Quirk مُتحقَّق من معرّفاتها", "23 / 23", GREEN),
        ("عناصر واجهة ثنائية اللغة", "129", INK),
        ("مكتبات خارجية مستخدمة", "0", INK),
        ("حجم المنصّة الكلي", "222 KB", INK),
        ("يعمل دون تثبيت أو حساب", "OK", GREEN),
    ]
    rh = 7.8

    def fn(c, oy):
        yy = oy
        for i, (label, val, col) in enumerate(rows):
            if i:
                d.line(p.x + Panel.PAD, yy, p.x + p.w - Panel.PAD, yy,
                       HexColor("#E3E8F6"), 0.3, dash=(1, 1.6))
            d.text(p.x + p.w - Panel.PAD, yy + 5.4, label, "Taj", 13.0, INK_2)
            d.text(p.x + Panel.PAD + 1.2, yy + 5.4, val, "Math", 10.4, col, align="left", shape=False)
            yy += rh
    p.custom(len(rows) * rh, fn)
    return p


def panel_eval(d, x, y, w_):
    p = Panel(d, x, y, w_, "08", "التقييم التعليمي", sub="الخطوة القادمة — قياس الأثر", accent=AMBER)
    p.bullets([
        "اختبار قبلي/بعدي من 20 سؤالًا (نفس بنك الأسئلة).",
        "مقياس الكسب المعياري: الفرق بين النتيجتين مقسومًا على (100 − النتيجة القبلية).",
        "عيّنة مستهدفة: 30–60 طالبًا بين 12 و17 سنة.",
        "مؤشرات إضافية: زمن المهمة وسهولة الاستخدام.",
    ], size=13.2, leading=19.4, marker=AMBER)
    return p


def panel_impact(d, x, y, w_):
    p = Panel(d, x, y, w_, "09", "الأثر والتوسّع", accent=CYAN)
    p.bullets([
        "أي مدرسة تتبنّاه برابط واحد: بلا تثبيت ولا حساب.",
        "يعمل على الجوّال والسبورة والحاسب.",
        "عربي أولًا، مع نسخة إنجليزية كاملة.",
        "قابل للتوسّع لأي مادة علمية أخرى.",
    ], size=13.2, leading=19.4)
    return p


# ------------------------------------------------------------------ التذييل
def footer(d):
    y = d.H - 34.0
    d.gradient_rect(0, y, d.W, 34.0, NAVY_2, NAVY)
    draw_qr(d, 21.0, y + 3.4, 23.0, URL)
    d.text(50.0, y + 11.8, "امسح الرمز وجرّب المنصّة", "Taj-B", 13.6, WHITE, align="left")
    d.text(50.0, y + 19.4, "meto2004-lang.github.io/saif", "Math", 10.0, CYAN_L, shape=False, align="left")
    d.text(50.0, y + 26.6, "على أي متصفّح — بلا تثبيت", "Taj", 10.2, MUTED, align="left")

    mid = d.W / 2
    d.text(mid, y + 12.4, "مدرسة الرواد الثانوية الأهلية", "Taj-B", 12.6, WHITE, align="center")
    d.text(mid, y + 19.6, "حي الازدهار — مدينة الرياض", "Taj", 11.4, MUTED, align="center")
    d.text(mid, y + 26.6, "المسار 13 — التقنيات الكمية والحوسبة المتقدمة", "Taj", 11.4,
           CYAN_L, align="center")

    xr = d.W - 20
    d.text(xr, y + 12.4, "فريق العمل", "Taj-B", 12.6, AMBER_L)
    d.text(xr, y + 19.6, "أسامة حمد عبدالرحمن الدايل  ·  عبدالله عمر محمد المسند", "Taj", 11.4, WHITE)
    d.text(xr, y + 26.6, "فارس داوود عبدالله الراجحي  ·  بإشراف أ. محمد السيد متولى", "Taj", 11.4, WHITE)


def references(d, y):
    label = "المراجع:"
    body = ("Nielsen & Chuang, Quantum Computation and Quantum Information, CUP 2010   ·   "
            "Gidney, Quirk Quantum Circuit Simulator, 2016   ·   "
            "Feynman, Simulating Physics with Computers, 1982")
    wl = tw(label, "Taj-B", 9.6)
    wb = tw(body, "Math", 9.4, shape=False)
    total = wl + wb + 3.0
    x0 = (d.W - total) / 2.0
    d.text(x0, y, body, "Math", 9.4, INK_3, align="left", shape=False)
    d.text(x0 + wb + 3.0 + wl, y, label, "Taj-B", 9.6, INK_3, align="right")


# ------------------------------------------------------------------ التجميع
def build(c, w_mm, h_mm, scale):
    # كل الإحداثيات بوحدات التصميم (A2) ثم يُقاس القماش كاملًا.
    d = Doc(c, DESIGN_W, DESIGN_H)
    c.scale(scale, scale)

    d.rect(0, 0, DESIGN_W, DESIGN_H, fill=WHITE)
    hh = header(d)

    col_w = (DESIGN_W - 2 * 15.0 - 14.0) / 2
    x_right = DESIGN_W - 15.0 - col_w
    x_left = 15.0
    top = hh + 12.0
    gap = 7.0
    avail = (DESIGN_H - 34.0 - 12.0) - top

    makers_r = [panel_problem, panel_solution, panel_content, panel_method, panel_impact]
    makers_l = [panel_science, panel_bell, panel_verify, panel_eval]

    # قياس الارتفاعات على قماش مؤقت
    meas = Canvas(BytesIO(), pagesize=(w_mm * MM, h_mm * MM))
    md = Doc(meas, DESIGN_W, DESIGN_H)
    ms = scale
    meas.scale(ms, ms)
    hs_r = [m(md, x_right, 0, col_w).height for m in makers_r]
    hs_l = [m(md, x_left, 0, col_w).height for m in makers_l]

    def total(hs):
        return sum(hs) + gap * (len(hs) - 1)

    print(f"    المساحة المتاحة {avail:.1f} مم | العمود الأيمن {total(hs_r):.1f} | "
          f"الأيسر {total(hs_l):.1f} | فارغ {avail - max(total(hs_r), total(hs_l)):.1f}")

    def place(makers, hs, x, target=None):
        ref = target if target is not None else avail
        extra = max(0.0, (ref - total(hs)) / max(1, len(hs) - 1))
        y = top
        for m, h in zip(makers, hs):
            m(d, x, y, col_w).draw()
            y += h + gap + extra
        return y - gap - extra

    # ضبط العمودين لينتهيا عند خط واحد
    target = max(total(hs_r), total(hs_l))
    end_r = place(makers_r, hs_r, x_right, target)
    end_l = place(makers_l, hs_l, x_left, target)
    references(d, min(max(end_r, end_l) + 7.0, DESIGN_H - 34.0 - 5.0))
    footer(d)


def main():
    which = sys.argv[1:] or ["A1", "A2", "A3"]
    for name in which:
        w_mm, h_mm = SIZES[name]
        scale = w_mm / DESIGN_W
        path = os.path.join(HERE, f"saif-poster-{name}.pdf")
        c = canvas.Canvas(path, pagesize=(w_mm * MM, h_mm * MM))
        c.setTitle("الملصق العلمي — كم | Quantum Learning Lab")
        c.setAuthor("فريق كم — مدرسة الرواد الثانوية الأهلية")
        c.setSubject("معرض ومسابقة سيف 2026 — المسار 13")
        c.setKeywords("quantum computing, Quirk, education, SAIF 2026")
        print(f"→ {name}")
        build(c, w_mm, h_mm, scale)
        c.showPage()
        c.save()
        print(f"  ✓ {os.path.basename(path)}  ({w_mm:.0f}×{h_mm:.0f} مم)")


if __name__ == "__main__":
    main()
