# custom_commands.py

from job_search.job_search_command import JobSearchCommand
from log_chat.chat_collector_command import ChatCollectorCommand
from log_vid.video_data_command import VideoDataCommand
from scenes.read_scenes_command import ReadScenesCommand
from scenes.write_scene_command import WriteSceneCommand
from shared.config import LOGGER_CONFIG
from cli_logger.logger import setup_logger
#from example.argparse import argparse
#from log_task.log_test import logTest
from log_task.estimate_task import estimateTask
from log_task.report_task import reportTask
from vid_to_mp3.vid_to_mp3_command import VidToMp3Command

logger = setup_logger(__name__, LOGGER_CONFIG)

def load():
    return {
        "vidmp3": VidToMp3Command().run,
        #"ping": lambda _: logger.info('ping'),
        #"argparse": argparse,
        #"logtest": logTest,
        "estimate_task": estimateTask,
        "report_task": reportTask,
        "doc_job": JobSearchCommand().run,
        "doc_chat": ChatCollectorCommand().run,
        "read_scene": ReadScenesCommand().run,
        "doc_scene": WriteSceneCommand().run,
        "doc_vid": VideoDataCommand().run
    }
