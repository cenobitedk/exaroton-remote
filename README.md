# Exaroton Remote

A lightweight desktop app for starting and stopping your [exaroton](https://exaroton.com) Minecraft servers without opening a browser.

- **Windows** — lives in the system tray, optional auto-launch on startup
- **macOS** — runs as a regular window (great for testing)

Built with Python + [customtkinter](https://github.com/TomSchimansky/CustomTkinter).

---

## Features

- Lists all your exaroton servers at a glance
- Shows live status (Offline, Starting, Online, Crashed, etc.) with colour-coded badges
- Displays player count and server software/version when online
- **Start** and **Stop** buttons — enabled only when the action makes sense
- **★ Favourite servers** — pin your most-used servers to the top of the list
- Manual **⟳ refresh** button in addition to auto-refresh every 8 seconds
- Displays the actual API error message when something goes wrong (e.g. "Server exceeds maximum storage size")
- **Single instance** — launching the app a second time brings the existing window to the front instead of opening a duplicate
- API token saved locally on first launch — never asked again
- **Windows:** system tray icon, hide-to-tray on close, "Start with Windows" toggle
- **macOS:** plain window, suitable for development and testing

---

## Requirements

### Windows
- Windows 10 or 11
- Python 3.11 or newer — download from [python.org](https://www.python.org/downloads/)
  > During install, check **"Add Python to PATH"**

### macOS
- macOS 12 or newer
- [Homebrew](https://brew.sh) — if not installed:
  ```bash
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  ```
- [pyenv](https://github.com/pyenv/pyenv) for Python version management
- `tcl-tk@8` — required for the GUI (one-time setup, see below)

---

## macOS setup (one-time)

Install the Tcl/Tk dependency and rebuild Python with tkinter support:

```bash
brew install tcl-tk@8

TCL_TK=$(brew --prefix tcl-tk@8)
LDFLAGS="-L$TCL_TK/lib" \
CPPFLAGS="-I$TCL_TK/include" \
PKG_CONFIG_PATH="$TCL_TK/lib/pkgconfig" \
PYTHON_CONFIGURE_OPTS="--with-tcltk-includes='-I$TCL_TK/include' --with-tcltk-libs='-L$TCL_TK/lib -ltcl8.6 -ltk8.6'" \
pyenv install --force 3.12.0
```

You only need to do this once.

---

## Building & installing

### Windows

1. Copy this folder to your PC.
2. Double-click **`build.bat`**.
3. The script builds the exe, then asks two questions:
   - **Copy to `%LOCALAPPDATA%\ExarotonRemote\`?** — recommended, keeps the exe in a permanent location
   - **Create a desktop shortcut?** — creates `ExarotonRemote.lnk` on your Desktop
4. Just hit **Enter** twice to accept both defaults.

You can also right-click the exe and choose **"Pin to Start"** to add it to the Start menu.

To enable auto-launch on boot: right-click the tray icon → **"Start with Windows"**.

### macOS

```bash
bash build.sh
```

The finished app appears in the **`dist/`** folder. Double-click to run, or drag to **Applications**.

---

## First launch

1. Launch the app.
2. A prompt will ask for your **exaroton API token**.
   - Log in to [exaroton.com](https://exaroton.com) → **Account → API** → copy your token.
   - Paste it into the prompt and click **Save & Continue**.
   - The token is saved automatically — you only need to do this once.
3. **Windows only:** the app hides to the **system tray** (near the clock, bottom-right corner). Look for a small green **E** icon.

---

## Usage

| Action | How |
|---|---|
| Show window | Windows: double-click the tray icon. macOS: app opens directly. |
| Hide window | Click **✕** — on Windows the app keeps running in the tray; on macOS it quits. |
| Start a server | Click the **Start** button next to the server (available when Offline) |
| Stop a server | Click the **Stop** button (available when Starting or Online) |
| Favourite a server | Click the **☆** star on a server card — it turns gold and the server moves to the top |
| Manual refresh | Click **⟳** in the top-right corner |
| Auto-refresh | Happens automatically every 8 seconds |
| Re-open from taskbar | Launching the app again brings the existing window to the front |

---

## Tray icon menu (Windows only)

Right-click the green **E** icon in the system tray:

| Option | What it does |
|---|---|
| Open | Shows the main window |
| Start with Windows | Toggle auto-launch on boot (checkmark = enabled) |
| Quit | Closes the app completely |

---

## Troubleshooting

**Tray icon not visible (Windows)**
Click the **^** arrow near the clock to reveal hidden tray icons. Drag the green E out to keep it always visible.

**Start/Stop buttons are greyed out**
Buttons are only active when the action makes sense — Start when the server is Offline, Stop when it is Starting or Online. Wait a moment for the status to refresh, or click **⟳**.

**Error dialog after entering token**
Double-check you copied the full token from exaroton account settings. Reset it by deleting:
- **Windows:** `%APPDATA%\ExarotonRemote\config.json`
- **macOS:** `~/Library/Application Support/ExarotonRemote/config.json`

The app will prompt for the token again on next launch.

**macOS: app crashes immediately**
Make sure you completed the one-time macOS setup (installing `tcl-tk@8` and rebuilding Python via pyenv). See [macOS setup](#macos-setup-one-time) above.

---

## Project structure

```
app.py               Main application & GUI
api.py               exaroton REST API wrapper
config.py            Token & favourites storage
single_instance.py   Prevents duplicate app instances
startup.py           Windows auto-launch (registry)
icon.py              Tray/window icon generator (Pillow)
build.bat            Windows build script (PyInstaller)
build.sh             macOS build script (PyInstaller)
requirements.txt
```

---

## License

MIT
