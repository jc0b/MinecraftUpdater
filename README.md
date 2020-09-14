# MinecraftUpdater
This Python script (based on the work done in [MinecraftUpdater](https://github.com/eclair4151/MinecraftUpdater)) will automate the updating of your [Paper-based](https://papermc.io) Minecraft server.
While it does not automatically restart your server, it will check whether your server requires updating, and download the newest version of Paper into your Minecraft directory.
Additionally, it will automatically remove old versions of Paper once the update has been completed.
                

## Usage
This script can be run both via `python3 update.py`, but can also be run by marking it as executable (`chmod +x update.py`) and running it as a binary with `./update.py`.
This script _requires_ your servers to be named according to the following convention:
``paper-<major>.<minor>.<patch>-<build>.jar``
Versions without a patch number are also valid (e.g. `paper-1.15-1.jar`).

All versions of Paper downloaded using this script will follow the naming conventions above, so you may have to rename only once.

If you do not have a version of Paper installed, or this script does not recognise your version because of the naming conventions above, it will download the latest build of Paper. 

Logs are written to `paper_updater.log`, in the same directory as the update script is run.

## Scheduling Updates
This script is intended to be run as a cron job.

## Future of this script
* Adding the ability to choose which version of Paper to download (useful for modded servers).
* Add the ability to choose whether old versions are deleted (useful for faster rollbacks).
* Add the ability to restart Minecraft servers automatically (supporting multiple `screen` sessions).
