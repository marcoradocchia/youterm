#!/usr/bin/env python3
# coding=utf-8
from argparse import ArgumentParser
from os import popen
from requests import get
from sys import exit
from subprocess import run
from utils.colorizer import Colorize
from utils.date import format_date
from utils.text import wrap

PASS_ENTRY = "youtube/youterm_api_key"
fg = Colorize.fg
style = Colorize.style


def get_api_key() -> str:
    return popen(f"pass show {PASS_ENTRY} | head -n 1").read().strip()


def yt_search(api_key: str, query: str, max_results: int) -> None:
    url = (
        "https://youtube.googleapis.com/youtube/"
        "v3/search?part=snippet&type=video&"
    )
    url += f"max_results={max_results}&q={query}&key={api_key}"
    return get(url).json()


def format_duration(input: str) -> str:
    print(input)
    if "DT" in input or "D" in input:
        return "--:--:--:--"
    dhms = {"H": None, "M": None, "S": None}
    string = ""
    # get values
    for unit in dhms:
        if unit in input:
            index = input.find(unit)
            dhms[unit] = input[:index]
            input = input[index + 1 :]
    # format string
    for unit in dhms:
        value = dhms[unit]
        if not value:
            del dhms[unit]
            break
    print(dhms)
    for unit in dhms:
        value = dhms[unit]
        if value is None:
            string += "00"
        elif len(value) < 2:
            string += ("0" + value)
        else:
            string += value
        string += ":"
    return string[:-1]


def get_details(video: dict, api_key: str) -> dict:
    url = (
        "https://youtube.googleapis.com/youtube/v3/"
        f"videos?id={video['id']}&part=snippet,contentDetails&key={api_key}"
    )
    item = get(url).json()["items"][0]
    video["title"] = item["snippet"]["title"]
    video["date"] = format_date(item["snippet"]["publishedAt"])
    video["duration"] = format_duration(item["contentDetails"]["duration"][2:])
    return video


def main_loop(api_key: str, results: int, video_fmt: str = "") -> None:
    query = str(input("Search youtube: "))
    if query.lower() == "q":
        quit()
    try:
        response = yt_search(api_key=api_key, query=query, max_results=results)
    except Exception:
        exit(
            fg(input="ERROR: unable to get response from YouTube", color="red")
        )
    videos = []
    for index, item in enumerate(response["items"]):
        video = {
            "num": f"[{str(index+1)}]",
            "id": item["id"]["videoId"],
            "channel": item["snippet"]["channelTitle"],
            "desc": item["snippet"]["description"],
        }
        video = get_details(video, api_key)
        print(
            f"├─ {fg(input=video['num'], color='red')}\n"
            "│   ├── "
            f"{wrap(input=video['title'], pref_len=8, color='yellow')}\n"
            f"│   ├── {fg(input=video['channel'], color='magenta')}\n"
            f"│   ├── {wrap(input=video['desc'], pref_len=8, color='green')}\n"
            f"│   ├── {fg(input=video['duration'], color='cyan')}\n"
            f"│   └── {fg(input=video['date'], color='blue')}"
        )
        videos.append(video)
    while True:
        while True:
            try:
                selection = input("-> Select song: ")
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
            fg(input="Playing: ", color="green")
            + style(input=videos[selection]["title"], style="bolditalic")
        )
        run(
            [
                "mpv",
                f"--ytdl-format={video_fmt}bestaudio",
                f"https://www.youtube.com/watch?v={selected_id}",
            ]
        )


def main() -> None:
    argparser = ArgumentParser(allow_abbrev=False)
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
    args = argparser.parse_args()
    key = get_api_key()
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
