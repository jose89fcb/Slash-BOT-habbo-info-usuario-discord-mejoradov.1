import discord, asyncio
from discord.ext import commands
import requests
import json
import discord
from urllib import parse, request
from requests import get
import datetime
import asyncio
import requests, json, discord, datetime, asyncio, aiohttp
from urllib import parse, request
import requests, bs4
import re
####
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_choice, create_option
from discord_slash import SlashCommand, SlashContext

###
from dateutil.parser import isoparse
import locale
locale.setlocale(locale.LC_TIME, "es_ES")
from datetime import datetime
from dateutil import relativedelta
from dateutil import parser
import time
import configparser

config = configparser.ConfigParser()
config.read("configuracion.ini")


bot = commands.Bot(command_prefix='!')
slash = SlashCommand(bot, sync_commands=True)

def calcular_tiempo_transcurrido(date1, date2):
    r = relativedelta.relativedelta(date2, date1)
    tiempo = ""

    if r.years != 0:
        tiempo += f"{r.years} Años "
    if r.months != 0:
        tiempo += f"{r.months} Meses "
    if r.days != 0:
        tiempo += f"{r.days} Días "
    if r.hours != 0:
        tiempo += f"{r.hours} Horas "
    if r.minutes != 0:
        tiempo += f"{r.minutes} Minutos "
    if r.seconds != 0:
        tiempo += f"{r.seconds} Segundos "

    return tiempo or "No disponible"

def generar_barra_progreso_con_porcentaje(percent, total_bloques=10):
    if percent == 0:
        # Cuando el porcentaje es 0, mostramos la barra llena
        barra = "█" * total_bloques
        return f"{barra} 100%"  # Mostramos como si estuviera lleno al 100%

    bloques_llenos = round((percent / 100) * total_bloques)
    bloques_llenos = min(bloques_llenos, total_bloques)  # Asegurarnos que no exceda el total de bloques

    bloques_vacios = total_bloques - bloques_llenos
    barra = f"{'█' * bloques_llenos}{'░' * bloques_vacios}"

    return f"{barra} {percent}%"

@slash.slash(
    name="habboinfo", description="Keko habbo Hotel",
    options=[
        create_option(
            name="keko",
            description="Escribe el keko",
            option_type=3,
            required=True
        ),
        create_option(
            name="hotel",
            description="Elige él hotel",
            option_type=3,
            required=True,
            choices=[
                create_choice(name="ES - Hotel España", value="es"),
                create_choice(name="BR - Hotel Brasil", value="com.br"),
                create_choice(name="COM - Hotel Estados Unidos", value="com"),
                create_choice(name="DE - Hotel Alemán", value="de"),
                create_choice(name="FR - Hotel Francés", value="fr"),
                create_choice(name="FI - Hotel Finlandia", value="fi"),
                create_choice(name="IT - Hotel Italiano", value="it"),
                create_choice(name="TR - Hotel Turquía", value="com.tr"),
                create_choice(name="NL - Hotel Holandés", value="nl")
            ]
        )
    ]
)
async def _habboinfo(ctx: SlashContext, keko: str, hotel: str):
    await ctx.defer()
    
    response = requests.get(f"https://www.habbo.{hotel}/api/public/users?name={keko}")

    try:
        data = response.json()
        id = data['uniqueId']
        Habbokeko = data['name']
        mision = data['motto']
        fecha_miembro = isoparse(data['memberSince']).timestamp()
        dt_object = datetime.fromtimestamp(fecha_miembro).strftime("%A, %#d de %B del %Y %H:%M:%S")

        grupos = len(requests.get(f"https://www.habbo.{hotel}/api/public/users/{id}/groups").json())
        salas = len(requests.get(f"https://www.habbo.{hotel}/api/public/users/{id}/rooms").json())
        fotos = len(requests.get(f"https://www.habbo.{hotel}/extradata/public/users/{id}/photos").json())
        amigos = len(requests.get(f"https://www.habbo.{hotel}/api/public/users/{id}/friends").json())
        placas = len(requests.get(f"https://www.habbo.{hotel}/api/public/users/{id}/badges").json())

        tiempo_miembro = calcular_tiempo_transcurrido(datetime.fromtimestamp(fecha_miembro), datetime.now())

        estado = "Desconectado ❌" if not data.get("online") else "En línea ✅"
        
        # Usamos el porcentaje que da la API
        porcentaje_completado = data['currentLevelCompletePercent']
        barra_progreso = generar_barra_progreso_con_porcentaje(porcentaje_completado)

        embed = discord.Embed(
            title=f"Esta es la info de 🡺 {Habbokeko}",
            description=(
                f"•ID🡺 {id}\n"
                f"•Estado🡺 {estado}\n"
                f"•Total XP🡺 {data['totalExperience']}\n"
                f"•Misión 🡺 {mision}\n"
                f"•Nivel actual🡺 {data['currentLevel']} ({barra_progreso})\n"  # Añadimos la barra de progreso aquí
                f"•Gemas Obtenidas (Estrellas)🡺 {data['starGemCount']}\n"
                f"•Hora Miembro desde🡺 {dt_object}\n"
                f"•Grupos Totales🡺 {grupos}\n"
                f"•Salas Totales🡺 {salas}\n"
                f"•Fotos Totales🡺 {fotos}\n"
                f"•Total Amigos🡺 {amigos}\n"
                f"•Placas Totales🡺 {placas}\n"
                f"•Tiempo Miembro desde🡺 {tiempo_miembro}\n"
                f"[Visita el perfil de {Habbokeko}](https://habbo.{hotel}/profile/{Habbokeko})"
            ),
            color=discord.Colour.random(),
            timestamp=datetime.utcnow()
        )
        await ctx.send(embed=embed)

    except discord.errors.Forbidden:
        await ctx.send("No pudimos enviarte el mensaje privado. Por favor, permite mensajes directos en tu configuración de privacidad.", hidden=True)
    except KeyError:
        await ctx.send("El keko no existe!", hidden=True)



@bot.event
async def on_ready():
    
   

    print("BOT " f'{bot.user.name}')
    activity = discord.Game(name="Habbo info", type=1)
    await bot.change_presence(status=discord.Status.online, activity=activity)

bot.run(config.get("token","tokenDiscord"))