import asyncio
import os
import dotenv
from spotdl import Spotdl
from pathlib import Path
import yt_dlp
import argparse

#adding in commands for the terminal interface using argparse

parser = argparse.ArgumentParser(description="Media Downloading tool")
subparsers = parser.add_subparsers(dest="command", help="Available commands")

#Commands and Arguements
download_command = subparsers.add_parser("download", help="Download the media via a link")
download_command.add_argument("--url", help="Provide the URL to download YT/SPOTIFY")
play_command = subparsers.add_parser("play", help="Play your music! upcoming update")

args = parser.parse_args()


dotenv.load_dotenv()


#async needed for modern python netowrking
async def main(url=None):

    while not url:
        url = input("Enter the URL of the media you want to download: ")



    if "spotify" in url:

        #find the music folder
        music_path = Path.home() / "Music"
        if not music_path.is_dir():
            print("Warning! \n Could not find a default Music folder")
            while True:
                custom_folder = input("Enter your Folder name: ")
                if custom_folder:
                    music_path = Path(custom_folder)
                    music_path.mkdir(parents=True, exist_ok=True)
                    break
                print("Input cannot be empty, Please enter a valid name.")

        #authmanager for spotify
        spotdl_client = Spotdl(
            client_id=os.getenv("PUBLIC_KEY"),
            client_secret=os.getenv("SECRET_KEY"),
            downloader_settings={
        "output": f"{music_path.as_posix()}/{{list-name}}/{{artists}} - {{title}}.{{output-ext}}"
        })

        #end of auth

        loop = asyncio.get_event_loop()
        songs = await loop.run_in_executor(None, spotdl_client.search, [url])

            
        if not songs:
            print("No songs found, exiting, check if the provided link is public.")
            return


        #downloading the Songs 
        if "playlist" in url:
            print("Gathering playlist Data")
            print(f"Found {len(songs)} songs, starting download")
            await spotdl_client.download_songs(songs)   
            print(f"Playlist download completed")

        if "track" in url:
            print("Found the song")
            await spotdl_client.download_songs(songs)
            print("Track Download Complete")



    if "youtube.com"  in url:


        #same as in spotify, we check for the Videos Folder in the home directory, if its not there, we ask for an input from the user.
        video_path =  Path.home() / "Videos"
        if not video_path.is_dir():
            print("Warning! \n Could not find a default Video folder")
            while True:
                custom_folder = input("Enter your Folder name: ")
                if custom_folder:
                    video_path = Path(custom_folder)
                    video_path.mkdir(parents=True, exist_ok=True)
                    break
                print("Input cannot be empty, Please enter a valid name.")
            
        ydl_opts = {
        'format': 'best', # Downloads the best quality
        'paths': {'home': str(video_path)},
        'outtmpl': '%(title)s.%(ext)s', # Saves the file using the video title
        }

        def download_yt_vid(url):
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

        print("Starting Youtube Video Download")

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, download_yt_vid, url)       


def main_entry():
    try:
        if args.command == "download":
            asyncio.run(main(args.url))
        elif args.command == "play":
            print("Upcoming update?")
        else:
            parser.print_help()
    except KeyboardInterrupt:
        print("Program stopped by User")