# Windows Task Scheduler Setup

1. Open **Start** → search **Task Scheduler** → open.
2. **Action** → **Create Task…**
3. **General** tab:
   - Name: `Email WhatsApp Watcher`
   - Select: **Run whether user is logged on or not**
   - Check: **Run with highest privileges**
4. **Triggers** tab:
   - New → `Begin the task` = **At startup**
5. **Actions** tab:
   - New → **Start a program**
   - Program/script: `C:\\path\\to\\project\\.venv\\Scripts\\python.exe`
   - Add arguments: `run_watcher.py`
   - Start in: `C:\\path\\to\\project`
6. **Conditions** tab:
   - Uncheck "Start the task only if the computer is on AC power" if needed.
7. Click **OK** and enter your Windows password when prompted.

Repeat steps to create a second task for `run_web.py` if you want the UI to start at boot.
