#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk
import subprocess


def clear_terminal():
    subprocess.run(['clear'], shell=True)


def validate_input(new_text):
    # new_text - the text of Entry widget
    if not new_text.isdigit():
        return False
    return True


def on_validate(action, value_if_allowed):
    if action == '1':           # Insert action
        return validate_input(value_if_allowed)
    else:
        return True


def main():
    root = tk.Tk()
    root.title("Entry Widget Validation Example")
    vcmd = root.register(on_validate)
    entry = tk.Entry(root, validate="key", validatecommand=(vcmd, '%d', '%P'))
    entry.focus_set()
    entry.pack(padx=10, pady=10)
    root.mainloop()


if __name__ == "__main__":
    main()
