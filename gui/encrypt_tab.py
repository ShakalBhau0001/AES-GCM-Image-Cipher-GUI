import re
import threading
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
from core.crypto import encrypt_file


def _password_strength(pw: str) -> tuple[str, str]:
    score = 0
    if len(pw) >= 8:
        score += 1
    if len(pw) >= 12:
        score += 1
    if re.search(r"[A-Z]", pw):
        score += 1
    if re.search(r"[0-9]", pw):
        score += 1
    if re.search(r"[^A-Za-z0-9]", pw):
        score += 1
    levels = [
        ("Very Weak", "#FC6464"),
        ("Weak", "#FFA500"),
        ("Fair", "#D4AC0D"),
        ("Strong", "#48C78E"),
        ("Very Strong", "#00C851"),
    ]
    return levels[min(score, 4)]


class EncryptTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self._output_dir: str | None = None
        self._show_pass = False
        self._build()

    # Build

    def _build(self):
        # Page title and description
        ctk.CTkLabel(
            self,
            text="🔒  Encrypt File",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#63B3ED",
            anchor="w",
        ).grid(row=0, column=0, padx=4, pady=(4, 2), sticky="w")

        ctk.CTkLabel(
            self,
            text="Encrypt any image using AES-256-GCM with a password.",
            font=ctk.CTkFont(size=12),
            text_color="#718096",
            anchor="w",
        ).grid(row=1, column=0, padx=4, pady=(0, 16), sticky="w")

        # Settings card
        card = ctk.CTkFrame(self, corner_radius=12)
        card.grid(row=2, column=0, sticky="ew", pady=(0, 12))
        card.grid_columnconfigure(1, weight=1)

        # File row
        self._add_label(card, "📄  Input File", row=0)
        self._file_var = tk.StringVar()
        ctk.CTkEntry(
            card,
            textvariable=self._file_var,
            placeholder_text="Select image or drag & drop…",
            height=36,
        ).grid(row=0, column=1, padx=(0, 8), pady=10, sticky="ew")
        ctk.CTkButton(
            card,
            text="Browse",
            width=80,
            height=36,
            fg_color="#2D3748",
            hover_color="#4A5568",
            command=self._browse_file,
        ).grid(row=0, column=2, padx=(0, 16), pady=10)

        # Output folder row
        self._add_label(card, "📁  Output Folder", row=1)
        self._outdir_var = tk.StringVar(value="Same as source")
        ctk.CTkEntry(
            card,
            textvariable=self._outdir_var,
            state="disabled",
            height=36,
            text_color="#718096",
        ).grid(row=1, column=1, padx=(0, 8), pady=6, sticky="ew")
        ctk.CTkButton(
            card,
            text="Choose",
            width=80,
            height=36,
            fg_color="#2D3748",
            hover_color="#4A5568",
            command=self._choose_outdir,
        ).grid(row=1, column=2, padx=(0, 16), pady=6)

        # Password row
        self._add_label(card, "🔑  Password", row=2)
        self._pass_var = tk.StringVar()
        self._pass_var.trace_add("write", self._on_pass_change)
        self._pass_entry = ctk.CTkEntry(
            card,
            textvariable=self._pass_var,
            show="•",
            placeholder_text="Enter strong password…",
            height=36,
        )
        self._pass_entry.grid(row=2, column=1, padx=(0, 8), pady=6, sticky="ew")
        self._eye_btn = ctk.CTkButton(
            card,
            text="👁",
            width=36,
            height=36,
            fg_color="#2D3748",
            hover_color="#4A5568",
            command=self._toggle_pass,
        )
        self._eye_btn.grid(row=2, column=2, padx=(0, 16), pady=6)

        # Strength indicator
        self._strength_lbl = ctk.CTkLabel(
            card,
            text="Password strength: —",
            font=ctk.CTkFont(size=11, slant="italic"),
            text_color="#718096",
            anchor="w",
        )
        self._strength_lbl.grid(row=3, column=1, padx=(0, 8), pady=(0, 10), sticky="w")

        # Encrypt button and progress
        self._enc_btn = ctk.CTkButton(
            self,
            text="🔒   Encrypt Now",
            height=46,
            corner_radius=10,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#276749",
            hover_color="#1C4532",
            command=self._run,
        )
        self._enc_btn.grid(row=3, column=0, sticky="ew", pady=(0, 12))

        # Progress
        self._progress = ctk.CTkProgressBar(self, height=12, corner_radius=6)
        self._progress.set(0)
        self._progress.grid(row=4, column=0, sticky="ew", pady=(0, 4))

        self._prog_lbl = ctk.CTkLabel(
            self,
            text="Ready",
            font=ctk.CTkFont(size=11),
            text_color="#718096",
            anchor="w",
        )
        self._prog_lbl.grid(row=5, column=0, sticky="w", pady=(0, 8))

        # Log
        log_card = ctk.CTkFrame(self, corner_radius=12)
        log_card.grid(row=6, column=0, sticky="nsew", pady=(0, 4))
        log_card.grid_columnconfigure(0, weight=1)
        log_card.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(6, weight=1)

        ctk.CTkLabel(
            log_card,
            text="Status Log",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w",
        ).grid(row=0, column=0, padx=14, pady=(10, 0), sticky="w")

        self._log = ctk.CTkTextbox(
            log_card,
            height=130,
            font=ctk.CTkFont(family="Consolas", size=12),
            state="disabled",
        )
        self._log.grid(row=1, column=0, padx=10, pady=(4, 10), sticky="nsew")

        # Clear button
        ctk.CTkButton(
            self,
            text="🗑  Clear",
            height=34,
            corner_radius=8,
            fg_color="#4A5568",
            hover_color="#2D3748",
            font=ctk.CTkFont(size=12),
            command=self._clear,
        ).grid(row=7, column=0, sticky="e", pady=(4, 0))

    # Helpers

    def _add_label(self, parent, text, row):
        ctk.CTkLabel(
            parent,
            text=text,
            anchor="w",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=140,
        ).grid(row=row, column=0, padx=16, pady=6, sticky="w")

    def _browse_file(self):
        path = filedialog.askopenfilename(
            filetypes=[
                ("Images", "*.png *.jpg *.jpeg *.bmp *.gif *.webp"),
                ("All files", "*.*"),
            ]
        )
        if path:
            self._file_var.set(path)

    def _choose_outdir(self):
        d = filedialog.askdirectory()
        if d:
            self._output_dir = d
            self._outdir_var.set(d)

    def _toggle_pass(self):
        self._show_pass = not self._show_pass
        self._pass_entry.configure(show="" if self._show_pass else "•")

    def _on_pass_change(self, *_):
        pw = self._pass_var.get()
        if pw:
            label, color = _password_strength(pw)
            self._strength_lbl.configure(
                text=f"Password strength: {label}", text_color=color
            )
        else:
            self._strength_lbl.configure(
                text="Password strength: —", text_color="#718096"
            )

    def _clear(self):
        self._file_var.set("")
        self._pass_var.set("")
        self._progress.set(0)
        self._prog_lbl.configure(text="Ready", text_color="#718096")
        self._log.configure(state="normal")
        self._log.delete("1.0", "end")
        self._log.configure(state="disabled")
        self._strength_lbl.configure(text="Password strength: —", text_color="#718096")

    def _log_msg(self, msg: str):
        from datetime import datetime

        ts = datetime.now().strftime("%H:%M:%S")
        self._log.configure(state="normal")
        self._log.insert("end", f"[{ts}]  {msg}\n")
        self._log.see("end")
        self._log.configure(state="disabled")

    def _set_progress(self, pct: int):
        self.after(0, lambda: self._progress.set(pct / 100))

    # Run encryption in a separate thread to keep UI responsive

    def _run(self):
        path = self._file_var.get().strip()
        pw = self._pass_var.get()

        if not path:
            self._log_msg("⚠  Please select a file.")
            return
        if not pw:
            self._log_msg("⚠  Please enter a password.")
            return

        self._enc_btn.configure(state="disabled")
        self._progress.set(0)
        self._prog_lbl.configure(text="Encrypting…", text_color="#63B3ED")

        threading.Thread(target=self._worker, args=(path, pw), daemon=True).start()

    def _worker(self, path: str, pw: str):
        try:
            encrypt_file(
                src_path=path,
                password=pw,
                out_dir=self._output_dir,
                progress_cb=self._set_progress,
                log_cb=lambda m: self.after(0, lambda msg=m: self._log_msg(msg)),
            )
            self.after(
                0, lambda: self._prog_lbl.configure(text="Done ✓", text_color="#48C78E")
            )
        except Exception as e:
            self.after(0, lambda: self._log_msg(f"❌  {e}"))
            self.after(
                0, lambda: self._prog_lbl.configure(text="Error", text_color="#FC6464")
            )
        finally:
            self.after(0, lambda: self._enc_btn.configure(state="normal"))
