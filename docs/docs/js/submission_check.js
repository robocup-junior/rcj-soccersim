function get_submission_errors(zipsize, entries) {
    var errors = [];
    var has_team_name_txt = false;
    var has_robot_dir = false;
    var has_robot_py = false;

    for (var i = 0; i < entries.length; i++) {
        var entry = entries[i];

        if (entry.filename === "team_name.txt" && !entry.directory) {
            has_team_name_txt = true;
        }
        if (entry.filename === "robot/robot.py" && !entry.directory) {
            has_robot_py = true;
        }

        if (entry.directory) {
            if (entry.filename === "robot/") {
                has_robot_dir = true;
            } else if ((entry.filename.split("/").length - 1) == 1) {
                /* Check whether there is just one top-level folder */
                errors.push("Found " + entry.filename + ". Only one top-level folder allowed!");
            }
        }
    }

    if (!has_team_name_txt) {
        errors.push("team_name.txt file not found in the submission!");
    }

    if (!has_robot_dir) {
        errors.push("robot/ directory not found in the submission!");
    }

    if (!has_robot_py) {
        errors.push("robot.py file not found within robot/ folder in the submission!");
    }

    if (zipsize > 10000000) {
        errors.push("The submission exceeds 10 MB allowed size!");
    }

    return errors;
}
