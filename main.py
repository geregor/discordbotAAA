import discord, psycopg2, asyncio,random, re
from discord.ext import commands
from config import *
#Подключение базы данных
conn = psycopg2.connect(dbname=db, user=user,
                        password=password, host=host)
cursor = conn.cursor()
#Подключение дискорд бота
bot = commands.Bot(command_prefix = settings['prefix']) # Так как мы указали префикс в settings, обращаемся к словарю с ключом prefix.

@bot.event
async def on_message(message):
    cursor.execute(f"SELECT * FROM Project1")
    questions = []
    answers = []
    arr = cursor.fetchall()
    for i in arr:
        questions.append(i[0])
    mes = message.content.replace(f"<@!{settings['id']}> ", '')

    if mes in questions and settings["id"] != message.author.id and f"<@!{settings['id']}>" in message.content:
        print( f"Пришло сообщение: {message.content}" )
        channel = message.channel
        nowmes = re.split(r' ', message.content, maxsplit=1)[1]
        for i in arr:
            if i[0] == nowmes:
                answers.append(i[1])
        try:
            await message.reply(answers[random.randint(0,len(answers))])
        except Exception as err:
            await on_message(message)

bot.run(settings['token'])
