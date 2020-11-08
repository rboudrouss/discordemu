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
        self.message = None
        self.BINDS = {
            # a/b buttons
            'a':(WindowEvent.PRESS_BUTTON_A, WindowEvent.RELEASE_BUTTON_A),
            'b':(WindowEvent.PRESS_BUTTON_B, WindowEvent.RELEASE_BUTTON_B),
            # start/select buttons
            's':(WindowEvent.PRESS_BUTTON_START,WindowEvent.RELEASE_BUTTON_START),
            'S':(WindowEvent.PRESS_BUTTON_SELECT,WindowEvent.RELEASE_BUTTON_SELECT),
            # arrows
            'u':(WindowEvent.PRESS_ARROW_UP,WindowEvent.RELEASE_ARROW_UP),
            'd':(WindowEvent.PRESS_ARROW_DOWN,WindowEvent.RELEASE_ARROW_DOWN),
            'r':(WindowEvent.PRESS_ARROW_RIGHT,WindowEvent.RELEASE_ARROW_RIGHT),
            'l':(WindowEvent.PRESS_ARROW_LEFT,WindowEvent.RELEASE_ARROW_LEFT)
        }

    async def add_allreactions(self):
        print("\nadding reactions...")
        await self.message.add_reaction('⬅️')  # arrow left
        await self.message.add_reaction('⬆️')  # arrow up
        await self.message.add_reaction('⬇️')  # arrow down
        await self.message.add_reaction('➡️')  # arrow right
        await self.message.add_reaction('🅰️')  # a button
        await self.message.add_reaction('🅱️')  # b button
        await self.message.add_reaction('⏺️')  # Start button
        await self.message.add_reaction('🔴')  # frames
        print('reactions added !')

    async def send_last_screen(self, ctx=None):

        if len(os.listdir("./screenshots/"))>10:
            os.remove("./screenshots/"+os.listdir("./screenshots/")[0])
        
        self.pyboy.send_input(WindowEvent.SCREENSHOT_RECORD)
        self.pyboy.tick()
        os.listdir("./screenshots/")
        
        channel = self.client.get_channel(774982243524280360)
        message = await channel.send(file=discord.File("./screenshots/"+os.listdir("./screenshots/")[-1]))
        url = message.attachments[0].url
        em = discord.Embed()
        em.set_image(url=url)
        
        if not self.message:
            self.message = await ctx.send(embed=em)
            await self.add_allreactions()
        else:
            await self.message.edit(embed=em)
    
    def get_button(self,button):
        return self.BINDS.get(button)

    async def click_button(self, button, nb, ctx=None):
        button,release = self.get_button(button)
        self.pyboy.send_input(button)
        for i in range(30):
            self.pyboy.tick()
        self.pyboy.send_input(release)
        await self.send_last_screen(ctx)
        if ctx:
            await ctx.message.delete()
        

    # events
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if self.user != user:
            return
        elif reaction.emoji in ["⬅️", "⬆️", "⬇️", "➡️", "🅰️", "🅱️",'⏺️','🔴']:
            try:
                await reaction.remove(user)
            except discord.errors.Forbidden:
                await self.client.send_message(user, 'I actually need the "manage messages" permission to actually delete the reaction --\'')

        if reaction.emoji == "⬅️":
            await self.click_button("l",30)
        elif reaction.emoji == "⬆️":
            await self.click_button("u",30)
        elif reaction.emoji == "⬇️":
            await self.click_button("d",30)
        elif reaction.emoji == "➡️":
            await self.click_button("r",30)
        elif reaction.emoji == "🅰️":
            await self.click_button("a",30)
        elif reaction.emoji == "🅱️":
            await self.click_button("b",30)
        elif reaction.emoji == '⏺️':
            await self.click_button("s",30)
        elif reaction.emoji == '🔴':
            for i in range(120):
                self.pyboy.tick()
            await self.send_last_screen()


    # commands
    @commands.command(aliases=["pokemon"])
    async def init(self, ctx):
        self.user = ctx.author
        self.pyboy = pokemon()
        await ctx.send("please wait")
        for i in range(1500):
            self.pyboy.tick()
        await self.send_last_screen(ctx)
    
    @commands.command(aliases=["f",'p'])
    async def frame(self, ctx, nb=120):
        for i in range(nb):
            self.pyboy.tick()
        await self.send_last_screen(ctx)
        await ctx.message.delete()
    
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
