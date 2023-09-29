import datetime
import time
from pathlib import Path

from controller import Supervisor

from recorder.consts import RecordingFileSuffix


class BaseVideoRecordAssistant:
    output_suffix = ""

    def __init__(
        self,
        supervisor: Supervisor,
        output_path: str = "",
        fastforward_rate: int = 1,
        resolution: str = "720p",
    ):
        self.supervisor = supervisor
        self.output_path = output_path
        self.fastforward_rate = fastforward_rate
        self.resolution = resolution

        self._is_recording = False

        if not isinstance(self.supervisor, Supervisor):
            raise TypeError("Unexpected supervisor instance")

    def create_title(self):
        if self.output_path == "":
            # When output path is not specified
            time_str = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
            return "{}/{}.{}".format(
                str(Path.home()), time_str, self.output_suffix
            )

        return self.output_path

    def get_resolution(self):
        res_table = {
            "480p": (720, 480),
            "720p": (1280, 720),
            "1080p": (1920, 1080),
        }

        if self.resolution not in res_table:
            raise ValueError("Invalid Resolution")

        return res_table[self.resolution]

    def start_recording(self):
        raise NotImplementedError

    def stop_recording(self):
        raise NotImplementedError

    def is_recording(self):
        return self._is_recording

    def wait_processing(self):
        raise NotImplementedError


class MP4VideoRecordAssistant(BaseVideoRecordAssistant):
    output_suffix = RecordingFileSuffix.MP4.value

    def start_recording(self):
        width, height = self.get_resolution()
        filename = self.create_title()

        # API details for movieStartRecording
        # https://www.cyberbotics.com/doc/reference/supervisor?tab-language=python#wb_supervisor_movie_start_recording
        self.supervisor.movieStartRecording(
            filename,
            width,
            height,
            quality=100,
            codec=0,
            acceleration=self.fastforward_rate,
            caption=False,
        )

        self._is_recording = True

    def stop_recording(self):
        self.supervisor.movieStopRecording()
        self._is_recording = False

    def wait_processing(self):
        while not self.supervisor.movieIsReady():
            time.sleep(1.0)


class X3DVideoRecordAssistant(BaseVideoRecordAssistant):
    output_suffix = RecordingFileSuffix.X3D.value

    def start_recording(self):
        filename = self.create_title()
        self.supervisor.animationStartRecording(filename)
        self._is_recording = True

    def stop_recording(self):
        self.supervisor.animationStopRecording()
        self._is_recording = False

    def wait_processing(self):
        pass
