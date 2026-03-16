# AES-GCM-Image-Cipher-GUI
A Python desktop application for AES-256-GCM image encryption and decryption, built with CustomTkinter. Features PBKDF2-HMAC-SHA256 key derivation, sidebar navigation, password strength indicator, and a modular core/gui architecture.

---

Project structure :-

```
AES-GCM-Image-Cipher-GUI/
│
├── core/
│   ├── __init__.py
│   └── crypto.py          ← crypto logic 
│
├── gui/
│   ├── __init__.py
│   ├── app.py             ← Main window + sidebar layout
│   ├── sidebar.py         ← Left navigation
│   ├── encrypt_tab.py     ← Encrypt tab
│   ├── decrypt_tab.py     ← Decrypt tab
│   └── about_tab.py       ← Crypto details + disclaimer
│
├── assets/                ← Screenshots 
├── main.py                ← Entry point
├── requirements.txt
└── README.md
```

---
