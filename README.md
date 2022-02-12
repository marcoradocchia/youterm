# YouTerm
CLI tool to search for [YouTube](https://youtube.com) videos and play selected
video's audio via `mpv`.

## Requirements
### YouTube API
This script retrieves video informations using YouTube APIs. An API key is
needed. You can obtain one registering a Google develper profile, adding a
project and creating an API key adding the _YouTube Data API v3_ service at
[this](https://console.cloud.google.com/apis/dashboard) link.
### Dependencies
This script does not rely on external Python dependencies, although it uses
external programs to provide audio streaming:
* `mpv`
* `youtube-dl` or `yt-dlp`
### Optional dependencies
To store the _YouTube_ API safely the _unix standard password manager_ `pass`
is required. The script looks for one password entry containing the API key at
`api/youtube`. Alternatively you can hardcode the API key modifying
the script.

## Installation
You can use this script cloning the repository with git:
```sh
git clone https://github.com/marcoradocchia/youterm.git
cd lyrterm
sudo make install
```
