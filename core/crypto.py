import os
import struct
from datetime import datetime
from hashlib import pbkdf2_hmac
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Constants
SALT_LEN = 16
IV_LEN = 12
KEY_LEN = 32  # AES-256
PBKDF2_ITERS = 310_000
ENC_EXT = ".gcm"
MAGIC = b"AESGCM"  # 6-byte header magic


# Key derivation


def derive_key(password: str, salt: bytes) -> bytes:
    return pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=salt,
        iterations=PBKDF2_ITERS,
        dklen=KEY_LEN,
    )


# Encrypt


def encrypt_file(
    src_path: str,
    password: str,
    out_dir: str | None,
    progress_cb,  # callable(int 0-100)
    log_cb,  # callable(str)
) -> str:

    if not os.path.isfile(src_path):
        raise FileNotFoundError(f"File not found: {src_path}")

    salt = os.urandom(SALT_LEN)
    iv = os.urandom(IV_LEN)

    log_cb(f"📂 Input     : {os.path.basename(src_path)}")
    log_cb(f"🔑 Deriving key  (PBKDF2-HMAC-SHA256, {PBKDF2_ITERS:,} iter)…")

    key = derive_key(password, salt)
    progress_cb(20)

    with open(src_path, "rb") as f:
        plaintext = f.read()

    file_size = len(plaintext)
    log_cb(f"📦 File size : {file_size:,} bytes")

    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(iv, plaintext, None)
    progress_cb(80)

    ext = _get_ext(src_path)
    ext_b = ext.encode("utf-8")

    dest_dir = out_dir or os.path.dirname(src_path) or "."
    out_name = f"{_timestamp()}_{os.path.basename(src_path)}{ENC_EXT}"
    out_path = os.path.join(dest_dir, out_name)

    with open(out_path, "wb") as f:
        f.write(MAGIC)
        f.write(salt)
        f.write(iv)
        f.write(struct.pack("B", len(ext_b)))
        f.write(ext_b)
        f.write(ciphertext)

    progress_cb(100)
    log_cb(f"✅ Encrypted  : {out_path}")
    return out_path


# Decrypt


def decrypt_file(
    src_path: str,
    password: str,
    out_dir: str | None,
    progress_cb,
    log_cb,
) -> str:

    if not os.path.isfile(src_path):
        raise FileNotFoundError(f"File not found: {src_path}")
    if not src_path.endswith(ENC_EXT):
        raise ValueError(f"Not a valid {ENC_EXT} file.")

    log_cb(f"📂 Input     : {os.path.basename(src_path)}")

    with open(src_path, "rb") as f:
        magic = f.read(len(MAGIC))
        if magic != MAGIC:
            raise ValueError("Invalid file — MAGIC header missing.")
        salt = f.read(SALT_LEN)
        iv = f.read(IV_LEN)
        ext_len = struct.unpack("B", f.read(1))[0]
        ext = f.read(ext_len).decode("utf-8")
        ciphertext = f.read()

    log_cb(f"🔑 Deriving key  (PBKDF2-HMAC-SHA256, {PBKDF2_ITERS:,} iter)…")
    key = derive_key(password, salt)
    progress_cb(40)

    try:
        aesgcm = AESGCM(key)
        plaintext = aesgcm.decrypt(iv, ciphertext, None)
    except Exception:
        raise ValueError("Decryption failed — wrong password or file tampered.")

    progress_cb(80)
    dest_dir = out_dir or os.path.dirname(src_path) or "."
    out_name = f"{_timestamp()}_restored" + (f".{ext}" if ext else "")
    out_path = os.path.join(dest_dir, out_name)

    with open(out_path, "wb") as f:
        f.write(plaintext)

    progress_cb(100)
    log_cb(f"✅ Decrypted  : {out_path}")
    return out_path


# Helpers


def _get_ext(path: str) -> str:
    _, ext = os.path.splitext(path)
    return ext.lstrip(".")


def _timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")
