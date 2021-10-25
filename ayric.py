# Based on https://github.com/AB-Law/Apple-Music-Discord-Rich-Presence,
# but repackaged, and with a few bugs squished.

from pypresence import Presence
import time
import os
import applescript
import subprocess
import random

c_id = "794212978135269388" 
RPC = Presence(c_id)

# red_icon = "red_appicon"
# black_icon = "black_appicon"
# white_icon = "white_appicon"
# itunes_icon = "itunes_appicon"
# celestial_icon = "celestial_icon"
# ll_icon = "ll_icon"
# relay_icon = "ll_icon"
# vice_icon = "vice_icon"
# multi_icon = "multi_appicon"

# icons = [red_icon, black_icon, white_icon, itunes_icon, celestial_icon,
#          ll_icon, relay_icon, vice_icon, multi_icon]

def running(app):
    count = int(subprocess.check_output(["osascript",
                                         "-e", "tell application \"System Events\"",
                                         "-e", "count (every process whose name is \"" + app + "\")",
                                         "-e", "end tell"]).strip())
    return count > 0


def state():
    return applescript.tell.app("Music", "player state as string").out


def grab_music_info():
    return subprocess.run(["osascript",
                           "-e", "tell application \"Music\"",
                           "-e", "get {name, artist, album, year, duration} of current track & {player position}",
                           "-e", "end tell"], capture_output=True).stdout.decode('utf-8').rstrip().split(", ")


def update(data):
    RPC.update(
        large_image='ll_icon',
        large_text="The best music platform",
        small_image="multi_appicon",
        small_text="Listening to " +
            data[0] + " by " + data[1] + " (" + data[3] + ")",
        details=data[0],
        state=data[1] + " — " + data[2] + " (" + data[3] + ")",
        end=time.time() + float(data[4]) - float(data[5]))


def stopped():
    RPC.update(
        large_image='ll_icon',
        large_text="The very best music platform",
        small_image="multi_appicon",
        small_text="Stopped",
        details="Paused")


def unavailable():
    RPC.update(
        large_image='ll_icon',
        large_text="An amazing music platform",
        small_image="multi_appicon",
        small_text="Listening to ",
        details="Apple Music does not have any info",
        state="Details unavailable due to some error")

def main():
    RPC.connect()
    if (running("Music")):
        while True:
            time.sleep(0.1)
            current_state = state()
            if current_state == "playing":
                data = grab_music_info()
                try:
                    update(data)
                except:
                    unavailable()
            else:
                stopped()

            time.sleep(5)

main()
