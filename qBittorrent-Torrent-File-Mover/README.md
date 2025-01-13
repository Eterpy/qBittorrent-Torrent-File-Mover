# qBittorrent Torrent File Mover

This Python script interacts with the qBittorrent Web API to automate the process of moving completed torrents to specific folders based on their filenames. It uses pattern matching using regular expressions to categorize and organize torrents.

## Requirements

- Python 3.x
- `requests` library

To install the required dependencies, run:

```bash
pip install -r requirements.txt
```

## Parameters in  `config.json` file
- **qbittorrent.url**: The URL of your qBittorrent Web UI (usually `http://localhost:8080`).
- **qbittorrent.username**: Your qBittorrent Web UI username.
- **qbittorrent.password**: Your qBittorrent Web UI password.
- **target_dir**: The base directory where torrents will be moved to.
- **patterns**: Note that the key represents the name of the target folder, and the value is a regular expression pattern that matches the torrent file name.

## Usage

1. Ensure your qBittorrent Web UI is running and accessible (**Must enable "Remote control" (Tools->Preferences->Web UI->Web User Interface)**.
2. Modify the `config.json` file.
3. Run the script:

```bash
python qBittorrent_move.py
```

4. If you want to automatically run the program after a torrent finishes downloading, set it up in qBittorent.

## Logging

All log messages (info, warnings, errors) will be printed to the console. You can modify the logging configuration in the script to log to a file if needed.

## Notes

- The script will only move torrents that are completed (not downloading).
- If a torrent file is already in the correct folder, it will not be moved.
- You can expand the regular expression patterns in `config.json` to suit your needs.
- This project has only been tested on **Mac and qBittorrent v5.0.0 and above**, and further testing is needed on Windows and Linux. **(Todo)**

## License

This project is open-source and available under the MIT License.

## TODO

| Task                                              | State |
| ------------------------------------------------- | ----- |
| Test running on Windows                           | ⬜     |
| Test running on Linux                             | ⬜     |
| Test running on Tests run on versions below 5.0.0 | ⬜     |