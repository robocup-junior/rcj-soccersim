from controller import Supervisor

from pathlib import Path
import datetime
import time

import logging


class VideoRecordAssistant:

    def __init__(self,
                 supervisor: Supervisor,
                 output_path: str = "",
                 fastforward_rate: int = 1,
                 resolution: str = "720p"):

        self.supervisor = supervisor
        self.output_path = output_path
        self.fastforward_rate = fastforward_rate
        self.resolution = resolution

        self.__recording = False

        if not isinstance(self.supervisor, Supervisor):
            raise TypeError("Unexpected supervisor instance")

    def create_title(self):

        if self.output_path == "":
            # When output path is not specified
            time_str = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
            return "{}/{}.mp4".format(str(Path.home()), time_str)

        return self.output_path

    def get_resolution(self):
        res_table = {"480p": (720, 480),
                     "720p": (1280, 720),
                     "1080p": (1920, 1080)}

        if self.resolution not in res_table:
            raise ValueError("Invalid Resolution")

        return res_table[self.resolution]

    def start_recording(self):
        width, height = self.get_resolution()
        filename = self.create_title()

        # API details for movieStartRecording
        # https://www.cyberbotics.com/doc/reference/supervisor?tab-language=python#wb_supervisor_movie_start_recording
        self.supervisor.movieStartRecording(filename,
                                            width,
                                            height,
                                            quality=100,
                                            codec=0,
                                            acceleration=self.fastforward_rate,
                                            caption=False)
        self.__recording = True

    def stop_recording(self):
        self.supervisor.movieStopRecording()
        self.__recording = False

    def is_recording(self):
        return self.__recording

    def wait_processing(self):
        logging.info('Processing Video...')
        while not self.supervisor.movieIsReady():
            time.sleep(1.0)

