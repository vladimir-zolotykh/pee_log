#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
"""Usage:
font = button_font.TooltipFont()
font=button_font.TooltipFont()"""
import tkinter.font as tkFont


class SingletonFont(tkFont.Font):
    _instances = {}

    def __new__(cls, family='sans-serif', size=8):
        if cls not in cls._instances:
            cls._instances[cls] = super().__new__(cls)
        return cls._instances[cls]

    def __init__(self, family='sans-serif', size=8):
        super().__init__(family=family, size=size)


class ButtonFont(SingletonFont): pass  # noqa
class TooltipFont(SingletonFont): pass  # noqa
