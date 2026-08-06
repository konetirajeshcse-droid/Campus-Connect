from tkinter import messagebox
from datetime import datetime
import helpers

data = helpers.load_data()

def check_login(u, p, r):
    if u in data["users"] and data["users"][u]["pass"] == p and r == data["users"][u]["role"]:
        return True, u, r
    return False, "", ""

def add_resource(cat, title, path, user):
    if not title or not path:
        messagebox.showwarning("Warning", "Enter Title and File/Link"); return
    rtype = "link" if path.startswith("http") else "file"
    data["resources"].append([cat, title, rtype, path, user, str(datetime.now())])
    helpers.save_data(data)

def delete_resource(index):
    data["resources"].pop(index); helpers.save_data(data)

def get_resources(search, fcat):
    return [r for r in data["resources"] if (search in r[1].lower() or search in r[0].lower()) and (fcat == "All" or r[0] == fcat)]

def delete_user(uname):
    if uname == "admin":
        messagebox.showerror("Error", "Cannot delete admin"); return
    data["users"].pop(uname); helpers.save_data(data)

def add_user(nu, np, nr):
    if nu in data["users"]:
        messagebox.showerror("Error", "User exists"); return
    data["users"][nu] = {"pass": np, "role": nr}; helpers.save_data(data)

