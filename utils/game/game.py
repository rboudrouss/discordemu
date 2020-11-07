# import os,sys

from pyboy import PyBoy

def pokemon():
    pyboy = PyBoy(
        'roms/Pokemon-VersionBleue(France).gb',
        window_type="headless", # "SDL2" if hidden
        window_scale=3,
        debug=False,
        game_wrapper=True
    )
    pyboy.set_emulation_speed(0)

    # while not pyboy.tick():
    #     pass

    return pyboy

if __name__ == '__main__':
    pyboy = pokemon()
    pyboy.set_emulation_speed(2)
    while not pyboy.tick():
        pass