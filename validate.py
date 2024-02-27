#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk
import inspect
import subprocess


def clear_terminal():
    subprocess.run(['clear'], shell=True)


def validate_input(new_text):
    if not new_text.isdigit():
        return False
    # Additional validation can be added here if needed
    return True


def on_validate(action,                 # %d
                index,                  # %i
                value_if_allowed,       # %P
                prior_value,            # %s
                text,                   # %S
                validation_type,        # %v
                trigger_type,           # %V
                widget_name):           # %W
    clear_terminal()
    frame = inspect.currentframe()
    args, _, _, values = inspect.getargvalues(frame)
    for i in args:
        print(f'{i} = {values[i]}')
    if action == '1':           # Insert action
        return validate_input(value_if_allowed)
    else:
        return True


def main():
    root = tk.Tk()
    root.title("Entry Widget Validation Example")

    vcmd = root.register(validate_input)  # Register the validation function

    entry = tk.Entry(root, validate="key", validatecommand=(vcmd, '%P'))
    entry.focus_set()
    entry.config(
        validatecommand=(entry.register(on_validate),
                         '%d',  # action
                         '%i',  # insertion index
                         '%P',  # widget's value after action (if allowed)
                         '%s',  # current widget's text
                         '%S',  # like %P (but unconditional)
                         '%v',  # validation result
                         '%V',  # type of validation
                         '%W',  # Entry widget name
                         ))
    entry.pack(padx=10, pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
