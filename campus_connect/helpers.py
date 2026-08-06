import json, os
from tkinter import scrolledtext
import PyPDF2
from docx import Document

file = "data.json"
THEMES = {
    "light": {"bg": "#F0F0F0", "fg": "black", "top": "lightblue", "frame": "white", "entry": "white"},
    "dark": {"bg": "#1E1E1E", "fg": "white", "top": "#0D0D0D", "frame": "#2D2D2D", "entry": "#3C3C3C"}
}
theme = "light"

def load_data():
    if os.path.exists(file):
        with open(file, "r") as f: data = json.load(f)
    else: data = {}
    data.setdefault("users", {"admin": {"pass": "123", "role": "Admin"}, "student": {"pass": "123", "role": "Student"}})
    data.setdefault("resources", [])
    save_data(data)
    return data

def save_data(data):
    with open(file, "w") as f: json.dump(data, f, indent=2)

def toggle_theme(root, top, top_label):
    global theme
    theme = "dark" if theme == "light" else "light"
    c = THEMES[theme]
    root.config(bg=c["bg"]); top.config(bg=c["top"]); top_label.config(bg=c["top"], fg=c["fg"])
    return theme

def get_preview_text(p):
    ext = os.path.splitext(p)[1].lower()
    try:
        if ext == ".pdf":
            with open(p, "rb") as f: return "\n".join([pg.extract_text() or "" for pg in PyPDF2.PdfReader(f).pages])
        elif ext == ".docx": return "\n".join([para.text for para in Document(p).paragraphs])
        else:
            with open(p, "r", encoding="utf-8", errors='ignore') as f: return f.read()
    except: return "Cannot preview this file"

def toggle_theme(root, top, top_label, style):
    global theme
    theme = "dark" if theme == "light" else "light"
    c = THEMES[theme]

    root.config(bg=c["bg"])
    top.config(bg=c["top"])
    top_label.config(bg=c["top"], fg=c["fg"])

    style.configure("TNotebook", background=c["bg"])
    style.configure("TNotebook.Tab", background=c["top"], foreground=c["fg"])

    style.theme_use('clam')
    style.configure("TFrame", background=c["frame"])
    style.configure("TLabel", background=c["frame"], foreground=c["fg"])
    style.configure("TButton", background=c["entry"], foreground=c["fg"])
    style.configure("TEntry", fieldbackground=c["entry"], foreground=c["fg"])
    style.configure("TCombobox", fieldbackground=c["entry"], foreground=c["fg"])
    style.configure("TNotebook", background=c["bg"])
    style.configure("TNotebook.Tab", background=c["entry"], foreground=c["fg"])

    return theme