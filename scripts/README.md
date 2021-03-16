# Scripts

## generate-soccer-world.py

A script used for generating Webots worlds that power the RoboCupJunior Soccer
Simulator. This script allows one to specify the colors of each side, the cover
images of robots as well as the controllers that ought to control the
respective robots.

To generate the "sample" world (located in `world/soccer.wbt`), run the
following command:

```bash
$ python generate-soccer-world.py \
    --template=templates/soccer.wbt.template \
    --blue_rgb='0 0 1' --yellow_rgb='1 1 0' \
    --blue_png_url='soccer/blue.png' \
    --yellow_png_url='soccer/yellow.png' \
    --controller_blue='rcj_soccer_player' \
    --controller_yellow='rcj_soccer_player'  > soccer.wbt
```

Among other things, this allows us to switch team sides without changing the
internal logic of the simulation.
