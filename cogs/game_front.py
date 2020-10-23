import discord
from discord.ext import commands
from pyboy import WindowEvent
from threading import Thread

from utils.game import *
from utils.secret_things import TESTERS

class GameFrontEnd(commands.Cog):
    def __init__(self, client):
        self.client = client

    # events
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        pass

    # commands
    @commands.command(aliases=["pokemon"])
    async def init(self, ctx):
        self.pyboy = pokemon()
        for i in range(1500):
            self.pyboy.tick()
    
    @commands.command()
    async def frame(self, ctx, nb:int):
        for i in range(nb):
            self.pyboy.tick()
    
    @commands.command()
    async def close(self, ctx):
        self.pyboy.stop()
    
    @commands.command()
    async def abutton(self, ctx, nb=30):
        for i in range(nb):
            self.pyboy.send_input(WindowEvent.PRESS_BUTTON_A)
            self.pyboy.tick()
    
    @commands.command()
    async def bbutton(self, ctx, nb=30):
        for i in range(nb):
            self.pyboy.send_input(WindowEvent.PRESS_BUTTON_B)
            self.pyboy.tick()
    
    @commands.command()
    async def darrow(self, ctx, nb=30):
        for i in range(nb):
            self.pyboy.send_input(WindowEvent.PRESS_ARROW_DOWN)
            self.pyboy.tick()
    
    @commands.command()
    async def uarrow(self, ctx, nb=30):
        for i in range(nb):
            self.pyboy.send_input(WindowEvent.PRESS_ARROW_UP)
            self.pyboy.tick()
    
    @commands.command()
    async def larrow(self, ctx, nb=30):
        for i in range(nb):
            self.pyboy.send_input(WindowEvent.PRESS_ARROW_LEFT)
            self.pyboy.tick()
    
    @commands.command()
    async def rbutton(self, ctx, nb=30):
        for i in range(nb):
            self.pyboy.send_input(WindowEvent.PRESS_ARROW_RIGHT)
            self.pyboy.tick()
    
    @commands.command()
    async def sbutton(self, ctx,nb=30):
        for i in range(nb):
            self.pyboy.send_input(WindowEvent.PRESS_BUTTON_START)
            self.pyboy.tick()
    
    @commands.command()
    async def loop(self, ctx):
        def gloop():
            while not self.pyboy.tick():
                pass
        
        mloop = Thread(target=gloop)
        mloop.start()


def setup(client):
    client.add_cog(GameFrontEnd(client))
