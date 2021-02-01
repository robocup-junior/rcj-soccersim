#!/bin/bash
./x11docker/x11docker --gpu --runtime=nvidia --network=none --verbose -- \
-v ${HOME}/webots_video_out/:/out \
-v $(pwd)/teams/${TEAM_Y}/bot1/bot1.py:/app/controllers/rcj_soccer_player_y1/rcj_soccer_player_y1.py:ro \
-v $(pwd)/teams/${TEAM_Y}/bot2/bot2.py:/app/controllers/rcj_soccer_player_y2/rcj_soccer_player_y2.py:ro \
-v $(pwd)/teams/${TEAM_Y}/bot3/bot3.py:/app/controllers/rcj_soccer_player_y3/rcj_soccer_player_y3.py:ro \
-v $(pwd)/teams/${TEAM_Y}/logo.png:/app/worlds/soccer/yellow.png:ro \
--env TEAM_YELLOW_NAME="$(cat $(pwd)/teams/${TEAM_Y}/team_name.txt)" \
-v $(pwd)/teams/${TEAM_B}/bot1/bot1.py:/app/controllers/rcj_soccer_player_b1/rcj_soccer_player_b1.py:ro \
-v $(pwd)/teams/${TEAM_B}/bot2/bot2.py:/app/controllers/rcj_soccer_player_b2/rcj_soccer_player_b2.py:ro \
-v $(pwd)/teams/${TEAM_B}/bot3/bot3.py:/app/controllers/rcj_soccer_player_b3/rcj_soccer_player_b3.py:ro \
-v $(pwd)/teams/${TEAM_B}/logo.png:/app/worlds/soccer/blue.png:ro \
--env TEAM_BLUE_NAME="$(cat $(pwd)/teams/${TEAM_B}/team_name.txt)" \
--env RCJ_SIM_AUTO_MODE=true \
--rm \
-- rcj-soccer-sim
