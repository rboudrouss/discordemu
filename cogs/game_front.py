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
    
    def tick(self,nb=30):
        for i in range(nb):
            self.pyboy.tick()
    

    def get_button(self,button):
        # TODO optimiser ça avec un dico ou en utilisant des ints
        if button == "a":
            button = WindowEvent.PRESS_BUTTON_A
            release = WindowEvent.RELEASE_BUTTON_A
        elif button == "b":
            button = WindowEvent.PRESS_BUTTON_B
            release = WindowEvent.RELEASE_BUTTON_B
        elif button == "s":
            button = WindowEvent.PRESS_BUTTON_START
            release = WindowEvent.RELEASE_BUTTON_START
        elif button == "S":
            button = WindowEvent.PRESS_BUTTON_SELECT
            release = WindowEvent.RELEASE_BUTTON_SELECT
        elif button == "d":
            button = WindowEvent.PRESS_ARROW_DOWN
            release = WindowEvent.RELEASE_ARROW_DOWN
        elif button == "u":
            button = WindowEvent.PRESS_ARROW_UP
            release = WindowEvent.PRESS_ARROW_UP
        elif button == "r":
            button = WindowEvent.PRESS_ARROW_RIGHT
            release = WindowEvent.RELEASE_ARROW_LEFT
        elif button == 'l':
            button = WindowEvent.PRESS_ARROW_LEFT
            release = WindowEvent.RELEASE_ARROW_LEFT
        return (button,release)

    async def click_button(self, button, nb, ctx):
        button,release = self.get_button(button)
        for i in range(nb):
            self.pyboy.send_input(button)
            self.pyboy.tick()
        for i in range(nb):
            self.pyboy.send_input(release)
            self.pyboy.tick()
        for i in range(100):
            self.pyboy.tick()
        await self.send_last_screen(ctx)
        

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
    
    @commands.command(aliases=["f",'p'])
    async def frame(self, ctx, nb=100):
        for i in range(nb):
            self.pyboy.tick()
        await self.send_last_screen(ctx)
    
    @commands.command(aliases=["c"])
    async def close(self, ctx):
        if self.mloop:
            self.mloop.terminate()
        await ctx.send("`closing game...`")
        self.pyboy.stop()
        await ctx.send("`game closed`")
    
    @commands.command(aliases=["a"])
    async def abutton(self, ctx, nb=30):
        await self.click_button("a",nb,ctx)
    
    @commands.command(aliases=["b"])
    async def bbutton(self, ctx, nb=30):
        await self.click_button('b',nb,ctx)
    
    @commands.command(aliases=["d"])
    async def darrow(self, ctx, nb=30):
        await self.click_button('d',nb,ctx)

    @commands.command(aliases=["r"])
    async def rarrow(self, ctx, nb=30):
        await self.click_button('r',nb,ctx)
    
    @commands.command(aliases=["u"])
    async def uarrow(self, ctx, nb=30):
        await self.click_button('u',nb,ctx)
    
    @commands.command(aliases=["l"])
    async def larrow(self, ctx, nb=30):
        await self.click_button('l',nb,ctx)
    
    @commands.command(aliases=["s"])
    async def sbutton(self, ctx,nb=30):
        await self.click_button('s',nb,ctx)
    
    @commands.command(aliases=["S"])
    async def slbutton(self, ctx,nb=30):
        await self.click_button('S',nb,ctx)
    
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
