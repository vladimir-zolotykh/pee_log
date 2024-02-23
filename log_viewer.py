#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk


if __name__ == '__main__':
    root = tk.Tk()
    log_list = tk.Listbox(root, width=40, height=25)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    log_list.grid(column=0, row=0, sticky=tk.NSEW)
    # (639, '2024-01-26 13:00:00', 439, 'Creatine'),
    # (640, '2024-01-26 13:31:00', 581, ''),
    # (641, '2024-01-26 14:00:00', 706, ''),
    log_list_test = [
        ('639', '2024-01-26 13:00:00', '439', 'Creatine'),
        ('640', '2024-01-26 13:31:00', '581', ''),
        ('641', '2024-01-26 14:00:00', '706', '')
    ]
    for item in log_list_test:
        line = '{:>5s}|{:20s}|{:>6s}|{:10s}'.format(*item)
        log_list.insert(tk.END, line)
    log_form = tk.Frame(root)
    log_form.grid(column=1, row=0, sticky=tk.N)
    label = tk.Label(log_form, text='Label')
    label.grid(column=0, row=0)
    label_entry = tk.Entry(log_form)
    label_entry.grid(column=1, row=0)
    volume_label = tk.Label(log_form, text='Volume')
    volume_label.grid(column=0, row=1)
    volume_value = tk.Entry(log_form)
    volume_value.grid(column=1, row=1)
    root.mainloop()
