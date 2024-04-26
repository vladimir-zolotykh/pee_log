#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk
import tkinter.font as tkFont


class Tooltip:
    def __init__(self, widget, text, font: tk.font.Font = None):
        self.widget = widget
        self.text = text
        if font is None:
            font = tkFont.Font(family='sans-serif', size=8)
        self.font = font
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        # For some widgets like Entry, (x, y) is always (0, 0)
        x, y, _, _ = self.widget.bbox('insert')
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            self.tooltip, text=self.text, background="lightyellow",
            font=self.font, relief="solid", borderwidth=1)
        label.pack(ipadx=1)

    def hide_tooltip(self, event):
        if self.tooltip:
            self.tooltip.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("300x200")

    # entry = tk.Entry(root)
    # entry.pack(pady=20)
    text_widget = tk.Text(root, width=40, height=10)
    text_widget.pack(pady=10)
    text_widget.insert("1.0", """\
This is a sample text.
You can click the button to get the bounding box of characters.""")

    tooltip_text = "This is the entry widget. You can type text here."
    # Tooltip(entry, tooltip_text)
    Tooltip(text_widget, tooltip_text)

    root.mainloop()
