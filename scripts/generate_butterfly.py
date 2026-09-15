import os
import random
from datetime import datetime, timedelta

USERNAME = os.environ.get("GITHUB_REPOSITORY_OWNER", "github")

WIDTH = 1050
HEIGHT = 180

CELL = 12
GAP = 3
STEP = CELL + GAP

START_X = 20
START_Y = 45

COLORS = [
    "#161b22",
    "#0e4429",
    "#006d32",
    "#26a641",
    "#39d353",
]

random.seed(42)

# Generate a GitHub-style contribution grid
weeks = 53
days = 7

grid = []

for week in range(weeks):
    column = []

    for day in range(days):
        level = random.choices(
            range(5),
            weights=[35, 25, 20, 13, 7]
        )[0]

        column.append(level)

    grid.append(column)


# Butterfly SVG
butterfly = """
<g id="butterfly">
    <g>
        <animateTransform
            attributeName="transform"
            type="translate"
            values="0 0; 0 -5; 0 0; 0 5; 0 0"
            dur="0.8s"
            repeatCount="indefinite"/>

        <!-- Left wing -->
        <ellipse
            cx="-7"
            cy="-4"
            rx="8"
            ry="11"
            fill="#ff69b4"
            opacity="0.9"/>

        <!-- Right wing -->
        <ellipse
            cx="7"
            cy="-4"
            rx="8"
            ry="11"
            fill="#b66cff"
            opacity="0.9"/>

        <!-- Lower wings -->
        <ellipse
            cx="-6"
            cy="7"
            rx="6"
            ry="8"
            fill="#ff9de2"
            opacity="0.9"/>

        <ellipse
            cx="6"
            cy="7"
            rx="6"
            ry="8"
            fill="#9d7cff"
            opacity="0.9"/>

        <!-- Body -->
        <ellipse
            cx="0"
            cy="2"
            rx="2"
            ry="10"
            fill="#222"/>

        <!-- Antennae -->
        <path
            d="M -1,-7 Q -6,-14 -9,-13"
            stroke="#222"
            fill="none"
            stroke-width="1"/>

        <path
            d="M 1,-7 Q 6,-14 9,-13"
            stroke="#222"
            fill="none"
            stroke-width="1"/>
    </g>
</g>
"""


# Build contribution squares
squares = ""

for week in range(weeks):
    for day in range(days):

        level = grid[week][day]

        x = START_X + week * STEP
        y = START_Y + day * STEP

        color = COLORS[level]

        squares += f"""
        <rect
            x="{x}"
            y="{y}"
            width="{CELL}"
            height="{CELL}"
            rx="2"
            fill="{color}">
            <animate
                attributeName="opacity"
                values="1;1;0.25;1"
                dur="{random.uniform(2,5):.2f}s"
                begin="{random.uniform(0,5):.2f}s"
                repeatCount="indefinite"/>
        </rect>
        """


# Butterfly path across the grid
path_points = []

for week in range(weeks):
    x = START_X + week * STEP + CELL / 2

    # Move through different rows
    day = week % 7
    y = START_Y + day * STEP + CELL / 2

    path_points.append(f"{x},{y}")


points = " ".join(path_points)


svg = f"""<?xml version="1.0" encoding="UTF-8"?>

<svg
    xmlns="http://www.w3.org/2000/svg"
    width="{WIDTH}"
    height="{HEIGHT}"
    viewBox="0 0 {WIDTH} {HEIGHT}">

    <rect
        width="100%"
        height="100%"
        fill="#0d1117"
        rx="10"/>

    <text
        x="20"
        y="25"
        fill="#8b949e"
        font-family="Arial"
        font-size="13">
        GitHub Contributions
    </text>

    {squares}

    <g>
        <animateMotion
            dur="18s"
            repeatCount="indefinite"
            rotate="auto">
            <mpath href="#butterflyPath"/>
        </animateMotion>

        {butterfly}
    </g>

    <path
        id="butterflyPath"
        d="M {points.replace(' ', ' L ')}"
        fill="none"
        stroke="none"/>

</svg>
"""


os.makedirs("dist", exist_ok=True)

with open("dist/github-butterfly.svg", "w", encoding="utf-8") as f:
    f.write(svg)

print("Butterfly animation generated successfully!")
