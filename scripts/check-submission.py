import os
import sys
import zipfile


def fail(message):
    print("FAIL: {}".format(message))
    sys.exit(1)


if len(sys.argv) != 2:
    fail("usage: python3 {} <path to zip>".format(sys.argv[0]))

submission = sys.argv[1]
if not os.path.exists(submission):
    fail("Path to {} does not exist!".format(submission))

if not zipfile.is_zipfile(submission):
    fail("{} is not a zip file!".format(submission))

archive = zipfile.ZipFile(submission, "r")
namelist = archive.namelist()

if "robot/" not in namelist:
    fail("robot/ folder not found in {}".format(submission))

if "robot/robot.py" not in namelist:
    fail("robot.py not found within robot/ folder in {}".format(submission))

if "team_name.txt" not in namelist:
    fail("team_name.txt not found in {}".format(submission))

for entry in namelist:
    if entry != "robot/" and entry.endswith("/") and entry.count("/") == 1:
        fail("{} found. Only one top-level folder allowed in {}".format(
                entry, submission
            )
        )

print("SUCCESS: {} looks fine!".format(submission))

