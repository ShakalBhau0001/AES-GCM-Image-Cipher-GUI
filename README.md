# 🔐 AES-GCM-Image-Cipher-GUI

### AES-256-GCM Image Encryption & Decryption Toolkit (GUI Edition)

**AES-GCM-Image-Cipher-GUI** is a modern, password-based **image encryption and decryption desktop application** built entirely in **Python (3.12.x compatible)** using **CustomTkinter**.
It allows **end users (non-technical)** to securely:
- Encrypt any image file using AES-256-GCM
- Decrypt `.gcm` encrypted files back to original format

All operations are performed **locally** with **no network usage**, ensuring full user privacy.

---

## ✨ Key Philosophy

This project is designed with three core goals:

1. **Security-first** – AES-256-GCM with PBKDF2 key derivation
2. **End-user friendly** – clean GUI, sidebar navigation, minimal clicks
3. **Modular architecture** – crypto logic strictly separated from UI

This is **not a toy project**. The crypto core works independently and can be imported or reused without the GUI.

---

## 🧩 Features

### 🔒 Encryption

Encrypt any image file using a password.

**Features**
- Supports PNG, JPG, BMP, GIF, WEBP and more
- Encrypted output: `.gcm`
- Random Salt + IV generated per file
- Original file extension preserved in header
- Timestamp in output filename (no overwrite)
- Password strength indicator

**Use-case**
> Secure personal images, sensitive photos, private files

---

### 🔓 Decryption

Decrypt `.gcm` encrypted files back to original format.

**Features**
- Restores original file extension automatically
- GCM Authentication Tag validates file integrity
- Detects wrong password or tampered files
- Clean error messages

**Use-case**
> Restore encrypted images with correct password

---

## 📁 Project Structure

```bash
AES-GCM-Image-Cipher-GUI/
│
├── core/
│   ├── __init__.py
│   └── crypto.py            # AES-256-GCM encryption / decryption logic
│
├── gui/
│   ├── __init__.py
│   ├── app.py               # Main window
│   ├── sidebar.py           # Left navigation sidebar
│   ├── encrypt_tab.py       # Encrypt tab UI
│   ├── decrypt_tab.py       # Decrypt tab UI
│   └── about_tab.py         # Crypto details + disclaimer
│
├── assets/                  # Screenshots
├── main.py                  # Entry point
├── requirements.txt
└── README.md
```

> ✔ Crypto logic (`core/`) and GUI (`gui/`) are **strictly separated** for maintainability.

---

## 🔐 Cryptography Details

| Component | Implementation |
|-----------|----------------|
| Encryption | AES-256-GCM (Authenticated) |
| Key Derivation | PBKDF2-HMAC-SHA256 |
| Iterations | 310,000 |
| Salt | 16 bytes (random per file) |
| IV | 12 bytes (random per file) |
| Auth Tag | 128-bit GCM tag |
| Output Extension | `.gcm` |

> ✔ GCM Authentication Tag detects any tampering — wrong password or modified file is immediately rejected.

---

## 🖥️ GUI Design

- Built with **CustomTkinter**
- Sidebar navigation (Encrypt / Decrypt / About)
- Password strength indicator
- Show / Hide password toggle
- Progress bar with background threading
- Status log with timestamps
- Dark / Light theme toggle
- Designed for **non-technical users**

Fully tested on:
- **Python 3.12.10**
- Windows 10 / 11

---

## 🚀 Getting Started

### 1️⃣ Clone Repository

```bash
git clone https://github.com/ShakalBhau0001/AES-GCM-Image-Cipher-GUI.git
cd AES-GCM-Image-Cipher-GUI
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run Application

```bash
python main.py
```

---

## 📦 requirements.txt

```txt
cryptography
customtkinter
pillow
```

_No hidden or unnecessary dependencies._

---

## ⚙️ How It Works

**1️⃣ Key Derivation**
- Password → PBKDF2-HMAC-SHA256 (310,000 iterations) → 32-byte AES-256 key

**2️⃣ Encryption**
- Random 16-byte Salt and 12-byte IV generated
- File encrypted using AES-256-GCM
- Encrypted file structure:
```
[MAGIC 6B] [SALT 16B] [IV 12B] [ext-len 1B] [ext NB] [ciphertext + 16B GCM tag]
```

**3️⃣ Decryption**
- Validates MAGIC header
- Extracts Salt, IV, and original extension
- Re-derives AES key using password + salt
- GCM tag verifies integrity before decryption
- Restores original file

---

## ⚠️ Common Errors

| Error | Reason |
|-------|--------|
| Wrong password | Decryption fails — GCM tag mismatch |
| Invalid file | MAGIC header missing |
| Tampered file | GCM authentication tag invalid |
| Wrong extension | Must select a `.gcm` file to decrypt |

---

## 🛣️ Roadmap

- Drag-and-drop file support
- Folder encryption support
- Progress bar for large files
- PyInstaller standalone builds
- Linux & macOS packaging

---

## ⚠️ Security Disclaimer

This project is intended for **educational and research purposes**.

While it uses modern cryptographic primitives, it has **not undergone formal security audits**.
Do not use it for protecting high-value or life-critical data.

---

## 🪪 Author

> Developer: **Shakal Bhau**
> GitHub: **[ShakalBhau0001](https://github.com/ShakalBhau0001)**

---

> "Encryption should be powerful — but never complicated for the user."
