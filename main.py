import discord
from discord.ext import commands
import requests
import re
import os
from keep_alive import keep_alive

# Remplace ton token ici
TOKEN = "MTMwODcxNDU3NjYxNDkxNjE4Ng.G6zLmu.vX3ZEgWPF288w6t-ZmZ8kVN55bHljzwG6SLiSU"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


# Fonction pour obtenir une URL d'image
def get_card_image_url(card_name):
    query = f"{card_name} "
    search_url = f"https://www.google.com/search?hl=fr&tbm=isch&q={query}"

    # Afficher l'URL pour déboguer
    print(f"URL générée pour la recherche : {search_url}")

    # En-têtes HTTP pour simuler un navigateur
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Faire une requête HTTP
    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        return None

    # Extraire les URLs d'images avec une regex simple
    image_urls = re.findall(r'"https://[^"]*\.jpg"', response.text)
    if image_urls:
        return image_urls[0].strip('"')  # Retourne la première image trouvée
    return None


# Commande pour afficher une carte
@bot.command(name='carte')
async def fetch_card(ctx, *, card_name: str):
    image_url = get_card_image_url(card_name)

    if image_url:
        # Envoyer l'image comme embed
        embed = discord.Embed(title=f"Carte : {card_name}",
                              color=discord.Color.blue())
        embed.set_image(url=image_url)
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"Aucune image trouvée pour **{card_name}**.")


# Événement pour indiquer que le bot est en ligne
@bot.event
async def on_ready():
    print(f'{bot.user} est en ligne et prêt à recevoir des commandes !')


# Lancer le bot
keep_alive()
bot.run(TOKEN)
