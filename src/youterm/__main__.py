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

from argparse import ArgumentParser
from sys import exit
from subprocess import run
from youterm.colorizer import Colorize
from youterm.text import wrap
from youterm.yt import yt_search, get_api_key, get_details
from threading import Thread

fg = Colorize.fg
style = Colorize.style


def main_loop(api_key: str, results: int, video_fmt: str = "") -> None:
    query = str(input("Search YouTube (`q` to quit): "))
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
            "num": f"[{str(index+1)}]",
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
                f"--ytdl-format={video_fmt}bestaudio",
                f"https://www.youtube.com/watch?v={selected_id}",
            ]
        )


def main() -> None:
    argparser = ArgumentParser(
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
        help="YouTube Data v3 API key",
    )
    args = argparser.parse_args()
    key = args.api or get_api_key()
    video_fmt = ""
    results = 5  # default value
    if args.video:
        # TODO: add video format selection
        video_fmt = "bestvideo+"
    if args.results:
        results = args.results
    while True:
        main_loop(api_key=key, results=results, video_fmt=video_fmt)


if __name__ == "__main__":
    main()
