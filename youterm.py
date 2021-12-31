#!/usr/bin/env python3
# coding=utf-8
from utils.colorizer import Colorize
from utils.text import wrapper
from os import popen
from requests import get
from sys import exit
from subprocess import run

PASS_ENTRY = "youtube/youterm_api_key"
fg = Colorize.fg

def get_api_key() -> str:
    return popen(f"pass show {PASS_ENTRY} | head -n 1").read().strip()

def yt_search(query: str, api_key: str, max_results: int = None) -> None:
    url = "https://youtube.googleapis.com/youtube/v3/search?part=snippet&type=video&"
    if max_results is not None:
        url += f"max_results={max_results}&"
    url += f"q={query}&key={api_key}"
    return get(url).json()

def format_date(date: str) -> str:
    date = date[:10]
    date = date.split('-')
    months = {
        '01': 'Jan',
        '02': 'Feb',
        '03': 'Mar',
        '04': 'Apr',
        '05': 'May',
        '06': 'Jun',
        '07': 'Jul',
        '08': 'Aug',
        '09': 'Sep',
        '10': 'Oct',
        '11': 'Nov',
        '12': 'Dec'
    }
    return f"{date[0]} {months[date[1]]} {date[2]}"

def format_duration(input: str) -> str:
    to_str = ""
    hours_index = input.find('H')
    minutes_index = input.find('M')
    seconds_index = input.find('S')
    if hours_index != -1:
        to_str += input[:hours_index] + ":"
    if minutes_index != -1:
        to_str += input[hours_index+1:minutes_index] + ":"
        seconds = input[minutes_index+1:seconds_index]
    else:
        seconds = input[:seconds_index]
    to_str += seconds
    return fg(input=to_str, color='cyan')

def get_details(video_id: str, api_key: str) -> dict:
    url = f"https://youtube.googleapis.com/youtube/v3/videos?id={video_id}&part=snippet,contentDetails&key={api_key}"
    item = get(url).json()['items'][0]
    details = {
        'title': fg(input=item['snippet']['title'], color='yellow'),
        'date': fg(input=format_date(item['snippet']['publishedAt']), color='green'),
        'duration': format_duration(item['contentDetails']['duration'][2:]),
    }
    return details

def main() -> None:
    api_key = get_api_key()
    try:
        query = str(input("Search youtube: "))
        if query.lower() == 'q':
            exit()
        response = yt_search(query=query, api_key=api_key)
    except:
        exit(fg(input="ERROR: unable to get response from YouTube", color='red'))
    for index, item in enumerate(response['items']):
        num = f"[{str(index+1)}]"
        video_id = item['id']['videoId']
        channel = fg(input=item['snippet']['channelTitle'], color='magenta')
        desc = item['snippet']['description']
        details = get_details(video_id, api_key)
        print(
            f"├─ {fg(input=num, color='red')}\n"
            f"│   ├── {details['title']}\n"
            f"│   ├── {channel}\n"
            f"│   ├── {wrapper(input=desc, prefix_length=8)}\n"
            f"│   ├── {details['duration']}\n"
            f"│   └── {details['date']}"
        )
    while True:
        try:
            selection = input("└ Select song: ")
            if selection.lower() == 'q':
                quit()
            selection = int(selection) - 1
            if selection < 0 or selection > len(response['items']):
                raise ValueError
            break
        except ValueError:
            print("│ ", end='')
            print(fg(input="Please insert a valid index (must be integer)", color='red'))
    selected_id = response['items'][selection]['id']['videoId']
    run(
        [
            'mpv',
            '--ytdl-format=bestaudio',
            f'https://www.youtube.com/watch?v={selected_id}'
        ]
    )

if __name__ == "__main__":
    while True:
        main()
