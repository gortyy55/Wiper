import discord
from discord.ext import commands
import asyncio
import senders
import datetime

client = commands.Bot(command_prefix="/", intents=discord.Intents.all())

# DEBUT Partie Lancement BOT
@client.event
async def on_ready():
    await client.tree.sync()
    channelid = 1242431221502447626
    channel = client.get_channel(channelid)
    if channel:
        await channel.purge()
        await ensure_menu_view(channel)
    else:
        print(f"channel {channelid} not found")
    print("started")
# FIN Partie Lancement BOT

# COMMANDES TEST
@client.command()
async def check(ctx, FirstName, LastName):
    result = senders.player(FirstName, LastName)
    if result:
        await ctx.send(f"{result}")
    else:
        await ctx.send("non trouver")

@client.command()
async def delete(ctx, FirstName, LastName):
    senders.delete_player(FirstName, LastName)
    await ctx.send(f"Deleted player {FirstName} {LastName}")

@client.command()
async def getids(ctx, id):
    view = Dropdown(id)
    results = senders.idfinder(id)
    if results:
        for result in results:
            await ctx.send(f"User ID: {result[0]}")
    else:
        await ctx.send(f"No users found with pattern: {id}")
# COMMANDES TEST

# Partie UI
class TicketModel(discord.ui.Modal, title="Wiper Belgium RP"):
    License = discord.ui.TextInput(label="License", placeholder="eg. AzeZf422Fdsqe", required=True, style=discord.TextStyle.short)
    
    async def on_submit(self, interaction: discord.Interaction):
        id = self.License.value
        if id:
            view = Dropdown(id)
            await interaction.response.send_message(f"Player ID: {id} found", view=view, ephemeral=True,delete_after=30)
        else:
            await interaction.response.send_message("Player not found", ephemeral=True,delete_after=30)

class SimpleView(discord.ui.View):
    @discord.ui.button(label="Wipe Une Personne", style=discord.ButtonStyle.success)
    async def remplir(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(TicketModel())

async def ensure_menu_view(channel):
    view = SimpleView()
    await channel.send("Wipe une Personne", view=view)
# Fin Partie UI

# partie dropdown
class Dropdown(discord.ui.View):
    def __init__(self, id):
        super().__init__()
        self.id = id
        self.add_item(self.NameSelect(id))
    
    class NameSelect(discord.ui.Select):
        def __init__(self, id):
            self.id = id
            options = self.generate_options(id)
            super().__init__(placeholder="Le Nom Du Joueur ?", options=options)

        def generate_options(self, id):
            options = []
            results = senders.idfinder(id)
            for result in results:
                label = result[0]
                value = result[0]  # Adjust this if the desired value is in a different index
                options.append(discord.SelectOption(label=label, value=value))
            return options

        async def callback(self, interaction: discord.Interaction):
            selected_id = self.values[0]
            senders.delete_player(selected_id)
            await interaction.response.send_message(f"Deleted player with ID: {selected_id}", ephemeral=True,delete_after=30)
            channelid = 1242479731295911978
            channel = client.get_channel(channelid)
            now = datetime.datetime.now()
            current_datetime = now.strftime("%d/%m/%Y %H:%M:%S")
            await channel.send(f"Le Joueur {selected_id} a etait wipe par {interaction.user.name} le {current_datetime}")

@client.command()
async def select(ctx, id):
    view = Dropdown(id)
    await ctx.send(view=view)

async def main():
    async with client:
        await client.start("")

asyncio.run(main())
