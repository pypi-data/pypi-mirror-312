import os
import yt_dlp
from cli_logger.logger import setup_logger
from shared.config import LOGGER_CONFIG

logger = setup_logger(__name__, LOGGER_CONFIG)

class VidToMp3:
    
    def validate_and_download(self, video_url: str, output_folder: str):
        logger.info("Running VidToMp3 with URL: %s", video_url)

        if not self._is_valid_vid_url(video_url):
            logger.exception("Invalid video URL format.")
            return

        try:
            self._download_as_mp3(video_url, output_folder)

        except ValueError as e:
            logger.exception(f"Error: {e}.")
        except Exception as e:
            logger.exception(f"Unexpected Error: {str(e)}")

    def _is_valid_vid_url(self, video_url: str):
        return isinstance(video_url, str) and ("youtube.com/watch?v=" in video_url or "youtu.be/" in video_url)

    def _download_as_mp3(self, video_url: str, output_folder: str):
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])

            logger.info("Download and conversion to MP3 completed.")

        except Exception as e:
            logger.error(f"Error: {str(e)}")
