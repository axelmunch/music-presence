from random import choice
from time import sleep

from pypresence import ActivityType, Presence, PyPresenceException, StatusDisplayType

import config
from CurrentMusic import CurrentMusic
from format_ordinal import format_ordinal

connected = False


def connect():
    global connected

    try:
        RPC.connect()
        print("Connected to Discord")
        connected = True
    except PyPresenceException:
        print("Cannot connect to Discord")
        connected = False


music = CurrentMusic()


RPC = Presence(config.DISCORD_CLIENT_ID)
connect()


cleared = False

while True:
    music.update()

    if music.id is not None:
        if music.song_changed or not connected:
            buttons = None
            if "youtube.com" in music.comment:
                buttons = [
                    {
                        "label": f"▶️ {music.title}"[:32],
                        "url": music.comment,
                    }
                ]

            large_image = None
            if config.COVER_IMAGES[0] != "":
                large_image = choice(config.COVER_IMAGES)

            print("Updating presence")
            try:
                RPC.update(
                    activity_type=ActivityType.LISTENING,
                    details=f"{music.artist} - {music.title}",
                    status_display_type=StatusDisplayType.DETAILS,
                    large_text=f'Playlist "{music.genre}"',
                    state=f"🔁{format_ordinal(music.plays + 1)} listen",
                    start=int(music.started_at),
                    end=int(music.ends_at),
                    large_image=large_image,
                    buttons=buttons,
                )
                cleared = False
            except AssertionError:
                connect()
            except PyPresenceException:
                connect()

    elif not cleared:
        print("Clearing presence")
        try:
            RPC.clear()
            cleared = True
        except AssertionError:
            connect()
        except PyPresenceException:
            connect()

    sleep(10)
