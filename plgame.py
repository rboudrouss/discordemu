from pyboy import PyBoy


pyboy = PyBoy(
    'roms/Pokemon-VersionBleue(France).gb',
    window_type="SDL2", # "headless" if hidden
    window_scale=3,
    debug=False,
    game_wrapper=True
)
pyboy.set_emulation_speed(2)

while not pyboy.tick():
    pass

