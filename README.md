# 📚 Campus Connect

Campus Connect is a desktop resource-sharing application built with **Python** and **Tkinter**. It lets students and admins log in, upload/browse study resources (PDFs, notes, links), and gives admins tools to manage users and content — all backed by a simple local JSON database.

## ✨ Features

- **Role-based login** — separate Admin and Student access
- **Resource management** — add, search, filter, open, and delete resources (files or links)
- **User management (Admin only)** — add and delete user accounts, with the default `admin` account protected from deletion
- **File preview support** — extract text from PDF and DOCX files for quick previews
- **Light/Dark theme toggle** — switch the UI's look and feel
- **Local JSON storage** — no external database required; data persists in `data.json`

## 🛠️ Tech Stack

- **Python 3.11**
- **Tkinter / ttk** — GUI
- **PyPDF2** — PDF text extraction
- **python-docx** — DOCX text extraction
- **JSON** — lightweight local data storage

## 📁 Project Structure

```
campus-connect/
├── main.py         # App entry point, builds the Tkinter UI
├── app_logic.py     # Core logic: login, add/delete resources & users
├── helpers.py        # Data load/save, theming, file preview helpers
├── data.json          # Local data store (users + resources)
└── settings.json       # Editor/environment settings
```

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- pip

### Installation

```bash
git clone https://github.com/<your-username>/campus-connect.git
cd campus-connect
pip install PyPDF2 python-docx
```

### Run the app

```bash
python main.py
```

### Default login credentials

| Role    | Username | Password |
|---------|----------|----------|
| Admin   | admin    | 123      |
| Student | student  | 123      |

> ⚠️ These are demo credentials stored in plain text in `data.json`. Change them before using this app with real data, and consider hashing passwords for anything beyond local/demo use.

## 📝 Usage

1. Log in with a username, password, and role (Admin/Student).
2. Browse resources in the **Resources** tab — search by title/category or filter by category.
3. Click **Add** to upload a new file as a resource.
4. Select a resource and click **Open** to view it, or **Delete** to remove it.
5. Admins can click **Manage Users** to add or remove user accounts.

## 🧭 Roadmap / Possible Improvements

- Hash and salt stored passwords instead of plain text
- Add link-based resources back into the UI (currently only file uploads are wired up)
- Cross-platform file opening (currently uses `os.startfile`, which is Windows-only)
- Add resource categories dynamically instead of a fixed list

## 📄 License

This project currently has no license specified. Add a `LICENSE` file (e.g. MIT) if you'd like others to freely use or contribute to it.
