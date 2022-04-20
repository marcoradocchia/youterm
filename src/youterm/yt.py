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

from os import popen
from requests import get
from youterm.date import format_date


PASS_ENTRY = "api/youtube"


def get_api_key() -> str:
    key = popen(f"pass show {PASS_ENTRY}").read().strip()
    if not key:  # handling no key in password store
        exit("Error occoured retrieving api key")
    return key


def yt_search(api_key: str, query: str, max_results: int) -> dict:
    url = (
        "https://youtube.googleapis.com/youtube/"
        "v3/search?part=snippet&type=video&"
    )
    url += f"max_results={max_results}&q={query}&key={api_key}"
    return get(url).json()


def format_duration(input: str) -> str:
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
    for unit in dhms:
        value = dhms[unit]
        if value is None:
            string += "00"
        elif len(value) < 2:
            string += "0" + value
        else:
            string += value
        string += ":"
    return string[:-1]


def get_details(video: dict, api_key: str) -> None:
    url = (
        "https://youtube.googleapis.com/youtube/v3/"
        f"videos?id={video['id']}&part=snippet,contentDetails&key={api_key}"
    )
    item = get(url).json()["items"][0]
    video["title"] = item["snippet"]["title"]
    video["date"] = format_date(item["snippet"]["publishedAt"])
    video["duration"] = format_duration(item["contentDetails"]["duration"][2:])
