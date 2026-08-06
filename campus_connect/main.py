import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess, os
import app_logic, helpers

root = tk.Tk()
style = ttk.Style()
root.geometry("1100x650")
root.title("Campus Connect")

user = user_role = ""
selected_path = ""

login_frame = main_frame = manage_frame = None
list1 = searchVar = filterCat = cat = titleE = None
manage_btn = delete_btn = None
tab1 = addFrame = None

def show(frame):
    global login_frame, main_frame, manage_frame
    for f in [login_frame, main_frame, manage_frame]:
        if f: f.pack_forget()
    if frame!= login_frame:
        top.pack(fill=tk.X)
        tabs.pack(fill=tk.BOTH, expand=1)
    else:
        top.pack_forget()
        tabs.pack_forget()
    frame.pack(fill=tk.BOTH, expand=1)

def show_manage():
    global manage_frame
    if manage_frame: manage_frame.destroy()
    manage_frame = tk.Frame(tab1)
    show(manage_frame)

    tk.Button(manage_frame, text="⬅ Back", command=lambda: show(main_frame)).pack(anchor="w", pady=5)
    tk.Label(manage_frame, text="Manage Users", font=("Arial", 14, "bold")).pack(pady=5)

    add_frame = tk.Frame(manage_frame)
    add_frame.pack(fill="x", pady=10, padx=10)

    new_user = tk.Entry(add_frame)
    new_pass = tk.Entry(add_frame, show="*")
    new_role = tk.StringVar(value="Student")

    tk.Label(add_frame, text="Username:").pack(side=tk.LEFT)
    new_user.pack(side=tk.LEFT, padx=5)
    tk.Label(add_frame, text="Password:").pack(side=tk.LEFT)
    new_pass.pack(side=tk.LEFT, padx=5)
    tk.Radiobutton(add_frame, text="Admin", variable=new_role, value="Admin").pack(side=tk.LEFT)
    tk.Radiobutton(add_frame, text="Student", variable=new_role, value="Student").pack(side=tk.LEFT)

    def do_add():
        if new_user.get() and new_pass.get():
            app_logic.add_user(new_user.get(), new_pass.get(), new_role.get())
            new_user.delete(0, tk.END); new_pass.delete(0, tk.END); refresh_users()
        else: messagebox.showwarning("Warning", "Enter Username and Password")
    tk.Button(add_frame, text="Add User", command=do_add).pack(side=tk.LEFT, padx=10)

    list_frame = tk.Frame(manage_frame)
    list_frame.pack(fill=tk.BOTH, expand=1, pady=5, padx=10)

    search_var = tk.StringVar()
    tk.Label(list_frame, text="Search:").pack(anchor="w")
    tk.Entry(list_frame, textvariable=search_var).pack(fill="x")

    lb = tk.Listbox(list_frame, selectmode=tk.SINGLE)
    lb.pack(fill=tk.BOTH, expand=1, pady=5)

    def refresh_users(*args):
        lb.delete(0, tk.END)
        s = search_var.get().lower()
        for u, info in app_logic.data["users"].items():
            if s in u.lower(): lb.insert(tk.END, f"{u} - {info['role']}")

    def do_delete():
        sel = lb.curselection()
        if not sel: return messagebox.showwarning("Warning", "Select a user")
        uname = lb.get(sel[0]).split(" - ")[0]
        if messagebox.askyesno("Confirm", f"Delete '{uname}'?"):
            app_logic.delete_user(uname); refresh_users()

    tk.Button(list_frame, text="Delete Selected User", command=do_delete, bg="red", fg="white").pack(pady=5)
    search_var.trace_add("write", refresh_users); refresh_users()

def do_login():
    global user, user_role
    ok, u, r = app_logic.check_login(e1.get(), e2.get(), role.get())
    if ok:
        user, user_role = u, r
        root.title(f"Campus Connect - {user}")
        top_label.config(text=f"Logged: {user} - {user_role}")
        if user_role == "Admin": manage_btn.pack(side=tk.LEFT, padx=5); delete_btn.pack(side="left", padx=5)
        else: manage_btn.pack_forget(); delete_btn.pack_forget()
        show(main_frame); showRes()
    else: messagebox.showerror("Error", "Wrong login")

def do_logout():
    global user, user_role
    user = user_role = ""
    e1.delete(0, tk.END); e2.delete(0, tk.END)
    show(login_frame)

def showRes(*args):
    list1.delete(0, tk.END)
    for i, r in enumerate(app_logic.get_resources(searchVar.get().lower(), filterCat.get())):
        list1.insert(tk.END, f"{i+1}. [{r[0]}] {r[1]}")

def saveRes():
    global selected_path
    if titleE.get() and selected_path:
        app_logic.add_resource(cat.get(), titleE.get(), selected_path, user)
        showRes(); addFrame.pack_forget(); titleE.delete(0, tk.END); selected_path = ""
        messagebox.showinfo("Success", "Resource saved!")
    else: messagebox.showwarning("Warning", "Enter Title and File")

def upload():
    global selected_path
    file = filedialog.askopenfilename(filetypes=[("PDF", "*.pdf"), ("DOCX", "*.docx"), ("All Files", "*.*")])
    if file:
        selected_path = file
        titleE.delete(0, tk.END)
        titleE.insert(0, os.path.splitext(os.path.basename(file))[0])

def deleteRes():
    sel = list1.curselection()
    if not sel: return messagebox.showwarning("Warning", "Select resource(s)")
    current = app_logic.get_resources(searchVar.get().lower(), filterCat.get())
    if messagebox.askyesno("Confirm", f"Delete {len(sel)} resource(s)?"):
        indexes = [app_logic.data["resources"].index(current[i]) for i in sel]
        for i in sorted(indexes, reverse=True): app_logic.delete_resource(i)
        showRes(); messagebox.showinfo("Success", "Deleted")

def openRes():
    sel = list1.curselection()
    if sel:
        current = app_logic.get_resources(searchVar.get().lower(), filterCat.get())
        path = app_logic.data["resources"][app_logic.data["resources"].index(current[sel[0]])][3]
        if path.startswith("http"): subprocess.call(["start", path], shell=True)
        else: os.startfile(path)
    else: messagebox.showwarning("Warning", "Select a resource")

def build_main():
    global main_frame, list1, searchVar, filterCat, titleE, cat, addFrame, delete_btn
    main_frame = tk.Frame(tab1)

    topFrame = tk.Frame(main_frame); topFrame.pack(fill="x", pady=5)
    searchVar = tk.StringVar(); filterCat = tk.StringVar(value="All")
    tk.Entry(topFrame, textvariable=searchVar).pack(side=tk.LEFT, padx=5)
    ttk.Combobox(topFrame, textvariable=filterCat, values=["All","PDFs","Notes"]).pack(side=tk.LEFT, padx=5)
    tk.Button(topFrame, text="Add", command=lambda: addFrame.pack(fill="x", pady=5)).pack(side=tk.LEFT, padx=5)

    list1 = tk.Listbox(main_frame, selectmode=tk.EXTENDED)
    list1.pack(fill=tk.BOTH, expand=1, pady=5)

    bottom = tk.Frame(main_frame); bottom.pack(fill="x", pady=10)
    tk.Button(bottom, text="Open", command=openRes).pack(side="left", padx=5)
    # tk.Button(bottom, text="Upload", command=upload).pack(side="left", padx=5) <-- REMOVED
    # tk.Button(bottom, text="Save", command=saveRes).pack(side="left", padx=5) <-- REMOVED
    delete_btn = tk.Button(bottom, text="Delete", command=deleteRes, bg="red", fg="white")
    delete_btn.pack(side="left", padx=5)
    tk.Button(bottom, text="Logout", command=do_logout).pack(side="right", padx=5)

    addFrame = tk.Frame(main_frame)
    cat = tk.StringVar(value="PDFs"); titleE = tk.Entry(addFrame)
    tk.Label(addFrame, text="Title:").pack(side=tk.LEFT); titleE.pack(side=tk.LEFT, padx=5)
    tk.Button(addFrame, text="File", command=upload).pack(side=tk.LEFT, padx=5) # File button ikkada matrame untundi
    tk.Button(addFrame, text="Save", command=saveRes).pack(side="left", padx=5) # Save button ikkada matrame untundi

    searchVar.trace_add("write", showRes)
    filterCat.trace_add("write", showRes)

top = tk.Frame(root)
top_label = tk.Label(top, text="Campus Connect")
top_label.pack(side="left", padx=10)
manage_btn = tk.Button(top, text="Manage Users", command=show_manage)

tabs = ttk.Notebook(root)
tab1 = tk.Frame(tabs)
tabs.add(tab1, text="Resources")

login_frame = tk.Frame(root)
box = tk.Frame(login_frame, bd=2, relief=tk.SOLID)
box.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
tk.Label(box, text="Campus Connect", font=("Arial", 14, "bold")).pack(pady=10)
tk.Label(box, text="Username").pack(); e1 = tk.Entry(box); e1.pack(pady=2)
tk.Label(box, text="Password").pack(); e2 = tk.Entry(box, show="*"); e2.pack(pady=2)
role = tk.StringVar(value="Student")
tk.Radiobutton(box, text="Admin", variable=role, value="Admin").pack(side=tk.LEFT, padx=10)
tk.Radiobutton(box, text="Student", variable=role, value="Student").pack(side=tk.LEFT, padx=10)
tk.Button(box, text="Login", command=do_login).pack(pady=10)

build_main()
show(login_frame)
root.mainloop()