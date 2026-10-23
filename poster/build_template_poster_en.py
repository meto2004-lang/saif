#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
English edition of the SAIF 2026 scientific poster — same official template.

Size: 36 × 48 in portrait (914 × 1219 mm), identical to the template geometry.
Typeface: IBM Plex Sans Arabic (Light / Regular / Medium / SemiBold / Bold) —
it carries full Latin coverage, so one family serves both editions.

    python3 build_template_poster_en.py            # PDF only
    python3 build_template_poster_en.py --preview  # PDF + PNG/JPG previews

Requirements: pymupdf, qrcode, pillow
"""

import os
import sys

import pymupdf

import poster_kit as K
from poster_kit import (BOX_BOOTH, BOX_FLAG, BOX_QR, CARD, INK, LINE, MINT, MUTED,
                        PANEL, SALMON, TEAL, Flow, cover, html, place_flag, rgb, text,
                        make_qr)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PDF = os.path.join(HERE, "saif-poster-36x48-en.pdf")
OUT_PNG = os.path.join(HERE, "preview-36x48-en.png")
OUT_JPG = os.path.join(HERE, "saif-poster-36x48-en.jpg")

K.set_direction("ltr")

HEADINGS = {
    "intro": "INTRODUCTION",
    "method": "METHODOLOGY",
    "results": "RESULTS",
    "innovation": "INNOVATION",
    "conclusion": "CONCLUSION",
    "future": "FUTURE WORK & REFERENCES",
}

STUDENTS = ("Osama Hamad Abdulrahman Al-Dailel · Abdullah Omar Mohammed Al-Musnad · "
            "Fares Dawood Abdullah Al-Rajhi")


# --------------------------------------------------------------------- title card
def build_header(page):
    cover(page, (CARD[0] + 0.6, CARD[1] + 0.6, CARD[2] - 0.6, CARD[3] - 0.6))

    # the three template boxes are drawn before the covering rect — redraw their frames
    for box in (BOX_QR, BOX_BOOTH, BOX_FLAG):
        page.draw_rect(pymupdf.Rect(*box), color=rgb(INK), fill=None, width=0.75)

    # ---------- left column: identity
    text(page, 96, 300, "QUANTUM LEARNING LAB", 22, "m", TEAL)

    html(page, (96, 300, 470, 408),
         '<span style="font-family:pb;font-size:76px;color:%s;">Kam</span>' % INK,
         align="left", line_height=1.25, tag="wordmark")

    html(page, (96, 402, 1010, 440),
         "Al-Rowad Private Secondary School — Al-Izdihar District — Riyadh",
         extra_css="body{font-size:26px;font-family:pm;}", align="left", line_height=1.2,
         tag="school")

    html(page, (96, 440, 1010, 472),
         "Track 13 — Quantum Technologies &amp; Advanced Computing · Ages 12–17",
         extra_css=f"body{{font-size:23px;color:{MUTED};}}", align="left", line_height=1.2,
         tag="track")

    # ---------- badge: flag + country
    bw = 44
    place_flag(page, (96, 486, 96 + bw * 1.5, 486 + bw))
    html(page, (96 + bw * 1.5 + 14, 484, 1010, 522),
         "Riyadh — Kingdom of Saudi Arabia",
         extra_css=f"body{{font-size:22px;font-family:pl;color:{MUTED};}}", align="left",
         line_height=1.2, tag="country")

    # ---------- flag inside its template box (fully contained)
    inner_w = BOX_FLAG[2] - BOX_FLAG[0] - 14
    inner_h = BOX_FLAG[3] - BOX_FLAG[1] - 14
    fh = inner_w * 2 / 3
    if fh > inner_h:
        fh = inner_h
        inner_w = fh * 3 / 2
    fx = BOX_FLAG[0] + (BOX_FLAG[2] - BOX_FLAG[0] - inner_w) / 2
    fy = BOX_FLAG[1] + (BOX_FLAG[3] - BOX_FLAG[1] - fh) / 2
    place_flag(page, (fx, fy, fx + inner_w, fy + fh))

    # ---------- QR
    make_qr()
    page.insert_image(pymupdf.Rect(BOX_QR[0] + 8, BOX_QR[1] + 8, BOX_QR[2] - 8, BOX_QR[3] - 8),
                      filename=K.QR_PNG)

    text(page, (BOX_BOOTH[0] + BOX_BOOTH[2]) / 2, BOX_BOOTH[3] - 16, "—", 30, "l", MUTED, "center")
    text(page, (BOX_BOOTH[0] + BOX_BOOTH[2]) / 2, BOX_BOOTH[3] - 42, "Booth", 12, "l", MUTED, "center")

    # ---------- title and people
    TX1 = 2005
    html(page, (1040, 276, TX1, 392),
         '<span style="font-family:pb;font-size:42px;color:%s;">“Kam” — an Arabic platform that turns '
         'quantum computing into a hands-on experience</span>' % INK,
         align="left", line_height=1.2, tag="title")

    html(page, (1040, 392, TX1, 424),
         "From concept to circuit in three steps — no advanced mathematics",
         extra_css=f"body{{font-size:24px;color:{TEAL};font-family:pm;}}", align="left",
         line_height=1.25, tag="subtitle")

    html(page, (1040, 424, TX1, 456),
         '<span style="font-family:pl;font-size:17px;color:%s;">Students: </span>'
         '<span style="font-family:pm;font-size:17px;">%s</span>' % (MUTED, STUDENTS),
         align="left", line_height=1.25, tag="students")

    html(page, (1040, 456, 1880, 490),
         '<span style="font-family:pl;font-size:18px;color:%s;">Supervisor: </span>'
         '<span style="font-family:pm;font-size:18px;">Mr. Mohammed El-Sayed Metwally — Computer '
         'Science Teacher</span>' % MUTED,
         align="left", line_height=1.25, tag="supervisor")

    html(page, (1890, 458, 2145, 490),
         '<span style="font-family:pl;font-size:18px;color:%s;">ID: ____________</span>' % MUTED,
         align="right", line_height=1.2, tag="id-field")


# --------------------------------------------------------------------- panel headings
def build_headings(page):
    for key, (card, content) in PANEL.items():
        cover(page, (card[0] + 0.6, card[1] + 0.6, card[2] - 0.6, content[3] + 1))
        html(page, (card[0] + 32, card[1] + 18, card[2] - 32, card[1] + 92),
             f'<span style="font-family:ps;font-size:48px;color:{INK};">{HEADINGS[key]}</span>',
             align="left", line_height=1.1, tag=f"head-{key}")


# --------------------------------------------------------------------- 1 introduction
def panel_intro(page):
    Flow(page, PANEL["intro"][1], gap=26, max_gap=90).add(
        '<span style="font-size:29px;line-height:1.42;">Quantum computing presents ideas unlike '
        'anything we know: a qubit that is 0 and 1 at the same time, and entanglement that links '
        'two qubits even when they are far apart.</span>', align="left", tag="lead"
    ).add(
        '<div class="box"><b style="font-size:29px;">The problem</b>'
        '<div style="margin-top:9px;font-size:28px;line-height:1.42;">'
        '•&nbsp; Global simulators are in English, so students stop at the terminology before '
        'understanding it.<br/>'
        '•&nbsp; Concepts arrive as abstract equations, so students memorize the rule without '
        'seeing its effect.<br/>'
        '•&nbsp; No single Arabic experience brings explanation, experiment and verification '
        'together.'
        '</div></div>', align="left", tag="problem"
    ).add(
        '<div class="q"><b style="font-size:29px;color:%s;">Our question</b>'
        '<div style="margin-top:10px;font-size:29px;line-height:1.4;">How do we turn a concept into '
        'a short experiment that a twelve-year-old understands, without advanced mathematics?</div>'
        '</div>' % SALMON, align="left", tag="question"
    ).add(
        '<div style="font-size:28px;line-height:1.45;"><b>Who is it for?</b> Students in grades 7–11 '
        '(ages 12–17), and teachers who want a ready first quantum lesson without complex '
        'preparation.</div>', align="left", tag="audience"
    ).render()


# --------------------------------------------------------------------- 2 methodology
def panel_method(page):
    x0, y0, x1, y1 = PANEL["method"][1]
    html(page, (x0, y0, x1, y0 + 56),
         "We built “Kam” in three stages, each reviewed before moving to the next.",
         extra_css="body{font-size:31px;}", align="left", line_height=1.3, tag="method-lead")

    steps = [
        ("1", "Analyse", "We reviewed several global simulators and compared content, language and "
                         "how each one presents the concept."),
        ("2", "Build", "We added a quantum simulator from scratch inside the browser, with a full "
                       "Arabic interface and no external libraries."),
        ("3", "Verify", "20 automated tests, and 23 circuits compared against the global Quirk "
                        "simulator."),
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
             align="left", line_height=1.2, tag=f"step-{i}")
        html(page, (cx + 24, top + 124, cx + w - 24, top + h - 205),
             f'<span style="font-size:28px;line-height:1.5;">{txt}</span>',
             align="left", line_height=1.5, tag=f"step-body-{i}")

        # small pictogram under each card
        iy = top + h - 190
        icon_cx = cx + w / 2
        if i == 0:      # analyse: comparison bars
            for k, hh in enumerate((60, 96, 44)):
                x = icon_cx - 90 + k * 66
                page.draw_rect(pymupdf.Rect(x, iy + 100 - hh, x + 44, iy + 100),
                               color=None, fill=rgb(TEAL), width=0)
        elif i == 1:    # build: tiny circuit
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
        else:           # verify: check mark
            page.draw_circle((icon_cx, iy + 66), 46, color=rgb(TEAL), fill=rgb(MINT), width=3)
            page.draw_line((icon_cx - 22, iy + 66), (icon_cx - 5, iy + 84), color=rgb(TEAL), width=7)
            page.draw_line((icon_cx - 5, iy + 84), (icon_cx + 24, iy + 44), color=rgb(TEAL), width=7)

    by = y1 - bar_h
    page.draw_rect(pymupdf.Rect(x0, by, x1, by + 132), color=None, fill=rgb(MINT), width=0)
    html(page, (x0 + 30, by + 14, x1 - 30, by + 60),
         '<span style="font-family:pl;font-size:26px;color:%s;">Every page of the platform follows '
         'the same path</span>' % MUTED, align="left", line_height=1.2, tag="path-label")
    html(page, (x0 + 30, by + 58, x1 - 30, by + 122),
         '<span style="font-family:ps;font-size:34px;color:%s;">Understand → Try → Verify</span>' % INK,
         align="left", line_height=1.2, tag="path-steps")


# --------------------------------------------------------------------- 3 results
def panel_results(page):
    x0, y0, x1, y1 = PANEL["results"][1]
    stats = [("6", "core concepts"), ("8", "quantum gates"), ("6", "ready experiments"),
             ("20", "interactive questions"), ("3", "worksheets"), ("20/20", "passing tests")]
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
         '<span style="font-family:ps;font-size:30px;">Bell circuit: gate H then CNOT</span>'
         f'<span style="font-family:pl;font-size:22px;color:{MUTED};">&nbsp;&nbsp;— an even split '
         'between 00 and 11 only</span>',
         align="left", line_height=1.25, tag="circuit-title")

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
         '<div style="font-size:26px;line-height:1.45;"><b>What does the result mean?</b> If we '
         'repeat the experiment a hundred times, “00” arrives about fifty times and “11” about '
         'fifty times, while “01” and “10” never appear — that is entanglement itself.</div>',
         align="left", line_height=1.45, tag="circuit-explain")


# --------------------------------------------------------------------- 4 innovation
def panel_innovation(page):
    x0, y0, x1, y1 = PANEL["innovation"][1]
    W = x1 - x0

    bullets = [
        "<b>A complete Arabic experience:</b> explanation, simulation and verification on a "
        "single page.",
        "<b>Works instantly:</b> on a computer or a phone, with no installation or account.",
        "<b>External verification:</b> every circuit is compared against the global Quirk "
        "simulator, so nobody is asked to trust us without evidence.",
        "<b>Transparency:</b> zero external libraries, and the code is open to review.",
    ]
    gap = 16
    body_css = "body{font-size:29px;}"
    heights = [K.measure(f'<div style="font-size:29px;line-height:1.4;">{b}</div>', W, body_css,
                         align="left", line_height=1.4) for b in bullets]
    y = y0
    for b, h in zip(bullets, heights):
        html(page, (x0, y, x1, y + h + 2), f'<div style="font-size:29px;line-height:1.4;">{b}</div>',
             body_css, align="left", line_height=1.4, tag="inn-bullet")
        y += h + gap

    table_top = y1 - 5 * 74
    box_top = y + 8
    box_bottom = table_top - 24
    if box_bottom - box_top > 70:
        page.draw_rect(pymupdf.Rect(x0, box_top, x1, box_bottom), color=None, fill=rgb(MINT), width=0)
        page.draw_rect(pymupdf.Rect(x0, box_top, x0 + 7, box_bottom), color=None, fill=rgb(TEAL), width=0)
        inner = (x0 + 34, box_top + 16, x1 - 30, box_bottom - 16)
        # نختار أكبر حجم خط يتّسع فعليًا للمساحة المتبقية
        for fs in (29, 27, 25, 23, 21):
            body = (f'<div style="font-size:{fs}px;line-height:1.38;"><b>The difference in how it is built</b>'
                    f'<div style="margin-top:6px;font-size:{fs - 1}px;">Students do not read about '
                    'superposition or memorize its formula… they watch the probabilities move on '
                    'screen every time they change a gate.</div></div>')
            hh = K.measure(body, inner[2] - inner[0], align="left", line_height=1.38)
            if hh <= inner[3] - inner[1]:
                break
        yy = inner[1] + max(0, (inner[3] - inner[1] - hh) / 2)
        html(page, (inner[0], yy, inner[2], yy + hh + 4), body,
             align="left", line_height=1.38, tag="inn-box")

    # comparison table: criterion | Kam | global simulators (left to right)
    c_key = W * 0.20
    c_ours = W * 0.40
    c_them = W - c_key - c_ours
    rh = 74
    ty = y1 - rh * 5

    page.draw_rect(pymupdf.Rect(x0, ty, x1, ty + rh), color=None, fill=rgb(INK), width=0)
    html(page, (x0 + c_key + 12, ty + 12, x0 + c_key + c_ours - 12, ty + rh - 10),
         '<span style="font-family:pb;font-size:24px;color:#FFFFFF;">“Kam”</span>',
         align="left", line_height=1.2, tag="cmp-h1")
    html(page, (x0 + c_key + c_ours + 12, ty + 12, x1 - 16, ty + rh - 10),
         '<span style="font-family:pl;font-size:22px;color:#FFFFFF;">Global simulators</span>',
         align="right", line_height=1.2, tag="cmp-h2")
    html(page, (x0 + 14, ty + 12, x0 + c_key - 12, ty + rh - 10),
         '<span style="font-family:ps;font-size:22px;color:#FFFFFF;">Criterion</span>',
         align="left", line_height=1.2, tag="cmp-h3")

    rows = [("Language", "Full Arabic, right to left", "English or machine translation"),
            ("Path to understanding", "Visual experiment first, then the symbol", "Equations and matrices"),
            ("Verification", "Published comparison with Quirk", "Internal, not disclosed"),
            ("Running it", "Browser directly, no account", "Software that needs installation")]
    ry = ty + rh
    for i, (key, ours, them) in enumerate(rows):
        bg = rgb("#FFFFFF") if i % 2 == 0 else rgb(MINT)
        page.draw_rect(pymupdf.Rect(x0, ry, x1, ry + rh), color=rgb(LINE), fill=bg, width=1)
        html(page, (x0 + 14, ry + 10, x0 + c_key - 12, ry + rh - 8),
             f'<span style="font-family:ps;font-size:21px;">{key}</span>', align="left",
             line_height=1.25, tag=f"cmp-k-{i}")
        html(page, (x0 + c_key + 12, ry + 10, x0 + c_key + c_ours - 12, ry + rh - 8),
             f'<span style="font-family:pm;font-size:22px;">{ours}</span>', align="left",
             line_height=1.25, tag=f"cmp-ours-{i}")
        html(page, (x0 + c_key + c_ours + 12, ry + 10, x1 - 16, ry + rh - 8),
             f'<span style="font-family:pl;font-size:20px;color:{MUTED};">{them}</span>', align="right",
             line_height=1.25, tag=f"cmp-them-{i}")
        ry += rh

    page.draw_rect(pymupdf.Rect(x0 + c_key, ty, x0 + c_key, ry), color=rgb(TEAL), fill=None, width=3)


# --------------------------------------------------------------------- 5 conclusion
def panel_conclusion(page):
    Flow(page, PANEL["conclusion"][1], gap=30, max_gap=90).add(
        '<div style="font-size:31px;line-height:1.5;">After the experiment, students explain '
        'superposition in their own words and connect every symbol in the circuit to a result '
        'they drew themselves.</div>', align="left", tag="con-1"
    ).add(
        '<div style="font-size:31px;line-height:1.5;">We shortened the distance between '
        'observation and conclusion to three steps: understand, try, verify.</div>',
        align="left", tag="con-2"
    ).add(
        '<div class="box"><span style="font-family:ps;font-size:31px;line-height:1.4;color:%s;">'
        'Simplifying science does not mean dropping its precision — it means ordering its path.'
        '</span></div>' % INK, align="left", tag="con-box"
    ).add(
        '<div style="font-size:28px;line-height:1.45;"><b>One-line takeaway:</b> a single platform, '
        'fully in Arabic, opens the door to quantum computing for a twelve-year-old — and its '
        'results are measured in numbers, not opinions.</div>', align="left", tag="con-3"
    ).render()


# --------------------------------------------------------------------- 6 future work
def panel_future(page):
    x0, y0, x1, y1 = PANEL["future"][1]
    qr_w = 180
    # QR on the left for LTR reading, text block to its right
    qx0 = x0
    tx0 = x0 + qr_w + 52

    qy0 = y0 + 40
    page.draw_rect(pymupdf.Rect(qx0 - 12, qy0 - 10, qx0 + qr_w + 12, qy0 + qr_w + 12),
                   color=rgb(LINE), fill=rgb("#FFFFFF"), width=1.4, radius=0.03)
    page.insert_image(pymupdf.Rect(qx0, qy0, qx0 + qr_w, qy0 + qr_w), filename=K.QR_PNG)
    html(page, (qx0 - 30, qy0 + qr_w + 14, qx0 + qr_w + 30, qy0 + qr_w + 92),
         '<span style="font-family:pm;font-size:20px;">Scan to visit the platform</span>',
         align="center", line_height=1.25, tag="qr-label")
    text(page, qx0 + qr_w / 2, qy0 + qr_w + 116, "meto2004-lang.github.io/saif", 13, "l", MUTED,
         "center")

    Flow(page, (tx0, y0, x1, y0 + 250), gap=24, max_gap=40).add(
        '<div style="font-size:28px;line-height:1.45;"><b>Measuring impact:</b> 30 students, a '
        'pre-test and a post-test, 20 questions.</div>', align="left", tag="fut-1"
    ).add(
        '<div style="font-size:28px;line-height:1.45;"><b>Scaling up:</b> an English edition, '
        'teacher pathways, and 3-qubit circuits.</div>', align="left", tag="fut-2"
    ).render()

    refs = ["Nielsen & Chuang, Quantum Computation and",
            "Quantum Information, Cambridge Univ. Press, 2010.",
            "Gidney, C., Quirk: Quantum Circuit Simulator, 2016.",
            "Feynman, R., Simulating Physics with Computers, 1982."]
    ry = y0 + 290
    html(page, (tx0, ry, x1, ry + 46),
         '<span style="font-family:pb;font-size:26px;">References</span>',
         align="left", line_height=1.2, tag="refs-title")
    for i, line in enumerate(refs):
        text(page, tx0, ry + 76 + i * 34, line, 22, "l", MUTED)


# --------------------------------------------------------------------- main
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
         '<span style="font-family:pl;font-size:18px;color:#FFFFFF;">Special thanks to our teacher '
         'Mr. Mohammed El-Sayed Metwally, to the Al-Rowad Private Secondary School family, and to '
         'the SAIF 2026 exhibition and competition organizing committee.</span>',
         align="left", line_height=1.2, tag="thanks")

    doc.set_metadata({
        "title": "\"Kam\" — an Arabic platform for quantum computing | SAIF 2026 poster (English)",
        "author": "Al-Rowad Private Secondary School — Riyadh",
        "subject": "SAIF 2026 Scientific Poster — 36×48 in, Track 13, ages 12–17",
        "keywords": "Kam, Quantum Learning Lab, SAIF 2026, quantum computing, education",
        "creator": "IBM Plex Sans Arabic",
    })

    K.save(doc, page, OUT_PDF, OUT_PNG, OUT_JPG, preview="--preview" in sys.argv, lang="en")


if __name__ == "__main__":
    main()
