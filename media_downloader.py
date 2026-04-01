import asyncio
import os
import dotenv
from spotdl import Spotdl
from pathlib import Path

#for future updates if spotify makes their api more accesable
dotenv.load_dotenv()

#async needed for modern python netowrking
async def main():



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
        "output": f"{music_path.as_posix()}{list-name}/{artists} - {title}.{output-ext}"
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

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Program stopped by User")