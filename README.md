<h1 align="center">🔐 lockstr</h1>
<p align="center">
  🇺🇸 <b>English</b> |
  🇪🇸 <a href="README_ES.md">Español</a>
</p>
<h3 align="center">lockstr is a secure, minimal, command-line file encryption tool built on Fernet symmetric cryptography.
It encrypts and decrypts files and directories in place, without ever exposing the encryption key on screen.</h3>

> ⚠️ Without the key, encrypted files are **permanently unrecoverable**.

---

## ✨ Features

* 🔒 Strong symmetric encryption (Fernet / AES + HMAC)
* 📁 Encrypt **files or entire directories** (recursive)
* 🧠 Magic header prevents accidental double-encryption
* 🧪 Dry-run mode (preview without changes)
* 📋 Encryption keys copied to clipboard (never printed)
* ⌨️ Secure key input (hidden input)
* 🔁 Atomic file replacement (no partial corruption)
* 🧰 Cross-platform (Linux, macOS, Windows)
* 🚫 No network access, no key storage, no telemetry

---

## 🔐 Cryptography Overview

lockstr uses **Fernet** from the `cryptography` library:

* AES-128-CBC encryption
* HMAC-SHA256 authentication
* Built-in integrity verification
* Tamper detection
* Symmetric key model

The same key is used to encrypt and decrypt data.

---

## 📦 Installation

### 1. Requirements

* Python **3.6+**
* Required packages:

  ```bash
  pip install cryptography pyperclip
  ```

#### Linux clipboard support (recommended)

```bash
sudo apt install xclip     # X11
sudo apt install wl-clipboard  # Wayland
```

---

### 2. Install lockstr

Clone the project with:

```bash
git clone https://github.com/urdev4ever/lockstr.git
cd lockstr
```

From the project directory:

```bash
python installer.py
```

This will:

* Copy `lockstr.py` to an appropriate system directory
* Create a `lockstr` command wrapper
* Add instructions if your PATH needs updating

---

## 🚀 Usage

### Basic syntax

```bash
lockstr encrypt <path>
lockstr decrypt <path>
```

Where `<path>` can be:

* A single file
* A directory (processed recursively)

---

### 🔒 Encrypt a file

```bash
lockstr encrypt secret.txt
```

* Generates a new encryption key
* Copies it to your clipboard
* Encrypts the file **in place**

---

### 🔓 Decrypt a file

```bash
lockstr decrypt secret.txt
```

* Prompts for the key (hidden input)
* Restores the original file

---

### 📁 Encrypt a directory

```bash
lockstr encrypt ./documents/
```

All files inside the directory will be encrypted recursively.

---

## 🧪 Dry-run Mode (Highly Recommended)

Preview what will be encrypted or decrypted **without modifying anything**:

```bash
lockstr encrypt ./backup/ --dry-run
```

This displays:

* File tree
* Number of files affected
* No changes are made

---

## ⚙️ Command-line Options

| Option                | Description                                  |
| --------------------- | -------------------------------------------- |
| `--dry-run`           | Show what would be processed without changes |
| `--confirm`           | Ask for confirmation before processing       |
| `--include-hidden`    | Include hidden files (`.filename`)           |
| `--continue-on-error` | Continue even if some files fail             |
| `-h, --help`          | Show help message                            |

---

## 🧠 Magic Header Protection

lockstr prepends a **magic header** to encrypted files:

```
LOCKSTR1\0
```

This allows lockstr to:

* Detect already-encrypted files
* Prevent double encryption
* Reject decryption attempts on plain files

---

## 🔑 Key Handling & Security

* Keys are **never printed**
* Keys are copied to the clipboard **once**
* Keys are not saved or logged
* Decryption requires manual key entry (hidden input)

> 📌 Save your key immediately in a password manager.

---

## ⚠️ Important Security Notes

* 🔥 If you lose the key, files are unrecoverable
* 🧠 lockstr does not store backups
* 🧪 Always test with `--dry-run`
* 💾 Backup important files before encryption
* 🦠 Does not protect against malware or keyloggers
* 📋 Clipboard contents may be readable by other applications

---

## 🛠️ Error Handling

lockstr safely handles:

* Invalid or corrupted ciphertext
* Wrong keys
* Permission errors
* Partial failures (optional continuation)
* Interrupted execution (Ctrl+C)

Atomic writes prevent file corruption.

---

## 🧱 Project Structure

```
lockstr/
├── lockstr.py      # Main CLI application
├── installer.py    # System installer
├── README.md
└── README_ES.md
```

---

## 🎯 Design Philosophy

lockstr is designed to be:

* **Explicit** — no hidden behavior
* **Safe-by-default** — dry-run and confirmation options
* **Local-only** — no networking
* **Hard to misuse** — magic headers and validation
* **Minimal** — does one thing well

It is **not** intended to be:

* A backup solution
* A password manager
* A cloud encryption tool

---

## 🧪 Tested Platforms

* Linux (X11 / Wayland)
* Windows 10+
* macOS (zsh / bash)

---

## 🧠 Final Warning

> **If you encrypt files and lose the key, there is no recovery, be extra careful**

> **This is by design.**

---
Made with <3 by URDev.
