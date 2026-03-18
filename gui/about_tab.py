import customtkinter as ctk


class AboutTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self._build()

    def _build(self):
        ctk.CTkLabel(
            self,
            text="ℹ️  About",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#63B3ED",
            anchor="w",
        ).grid(row=0, column=0, padx=4, pady=(4, 16), sticky="w")

        # Info card
        card = ctk.CTkFrame(self, corner_radius=12)
        card.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        card.grid_columnconfigure(0, weight=1)

        rows = [
            ("🔐  Tool", "AES-256-GCM Image Cipher"),
            ("🐍  Language", "Python 3.12+"),
            ("🛡  Encryption", "AES-256-GCM (Authenticated)"),
            ("🔑  Key Derivation", "PBKDF2-HMAC-SHA256"),
            ("🔁  Iterations", "310,000"),
            ("🧂  Salt", "16 bytes (random per file)"),
            ("📦  Output ext", ".gcm"),
            ("👨‍💻  Author", "Shakal Bhau"),
        ]

        for i, (label, value) in enumerate(rows):
            ctk.CTkLabel(
                card,
                text=label,
                font=ctk.CTkFont(size=12, weight="bold"),
                anchor="w",
                width=180,
            ).grid(row=i, column=0, padx=16, pady=6, sticky="w")
            ctk.CTkLabel(
                card,
                text=value,
                font=ctk.CTkFont(size=12),
                anchor="w",
                text_color="#A0AEC0",
            ).grid(row=i, column=1, padx=(0, 16), pady=6, sticky="w")

        # Disclaimer
        disc = ctk.CTkFrame(self, corner_radius=12, fg_color="#2D1B1B")
        disc.grid(row=2, column=0, sticky="ew", pady=12)
        ctk.CTkLabel(
            disc,
            text="⚠️  Disclaimer",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#FC8181",
            anchor="w",
        ).grid(row=0, column=0, padx=16, pady=(12, 4), sticky="w")
        ctk.CTkLabel(
            disc,
            text=(
                "This tool is for educational and research purposes only.\n"
                "It has not undergone a formal security audit.\n"
                "Do not use it for high-value or life-critical data."
            ),
            font=ctk.CTkFont(size=11),
            text_color="#FEB2B2",
            anchor="w",
            justify="left",
        ).grid(row=1, column=0, padx=16, pady=(0, 12), sticky="w")
