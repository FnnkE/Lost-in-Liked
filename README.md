# Lost in Liked 

This Python project creates a Spotify playlist that contains the songs found in the users "Liked Songs" that aren't in any playlists in their library.

## Table of Contents
---
- [Background](docs/README.md)
    - [Packages](docs/README.md)
    - [Developer Portal](docs/README.md)
    - [.env](docs/README.md)
- [Install](docs/README.md)
- [Usage](docs/README.md)
- [License](docs/README.md)

## Background
---
As an active Spotify user, I've always wanted to integrate programming into my music listening. The way I use the "Liked Songs" feature is a little unique. Sometimes if there is a song that I think I might enjoy, I will "like" the song to go back to later. However, I typically forget and never go back to it. This is how "Lost in Liked" was created. At first I updated it manually but I would always forget to add or remove songs. This repo is the result of me automating the process.

## Install
---
### Packages
Before running the main script, a couple packages need to be downloaded. These are "Spotipy" and "dotenv". These can be installed seperately or you can run the below code to install both.
```
pip install -r requirements.txt
```

### Developer Portal
Additionally, an application will have to be created in the Spotify Developer Portal. More instructions will be created later on how to set up the application. The most important step is to add 'http://lost-in-like.com' as your redirect URL.

### .env
Finally, in the folder with main.py, create a ".env" file formatted the same way as below. Replace the underscores with client ID and secret from the application.
```
CLIENT_ID="___"
CLIENT_SECRET="___"
```

## Usage
---
In order to run the program, open your terminal and navigate to the location of the downloaded file. Run the script using
```
python3 main.py
```
The program will redirect you to an authentication page for Spotify. After accepting, copy the URL and paste it into the terminal. The playlist will be created under the name "</> Lost in Liked". The name can be changed but do not remove the "<LL/>" tag in the description.

Note: The program will look through your playlists to find the tag. Do not delete this and do not add it to another playlist.

## License
---
FnkE © 2023