<div align="center">
  <h1 align="center">YouTerm</h1>

  ![GitHub releases](https://img.shields.io/github/downloads/marcoradocchia/youterm/total?color=%23a9b665&logo=github)
  ![GitHub source size](https://img.shields.io/github/languages/code-size/marcoradocchia/youterm?color=ea6962&logo=github)
  ![GitHub open issues](https://img.shields.io/github/issues-raw/marcoradocchia/youterm?color=%23d8a657&logo=github)
  ![GitHub open pull requests](https://img.shields.io/github/issues-pr-raw/marcoradocchia/youterm?color=%2389b482&logo=github)
  ![GitHub sponsors](https://img.shields.io/github/sponsors/marcoradocchia?color=%23d3869b&logo=github)
  ![PyPi downloads](https://img.shields.io/pypi/dm/youterm?color=d4be98&label=pypi%20downloads&logo=pypi&logoColor=fff)
  ![PyPi version](https://img.shields.io/pypi/v/youterm?logo=pypi&logoColor=fff)
  ![GitHub license](https://img.shields.io/github/license/marcoradocchia/youterm?color=%23e78a4e)
</div>

CLI tool to search for [YouTube](https://youtube.com) videos and play selected
video/audio via `mpv`.

![yotuerm](assets/youterm.png)

## Requirements

### YouTube API

`youterm` retrieves video informations using YouTube APIs. An API key is
needed. You can obtain one registering a Google developer profile, adding a
project and creating an API key adding the *YouTube Data API v3* service at
[this](https://console.cloud.google.com/apis/dashboard) link.

### Dependencies

`youterm` does not rely on external Python libraries, although it uses
external programs to provide audio/video streaming:

- `mpv`
- `yt-dlp` or `youtube-dl`

### Optional dependencies

To store the *YouTube* API safely the *unix standard password manager* `pass`
is required. `youterm` looks for one password entry containing the API key at
`api/youtube`, or any custom specified entry[^1], in the password-store[^2].
Alternatively you can pass the API key to `youterm` as a command line argument
(see [Usage](#Usage)) or using a config file[^3] (see
[Configuration](#Configuration)).

[^1]: You can specify custom `pass` entries for the API key using a config file
  (see [Configuration](#Configuration))
[^2]: Create entry using `pass insert api/youtube` or `pass insert <entry>` for
  custom entry (where `<entry>` is a placeholder for the actual entry name)
[^3]: *Not recommended*

## Installation

Install `youterm` using `pip`:

```bash
pip3 install youterm
```

## Usage

Invoking `youterm` with no flags defaults to audio only. Below the usage:

```
usage: youterm [-h] [-v] [-r <n>] [-a <api_key>] [-q <resolution>]

CLI tool to search for YouTube videos and play selected audio/video via MPV

options:
  -h, --help            show this help message and exit
  -v, --video           Play video
  -r <n>, --results <n>
                        Number of search results displayed
  -a <api_key>, --api <api_key>
                        YouTube Data API v3 key
  -q <resolution>, --quality <resolution>
                        Choose video quality (if not available choose closest lower)
```

## Configuration

You can specify your default options for `youterm` using a config file[^4]
located at:
[^4]: `ini` file structure

- `~/.config/youterm/config` on **Linux** and Unix based systems (following
  the XDG Base Directory specifications)
- `C:\Users\<username>\AppData\Roaming\youterm\config` on **Windows** systems
  (where `<username>` is a placeholder for the actual user name)

Below follows a configuration template:

```ini
[api]
# YouTube Data API v3 key (can be overridden using CLI argument)
key = <api_key>
# pass entry containing the API key (if you want to use pass to store the key)
# if not set defaults to: "api/youtube"
pass_entry = <pass_entry>

[search]
# default number of search results (can be overridden using CLI argument)
# if not set defaults to: 5
results = <num>

[video]
# default video resolution (can be overridden using CLI argument)
# if not set defaults to: bestvideo
# valid options are: 144, 240, 360, 480, 720, 1080, 1440, 2160
quality = <video_resolution>
```

## Changelog

For the complete changelog see [CHANGELOG.md](./CHANGELOG.md).
