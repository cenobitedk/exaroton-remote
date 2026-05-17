import sys
import threading
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import pystray

import config as cfg
import startup
from api import ExarotonAPI
from icon import make_icon

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

POLL_INTERVAL_MS = 8000

STATUS_STYLE = {
    "Online":     ("#2ecc71", "#1a7a43"),
    "Offline":    ("#95a5a6", "#444"),
    "Starting":   ("#f39c12", "#7a4e00"),
    "Stopping":   ("#e67e22", "#7a3e00"),
    "Restarting": ("#f39c12", "#7a4e00"),
    "Crashed":    ("#e74c3c", "#7a1a1a"),
}


def status_style(label: str):
    return STATUS_STYLE.get(label, ("#bdc3c7", "#444"))


class TokenDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("API Token")
        self.geometry("420x200")
        self.resizable(False, False)
        self.grab_set()
        self.result = None

        ctk.CTkLabel(self, text="Enter your exaroton API token:", font=("Segoe UI", 14)).pack(pady=(24, 8))
        self.entry = ctk.CTkEntry(self, width=340, show="*", placeholder_text="Token from account settings")
        self.entry.pack(pady=4)
        ctk.CTkButton(self, text="Save & Continue", command=self._save).pack(pady=16)
        self.entry.bind("<Return>", lambda _: self._save())

    def _save(self):
        token = self.entry.get().strip()
        if token:
            self.result = token
            self.destroy()


class ServerCard(ctk.CTkFrame):
    def __init__(self, parent, server_data: dict, api: ExarotonAPI, on_action):
        super().__init__(parent, corner_radius=10)
        self.server_id = server_data["id"]
        self.api = api
        self.on_action = on_action
        self._busy = False

        self.columnconfigure(1, weight=1)

        self.name_label = ctk.CTkLabel(self, text=server_data["name"],
                                        font=("Segoe UI", 15, "bold"), anchor="w")
        self.name_label.grid(row=0, column=0, columnspan=4, padx=16, pady=(12, 2), sticky="w")

        addr = server_data.get("address") or ""
        self.addr_label = ctk.CTkLabel(self, text=addr, font=("Segoe UI", 11),
                                        text_color="#888", anchor="w")
        self.addr_label.grid(row=1, column=0, columnspan=4, padx=16, pady=(0, 6), sticky="w")

        self.status_label = ctk.CTkLabel(self, text="…", font=("Segoe UI", 12, "bold"),
                                          width=90, corner_radius=6)
        self.status_label.grid(row=2, column=0, padx=16, pady=(0, 12), sticky="w")

        self.info_label = ctk.CTkLabel(self, text="", font=("Segoe UI", 11),
                                        text_color="#aaa", anchor="w")
        self.info_label.grid(row=2, column=1, padx=4, pady=(0, 12), sticky="w")

        self.start_btn = ctk.CTkButton(self, text="Start", width=70,
                                        fg_color="#27ae60", hover_color="#1e8449",
                                        command=self._start)
        self.start_btn.grid(row=2, column=2, padx=(4, 6), pady=(0, 12))

        self.stop_btn = ctk.CTkButton(self, text="Stop", width=70,
                                       fg_color="#c0392b", hover_color="#922b21",
                                       command=self._stop)
        self.stop_btn.grid(row=2, column=3, padx=(0, 16), pady=(0, 12))

        self.update(server_data)

    def update(self, server_data: dict):
        status_code = server_data.get("status", 0)
        label = self.api.status_label(status_code)
        fg, bg = status_style(label)
        self.status_label.configure(text=f"  {label}  ", text_color=fg, fg_color=bg)

        players = server_data.get("players") or {}
        count = players.get("count", 0)
        max_p = players.get("max", 0)
        sw = (server_data.get("software") or {})
        sw_name = sw.get("name") or ""
        sw_ver = sw.get("version") or ""

        parts = []
        if label == "Online":
            parts.append(f"Players: {count}/{max_p}")
        if sw_name:
            parts.append(f"{sw_name} {sw_ver}".strip())
        self.info_label.configure(text="  •  ".join(parts))

        can_start = status_code == 0
        can_stop = status_code == 1
        if not self._busy:
            self.start_btn.configure(state="normal" if can_start else "disabled")
            self.stop_btn.configure(state="normal" if can_stop else "disabled")

    def _set_busy(self, busy: bool):
        self._busy = busy
        state = "disabled" if busy else "normal"
        self.start_btn.configure(state=state)
        self.stop_btn.configure(state=state)

    def _start(self):
        self._set_busy(True)
        threading.Thread(target=self._do_action, args=("start",), daemon=True).start()

    def _stop(self):
        self._set_busy(True)
        threading.Thread(target=self._do_action, args=("stop",), daemon=True).start()

    def _do_action(self, action: str):
        try:
            if action == "start":
                self.api.start(self.server_id)
            else:
                self.api.stop(self.server_id)
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Error", str(e)))
            self.after(0, lambda: self._set_busy(False))
        else:
            self.after(500, self.on_action)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Exaroton Remote")
        self.geometry("520x600")
        self.minsize(460, 400)
        self.api: ExarotonAPI | None = None
        self.cards: dict[str, ServerCard] = {}
        self._poll_job = None
        self._tray_icon: pystray.Icon | None = None

        self._build_ui()
        self._setup_tray()
        # Intercept window close → hide to tray
        self.protocol("WM_DELETE_WINDOW", self._hide)
        self.after(100, self._init_api)

    # ------------------------------------------------------------------ UI

    def _build_ui(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        header = ctk.CTkFrame(self, height=54, corner_radius=0)
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=1)
        ctk.CTkLabel(header, text="Exaroton Remote",
                     font=("Segoe UI", 18, "bold")).grid(row=0, column=0, padx=20, pady=12, sticky="w")
        self.credit_label = ctk.CTkLabel(header, text="", font=("Segoe UI", 12), text_color="#aaa")
        self.credit_label.grid(row=0, column=1, padx=20, pady=12, sticky="e")

        self.scroll = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        self.scroll.grid(row=1, column=0, sticky="nsew", padx=12, pady=12)
        self.scroll.columnconfigure(0, weight=1)

        self.status_bar = ctk.CTkLabel(self, text="", font=("Segoe UI", 11), text_color="#666")
        self.status_bar.grid(row=2, column=0, pady=(0, 6))

    # ------------------------------------------------------------------ Tray

    def _setup_tray(self):
        icon_image = make_icon(64)

        menu = pystray.Menu(
            pystray.MenuItem("Open", self._show, default=True),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(
                "Start with Windows",
                self._toggle_startup,
                checked=lambda _: startup.is_enabled(),
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quit", self._quit),
        )
        self._tray_icon = pystray.Icon("ExarotonRemote", icon_image, "Exaroton Remote", menu)
        self._tray_icon.run_detached()

    def _show(self, *_):
        self.after(0, self._do_show)

    def _do_show(self):
        self.deiconify()
        self.lift()
        self.focus_force()

    def _hide(self):
        self.withdraw()

    def _toggle_startup(self, *_):
        startup.toggle()

    def _quit(self, *_):
        if self._poll_job:
            self.after_cancel(self._poll_job)
        if self._tray_icon:
            self._tray_icon.stop()
        self.after(0, self.destroy)

    # ------------------------------------------------------------------ API

    def _init_api(self):
        token = cfg.load_token()
        if not token:
            self._do_show()
            token = self._prompt_token()
        if not token:
            self._quit()
            return
        self.api = ExarotonAPI(token)
        self._refresh()

    def _prompt_token(self) -> str | None:
        dlg = TokenDialog(self)
        self.wait_window(dlg)
        if dlg.result:
            cfg.save_token(dlg.result)
        return dlg.result

    def _refresh(self):
        if self._poll_job:
            self.after_cancel(self._poll_job)
        threading.Thread(target=self._fetch_all, daemon=True).start()

    def _fetch_all(self):
        try:
            account = self.api.account()
            servers = self.api.servers()
            self.after(0, lambda: self._update_ui(account, servers))
        except Exception as e:
            self.after(0, lambda: self.status_bar.configure(text=f"Error: {e}"))
        finally:
            self._poll_job = self.after(POLL_INTERVAL_MS, self._refresh)

    def _update_ui(self, account: dict, servers: list):
        credits = account.get("credits", 0)
        self.credit_label.configure(text=f"{credits:.0f} credits")

        existing_ids = set(self.cards.keys())
        new_ids = {s["id"] for s in servers}

        for sid in existing_ids - new_ids:
            self.cards[sid].grid_forget()
            self.cards[sid].destroy()
            del self.cards[sid]

        for i, srv in enumerate(servers):
            sid = srv["id"]
            if sid in self.cards:
                self.cards[sid].update(srv)
            else:
                card = ServerCard(self.scroll, srv, self.api, self._refresh)
                card.grid(row=i, column=0, sticky="ew", pady=6, padx=4)
                self.cards[sid] = card

        self.status_bar.configure(text=f"Last updated: {self._now()}")

    @staticmethod
    def _now() -> str:
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")


def main():
    # On Windows, hide the console window when running as a frozen exe
    if sys.platform == "win32" and getattr(sys, "frozen", False):
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

    app = App()
    # Start hidden — tray icon is always present; double-click or "Open" to show
    app.withdraw()
    app.mainloop()


if __name__ == "__main__":
    main()
