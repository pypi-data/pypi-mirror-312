import os
import yt_dlp
from cli_logger.logger import setup_logger
from shared.config import LOGGER_CONFIG
from pytoolbox.file_system import ensure_folder_exists
from keyval_storage.config_and_key_value_storage_data_model import ConfigAndKeyValueStorageDataModel
from shared.constants import APP_NAME, DOWNLOAD_FOLDER_KEY

logger = setup_logger(__name__, LOGGER_CONFIG)

class VideoToMp3():      
    def __init__(self):
        self._output_folder: str = ''
        self._dataStorage = ConfigAndKeyValueStorageDataModel(APP_NAME)

    def run(self, args: str):
        argsList = args.split()

        logger.debug("argsList:", argsList, "Length:", len(argsList))
        
        if len(argsList) != 1:
            logger.error("Error: One argument is required - video_url.")
            return

        video_url = argsList[0]

        if not self._is_valid_video_url(video_url):
            logger.error("Invalid video URL format. URL must be a valid YouTube link.")
            return
        
        dataStorage = self._dataStorage.getKeyValueStorage_LoadUsingConfig()
        self._output_folder = dataStorage.get(DOWNLOAD_FOLDER_KEY)

        if not self._output_folder:
            output_folder = input("Provide folder to SAVE downloads> ").strip()
            ensure_folder_exists(output_folder)
            self._output_folder = output_folder
            dataStorage.set(DOWNLOAD_FOLDER_KEY, self._output_folder)
        
        try:
            self._download_youtube_as_mp3(video_url)

        except ValueError as e:
            logger.error(f"Error: {e}.")
        except Exception as e:
            logger.error(f"Unexpected Error: {str(e)}")

    def _is_valid_video_url(self, video_url: str):
        return isinstance(video_url, str) and ("youtube.com/watch?v=" in video_url or "youtu.be/" in video_url)

    def _download_youtube_as_mp3(self, video_url: str):
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': os.path.join(self._output_folder, '%(title)s.%(ext)s'),
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            
            logger.info("Download and conversion to MP3 completed.")
        
        except Exception as e:
            logger.error(f"Error: {str(e)}")
