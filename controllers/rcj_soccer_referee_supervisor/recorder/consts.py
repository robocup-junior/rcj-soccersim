from enum import Enum


class RecordingFormat(Enum):
    MP4 = "mp4"
    X3D = "x3d"

    @classmethod
    def all(cls):
        return list(map(lambda member: member.value, cls))


class RecordingFileSuffix(Enum):
    MP4 = "mp4"
    X3D = "html"
