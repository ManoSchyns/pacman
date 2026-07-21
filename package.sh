#!/bin/bash

set -e

rm -rf pacman_42.zip

pyinstaller --onefile \
    --name pacman_42 \
    --add-data "assets:assets" \
    --add-data "game/srcs:game/srcs" \
    --add-data "sprietsheet:sprietsheet" \
    main.py

cp config.json dist/

cat > dist/README.md << EOF
PACMAN 42

Launch:
    ./pacman_42 config.json

Controls:
    Arrow keys : Move Pacman
    SPACE      : Skip Level
    ESC        : Pause Menu

Configuration:
    The game uses the JSON configuration file provided as argument.

The configuration file supports:
    - level_list
    - lives
    - pacgum
    - points_per_pacgum
    - points_per_super_pacgum
    - points_per_ghost
    - seed
    - level_max_time

If a value is missing or invalid, a default value is used.
EOF

(cd dist && zip -r ../pacman_42.zip pacman_42 config.json README.md)

rm -rf build dist pacman_42.spec