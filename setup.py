'''setup.py'''

import cx_Freeze

executables = [cx_Freeze.Executable("snake.py")]

cx_Freeze.setup(
    name="Snake RPG",
    options={"build_exe":{"packages":["pygame"],"include_files":["EightBitDragon.ttf","snake_body.png","snake_head.png","snake_tail.png","snake_turn.png","apple.png"]}},
    description="A Snake Game with RPG Elements",
    executables = executables
)
