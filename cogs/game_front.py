import os,sys
import discord
from discord.ext import commands
from pyboy import WindowEvent
from threading import Thread

from utils.game import *
from utils.secret_things import TESTERS

class GameFrontEnd(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.mloop = None

    async def send_last_screen(self, ctx):
        if len(os.listdir("./screenshots/"))>10:
            os.remove("./screenshots/"+os.listdir("./screenshots/")[0])
        self.pyboy.send_input(WindowEvent.SCREENSHOT_RECORD)
        for i in range(100):
            self.pyboy.tick()
        os.listdir("./screenshots/")
        await ctx.send('fromage',file=discord.File("./screenshots/"+os.listdir("./screenshots/")[-1]))

    # events
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        pass

    # commands
    @commands.command(aliases=["pokemon"])
    async def init(self, ctx):
        self.pyboy = pokemon()
        await ctx.send("please wait")
        for i in range(1500):
            self.pyboy.tick()
        await self.send_last_screen(ctx)
    
    @commands.command()
    async def frame(self, ctx, nb=100):
        for i in range(nb):
            self.pyboy.tick()
        await self.send_last_screen(ctx)
    
    @commands.command()
    async def close(self, ctx):
        if self.mloop:
            self.mloop.terminate()
        await ctx.send("`closing game...`")
        self.pyboy.stop()
        await ctx.send("`game closed`")
    
    @commands.command()
    async def abutton(self, ctx, nb=30):
        print(nb)
        for i in range(nb):
            self.pyboy.send_input(WindowEvent.PRESS_BUTTON_A)
            self.pyboy.tick()
        for i in range(nb):
            self.pyboy.send_input(WindowEvent.RELEASE_BUTTON_A)
            self.pyboy.tick()
        for i in range(100):
            self.pyboy.tick()
        await self.send_last_screen(ctx)
    
    @commands.command()
    async def bbutton(self, ctx, nb=30):
        for i in range(nb):
            self.pyboy.send_input(WindowEvent.PRESS_BUTTON_B)
            self.pyboy.tick()
        for i in range(nb):
            self.pyboy.send_input(WindowEvent.RELEASE_BUTTON_B)
            self.pyboy.tick()
        for i in range(100):
            self.pyboy.tick()
        await self.send_last_screen(ctx)
    
    @commands.command()
    async def darrow(self, ctx, nb=30):
        for i in range(nb):
            self.pyboy.send_input(WindowEvent.PRESS_ARROW_DOWN)
            self.pyboy.tick()
        for i in range(nb):
            self.pyboy.send_input(WindowEvent.RELEASE_ARROW_DOWN)
            self.pyboy.tick()
        for i in range(100):
            self.pyboy.tick()
        await self.send_last_screen(ctx)

    @commands.command()
    async def rarrow(self, ctx, nb=30):
        for i in range(nb):
            self.pyboy.send_input(WindowEvent.PRESS_ARROW_RIGHT)
            self.pyboy.tick()
        for i in range(nb):
            self.pyboy.send_input(WindowEvent.RELEASE_ARROW_RIGHT)
            self.pyboy.tick()
        for i in range(100):
            self.pyboy.tick()
        await self.send_last_screen(ctx)
    
    @commands.command()
    async def uarrow(self, ctx, nb=30):
        for i in range(nb):
            self.pyboy.send_input(WindowEvent.PRESS_ARROW_UP)
            self.pyboy.tick()
        for i in range(nb):
            self.pyboy.send_input(WindowEvent.RELEASE_ARROW_UP)
            self.pyboy.tick()
        for i in range(100):
            self.pyboy.tick()
        await self.send_last_screen(ctx)
    
    @commands.command()
    async def larrow(self, ctx, nb=30):
        for i in range(nb):
            self.pyboy.send_input(WindowEvent.PRESS_ARROW_LEFT)
            self.pyboy.tick()
        for i in range(nb):
            self.pyboy.send_input(WindowEvent.RELEASE_ARROW_LEFT)
            self.pyboy.tick()
        for i in range(100):
            self.pyboy.tick()
        await self.send_last_screen(ctx)
    
    
    @commands.command()
    async def sbutton(self, ctx,nb=30):
        for i in range(nb):
            self.pyboy.send_input(WindowEvent.PRESS_BUTTON_START)
            self.pyboy.tick()
        for i in range(nb):
            self.pyboy.send_input(WindowEvent.RELEASE_BUTTON_START)
            self.pyboy.tick()
        for i in range(100):
            self.pyboy.tick()
        await self.send_last_screen(ctx)
    
    @commands.command()
    async def slbutton(self, ctx,nb=30):
        for i in range(nb):
            self.pyboy.send_input(WindowEvent.PRESS_BUTTON_SELECT)
            self.pyboy.tick()
        for i in range(nb):
            self.pyboy.send_input(WindowEvent.RELEASE_BUTTON_SELECT)
            self.pyboy.tick()
        for i in range(100):
            self.pyboy.tick()
        await self.send_last_screen(ctx)
    
    
    @commands.command()
    async def loop(self, ctx):
        # FIXME
        def gloop():
            while not self.pyboy.tick():
                pass
        
        self.mloop = Thread(target=gloop)
        self.mloop.start()


def setup(client):
    client.add_cog(GameFrontEnd(client))
