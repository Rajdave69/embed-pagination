import discord
from discord.ext import commands


class Simple(discord.ui.View):
    """
    Embed Paginator.

    Parameters:
    ----------
    timeout: int
        How long the Paginator should time out in, after the last interaction. (In seconds) (Overrides default of 60)
    previous_button: discord.ui.Button
        Overrides default previous button.
    next_button: discord.ui.Button
        Overrides default next button.
    page_counter_style: discord.ButtonStyle
        Overrides default page counter style.
    initial_page: int
        Page to start the pagination on.
    allow_ext_input: bool
        Overrides ability for 3rd party to interact with button.
    delete_on_timeout: bool
        Deletes the paginator when timeout occurs if set to True.
    """

    def __init__(self, *,
                 timeout: int = 60,
                 previous_button: discord.ui.Button = discord.ui.Button(emoji=discord.PartialEmoji(name="\U000025c0")),
                 next_button: discord.ui.Button = discord.ui.Button(emoji=discord.PartialEmoji(name="\U000025b6")),
                 page_counter_style: discord.ButtonStyle = discord.ButtonStyle.grey,
                 initial_page: int = 0,
                 allow_ext_input: bool = False,
                 delete_on_timeout: bool = False,
                 ephemeral: bool = False) -> None:

        self.previous_button = previous_button
        self.next_button = next_button
        self.page_counter_style = page_counter_style
        self.InitialPage = initial_page
        self.AllowExtInput = allow_ext_input
        self.DeleteOnTimeout = delete_on_timeout
        self.ephemeral = ephemeral

        self.pages = None
        self.ctx = None
        self.message = None
        self.current_page = None
        self.page_counter = None
        self.total_page_count = None

        super().__init__(timeout=timeout)

    async def start(self, ctx: discord.Interaction | commands.Context, pages: list[discord.Embed]):
        if isinstance(ctx, discord.Interaction):
            ctx = await commands.Context.from_interaction(ctx)
        if len(pages) == 0:
            raise ValueError("Pages must contain at least 1 embed.")

        self.pages = pages
        self.total_page_count = len(pages)
        self.ctx = ctx
        self.current_page = self.InitialPage

        self.previous_button.callback = self.previous_button_callback
        self.next_button.callback = self.next_button_callback

        self.page_counter = SimplePaginatorPageCounter(style=self.page_counter_style,
                                                       total_pages=self.total_page_count,
                                                       initial_page=self.InitialPage)

        self.add_item(self.previous_button)
        self.add_item(self.page_counter)
        self.add_item(self.next_button)

        self.message = await ctx.send(embed=self.pages[self.InitialPage], view=self, ephemeral=self.ephemeral)

    async def previous(self):
        if self.current_page == 0:
            self.current_page = self.total_page_count - 1
        else:
            self.current_page -= 1

        self.page_counter.label = f"{self.current_page + 1}/{self.total_page_count}"
        await self.message.edit(embed=self.pages[self.current_page], view=self)

    async def next(self):
        if self.current_page == self.total_page_count - 1:
            self.current_page = 0
        else:
            self.current_page += 1

        self.page_counter.label = f"{self.current_page + 1}/{self.total_page_count}"
        await self.message.edit(embed=self.pages[self.current_page], view=self)

    async def next_button_callback(self, interaction: discord.Interaction):
        if interaction.user != self.ctx.author and self.AllowExtInput:
            embed = discord.Embed(description="This pagination was not executed by you.",
                                  color=discord.Colour.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        await self.next()
        await interaction.response.defer()

    async def previous_button_callback(self, interaction: discord.Interaction):
        if interaction.user != self.ctx.author and self.AllowExtInput:
            embed = discord.Embed(description="This pagination was not executed by you.",
                                  color=discord.Colour.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        await self.previous()
        await interaction.response.defer()

    # Override default implementation in discord.ui.View
    async def on_timeout(self) -> None:
        if self.DeleteOnTimeout:
            await self.message.delete()


class SimplePaginatorPageCounter(discord.ui.Button):
    def __init__(self, style: discord.ButtonStyle, total_pages, initial_page):
        super().__init__(label=f"{initial_page + 1}/{total_pages}", style=style, disabled=True)
