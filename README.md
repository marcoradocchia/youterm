# YouTerm
CLI tool to search for YouTube videos and play selected video's audio via
`mpv`.

## Requirements
###YouTube API
This script retrieves video informations using YouTube APIs. An API key is
needed. You can obtain one registering a Google develper profile, adding a
project and creating an API key adding the *YouTube Data API v3* service at
[this](https://console.cloud.google.com/apis/dashboard) link.

### Dependencies
This script does not rely on external Python dependencies, although it uses
external programs to provide audio streaming:
* `mpv`
* `youtube-dl` or `yt-dlp`
### Optional dependencies
To store the youtube api safely the unix standard password manager `pass` is
required. The script looks for one password entry containing the API key at
`youtube/youterm_api_key`. Alternatively you can hardcode the api key modifying
the script.

## Installation
You can use this script cloning the repository.
