import json
import os
from typing import List, Dict, Any, Optional

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

# ---- OG-style files ----
VAULT_FILE = "vault_data.enc"
SALT_FILE = VAULT_FILE + ".salt"   # ✅ "SALT_FILE under VAULT_FILE"

# ---- Crypto params ----
_SALT_LEN = 16
_NONCE_LEN = 12
_KEY_LEN = 32

# Scrypt settings (balanced for typical Windows devices)
_KDF_N = 2**15
_KDF_R = 8
_KDF_P = 1


# ----------------- Internal helpers -----------------
def _read_file(path: str) -> Optional[bytes]:
    try:
        with open(path, "rb") as f:
            return f.read()
    except FileNotFoundError:
        return None


def _write_file(path: str, data: bytes) -> None:
    with open(path, "wb") as f:
        f.write(data)


def _ensure_salt() -> bytes:
    salt = _read_file(SALT_FILE)
    if salt is None or len(salt) != _SALT_LEN:
        salt = os.urandom(_SALT_LEN)
        _write_file(SALT_FILE, salt)
    return salt


def _derive_key(master_password: str, salt: bytes) -> bytes:
    if not master_password:
        raise ValueError("Master password required.")
    kdf = Scrypt(salt=salt, length=_KEY_LEN, n=_KDF_N, r=_KDF_R, p=_KDF_P)
    return kdf.derive(master_password.encode("utf-8"))


def _encrypt_entries(entries: List[Dict[str, Any]], master_password: str) -> bytes:
    salt = _ensure_salt()
    key = _derive_key(master_password, salt)
    aesgcm = AESGCM(key)

    nonce = os.urandom(_NONCE_LEN)
    plaintext = json.dumps(entries, ensure_ascii=False).encode("utf-8")
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)

    # VAULT_FILE format: [nonce][ciphertext]
    return nonce + ciphertext


def _decrypt_entries(blob: bytes, master_password: str) -> List[Dict[str, Any]]:
    if len(blob) < _NONCE_LEN + 1:
        return []

    salt = _read_file(SALT_FILE)
    if salt is None or len(salt) != _SALT_LEN:
        return []

    nonce = blob[:_NONCE_LEN]
    ciphertext = blob[_NONCE_LEN:]

    key = _derive_key(master_password, salt)
    aesgcm = AESGCM(key)

    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    data = json.loads(plaintext.decode("utf-8"))

    return data if isinstance(data, list) else []


def _load_raw(master_password: str) -> List[Dict[str, Any]]:
    blob = _read_file(VAULT_FILE)
    if blob is None:
        return []
    return _decrypt_entries(blob, master_password)


def _save_raw(entries: List[Dict[str, Any]], master_password: str) -> None:
    blob = _encrypt_entries(entries, master_password)
    _write_file(VAULT_FILE, blob)


# ----------------- Public API For GUI -----------------
def load_entries(master_password: str) -> List[Dict[str, Any]]:
    """
    GUI calls: load_entries(mp)
    Raises ValueError for empty password.
    Returns [] if vault missing.
    Returns [] if wrong password/tamper (GUI can treat as wrong password).
    """
    if not master_password:
        raise ValueError("Master password required.")
    try:
        return _load_raw(master_password)
    except Exception:
        return []


def add_entry(master_password: str, site: str, username: str, password: str) -> bool:
    """
    GUI calls: add_entry(master_pw_cache, site, user, pw)
    Returns True if saved.
    """
    if not master_password:
        raise ValueError("Master password required.")

    entry = {"site": site, "username": username, "password": password}

    entries = load_entries(master_password)
    entries.append(entry)
    _save_raw(entries, master_password)
    return True


def delete_entry(master_password: str, index: int) -> bool:
    """
    GUI calls: delete_entry(master_pw_cache, idx)
    """
    if not master_password:
        raise ValueError("Master password required.")

    entries = load_entries(master_password)
    if 0 <= index < len(entries):
        entries.pop(index)
        _save_raw(entries, master_password)
        return True
    return False


def reset_vault() -> None:
    """
    GUI calls: reset_vault()
    We do NOT need master password because GUI is "factory reset".
    To allow a fresh master password, we delete both files.
    """
    # Delete vault + salt so if password is forgotten, user can start fresh
    try:
        os.remove(VAULT_FILE)
    except FileNotFoundError:
        pass
    try:
        os.remove(SALT_FILE)
    except FileNotFoundError:
        pass