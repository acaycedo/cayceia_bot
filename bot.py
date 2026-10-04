import os
import discord
import logging
from dotenv import load_dotenv
from openai import OpenAI

# 1. Configuración del sistema de registros (Logging)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

# 2. Cargar las credenciales
if os.path.exists("register.env"):
    load_dotenv("register.env")
else:
    load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# 3. Configurar el cliente de OpenRouter
ai_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

# 4. Configurar permisos del bot de Discord
intents = discord.Intents.default()
intents.message_content = True
bot_client = discord.Client(intents=intents)

# FUNCIÓN AUXILIAR: Divide textos largos en fragmentos menores a 2000 caracteres
def dividir_mensaje(texto, limite=1900):
    return [texto[i:i + limite] for i in range(0, len(texto), limite)]

@bot_client.event
async def on_ready():
    logging.info(f"✅ Bot conectado y listo como: {bot_client.user}")
    servidores = bot_client.guilds
    logging.info(f"🌐 Actualmente el bot está presente en {len(servidores)} servidor(es):")
    for guild in servidores:
        logging.info(f"   • Servidor: '{guild.name}' (ID: {guild.id}) - Miembros: {guild.member_count}")

@bot_client.event
async def on_guild_join(guild):
    logging.info(f"🚨 ¡EL BOT FUE AGREGADO A UN NUEVO SERVIDOR!")
    logging.info(f"   • Nombre: {guild.name}")
    logging.info(f"   • ID: {guild.id}")

@bot_client.event
async def on_guild_remove(guild):
    logging.warning(f"⚠️ El bot fue removido del servidor: '{guild.name}' (ID: {guild.id})")

@bot_client.event
async def on_message(message):
    if message.author == bot_client.user or message.author.bot:
        return

    COMANDO = "!ia"
    es_mencionado = bot_client.user.mentioned_in(message)
    empieza_con_comando = message.content.startswith(COMANDO)

    if not (empieza_con_comando or es_mencionado):
        return

    prompt = message.content
    if empieza_con_comando:
        prompt = prompt[len(COMANDO):].strip()
    elif es_mencionado:
        prompt = prompt.replace(f"<@{bot_client.user.id}>", "").strip()

    if not prompt:
        await message.channel.send("❓ Por favor escribe tu consulta después del comando. Ejemplo: `!ia ¿Qué es una API?`")
        return

    nombre_servidor = message.guild.name if message.guild else "Mensaje Privado (DM)"
    id_servidor = message.guild.id if message.guild else "N/A"
    canal_nombre = message.channel.name if hasattr(message.channel, 'name') else "DM"
    usuario = f"{message.author.name} ({message.author.id})"

    logging.info("--------------------------------------------------")
    logging.info(f"📥 CONSULTA RECIBIDA:")
    logging.info(f"   📍 Servidor: {nombre_servidor} (ID: {id_servidor})")
    logging.info(f"   💬 Canal: #{canal_nombre}")
    logging.info(f"   👤 Usuario: {usuario}")
    logging.info(f"   ❓ Mensaje: \"{prompt}\"")

    async with message.channel.typing():
        try:
            completion = ai_client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "https://universidad.edu",
                    "X-Title": "Proyecto Universitario Discord Bot",
                },
                model="openrouter/auto",
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un asistente tecnico de hardware y software académico preciso y conciso."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            respuesta = completion.choices[0].message.content

            # Si la respuesta supera el límite de Discord, se envía en varios mensajes
            fragmentos = dividir_mensaje(respuesta)
            for parte in fragmentos:
                await message.channel.send(parte)

            logging.info(f"✅ Respuesta enviada con éxito a '{nombre_servidor}' ({len(fragmentos)} mensaje/s)")
            logging.info("--------------------------------------------------")

        except Exception as error:
            logging.error(f"❌ Error al procesar la solicitud para '{nombre_servidor}': {error}")
            await message.channel.send("⚠️ Ocurrió un error al procesar tu solicitud con OpenRouter.")

if __name__ == "__main__":
    bot_client.run(DISCORD_TOKEN)