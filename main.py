import json
import os
import tkinter as tk
from tkinter import messagebox

SAVE_FILE = "account.json"
ACCOUNTS_FILE = "accounts.json"
STYLE_FILE = "style.css"

DEFAULT_ACCOUNT = {
    "name": "Owner jj",
    "money": 0,
    "level": 1,
    "rebirths": 0,
}

STYLE = {
    "background": "#090d16",
    "panel": "#111827",
    "button": "#2563eb",
    "button_text": "#ffffff",
    "text": "#ffffff",
    "console": "#05070b",
}


def load_css():
    if not os.path.exists(STYLE_FILE):
        return

    try:
        with open(STYLE_FILE, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line or ":" not in line:
                    continue
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip().rstrip(";")
                if key in STYLE:
                    STYLE[key] = value
    except (OSError, UnicodeError):
        pass


def clean_account(data, name=None):
    result = DEFAULT_ACCOUNT.copy()
    if isinstance(data, dict):
        result.update(data)
    result["name"] = name or str(result.get("name") or DEFAULT_ACCOUNT["name"])

    for key in ("money", "level", "rebirths"):
        try:
            result[key] = max(0, int(result[key]))
        except (TypeError, ValueError):
            result[key] = DEFAULT_ACCOUNT[key]

    return result


def load_accounts():
    data = {}
    if os.path.exists(ACCOUNTS_FILE):
        try:
            with open(ACCOUNTS_FILE, "r", encoding="utf-8") as file:
                loaded = json.load(file)
                if isinstance(loaded, dict):
                    data = loaded
        except (OSError, json.JSONDecodeError):
            pass

    accounts = {}
    for name, saved_account in data.items():
        if isinstance(name, str) and name.strip():
            accounts[name] = clean_account(saved_account, name)

    accounts.setdefault("Owner jj", clean_account(DEFAULT_ACCOUNT, "Owner jj"))
    return accounts


def save_accounts():
    with open(ACCOUNTS_FILE, "w", encoding="utf-8") as file:
        json.dump(accounts, file, indent=4)


def load_current_account(accounts):
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as file:
                saved = clean_account(json.load(file))
                return accounts.get(saved["name"], saved)
        except (OSError, json.JSONDecodeError):
            pass
    return accounts["Owner jj"].copy()


def save_current_account():
    accounts[account["name"]] = account.copy()
    save_accounts()
    with open(SAVE_FILE, "w", encoding="utf-8") as file:
        json.dump(account, file, indent=4)


load_css()
accounts = load_accounts()
account = load_current_account(accounts)
accounts[account["name"]] = account.copy()
save_accounts()
save_current_account()

root = tk.Tk()
root.title("MoneyGame")
root.geometry("430x700")
root.configure(bg=STYLE["background"])
root.resizable(False, False)


def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()


def make_button(parent, text, command, width=22):
    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=STYLE["button"],
        fg=STYLE["button_text"],
        activebackground=STYLE["button"],
        activeforeground=STYLE["button_text"],
        font=("Arial", 16, "bold"),
        width=width,
        height=2,
        relief="flat",
        bd=0,
    )


def loading_screen():
    clear_screen()
    tk.Label(root, text="MONEYGAME", bg=STYLE["background"], fg=STYLE["text"], font=("Arial", 30, "bold")).pack(pady=(180, 20))
    tk.Label(root, text="Loading MoneyGame...", bg=STYLE["background"], fg=STYLE["text"], font=("Arial", 14)).pack(pady=10)

    progress = tk.Canvas(root, width=300, height=20, bg=STYLE["console"], highlightthickness=0)
    progress.pack(pady=20)
    bar = progress.create_rectangle(0, 0, 0, 20, fill=STYLE["button"], outline="")

    def animate(value=0):
        if value <= 300:
            progress.coords(bar, 0, 0, value, 20)
            root.after(12, lambda: animate(value + 5))
        else:
            root.after(300, main_menu)

    animate()


def main_menu():
    clear_screen()
    tk.Label(root, text="MONEYGAME", bg=STYLE["background"], fg=STYLE["text"], font=("Arial", 32, "bold")).pack(pady=(70, 10))
    tk.Label(root, text=f"Account: {account['name']}", bg=STYLE["background"], fg=STYLE["text"], font=("Arial", 14)).pack(pady=10)
    make_button(root, "▶ Play", game_screen).pack(pady=12)
    make_button(root, "⚙ Settings", settings_screen).pack(pady=12)
    make_button(root, "👤 Account", account_screen).pack(pady=12)
    make_button(root, "✕ Exit", root.destroy).pack(pady=12)


def game_screen():
    clear_screen()
    tk.Label(root, text="MONEYGAME", bg=STYLE["background"], fg=STYLE["text"], font=("Arial", 27, "bold")).pack(pady=20)
    account_label = tk.Label(root, text="", bg=STYLE["background"], fg=STYLE["text"], font=("Arial", 14))
    account_label.pack()
    money_label = tk.Label(root, text="", bg=STYLE["background"], fg=STYLE["text"], font=("Arial", 21, "bold"))
    money_label.pack(pady=8)
    level_label = tk.Label(root, text="", bg=STYLE["background"], fg=STYLE["text"], font=("Arial", 15))
    level_label.pack()
    rebirth_label = tk.Label(root, text="", bg=STYLE["background"], fg=STYLE["text"], font=("Arial", 14))
    rebirth_label.pack(pady=5)

    frame = tk.Frame(root, bg=STYLE["panel"], bd=2, relief="ridge")
    frame.pack(padx=20, pady=15, fill="x")
    tk.Label(frame, text="CONSOLE", bg=STYLE["panel"], fg=STYLE["text"], font=("Arial", 14, "bold")).pack(pady=8)
    console = tk.Text(frame, bg=STYLE["console"], fg=STYLE["text"], insertbackground="white", font=("Courier New", 11), height=6)
    console.pack(padx=8, pady=8, fill="x")
    console.insert("end", "Worker (0 level)\nPage (unsafe) (level 100)\n\nACCESS: Page (unsafe)\n")
    console.config(state="disabled")

    def update():
        account_label.config(text=f"Account: {account['name']}")
        money_label.config(text=f"Money: ${account['money']}")
        level_label.config(text=f"Level: {account['level']}")
        rebirth_label.config(text=f"Rebirths: {account['rebirths']}")
        save_current_account()

    def earn_money():
        account["money"] += 10
        update()

    def level_up():
        cost = account["level"] * 100
        if account["money"] < cost:
            messagebox.showwarning("Not enough money", f"You need ${cost} to level up.")
            return
        account["money"] -= cost
        account["level"] += 1
        update()

    def rebirth():
        if account["level"] < 10:
            messagebox.showwarning("Rebirth", "You need level 10 to rebirth.")
            return
        account["money"] = 0
        account["level"] = 1
        account["rebirths"] += 1
        update()

    make_button(root, "💰 Earn money", earn_money, 18).pack(pady=4)
    make_button(root, "⬆ Level up", level_up, 18).pack(pady=4)
    make_button(root, "🔄 Rebirth", rebirth, 18).pack(pady=4)
    tk.Button(root, text="← Back", command=main_menu, bg=STYLE["panel"], fg=STYLE["text"], font=("Arial", 12, "bold"), relief="flat").pack(pady=10)
    update()


def settings_screen():
    clear_screen()
    tk.Label(root, text="⚙ SETTINGS", bg=STYLE["background"], fg=STYLE["text"], font=("Arial", 27, "bold")).pack(pady=(70, 30))
    tk.Label(root, text="MoneyGame Settings\n\nMain file: main.py\nUI colors: style.css\nHardware layer: hardware.java", bg=STYLE["background"], fg=STYLE["text"], font=("Arial", 14), justify="center").pack(pady=20)
    make_button(root, "← Back", main_menu).pack(pady=30)


def account_screen():
    clear_screen()
    tk.Label(root, text="👤 ACCOUNT", bg=STYLE["background"], fg=STYLE["text"], font=("Arial", 27, "bold")).pack(pady=(45, 20))
    tk.Label(root, text=f"Current account:\n\n{account['name']}", bg=STYLE["panel"], fg=STYLE["text"], font=("Arial", 17, "bold"), width=25, height=4).pack(pady=15)

    make_button(root, "+ Create Account", create_account).pack(pady=8)
    if len(accounts) > 1:
        make_button(root, "Switch Account", switch_account).pack(pady=8)
    make_button(root, "← Back", main_menu).pack(pady=8)


def create_account():
    popup = tk.Toplevel(root)
    popup.title("Create Account")
    popup.geometry("360x240")
    popup.configure(bg=STYLE["background"])
    popup.resizable(False, False)
    tk.Label(popup, text="Create Fake Account", bg=STYLE["background"], fg=STYLE["text"], font=("Arial", 18, "bold")).pack(pady=20)
    tk.Label(popup, text="Account name:", bg=STYLE["background"], fg=STYLE["text"], font=("Arial", 13)).pack()
    entry = tk.Entry(popup, font=("Arial", 14), width=25)
    entry.pack(pady=10)

    def create():
        name = entry.get().strip()
        if not name:
            messagebox.showwarning("Account", "Enter a name.", parent=popup)
            return
        if name in accounts:
            messagebox.showerror("Name Taken", "That account name is already taken.", parent=popup)
            return
        accounts[name] = clean_account({}, name)
        switch_to(name)
        save_accounts()
        popup.destroy()
        account_screen()

    make_button(popup, "Create", create, 15).pack(pady=15)


def switch_to(name):
    global account
    save_current_account()
    account = accounts[name].copy()
    save_current_account()


def switch_account():
    popup = tk.Toplevel(root)
    popup.title("Switch Account")
    popup.geometry("320x300")
    popup.configure(bg=STYLE["background"])
    tk.Label(popup, text="Choose an account", bg=STYLE["background"], fg=STYLE["text"], font=("Arial", 16, "bold")).pack(pady=15)

    for name in sorted(accounts):
        def choose(selected=name):
            switch_to(selected)
            popup.destroy()
            account_screen()
        make_button(popup, name, choose, 18).pack(pady=4)


loading_screen()
root.mainloop()
