#!/usr/bin/env python3
# coding=utf-8

# youterm: CLI tool to search for YouTube videos and play selected video/audio
# via MPV
# Copyright (C) 2022 Marco Radocchia
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see https://www.gnu.org/licenses/.

from argparse import ArgumentParser, Namespace
from configparser import ConfigParser
from os import name as os_name
from os.path import expanduser
from sys import exit
from subprocess import run
from youterm.colorizer import Colorize
from youterm.text import wrap
from youterm.yt import yt_search, get_api_key, get_details
from threading import Thread

# search history, input navigation and copy/paste (this only works on linux)
# import readline

fg = Colorize.fg
style = Colorize.style


def parse_arguments() -> Namespace:
    """
    Parse command line arguments and return argparse.Namespace
    """
    argparser = ArgumentParser(
        prog="youterm",
        description=""" CLI tool to search for YouTube videos and play selected
            video/audio via MPV""",
        allow_abbrev=False,
    )
    argparser.add_argument(
        "-v", "--video", action="store_true", help="Play video"
    )
    argparser.add_argument(
        "-r",
        "--results",
        type=int,
        metavar=("<n>"),
        help="Number of search results displayed",
    )
    argparser.add_argument(
        "-a",
        "--api",
        type=str,
        metavar=("<api_key>"),
        help="YouTube Data API v3 key",
    )
    argparser.add_argument(
        "-q",
        "--quality",
        type=str,
        metavar=("<resolution>"),
        choices=["144", "240", "360", "480", "720", "1080", "1440", "2160"],
        help="Choose video quality (if not available choose closest lower)",
    )
    return argparser.parse_args()


def parse_config() -> ConfigParser:
    """
    Parse config file and return configparser.ConfigParser
    """

    def config_file() -> str:
        if os_name == "posix":  # if os is linux/bsd/macos/...
            return expanduser("~/.config/youterm/config")
        elif os_name == "nt":  # if os is windows
            return expanduser("~\\AppData\\Roaming\\youterm\\config")
        else:
            exit("Sorry this OS is not supported")

    config = ConfigParser()
    config.read(config_file())
    return config


def get_config_option(config: ConfigParser, section: str, option: str) -> str:
    """
    Return config option if section and options appear in the config file;
    return None if not
    """
    if config.has_section(section) and config.has_option(section, option):
        return config.get(section, option)
    else:
        return None


def main_loop(api_key: str, results: int, quality: str) -> None:
    """
    Main loop
    """
    query = input("Search YouTube (`q` to quit): ")
    if query.lower() == "q":
        quit()
    try:
        response = yt_search(api_key=api_key, query=query, max_results=results)
    except Exception:
        exit(
            fg(input="ERROR: unable to get response from YouTube", color="red")
        )

    videos = []
    threads = []

    for index, item in enumerate(response["items"]):
        video = {
            "num": f"[{index+1}]",
            "id": item["id"]["videoId"],
            "channel": item["snippet"]["channelTitle"],
            "desc": item["snippet"]["description"],
        }
        threads.append(Thread(target=get_details, args=[video, api_key]))
        videos.append(video)

    # perform the requests in different threads (faster because of paralelized
    # response times)
    for thread in threads:
        thread.start()

    # wait for all threads to finish before continuing to avoid working with
    # data is not yet received
    for thread in threads:
        thread.join()

    for video in videos:
        print(
            f"├─ {fg(input=video['num'], color='red')}\n"
            "│   ├── "
            f"{wrap(input=video['title'], pref_len=8, color='yellow')}\n"
            f"│   ├── {fg(input=video['channel'], color='magenta')}\n"
            f"│   ├── {wrap(input=video['desc'], pref_len=8, color='green')}\n"
            f"│   ├── {fg(input=video['duration'], color='cyan')}\n"
            f"│   └── {fg(input=video['date'], color='blue')}"
        )

    while True:
        while True:
            try:
                selection = input(
                    "└ Select video (`q` to go back to search): "
                )
                if selection.lower() == "q":
                    return
                selection = int(selection) - 1
                if selection < 0 or selection > len(videos):
                    raise ValueError
                break
            except ValueError:
                print(
                    fg(
                        input="Please insert a valid index (integer)",
                        color="red",
                    )
                )
        selected_id = videos[selection]["id"]
        print(
            fg(input="Playing: ", color="green"),
            style(input=videos[selection]["title"], style="bolditalic"),
        )
        print(
            fg(input="URL: ", color="yellow"),
            f"https://youtu.be/{videos[selection]['id']}",
        )
        run(
            [
                "mpv",
                f"--ytdl-format={quality}",
                f"https://www.youtube.com/watch?v={selected_id}",
            ]
        )


def main() -> None:
    """
    Main function
    """
    args = parse_arguments()
    config = parse_config()

    key = (
        args.api
        or get_config_option(config=config, section="api", option="key")
        or get_api_key(
            pass_entry=get_config_option(
                config=config, section="api", option="pass_entry"
            )
        )
    )
    results = (
        args.results
        or get_config_option(config=config, section="search", option="results")
        or 5  # default value
    )
    if args.video:
        quality = args.quality or get_config_option(
            config=config, section="video", option="quality"
        )
        if quality is None:
            # no quality chosen, default to bestvideo+bestaudio:
            # "merge the best video-only format and the best audio-only format,
            # or download the best combined format if video-only format is not
            # available" (https://github.com/yt-dlp/yt-dlp#filtering-formats)
            quality = "bv+ba/b"
        else:
            quality = f"bv*[height<=?{quality}]+ba/b"
    else:
        quality = "bestaudio"

    while True:
        # enter main application loop
        main_loop(api_key=key, results=results, quality=quality)


if __name__ == "__main__":
    main()
