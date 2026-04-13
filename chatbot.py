import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk, messagebox, filedialog, simpledialog
import base64
import platform


def _font_exists(family):
    return family in tkfont.families()


def _ui_family():
    if platform.system() == "Darwin":
        return "SF Pro Text"
    if platform.system() == "Windows":
        return "Segoe UI Variable Text" if _font_exists("Segoe UI Variable Text") else "Segoe UI"
    return "Ubuntu" if _font_exists("Ubuntu") else "Segoe UI"


def _mono_family():
    if platform.system() == "Darwin":
        return "SF Mono"
    for name in ("Cascadia Mono", "Consolas", "Courier New"):
        if _font_exists(name):
            return name
    return "Consolas"


_ui_family_cached = None
_mono_family_cached = None


def ui_font(size=10, weight="normal"):
    global _ui_family_cached
    if _ui_family_cached is None:
        _ui_family_cached = _ui_family()
    if weight == "normal":
        return (_ui_family_cached, size)
    return (_ui_family_cached, size, weight)


def mono_font(size=9):
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
    NAVY = "#1E3D63"
    BLUE = "#0E7AE6"
    BG = "#ECEDEF"
    PANEL = "#F7F8FA"
    WHITE = "#FFFFFF"
    BORDER = "#CDD3DB"
    TEXT = "#1F2937"
    MUTED = "#6B7280"

    def __init__(self, root):
        self.root = root
        self.root.title("CryptoChat Lab")
        self.root.geometry("1280x820")
        self.root.minsize(1100, 720)
        self.root.configure(bg=self.BG)
        self.mode = tk.StringVar(value="Symmetric")
        self.status_var = tk.StringVar(value="Ready")
        self.current_tab = "Chat Workspace"
        self.top_tab_buttons = {}
        self.views = {}

        self.build_top_bar()
        self.build_layout()
        self.toggle_mode()

    def build_top_bar(self):
        top = tk.Frame(self.root, bg=self.NAVY, height=56)
        top.pack(fill=tk.X)
        top.pack_propagate(False)

        left = tk.Frame(top, bg=self.NAVY)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=12)
        tk.Label(left, text="●", fg="#3AB4F2", bg=self.NAVY, font=ui_font(10, "bold")).pack(side=tk.LEFT, padx=(0, 6))
        tk.Label(left, text="CryptoChat Lab", fg="white", bg=self.NAVY, font=ui_font(12, "bold")).pack(side=tk.LEFT)

        tabs = ("Chat Workspace", "Encryption Mode Selector", "Decryption Panel", "Message Receive Pane")
        for label in tabs:
            btn = tk.Button(
                top,
                text=label,
                bg=self.BLUE,
                fg="white",
                relief=tk.FLAT,
                font=ui_font(8, "bold"),
                padx=8,
                pady=2,
                cursor="hand2",
                command=lambda n=label: self.on_tab_clicked(n),
            )
            btn.pack(side=tk.LEFT, padx=4)
            self.top_tab_buttons[label] = btn

        tk.Button(
            top,
            text="New Session",
            bg=self.BLUE,
            fg="white",
            relief=tk.FLAT,
            font=ui_font(8, "bold"),
            cursor="hand2",
            padx=10,
            pady=2,
            command=self.new_session,
        ).pack(side=tk.RIGHT, padx=12)

    def build_layout(self):
        body = tk.Frame(self.root, bg=self.BG, padx=14, pady=14)
        body.pack(fill=tk.BOTH, expand=True)
        body.grid_columnconfigure(1, weight=1)
        body.grid_rowconfigure(0, weight=1)

        self.build_left_nav(body)
        self.build_center_workspace(body)
        self.build_right_panel(body)

    def build_left_nav(self, parent):
        left = tk.Frame(parent, bg=self.PANEL, width=190, highlightthickness=1, highlightbackground=self.BORDER)
        left.grid(row=0, column=0, sticky="ns", padx=(0, 10))
        left.grid_propagate(False)

        items = [
            "Chat Workspace",
            "Encryption Mode Selector",
            "Decryption Panel",
            "Message Receive Pane",
            "Settings & Help",
        ]
        for i, name in enumerate(items):
            bg = "#DCEBFB" if i == 0 else self.PANEL
            tk.Label(left, text=name, bg=bg, fg=self.TEXT, font=ui_font(9), anchor="w", padx=10, pady=8).pack(fill=tk.X, padx=10, pady=(10 if i == 0 else 2, 0))

        tk.Frame(left, bg=self.BORDER, height=1).pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=8)
        tk.Label(left, text="Session\nActive: AES-256-CBC", bg=self.PANEL, fg=self.MUTED, justify="left", font=ui_font(8)).pack(side=tk.BOTTOM, anchor="w", padx=10, pady=(0, 8))

    def build_center_workspace(self, parent):
        center = tk.Frame(parent, bg=self.PANEL, highlightthickness=1, highlightbackground=self.BORDER)
        center.grid(row=0, column=1, sticky="nsew", padx=(0, 10))
        center.grid_columnconfigure(0, weight=1)
        center.grid_rowconfigure(1, weight=1)

        hdr = tk.Frame(center, bg=self.PANEL, pady=10, padx=12)
        hdr.grid(row=0, column=0, sticky="ew")
        self.header_title = tk.Label(hdr, text="Secure Chat • Project Aurora", bg=self.PANEL, fg=self.TEXT, font=ui_font(17, "bold"))
        self.header_title.pack(side=tk.LEFT)
        tk.Button(hdr, text="Clear History", bg=self.WHITE, fg=self.TEXT, relief=tk.FLAT, font=ui_font(8), cursor="hand2", command=self.clear_history).pack(side=tk.RIGHT, padx=4)
        tk.Button(hdr, text="Export Transcript", bg=self.BLUE, fg="white", relief=tk.FLAT, font=ui_font(8, "bold"), cursor="hand2", command=self.export_transcript).pack(side=tk.RIGHT, padx=4)

        self.content_host = tk.Frame(center, bg=self.PANEL, padx=12, pady=4)
        self.content_host.grid(row=1, column=0, sticky="nsew")
        self.content_host.grid_columnconfigure(0, weight=1)
        self.content_host.grid_rowconfigure(0, weight=1)

        self.build_workspace_view()
        self.build_encryption_view()
        self.build_decryption_view()
        self.build_receiver_view()

        footer = tk.Frame(center, bg=self.PANEL, pady=10, padx=12)
        footer.grid(row=2, column=0, sticky="ew")
        tk.Label(footer, text="Mode", bg=self.PANEL, fg=self.MUTED, font=ui_font(9, "bold")).pack(side=tk.LEFT, padx=(0, 6))
        mode_combo = ttk.Combobox(footer, textvariable=self.mode, values=["Symmetric", "Asymmetric"], state="readonly", width=18)
        mode_combo.pack(side=tk.LEFT, padx=8)
        mode_combo.bind("<<ComboboxSelected>>", self.toggle_mode)

        composer = tk.Frame(center, bg=self.PANEL, padx=12, pady=8)
        composer.grid(row=3, column=0, sticky="ew")
        self.msg_input = tk.Text(
            composer,
            height=2,
            bg=self.WHITE,
            fg=self.TEXT,
            font=mono_font(10),
            wrap=tk.WORD,
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground=self.BORDER,
            padx=8,
            pady=8,
        )
        self.msg_input.pack(side=tk.LEFT, fill=tk.X, expand=True)

        action_bar = tk.Frame(composer, bg=self.PANEL)
        action_bar.pack(side=tk.LEFT, padx=(8, 0))
        self.send_btn = tk.Button(action_bar, text="Send", command=self.process_message, bg=self.BLUE, fg="white", relief=tk.FLAT, font=ui_font(9, "bold"), cursor="hand2", padx=14)
        self.send_btn.pack(side=tk.LEFT, padx=2)
        tk.Button(action_bar, text="Clear", command=lambda: self.msg_input.delete("1.0", tk.END), bg=self.WHITE, fg=self.TEXT, relief=tk.FLAT, font=ui_font(8), cursor="hand2").pack(side=tk.LEFT, padx=2)
        tk.Label(center, textvariable=self.status_var, bg=self.PANEL, fg=self.MUTED, font=ui_font(8), anchor="w").grid(row=4, column=0, sticky="ew", padx=12, pady=(0, 8))
        self.show_view("Chat Workspace")

    def _make_view_frame(self, key):
        frame = tk.Frame(self.content_host, bg=self.PANEL)
        frame.grid(row=0, column=0, sticky="nsew")
        self.views[key] = frame
        return frame

    def build_workspace_view(self):
        convo = self._make_view_frame("Chat Workspace")
        convo.grid_columnconfigure(0, weight=1)
        self.network_log = self.create_chat_card(convo, "SecureBot", "Alg: AES-256-CBC", "#F3F4F6")
        self.recipient_view = self.create_chat_card(convo, "You", "Alg: RSA-2048", "#FFFFFF")
        self.preview_box = self.create_chat_card(convo, "You • Preview", "Alg: ChaCha20", "#DCEBFB")

    def build_encryption_view(self):
        panel = self._make_view_frame("Encryption Mode Selector")
        panel.grid_columnconfigure(0, weight=1)
        card = tk.Frame(panel, bg=self.WHITE, highlightthickness=1, highlightbackground=self.BORDER, padx=14, pady=12)
        card.pack(fill=tk.X)
        tk.Label(card, text="Encryption Mode Selector", bg=self.WHITE, fg=self.TEXT, font=ui_font(12, "bold")).pack(anchor="w")
        tk.Label(card, text="Choose algorithm profile for outgoing messages.", bg=self.WHITE, fg=self.MUTED, font=ui_font(9)).pack(anchor="w", pady=(2, 10))
        tk.Radiobutton(card, text="Symmetric (AES-sim)", variable=self.mode, value="Symmetric", command=self.toggle_mode, bg=self.WHITE, fg=self.TEXT, font=ui_font(9), selectcolor=self.WHITE).pack(anchor="w")
        tk.Radiobutton(card, text="Asymmetric (RSA-sim)", variable=self.mode, value="Asymmetric", command=self.toggle_mode, bg=self.WHITE, fg=self.TEXT, font=ui_font(9), selectcolor=self.WHITE).pack(anchor="w")
        tk.Label(card, text="Key is managed from the right-side panel.", bg=self.WHITE, fg=self.MUTED, font=ui_font(8)).pack(anchor="w", pady=(10, 0))

    def build_decryption_view(self):
        panel = self._make_view_frame("Decryption Panel")
        panel.grid_columnconfigure(0, weight=1)
        card = tk.Frame(panel, bg=self.WHITE, highlightthickness=1, highlightbackground=self.BORDER, padx=14, pady=12)
        card.pack(fill=tk.BOTH, expand=True)
        tk.Label(card, text="Decryption Panel", bg=self.WHITE, fg=self.TEXT, font=ui_font(12, "bold")).pack(anchor="w")
        tk.Label(card, text="Paste ciphertext then decrypt with current mode/key.", bg=self.WHITE, fg=self.MUTED, font=ui_font(9)).pack(anchor="w", pady=(2, 8))
        self.decrypt_input = tk.Text(card, height=6, bg=self.WHITE, fg=self.TEXT, relief=tk.FLAT, highlightthickness=1, highlightbackground=self.BORDER, font=mono_font(9), padx=8, pady=8)
        self.decrypt_input.pack(fill=tk.X)
        tk.Button(card, text="Decrypt", command=self.decrypt_message, bg=self.BLUE, fg="white", relief=tk.FLAT, font=ui_font(9, "bold"), cursor="hand2").pack(anchor="w", pady=8)
        self.decrypt_output = tk.Text(card, height=8, state="disabled", bg="#F8FAFC", fg=self.TEXT, relief=tk.FLAT, highlightthickness=1, highlightbackground=self.BORDER, font=mono_font(9), padx=8, pady=8)
        self.decrypt_output.pack(fill=tk.BOTH, expand=True)

    def build_receiver_view(self):
        panel = self._make_view_frame("Message Receive Pane")
        panel.grid_columnconfigure(0, weight=1)
        card = tk.Frame(panel, bg=self.WHITE, highlightthickness=1, highlightbackground=self.BORDER, padx=14, pady=12)
        card.pack(fill=tk.BOTH, expand=True)
        tk.Label(card, text="Message Receive Pane", bg=self.WHITE, fg=self.TEXT, font=ui_font(12, "bold")).pack(anchor="w")
        tk.Label(card, text="Captured encrypted payloads arrive here.", bg=self.WHITE, fg=self.MUTED, font=ui_font(9)).pack(anchor="w", pady=(2, 8))
        self.incoming_list = tk.Listbox(card, height=10, font=mono_font(9), bg=self.WHITE, fg=self.TEXT, relief=tk.FLAT, highlightthickness=1, highlightbackground=self.BORDER)
        self.incoming_list.pack(fill=tk.BOTH, expand=True)
        tk.Button(card, text="Load Selected to Decryption Panel", command=self.load_selected_incoming, bg=self.BLUE, fg="white", relief=tk.FLAT, font=ui_font(8, "bold"), cursor="hand2").pack(anchor="w", pady=(8, 0))

    def create_chat_card(self, parent, speaker, meta, bg_color):
        card = tk.Frame(parent, bg=bg_color, highlightthickness=1, highlightbackground=self.BORDER)
        card.pack(fill=tk.X, pady=7)
        tk.Label(card, text=speaker, bg=bg_color, fg=self.TEXT, font=ui_font(10, "bold")).pack(anchor="w", padx=10, pady=(8, 0))
        tk.Label(card, text=meta, bg=bg_color, fg=self.MUTED, font=ui_font(8)).pack(anchor="e", padx=10)
        text_box = tk.Text(
            card,
            height=5,
            bg=bg_color,
            fg=self.TEXT,
            state="disabled",
            wrap=tk.WORD,
            relief=tk.FLAT,
            font=mono_font(9),
            padx=10,
            pady=8,
        )
        text_box.pack(fill=tk.X)
        return text_box

    def build_right_panel(self, parent):
        right = tk.Frame(parent, bg=self.PANEL, width=280, highlightthickness=1, highlightbackground=self.BORDER)
        right.grid(row=0, column=2, sticky="ns")
        right.grid_propagate(False)

        tk.Label(right, text="Session Keys & Logs", bg=self.PANEL, fg=self.TEXT, font=ui_font(11, "bold")).pack(anchor="w", padx=10, pady=(12, 4))
        self.key_label = tk.Label(right, text="Shared secret (shift)", bg=self.PANEL, fg=self.MUTED, font=ui_font(9, "bold"))
        self.key_label.pack(anchor="w", padx=10)
        self.key_entry = ttk.Entry(right)
        self.key_entry.insert(0, "3")
        self.key_entry.pack(fill=tk.X, padx=10, pady=(4, 10))

        for title, detail in (("AES-256-CBC", "Session Key: Rotated 2d ago"), ("RSA-2048", "Active Private Key"), ("ChaCha20", "Ephemeral Nonce")):
            panel = tk.Frame(right, bg=self.WHITE, highlightthickness=1, highlightbackground=self.BORDER)
            panel.pack(fill=tk.X, padx=10, pady=4)
            tk.Label(panel, text=title, bg=self.WHITE, fg=self.TEXT, font=ui_font(9, "bold")).pack(anchor="w", padx=8, pady=(7, 0))
            tk.Label(panel, text=detail, bg=self.WHITE, fg=self.MUTED, font=ui_font(8)).pack(anchor="w", padx=8, pady=(0, 7))

        chart = tk.Canvas(right, width=240, height=80, bg=self.WHITE, highlightthickness=1, highlightbackground=self.BORDER)
        chart.pack(padx=10, pady=(10, 8))
        chart.create_line(8, 70, 35, 55, 58, 60, 79, 45, 102, 48, 130, 36, 160, 42, 188, 26, 225, 20, fill=self.BLUE, width=2)

        tk.Button(right, text="Import Key", command=self.import_key, bg=self.WHITE, fg=self.TEXT, relief=tk.FLAT, font=ui_font(8), cursor="hand2").pack(side=tk.LEFT, padx=(10, 4), pady=12)
        tk.Button(right, text="Export Session", command=self.export_session, bg=self.BLUE, fg="white", relief=tk.FLAT, font=ui_font(8, "bold"), cursor="hand2").pack(side=tk.LEFT, padx=4, pady=12)

    def on_tab_clicked(self, name):
        self.show_view(name)
        self.status_var.set(f"Opened: {name}")

    def show_view(self, name):
        self.current_tab = name
        if name in self.views:
            self.views[name].tkraise()
        self.header_title.config(text=f"{name} • Project Aurora")
        for tab_name, btn in self.top_tab_buttons.items():
            btn.config(bg="#2BA0E8" if tab_name == name else self.BLUE)

    def new_session(self):
        self.clear_history()
        self.msg_input.delete("1.0", tk.END)
        self.status_var.set("New session started")

    def toggle_mode(self, event=None):
        if self.mode.get() == "Asymmetric":
            self.key_label.config(text="Public key (simulated)")
            self.key_entry.config(state="normal")
            self.key_entry.delete(0, tk.END)
            self.key_entry.insert(0, "RSA_PUB_8821")
            self.key_entry.config(state="disabled")
        else:
            self.key_label.config(text="Shared secret (shift)")
            self.key_entry.config(state="normal")
            if not self.key_entry.get().isdigit():
                self.key_entry.delete(0, tk.END)
                self.key_entry.insert(0, "3")

    def process_message(self):
        raw_text = self.msg_input.get("1.0", tk.END).strip()
        if not raw_text:
            return

        if self.mode.get() == "Symmetric":
            try:
                key = int(self.key_entry.get())
                encrypted = caesar_cipher(raw_text, key)
                decrypted = caesar_cipher(encrypted, key, decrypt=True)
                protocol_info = f"AES-SIM key:{key}"
            except ValueError:
                messagebox.showerror("Invalid key", "Symmetric key must be a number.")
                return
        else:
            encrypted = base64.b64encode(raw_text.encode()).decode()
            decrypted = base64.b64decode(encrypted.encode()).decode()
            protocol_info = "RSA-2048 simulated"

        self.update_box(self.network_log, f"[{protocol_info}] Ciphertext:\n{encrypted}\n\n")
        self.update_box(self.recipient_view, f"Plaintext:\n{decrypted}\n\n")
        self.update_box(self.preview_box, f"Preview:\n{encrypted[:72]}...\n")
        if hasattr(self, "incoming_list"):
            self.incoming_list.insert(tk.END, f"{protocol_info}: {encrypted}")
        self.msg_input.delete("1.0", tk.END)
        self.status_var.set(f"Message processed in {self.mode.get()} mode")

    def clear_history(self):
        for box in (self.network_log, self.recipient_view, self.preview_box):
            box.config(state="normal")
            box.delete("1.0", tk.END)
            box.config(state="disabled")
        if hasattr(self, "incoming_list"):
            self.incoming_list.delete(0, tk.END)
        self.status_var.set("History cleared")

    def decrypt_message(self):
        cipher_text = self.decrypt_input.get("1.0", tk.END).strip()
        if not cipher_text:
            self.status_var.set("No ciphertext to decrypt")
            return
        try:
            if self.mode.get() == "Symmetric":
                output = caesar_cipher(cipher_text, int(self.key_entry.get()), decrypt=True)
            else:
                output = base64.b64decode(cipher_text.encode()).decode()
        except Exception as exc:
            messagebox.showerror("Decrypt failed", f"Could not decrypt payload:\n{exc}")
            return
        self.decrypt_output.config(state="normal")
        self.decrypt_output.delete("1.0", tk.END)
        self.decrypt_output.insert(tk.END, output)
        self.decrypt_output.config(state="disabled")
        self.status_var.set("Ciphertext decrypted")

    def load_selected_incoming(self):
        if not hasattr(self, "incoming_list"):
            return
        selection = self.incoming_list.curselection()
        if not selection:
            self.status_var.set("Select an incoming message first")
            return
        selected = self.incoming_list.get(selection[0])
        payload = selected.split(": ", 1)[1]
        self.decrypt_input.delete("1.0", tk.END)
        self.decrypt_input.insert("1.0", payload)
        self.show_view("Decryption Panel")
        self.status_var.set("Loaded incoming payload to Decryption Panel")

    def export_transcript(self):
        transcript = self._build_transcript()
        if not transcript.strip():
            messagebox.showinfo("Export Transcript", "There is no transcript data yet.")
            return

        path = filedialog.asksaveasfilename(
            title="Export Transcript",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            f.write(transcript)
        self.status_var.set(f"Transcript exported to {path}")

    def import_key(self):
        key_value = simpledialog.askstring("Import Key", "Enter a key value:")
        if key_value is None:
            return
        self.key_entry.config(state="normal")
        self.key_entry.delete(0, tk.END)
        self.key_entry.insert(0, key_value.strip())
        if self.mode.get() == "Asymmetric":
            self.key_entry.config(state="disabled")
        self.status_var.set("Key imported")

    def export_session(self):
        session_data = self._build_transcript() or "No messages in session.\n"
        session_data += f"\nMode: {self.mode.get()}\nKey: {self.key_entry.get()}\n"
        path = filedialog.asksaveasfilename(
            title="Export Session",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            f.write(session_data)
        self.status_var.set(f"Session exported to {path}")

    def _build_transcript(self):
        parts = [
            "=== SecureBot / Network Intercept ===\n" + self.get_box_text(self.network_log),
            "=== Recipient View ===\n" + self.get_box_text(self.recipient_view),
            "=== Preview ===\n" + self.get_box_text(self.preview_box),
        ]
        return "\n".join(parts).strip()

    def get_box_text(self, box):
        box.config(state="normal")
        text = box.get("1.0", tk.END)
        box.config(state="disabled")
        return text.strip()

    def update_box(self, box, text):
        box.config(state="normal")
        box.insert(tk.END, text)
        box.see(tk.END)
        box.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = ProfessionalCryptoDemo(root)
    root.mainloop()
