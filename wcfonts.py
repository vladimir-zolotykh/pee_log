#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Literal, Dict
from tkinter.font import Font
font_config: Dict[str, Dict] = {
    'WcButtonFont':  {'family': 'sans-serif', 'size': 8},
    'WcMenuFont':    {'family': 'sans-serif', 'size': 8},
    'WcTooltipFont': {'family': 'sans-serif', 'size': 8}}
wcfonts = {}


def wcfont(
        font_name: Literal['WcButtonFont', 'WcTooltipFont', 'WcMenuFont']
) -> Font:
    if font_name not in wcfonts:
        font = Font(name=font_name, **font_config[font_name])
        wcfonts[font_name] = font
    return wcfonts[font_name]
