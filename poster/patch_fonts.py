#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إصلاح خطوط Tajawal لإنتاج PDF عربي سليم
=====================================
خط Tajawal لا يتضمّن «الأشكال المعزولة» (isolated forms) من نطاق
Arabic Presentation Forms-B (U+FE70–U+FEFF)، وهي الأشكال التي يُنتجها
arabic_reshaper للحروف غير المتّصلة بما قبلها (ا، د، ر، و، ة …).
لذلك تظهر تلك الحروف مربّعات فارغة عند الرسم.

هذا السكربت يضيف لكل شكل معزول ناقص تعيينًا (cmap) إلى محرف الحرف الأصلي،
فيكون الشكل المعزول في الخط هو نفسه محرف الحرف الأساسي — وهو مطابق بصريًا.

    python3 patch_fonts.py
"""

import os
import sys
import unicodedata

from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = ["Tajawal-Regular.ttf", "Tajawal-Bold.ttf", "Tajawal-Black.ttf"]


def patch(path):
    font = TTFont(path)
    base_cmap = font.getBestCmap()
    added = 0
    for table in font["cmap"].tables:
        if not table.isUnicode():
            continue
        cmap = table.cmap
        for cp in range(0xFE70, 0xFF00):
            if cp in cmap:
                continue
            decomp = unicodedata.decomposition(chr(cp))
            if not decomp or not decomp.startswith("<isolated>"):
                continue          # الأشكال المتصلة موجودة أصلًا؛ لا نلمسها
            base_cp = int(decomp.split()[1], 16)
            gname = base_cmap.get(base_cp)
            if gname:
                cmap[cp] = gname
                added += 1
    font.save(path)
    return added


def main():
    for name in FONTS:
        path = os.path.join(HERE, "fonts", name)
        n = patch(path)
        print(f"✓ {name}: أُضيف {n} شكلًا معزولًا")


if __name__ == "__main__":
    main()
