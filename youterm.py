#!/usr/bin/env python3
# coding=utf-8
from utils.colorizer import Colorize
from utils.text import wrap
from utils.date import format_date
from os import popen
from requests import get
from sys import exit
from subprocess import run

PASS_ENTRY = "youtube/youterm_api_key"
fg = Colorize.fg


def get_api_key() -> str:
    return popen(f"pass show {PASS_ENTRY} | head -n 1").read().strip()


def yt_search(query: str, api_key: str, max_results: int = None) -> None:
    url = (
        "https://youtube.googleapis.com/youtube/"
        "v3/search?part=snippet&type=video&"
    )
    if max_results is not None:
        url += f"max_results={max_results}&"
    url += f"q={query}&key={api_key}"
    return get(url).json()


def format_duration(input: str) -> str:
    to_str = ""
    hours_index = input.find("H")
    minutes_index = input.find("M")
    seconds_index = input.find("S")
    if hours_index != -1:
        to_str += input[:hours_index] + ":"
    if minutes_index != -1:
        to_str += input[hours_index+1:minutes_index] + ":"
        seconds = input[minutes_index+1:seconds_index]
    else:
        seconds = input[:seconds_index]
    if len(seconds) == 1:
        seconds = "0" + seconds
    to_str += seconds
    return to_str


def get_details(video_id: str, api_key: str) -> dict:
    url = (
        "https://youtube.googleapis.com/youtube/v3/"
        f"videos?id={video_id}&part=snippet,contentDetails&key={api_key}"
    )
    item = get(url).json()["items"][0]
    details = {
        "title": item["snippet"]["title"],
        "date": format_date(item["snippet"]["publishedAt"]),
        "duration": format_duration(item["contentDetails"]["duration"][2:]),
    }
    return details


def main(api_key: str) -> None:
    query = str(input("Search youtube: "))
    if query.lower() == "q":
        quit()
    try:
        response = yt_search(query=query, api_key=api_key)
    except Exception:
        exit(
            fg(input="ERROR: unable to get response from YouTube", color="red")
        )
    for index, item in enumerate(response["items"]):
        num = f"[{str(index+1)}]"
        video_id = item["id"]["videoId"]
        channel = item["snippet"]["channelTitle"]
        desc = item["snippet"]["description"]
        details = get_details(video_id, api_key)
        print(
            f"├─ {fg(input=num, color='red')}\n"
            "│   ├── "
            f"{wrap(input=details['title'], pref_len=8, color='yellow')}\n"
            f"│   ├── {fg(input=channel, color='magenta')}\n"
            f"│   ├── {wrap(input=desc, pref_len=8, color='green')}\n"
            f"│   ├── {fg(input=details['duration'], color='cyan')}\n"
            f"│   └── {fg(input=details['date'], color='blue')}"
        )
    while True:
        try:
            selection = input("└ Select song: ")
            if selection.lower() == "q":
                return
            selection = int(selection) - 1
            if selection < 0 or selection > len(response["items"]):
                raise ValueError
            break
        except ValueError:
            print("│ ", end="")
            print(fg(
                input="Please insert a valid index (must be integer)",
                color="red"
            ))
    selected_id = response["items"][selection]["id"]["videoId"]
    run(
        [
            "mpv",
            "--ytdl-format=bestaudio",
            f"https://www.youtube.com/watch?v={selected_id}",
        ]
    )


if __name__ == "__main__":
    key = get_api_key()
    while True:
        main(api_key=key)
