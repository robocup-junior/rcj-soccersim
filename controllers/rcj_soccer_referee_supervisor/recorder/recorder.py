from controller import Supervisor


class VideoRecordAssistant:

    def __init__(self, supervisor, resolution="720p"):
        self.supervisor = supervisor
        self.resolution = resolution

        if not isinstance(self.supervisor, Supervisor):
            raise TypeError()

    def create_title(self):
        title = "test.mp4"
        return title

    def get_resolution(self):
        res_table = {"480p": (720, 480),
                     "720p": (1280, 720),
                     "1080p": (1920, 1080)}

        if(self.resolution not in res_table):
            raise ValueError("Invalid Resolution")

        return res_table[self.resolution]

    def start_recording(self):
        width, height = self.get_resolution()
        filename = "./"+self.create_title()
        self.supervisor.movieStartRecording(filename,
                                            width,
                                            height,
                                            quality=100,
                                            codec=0,
                                            acceleration=1,
                                            caption=False)
        return

    def stop_recording(self):
        self.supervisor.movieStopRecording()
        return
