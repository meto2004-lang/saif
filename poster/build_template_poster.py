#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مولّد الملصق العلمي العربي على قالب سيف الرسمي 2026.

المقاس: 36 × 48 بوصة طوليًا (914 × 1219 مم) — مطابق لأبعاد القالب حرفيًا.
الخط المعتمد: IBM Plex Sans Arabic (Light / Regular / Medium / SemiBold / Bold).

    python3 build_template_poster.py            # PDF فقط
    python3 build_template_poster.py --preview  # PDF + معاينات PNG/JPG

للنسخة الإنجليزية: build_template_poster_en.py
المتطلبات: pymupdf, qrcode, pillow
"""

import os
import sys

import pymupdf

import poster_kit as K
from poster_kit import (BOX_BOOTH, BOX_FLAG, BOX_QR, CARD, FLAG_SVG, INK, LINE, MINT,
                        MUTED, PANEL, SALMON, TEAL, Flow, cover, html, place_flag, rgb,
                        text, make_qr)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PDF = os.path.join(HERE, "saif-poster-36x48.pdf")
OUT_PNG = os.path.join(HERE, "preview-36x48.png")
OUT_JPG = os.path.join(HERE, "saif-poster-36x48.jpg")

K.set_direction("rtl")

HEADINGS = {
    "intro": ("المقدمة", "INTRODUCTION"),
    "method": ("المنهجية", "METHODOLOGY"),
    "results": ("النتائج", "RESULTS"),
    "innovation": ("الابتكار", "INNOVATION"),
    "conclusion": ("الخاتمة", "CONCLUSION"),
    "future": ("العمل المستقبلي والمراجع", "FUTURE WORK & REFERENCES"),
}


# --------------------------------------------------------------------- بطاقة العنوان
def build_header(page):
    cover(page, (CARD[0] + 0.6, CARD[1] + 0.6, CARD[2] - 0.6, CARD[3] - 0.6))

    # إعادة رسم إطارات الخانات الثلاث (غطاء البطاقة يمحوها لأنها مرسومة قبله)
    for box in (BOX_QR, BOX_BOOTH, BOX_FLAG):
        page.draw_rect(pymupdf.Rect(*box), color=rgb(INK), fill=None, width=0.75)

    # ---------- اليسار: الهوية
    text(page, 96, 300, "QUANTUM LEARNING LAB", 22, "m", TEAL)

    html(page, (96, 300, 470, 408),
         '<span style="font-family:pb;font-size:76px;color:%s;">كم</span>' % INK,
         align="left", line_height=1.25, tag="wordmark")

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

    # ---------- العلم في خانته من القالب (داخل الإطار تمامًا)
    inner_w = BOX_FLAG[2] - BOX_FLAG[0] - 14
    inner_h = BOX_FLAG[3] - BOX_FLAG[1] - 14
    fh = inner_w * 2 / 3
    if fh > inner_h:
        fh = inner_h
        inner_w = fh * 3 / 2
    fx = BOX_FLAG[0] + (BOX_FLAG[2] - BOX_FLAG[0] - inner_w) / 2
    fy = BOX_FLAG[1] + (BOX_FLAG[3] - BOX_FLAG[1] - fh) / 2
    place_flag(page, (fx, fy, fx + inner_w, fy + fh))

    # ---------- رمز QR
    make_qr()
    page.insert_image(pymupdf.Rect(BOX_QR[0] + 8, BOX_QR[1] + 8, BOX_QR[2] - 8, BOX_QR[3] - 8),
                      filename=K.QR_PNG)

    text(page, (BOX_BOOTH[0] + BOX_BOOTH[2]) / 2, BOX_BOOTH[3] - 16, "—", 30, "l", MUTED, "center")
    text(page, (BOX_BOOTH[0] + BOX_BOOTH[2]) / 2, BOX_BOOTH[3] - 42, "Booth", 12, "l", MUTED, "center")

    # ---------- العنوان والقائمون عليه
    TX1 = 2005
    html(page, (1040, 278, TX1, 424),
         '<span style="font-family:pb;font-size:50px;color:%s;">«كم» منصة عربية تجعل الحوسبة الكمية '
         'تجربة يراها الطالب ويصنعها بنفسه</span>' % INK,
         line_height=1.22, tag="title")

    html(page, (1040, 412, TX1, 448),
         "من المفهوم إلى الدائرة في ثلاث خطوات — دون رياضيات متقدمة",
         extra_css=f"body{{font-size:24px;color:{TEAL};font-family:pm;}}", line_height=1.25,
         tag="subtitle")

    html(page, (1040, 442, TX1, 472),
         '<span style="font-family:pl;font-size:19px;color:%s;">الطلاب: </span>'
         '<span style="font-family:pm;font-size:19px;">أسامة حمد عبدالرحمن الدايل · '
         'عبدالله عمر محمد المسند · فارس داوود عبدالله الراجحي</span>' % MUTED,
         line_height=1.25, tag="students")

    html(page, (1040, 470, 1868, 500),
         '<span style="font-family:pl;font-size:19px;color:%s;">المشرف: </span>'
         '<span style="font-family:pm;font-size:19px;">الأستاذ محمد السيد متولى — معلم الحاسب الآلي</span>'
         % MUTED, line_height=1.25, tag="supervisor")

    # حقل رقم الطالب: على سطر المشرف نفسه، في أقصى اليمين
    html(page, (1880, 470, 2145, 500),
         '<span style="font-family:pl;font-size:18px;color:%s;">ID: ____________</span>' % MUTED,
         align="right", direction="ltr", line_height=1.2, tag="id-field")


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
        cx = K.col_x(x0, x1, i, w, gap)
        page.draw_rect(pymupdf.Rect(cx, top, cx + w, top + h), color=rgb(LINE),
                       fill=rgb("#FFFFFF"), width=1.4, radius=0.03)
        html(page, (cx + 26, top + 26, cx + w - 26, top + 104),
             f'<span style="font-family:pb;font-size:54px;color:{TEAL};">{num}</span>'
             f'<span style="font-family:ps;font-size:34px;color:{INK};">&nbsp;&nbsp;{title}</span>',
             line_height=1.2, tag=f"step-{i}")
        html(page, (cx + 24, top + 124, cx + w - 24, top + 124 + 190),
             f'<span style="font-size:30px;line-height:1.55;">{txt}</span>',
             line_height=1.55, tag=f"step-body-{i}")

        # رسم توضيحي صغير أسفل كل بطاقة
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
        cx = K.col_x(x0, x1, col, w, gap)
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
    heights = [K.measure(f'<div style="font-size:31px;line-height:1.45;">{b}</div>', W, body_css,
                         line_height=1.45) for b in bullets]
    y = y0
    for b, h in zip(bullets, heights):
        html(page, (x0, y, x1, y + h + 2), f'<div style="font-size:31px;line-height:1.45;">{b}</div>',
             body_css, line_height=1.45, tag="inn-bullet")
        y += h + gap

    table_top = y1 - 5 * 74
    box_top = y + 6
    box_bottom = table_top - 26
    if box_bottom - box_top > 90:
        page.draw_rect(pymupdf.Rect(x0, box_top, x1, box_bottom), color=None, fill=rgb(MINT), width=0)
        page.draw_rect(pymupdf.Rect(x0, box_top, x0 + 7, box_bottom), color=None, fill=rgb(TEAL), width=0)
        inner = (x0 + 34, box_top + 22, x1 - 30, box_bottom - 22)
        hh = K.measure('<div style="font-size:30px;line-height:1.45;"><b>الفرق في البناء</b>'
                       '<div style="margin-top:10px;font-size:29px;">الطالب لا يقرأ عن التراكب ولا يحفظ '
                       'صيغته… بل يرى الاحتمالات تتحرك على الشاشة كلما غيّر البوابة.</div></div>',
                       inner[2] - inner[0], line_height=1.45)
        yy = inner[1] + max(0, (inner[3] - inner[1] - hh) / 2)
        html(page, (inner[0], yy, inner[2], yy + hh + 4),
             '<div style="font-size:30px;line-height:1.45;"><b>الفرق في البناء</b>'
             '<div style="margin-top:10px;font-size:29px;">الطالب لا يقرأ عن التراكب ولا يحفظ '
             'صيغته… بل يرى الاحتمالات تتحرك على الشاشة كلما غيّر البوابة.</div></div>',
             line_height=1.45, tag="inn-box")

    # جدول مقارنة مع المحاكيات المتاحة
    c_key = W * 0.19
    c_them = W * 0.27
    c_ours = W - c_key - c_them
    rh = 74
    ty = y1 - rh * 5

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
    page.insert_image(pymupdf.Rect(qx0, qy0, x1, qy0 + qr_w), filename=K.QR_PNG)
    html(page, (qx0 - 40, qy0 + qr_w + 14, x1 + 10, qy0 + qr_w + 92),
         '<span style="font-family:pm;font-size:21px;">امسح الرمز لزيارة المنصة</span>',
         align="center", line_height=1.25, tag="qr-label")
    text(page, x1 - qr_w / 2, qy0 + qr_w + 116, "meto2004-lang.github.io/saif", 13, "l", MUTED, "center")


# --------------------------------------------------------------------- الرئيسية
def main():
    doc = pymupdf.open(K.TEMPLATE)
    page = K.prepare_page(doc)

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

    K.save(doc, page, OUT_PDF, OUT_PNG, OUT_JPG,
           preview="--preview" in sys.argv, lang="ar")


if __name__ == "__main__":
    main()
