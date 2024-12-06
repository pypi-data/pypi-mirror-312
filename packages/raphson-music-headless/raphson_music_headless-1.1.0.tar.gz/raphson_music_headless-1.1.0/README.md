# Headless playback server for Raphson Music

Client for the Raphson Music server that can be controlled remotely via a simple web interface or [Home Assistant](https://codeberg.org/raphson/music-headless-ha/).

## Installation

### Using pipx (recommended)

```
pipx install raphson-music-headless
```

Run: `raphson-music-headless`

### Using distribution packages
 * Debian: `apt install python3-aiohttp python3-vlc`
 * Fedora: `dnf install python3-aiohttp python3-vlc`

Then install the rest from PyPi: `pip install --user raphson-music-headless`

### From Git
```
git clone https://codeberg.org/raphson/music-headless
cd music-headless
python3 -m raphson_music_headless
```

To install:
```
pip install --user .
```

## Usage

1. Create a `config.json` file with credentials (see `config.json.example`).
2. Run `raphson-music-headless --config config.json`

By default, the program looks for a configuration file at `/etc/raphson-music-headless.json`.

## API

See [API.md](./docs/API.md)

## Temporary files

The server writes music to temporary files so VLC can access them. On Linux, the `/tmp` directory is used for this purpose. It is strongly recommended to mount `tmpfs` on `/tmp` to avoid unnecessary writes to your disk, especially when using a Raspberry Pi with sd card.

Check if it is the case by running `mount | grep /tmp`. It should show something like: `tmpfs on /tmp type tmpfs ...`

## Cache size

The `cache_size` setting determines the number of cached tracks for each playlist. These tracks are kept in memory, consuming roughly 3 - 6MB per track including cover image. Say `cache_size` is set to 4 and you use a maximum of 10 playlists, you will need around 200MiB of memory.

## Bugs

When playing mono audio (like news), sound may only be played on the left channel. This appears to be an issue with PipeWire.
