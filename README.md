# Exaroton Remote

A small desktop app that lets you start and stop your [exaroton](https://exaroton.com) Minecraft servers with a couple of clicks.

- **Windows** — lives in the system tray, start with Windows support
- **macOS** — runs as a regular window, useful for testing

---

## Requirements

### Windows
- Windows 10 or 11
- Python 3.11 or newer — download from [python.org](https://www.python.org/downloads/) (check **"Add Python to PATH"** during install)

### macOS
- macOS 12 or newer
- [Homebrew](https://brew.sh) — if not installed, run:
  ```bash
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  ```
- [pyenv](https://github.com/pyenv/pyenv) for Python version management
- **tcl-tk@8** — required for the GUI (one-time setup, see below)

---

## macOS setup (one-time)

If you haven't already, install the Tcl/Tk dependency and rebuild Python with tkinter support:

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

## Building the app

### Windows

1. Copy this folder to your PC.
2. Double-click **`build.bat`**.
3. The finished exe is in the **`dist\`** folder.

### macOS

1. Open a terminal in this folder.
2. Run:
   ```bash
   bash build.sh
   ```
3. The finished app is in the **`dist/`** folder.

---

## Installation

### Windows

1. Move `dist\ExarotonRemote.exe` somewhere permanent, for example:
   ```
   C:\Users\YourName\AppData\Local\ExarotonRemote\ExarotonRemote.exe
   ```
2. Right-click the exe and choose **"Pin to Start"** so it's easy to find.

### macOS

Double-click `dist/ExarotonRemote.app` to run it, or drag it to your **Applications** folder.

---

## First launch

1. Launch the app.
2. A prompt will ask for your **exaroton API token**.
   - Log in to [exaroton.com](https://exaroton.com), go to **Account → API**, and copy your token.
   - Paste it into the prompt and click **Save & Continue**.
   - The token is saved automatically — you only need to do this once.
3. **Windows only:** the app disappears into the **system tray** (near the clock, bottom-right). Look for a small green **E** icon.

---

## Daily use

- **Show the window** — on Windows, double-click the green E tray icon. On macOS it opens directly.
- **Hide the window** — click the X button. On Windows the app keeps running in the tray; on macOS it quits.
- **Start a server** — click the **Start** button next to the server you want.
- **Stop a server** — click the **Stop** button (available when the server is starting or online).
- The status of each server updates automatically every 8 seconds.

---

## Tray icon menu (Windows only)

Right-click the green E icon in the system tray for these options:

| Option | What it does |
|---|---|
| Open | Shows the main window |
| Start with Windows | Toggles whether the app launches automatically on boot |
| Quit | Closes the app completely |

To enable auto-start: right-click the tray icon and click **"Start with Windows"** — a checkmark will appear. Click again to disable.

---

## Troubleshooting

**The tray icon doesn't appear after launching (Windows).**
Click the **^** arrow near the clock to see hidden tray icons, then drag the green E icon out to keep it visible.

**"Start" and "Stop" buttons are greyed out.**
The buttons are only active when an action makes sense — Start is available for offline servers, Stop for servers that are starting or online. Wait a moment for the status to refresh.

**The app shows an error after entering the token.**
Double-check that you copied the full token from the exaroton account settings page. You can reset it by deleting the config file:
- **Windows:** `C:\Users\YourName\AppData\Roaming\ExarotonRemote\config.json`
- **macOS:** `~/Library/Application Support/ExarotonRemote/config.json`

The app will ask for the token again on next launch.

**macOS: app crashes immediately.**
Make sure you completed the one-time macOS setup above (installing `tcl-tk@8` and rebuilding Python via pyenv).
