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

    def __init__(
            self, *,
            timeout: int = 60,
            first_button: discord.ui.Button = discord.ui.Button(label="<<", style=discord.ButtonStyle.blurple),
            previous_button: discord.ui.Button = discord.ui.Button(label="<", style=discord.ButtonStyle.red),
            next_button: discord.ui.Button = discord.ui.Button(label=">", style=discord.ButtonStyle.green),
            last_button: discord.ui.Button = discord.ui.Button(label=">>", style=discord.ButtonStyle.blurple),
            page_counter_style: discord.ButtonStyle = discord.ButtonStyle.blurple,
            initial_page: int = 0,
            allow_ext_input: bool = False,
            on_timeout: str = 'disable_view',
            ephemeral: bool = False
    ) -> None:

        self.previous_button = previous_button
        self.next_button = next_button
        self.first_button = first_button
        self.last_button = last_button
        self.page_counter_style = page_counter_style
        self.initial_page = initial_page
        self.allow_ext_input = allow_ext_input
        self.ontimeout = on_timeout
        self.ephemeral = ephemeral

        if self.ontimeout not in ['delete_message', 'remove_view', 'disable_view', 'do_nothing']:
            raise ValueError("on_timeout must be one of the following: 'delete_message', 'remove_view', "
                             "'disable_view', 'do_nothing'")
        if self.ontimeout == 'delete_message' and self.ephemeral:
            raise ValueError("Cannot delete message when ephemeral is set to True.")
        if self.ontimeout == 'remove_view' and self.ephemeral:
            raise ValueError("Cannot remove view when ephemeral is set to True.")
        if self.ontimeout == 'disable_view' and self.ephemeral:
            raise ValueError("Cannot disable view when ephemeral is set to True.")

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
        self.current_page = self.initial_page

        self.previous_button.callback = self.previous_button_callback
        self.next_button.callback = self.next_button_callback
        self.first_button.callback = self.first_button_callback
        self.last_button.callback = self.last_button_callback

        self.page_counter = SimplePaginatorPageCounter(
            style=self.page_counter_style,
            total_pages=self.total_page_count,
            initial_page=self.initial_page
        )

        self.add_item(self.first_button)
        self.add_item(self.previous_button)
        self.add_item(self.page_counter)
        self.add_item(self.next_button)
        self.add_item(self.last_button)

        if self.initial_page == 0:
            self.previous_button.disabled = True
            self.first_button.disabled = True
        elif self.initial_page == self.total_page_count - 1:
            self.next_button.disabled = True
            self.last_button.disabled = True

        self.message = await ctx.send(embed=self.pages[self.initial_page], view=self, ephemeral=self.ephemeral)

    async def previous(self):
        if self.current_page == 0:
            self.current_page = self.total_page_count - 1
        else:
            self.current_page -= 1

        self.page_counter.label = f"{self.current_page + 1}/{self.total_page_count}"

        # if current page is 1, then disable the previous button
        if self.current_page == 0:
            self.next_button.disabled = False
            self.last_button.disabled = False

            self.previous_button.disabled = True
            self.first_button.disabled = True

        elif self.current_page == self.total_page_count - 1:
            self.next_button.disabled = False
            self.last_button.disabled = False

            self.previous_button.disabled = True
            self.first_button.disabled = True

        else:
            self.next_button.disabled = False
            self.last_button.disabled = False

            self.previous_button.disabled = False
            self.first_button.disabled = False

        await self.message.edit(embed=self.pages[self.current_page], view=self)

    async def next(self):
        if self.current_page == self.total_page_count - 1:
            self.current_page = 0
        else:
            self.current_page += 1

        self.page_counter.label = f"{self.current_page + 1}/{self.total_page_count}"

        # if the current page is the last page, then disable the next button
        if self.current_page == 0:
            self.next_button.disabled = True
            self.last_button.disabled = True

            self.previous_button.disabled = False
            self.first_button.disabled = False

        elif self.current_page == self.total_page_count - 1:
            self.next_button.disabled = True
            self.last_button.disabled = True

            self.previous_button.disabled = False
            self.first_button.disabled = False

        else:
            self.next_button.disabled = False
            self.last_button.disabled = False

            self.previous_button.disabled = False
            self.first_button.disabled = False

        await self.message.edit(embed=self.pages[self.current_page], view=self)

    async def first(self):
        self.current_page = 0

        self.page_counter.label = f"1/{self.total_page_count}"

        # if current page is 1, then disable the previous button

        self.previous_button.disabled = True
        self.first_button.disabled = True

        self.next_button.disabled = False
        self.last_button.disabled = False

        await self.message.edit(embed=self.pages[self.current_page], view=self)

    async def last(self):
        self.current_page = self.total_page_count - 1

        self.page_counter.label = f"{self.total_page_count}/{self.total_page_count}"

        # if current page is 1, then disable the previous button

        self.previous_button.disabled = False
        self.first_button.disabled = False

        self.next_button.disabled = True
        self.last_button.disabled = True

        await self.message.edit(embed=self.pages[self.current_page], view=self)

    async def next_button_callback(self, interaction: discord.Interaction):
        if interaction.user != self.ctx.author and self.allow_ext_input:
            embed = discord.Embed(
                description="This pagination was not executed by you.",
                color=discord.Colour.red()
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        await self.next()
        await interaction.response.defer()

    async def previous_button_callback(self, interaction: discord.Interaction):
        if interaction.user != self.ctx.author and self.allow_ext_input:
            embed = discord.Embed(
                description="This pagination was not executed by you.",
                color=discord.Colour.red()
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        await self.previous()
        await interaction.response.defer()

    async def first_button_callback(self, interaction: discord.Interaction):
        if interaction.user != self.ctx.author and self.allow_ext_input:
            embed = discord.Embed(
                description="This pagination was not executed by you.",
                color=discord.Colour.red()
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        await self.first()
        await interaction.response.defer()

    async def last_button_callback(self, interaction: discord.Interaction):
        if interaction.user != self.ctx.author and self.allow_ext_input:
            embed = discord.Embed(
                description="This pagination was not executed by you.",
                color=discord.Colour.red()
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        await self.last()
        await interaction.response.defer()

    # Override default implementation in discord.ui.View
    async def on_timeout(self) -> None:
        # possible values = ['delete_message', 'remove_view', 'disable_view', 'do_nothing']
        if self.ontimeout == "delete_message":
            await self.message.delete()
        elif self.ontimeout == "remove_view":
            await self.message.edit(view=None)
        elif self.ontimeout == "disable_view":
            for child in self.children:
                child.disabled = True
            await self.message.edit(view=self)


class SimplePaginatorPageCounter(discord.ui.Button):
    def __init__(self, style: discord.ButtonStyle, total_pages, initial_page):
        super().__init__(label=f"{initial_page + 1}/{total_pages}", style=style, disabled=True)
