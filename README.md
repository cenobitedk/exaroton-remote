# Exaroton Remote

A small Windows app that lives in the system tray and lets you start and stop your [exaroton](https://exaroton.com) Minecraft servers with a couple of clicks.

## Requirements

- Windows 10 or 11
- Python 3.11 or newer — download from [python.org](https://www.python.org/downloads/) (check "Add Python to PATH" during install)

## Building the app

1. Download or copy this folder to your Windows PC.
2. Double-click **`build.bat`**.
   - It will install the required Python packages and build `ExarotonRemote.exe`.
   - This takes a minute or two the first time.
3. When it's done, the finished exe is in the **`dist\`** folder.

## Installation

1. Move `dist\ExarotonRemote.exe` somewhere permanent, for example:
   ```
   C:\Users\YourName\AppData\Local\ExarotonRemote\ExarotonRemote.exe
   ```
2. Right-click the exe and choose **"Pin to Start"** so it's easy to find.

## First launch

1. Double-click the exe (or launch it from the Start menu).
2. A prompt will ask for your **exaroton API token**.
   - Log in to [exaroton.com](https://exaroton.com), go to **Account → API**, and copy your token.
   - Paste it into the prompt and click **Save & Continue**.
   - The token is saved automatically — you only need to do this once.
3. The app will disappear into the **system tray** (the icon area near the clock in the bottom-right corner of the screen). Look for a small green **E** icon.

## Daily use

- **Show the window** — double-click the green E tray icon.
- **Hide the window** — click the X button. The app keeps running in the tray.
- **Start a server** — open the window and click the **Start** button next to the server you want.
- **Stop a server** — click the **Stop** button (only available when the server is online).
- The status of each server updates automatically every 8 seconds.

## Tray icon menu

Right-click the green E icon in the system tray for these options:

| Option | What it does |
|---|---|
| Open | Shows the main window |
| Start with Windows | Toggles whether the app launches automatically when the PC starts |
| Quit | Closes the app completely |

## Start with Windows

To make the app start automatically every time the PC boots:

1. Right-click the tray icon.
2. Click **"Start with Windows"** — a checkmark will appear next to it.

To turn it off, click the same option again.

## Troubleshooting

**The tray icon doesn't appear after launching.**
Make sure the system tray isn't hiding icons. Click the **^** arrow near the clock to see hidden tray icons, then drag the green E icon out to keep it visible.

**"Start" and "Stop" buttons are greyed out.**
The buttons are only active when an action makes sense — Start is available for offline servers, Stop for online servers. Wait a moment for the status to refresh.

**The app shows an error after entering the token.**
Double-check that you copied the full token from the exaroton account settings page. You can reset it by deleting the config file at:
```
C:\Users\YourName\AppData\Roaming\ExarotonRemote\config.json
```
The app will ask for the token again on next launch.
