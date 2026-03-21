import customtkinter as ctk


class Sidebar(ctk.CTkFrame):
    NAV_ITEMS = [
        ("🔒  Encrypt", "encrypt"),
        ("🔓  Decrypt", "decrypt"),
        ("ℹ️   About", "about"),
    ]

    def __init__(self, master, on_navigate, **kwargs):
        super().__init__(
            master,
            width=200,
            corner_radius=0,
            fg_color="#1A1A2E",
            **kwargs,
        )
        self.grid_propagate(False)
        self.grid_rowconfigure(10, weight=1)  # spacer row
        self._on_navigate = on_navigate
        self._active_tab = "encrypt"
        self._nav_buttons: dict[str, ctk.CTkButton] = {}
        self._build()

    # Build

    def _build(self):
        # Logo / title
        ctk.CTkLabel(
            self,
            text="🔐",
            font=ctk.CTkFont(size=40),
        ).grid(row=0, column=0, padx=20, pady=(28, 0))

        ctk.CTkLabel(
            self,
            text="AES-GCM\nImage Cipher",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#63B3ED",
            justify="center",
        ).grid(row=1, column=0, padx=20, pady=(4, 0))

        ctk.CTkLabel(
            self,
            text="v1.0",
            font=ctk.CTkFont(size=11),
            text_color="#4A5568",
        ).grid(row=2, column=0, pady=(0, 20))

        # Separator
        ctk.CTkFrame(self, height=1, fg_color="#2D3748").grid(
            row=3, column=0, sticky="ew", padx=16, pady=(0, 16)
        )

        # Nav buttons
        for i, (label, key) in enumerate(self.NAV_ITEMS):
            btn = ctk.CTkButton(
                self,
                text=label,
                anchor="w",
                height=42,
                corner_radius=8,
                font=ctk.CTkFont(size=13, weight="bold"),
                fg_color="transparent",
                hover_color="#2D3748",
                text_color="#A0AEC0",
                command=lambda k=key: self._navigate(k),
            )
            btn.grid(row=4 + i, column=0, padx=12, pady=3, sticky="ew")
            self._nav_buttons[key] = btn

        # Spacer -> row 10 is weight=1 spacer --> Separator
        ctk.CTkFrame(self, height=1, fg_color="#2D3748").grid(
            row=11, column=0, sticky="ew", padx=16, pady=8
        )

        # Theme toggle
        self._theme_btn = ctk.CTkButton(
            self,
            text="☀  Light Mode",
            height=36,
            corner_radius=8,
            font=ctk.CTkFont(size=12),
            fg_color="#2D3748",
            hover_color="#4A5568",
            text_color="#A0AEC0",
            command=self._toggle_theme,
        )
        self._theme_btn.grid(row=12, column=0, padx=12, pady=4, sticky="ew")

        # Author info
        ctk.CTkLabel(
            self,
            text="Shakal Bhau",
            font=ctk.CTkFont(size=10),
            text_color="#4A5568",
        ).grid(row=13, column=0, pady=(4, 16))

        # Highlight default tab
        self._set_active("encrypt")

    # Navigation

    def _navigate(self, key: str):
        self._set_active(key)
        self._on_navigate(key)

    def _set_active(self, key: str):
        for k, btn in self._nav_buttons.items():
            if k == key:
                btn.configure(fg_color="#2B4C7E", text_color="#FFFFFF")
            else:
                btn.configure(fg_color="transparent", text_color="#A0AEC0")
        self._active_tab = key

    def _toggle_theme(self):
        mode = ctk.get_appearance_mode()
        if mode == "Dark":
            ctk.set_appearance_mode("light")
            self._theme_btn.configure(text="🌙  Dark Mode")
        else:
            ctk.set_appearance_mode("dark")
            self._theme_btn.configure(text="☀  Light Mode")
