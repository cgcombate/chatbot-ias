import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk, messagebox
import base64
import platform


def _ui_family():
    if platform.system() == "Darwin":
        return "SF Pro Text"
    if platform.system() == "Windows":
        return "Segoe UI Variable Text" if _font_exists("Segoe UI Variable Text") else "Segoe UI"
    return "Ubuntu" if _font_exists("Ubuntu") else "Segoe UI"


def _display_family():
    if platform.system() == "Darwin":
        return "SF Pro Display"
    return _ui_family()


def _mono_family():
    if platform.system() == "Darwin":
        return "SF Mono"
    for name in ("Cascadia Mono", "Consolas", "Courier New"):
        if _font_exists(name):
            return name
    return "Consolas"


def _font_exists(family):
    return family in tkfont.families()


# Defer font check until Tk root exists — families() needs default root
_ui_family_cached = None
_display_family_cached = None
_mono_family_cached = None


def ui_font(size=13, weight="normal"):
    global _ui_family_cached
    if _ui_family_cached is None:
        _ui_family_cached = _ui_family()
    if weight == "normal":
        return (_ui_family_cached, size)
    return (_ui_family_cached, size, weight)


def display_font(size=22, weight="bold"):
    global _display_family_cached
    if _display_family_cached is None:
        _display_family_cached = _display_family()
    if weight == "normal":
        return (_display_family_cached, size)
    return (_display_family_cached, size, weight)


def mono_font(size=12):
    global _mono_family_cached
    if _mono_family_cached is None:
        _mono_family_cached = _mono_family()
    return (_mono_family_cached, size)


def caesar_cipher(text, shift, decrypt=False):
    if decrypt:
        shift = -shift
    result = ""
    for char in text:
        if char.isalpha():
            start = ord("A") if char.isupper() else ord("a")
            result += chr((ord(char) - start + shift) % 26 + start)
        else:
            result += char
    return result


class ProfessionalCryptoDemo:
    # Apple-inspired palette (light shell)
    BG_WINDOW = "#F5F5F7"
    BG_CARD = "#FFFFFF"
    BG_HEADER = "#FAFAFA"
    BORDER = "#D2D2D7"
    TEXT_PRIMARY = "#1D1D1F"
    TEXT_SECONDARY = "#6E6E73"
    ACCENT = "#007AFF"
    ACCENT_HOVER = "#0066D6"
    DESTRUCTIVE = "#FF3B30"
    SUCCESS = "#34C759"
    LOG_BG = "#1C1C1E"
    LOG_FG = "#30D158"
    RECV_BG = "#FFFFFF"
    RECV_FG = "#1D1D1F"

    def __init__(self, root):
        self.root = root
        self.root.title("SecureChat Protocol Demo")
        self.root.geometry("880x640")
        self.root.minsize(720, 520)
        self.root.configure(bg=self.BG_WINDOW)

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("App.TFrame", background=self.BG_WINDOW)
        style.configure("Card.TFrame", background=self.BG_CARD)
        style.configure(
            "App.TLabel",
            background=self.BG_WINDOW,
            foreground=self.TEXT_PRIMARY,
            font=ui_font(13),
        )
        style.configure(
            "Muted.TLabel",
            background=self.BG_WINDOW,
            foreground=self.TEXT_SECONDARY,
            font=ui_font(12),
        )
        style.configure(
            "Card.TLabel",
            background=self.BG_CARD,
            foreground=self.TEXT_PRIMARY,
            font=ui_font(13),
        )
        style.configure(
            "CardMuted.TLabel",
            background=self.BG_CARD,
            foreground=self.TEXT_SECONDARY,
            font=ui_font(11),
        )
        style.configure(
            "Section.TLabel",
            background=self.BG_CARD,
            foreground=self.TEXT_SECONDARY,
            font=ui_font(11, "bold"),
        )
        style.configure(
            "TCombobox",
            fieldbackground=self.BG_CARD,
            background=self.BG_CARD,
            foreground=self.TEXT_PRIMARY,
            arrowcolor=self.TEXT_SECONDARY,
            bordercolor=self.BORDER,
            lightcolor=self.BG_CARD,
            darkcolor=self.BORDER,
            font=ui_font(12),
        )
        style.map(
            "TCombobox",
            fieldbackground=[("readonly", self.BG_CARD)],
            selectbackground=[("readonly", self.ACCENT)],
            selectforeground=[("readonly", "#FFFFFF")],
        )
        style.configure(
            "TEntry",
            fieldbackground=self.BG_CARD,
            foreground=self.TEXT_PRIMARY,
            bordercolor=self.BORDER,
            lightcolor=self.BG_CARD,
            darkcolor=self.BORDER,
            insertcolor=self.TEXT_PRIMARY,
            font=ui_font(12),
        )

        # --- Header ---
        header_wrap = tk.Frame(root, bg=self.BG_HEADER, highlightthickness=1, highlightbackground=self.BORDER)
        header_wrap.pack(fill=tk.X)
        header_inner = tk.Frame(header_wrap, bg=self.BG_HEADER, padx=28, pady=18)
        header_inner.pack(fill=tk.X)
        tk.Label(
            header_inner,
            text="Cryptography Protocol Analyzer",
            bg=self.BG_HEADER,
            fg=self.TEXT_PRIMARY,
            font=display_font(22, "bold"),
        ).pack(anchor=tk.W)
        tk.Label(
            header_inner,
            text="Symmetric and asymmetric flows in one place.",
            bg=self.BG_HEADER,
            fg=self.TEXT_SECONDARY,
            font=ui_font(13),
        ).pack(anchor=tk.W, pady=(4, 0))

        main_container = ttk.Frame(root, style="App.TFrame", padding=(28, 24))
        main_container.pack(fill=tk.BOTH, expand=True)

        # Card: controls + visualization
        card = tk.Frame(
            main_container,
            bg=self.BG_CARD,
            highlightthickness=1,
            highlightbackground=self.BORDER,
        )
        card.pack(fill=tk.BOTH, expand=True)

        card_inner = tk.Frame(card, bg=self.BG_CARD, padx=24, pady=22)
        card_inner.pack(fill=tk.BOTH, expand=True)

        # --- Left: controls ---
        left_panel = tk.Frame(card_inner, bg=self.BG_CARD, width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 28))
        left_panel.pack_propagate(False)

        ttk.Label(left_panel, text="PROTOCOL", style="Section.TLabel").pack(anchor=tk.W)
        self.mode = tk.StringVar(value="Symmetric")
        mode_cb = ttk.Combobox(
            left_panel,
            textvariable=self.mode,
            values=["Symmetric", "Asymmetric"],
            state="readonly",
            width=28,
        )
        mode_cb.pack(fill=tk.X, pady=(6, 16))
        mode_cb.bind("<<ComboboxSelected>>", self.toggle_mode)

        self.key_label = ttk.Label(left_panel, text="Shared secret (shift)", style="Section.TLabel")
        self.key_label.pack(anchor=tk.W)
        self.key_entry = ttk.Entry(left_panel, font=ui_font(12))
        self.key_entry.insert(0, "3")
        self.key_entry.pack(fill=tk.X, pady=(6, 16))

        ttk.Label(left_panel, text="Message", style="Section.TLabel").pack(anchor=tk.W)
        self.msg_input = tk.Text(
            left_panel,
            height=5,
            width=32,
            font=mono_font(12),
            bg=self.BG_WINDOW,
            fg=self.TEXT_PRIMARY,
            insertbackground=self.TEXT_PRIMARY,
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground=self.BORDER,
            highlightcolor=self.ACCENT,
            padx=10,
            pady=10,
            wrap=tk.WORD,
        )
        self.msg_input.pack(fill=tk.X, pady=(6, 18))

        self.send_btn = tk.Button(
            left_panel,
            text="Encrypt & send",
            bg=self.ACCENT,
            fg="#FFFFFF",
            activebackground=self.ACCENT_HOVER,
            activeforeground="#FFFFFF",
            font=ui_font(13, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=16,
            pady=10,
            command=self.process_message,
        )
        self.send_btn.pack(fill=tk.X)

        # Divider
        sep = ttk.Separator(card_inner, orient=tk.VERTICAL)
        sep.pack(side=tk.LEFT, fill=tk.Y, padx=0)

        # --- Right: logs ---
        right_panel = tk.Frame(card_inner, bg=self.BG_CARD)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        ttk.Label(
            right_panel,
            text="Network intercept",
            style="Section.TLabel",
            foreground=self.DESTRUCTIVE,
        ).pack(anchor=tk.W)
        ttk.Label(
            right_panel,
            text="What an eavesdropper would see on the wire.",
            style="CardMuted.TLabel",
        ).pack(anchor=tk.W, pady=(0, 6))

        self.network_log = tk.Text(
            right_panel,
            height=10,
            bg=self.LOG_BG,
            fg=self.LOG_FG,
            font=mono_font(12),
            state="disabled",
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground=self.BORDER,
            padx=12,
            pady=12,
            wrap=tk.WORD,
        )
        self.network_log.pack(fill=tk.BOTH, expand=False, pady=(0, 18))

        ttk.Label(
            right_panel,
            text="Recipient",
            style="Section.TLabel",
            foreground=self.ACCENT,
        ).pack(anchor=tk.W)
        ttk.Label(
            right_panel,
            text="Decrypted view at the destination.",
            style="CardMuted.TLabel",
        ).pack(anchor=tk.W, pady=(0, 6))

        self.recipient_view = tk.Text(
            right_panel,
            height=10,
            bg=self.BG_WINDOW,
            fg=self.RECV_FG,
            font=ui_font(13),
            state="disabled",
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground=self.BORDER,
            padx=12,
            pady=12,
            wrap=tk.WORD,
        )
        self.recipient_view.pack(fill=tk.BOTH, expand=True)

    def toggle_mode(self, event=None):
        if self.mode.get() == "Asymmetric":
            self.key_label.config(text="Public key (simulated)")
            self.key_entry.delete(0, tk.END)
            self.key_entry.insert(0, "RSA_PUB_8821")
            self.key_entry.config(state="disabled")
        else:
            self.key_label.config(text="Shared secret (shift)")
            self.key_entry.config(state="normal")

    def process_message(self):
        raw_text = self.msg_input.get("1.0", tk.END).strip()
        if not raw_text:
            return

        if self.mode.get() == "Symmetric":
            try:
                key = int(self.key_entry.get())
                encrypted = caesar_cipher(raw_text, key)
                decrypted = caesar_cipher(encrypted, key, decrypt=True)
                protocol_info = f"[PROTOCOL: AES-SIM / KEY: {key}]"
            except Exception:
                messagebox.showerror("Invalid key", "Symmetric key must be a number.")
                return
        else:
            encrypted = base64.b64encode(raw_text.encode()).decode()
            decrypted = base64.b64decode(encrypted.encode()).decode()
            protocol_info = "[PROTOCOL: RSA-2048 / PKI-AUTH]"

        self.update_box(self.network_log, f"{protocol_info}\nCIPHERTEXT: {encrypted}\n\n", self.LOG_FG)
        self.update_box(self.recipient_view, f"From sender: {decrypted}\n", self.RECV_FG)
        self.msg_input.delete("1.0", tk.END)

    def update_box(self, box, text, color):
        box.config(state="normal", fg=color)
        box.insert(tk.END, text)
        box.see(tk.END)
        box.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = ProfessionalCryptoDemo(root)
    root.mainloop()
