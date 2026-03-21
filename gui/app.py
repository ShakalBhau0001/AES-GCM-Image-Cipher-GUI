import customtkinter as ctk

from gui.sidebar import Sidebar
from gui.encrypt_tab import EncryptTab
from gui.decrypt_tab import DecryptTab
from gui.about_tab import AboutTab


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("🔐 AES-256-GCM Image Cipher  v1.0")
        self.geometry("860x620")
        self.minsize(780, 560)
        self._build()

    # Layout

    def _build(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self._sidebar = Sidebar(self, on_navigate=self._navigate)
        self._sidebar.grid(row=0, column=0, sticky="nsew")
        self._content = ctk.CTkFrame(self, corner_radius=0, fg_color="#171923")
        self._content.grid(row=0, column=1, sticky="nsew")
        self._content.grid_columnconfigure(0, weight=1)
        self._content.grid_rowconfigure(0, weight=1)
        self._tabs: dict[str, ctk.CTkFrame] = {
            "encrypt": EncryptTab(self._content),
            "decrypt": DecryptTab(self._content),
            "about": AboutTab(self._content),
        }
        for tab in self._tabs.values():
            tab.grid(row=0, column=0, padx=28, pady=24, sticky="nsew")

        # Show default tab
        self._navigate("encrypt")

    # Navigation

    def _navigate(self, key: str):
        for k, tab in self._tabs.items():
            if k == key:
                tab.tkraise()
