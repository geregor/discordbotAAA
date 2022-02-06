import discord, psycopg2, asyncio, re
from discord.ext import commands
from config import *

#Подключение базы данных
conn = psycopg2.connect(dbname=db, user=user,
                        password=password, host=host)
cursor = conn.cursor()
#Подключение дискорд бота
bot = commands.Bot(command_prefix = settings['prefix']) # Так как мы указали префикс в settings, обращаемся к словарю с ключом prefix.

@bot.command('create')
async def create_question(ctx): # Создаём функцию и передаём аргумент ctx.
    author = ctx.message.author
    value = False
    cursor.execute( f"SELECT user_id FROM admins" )
    arr = cursor.fetchall()
    for i in arr :
        if author.id == i [ 0 ] :
            value = True
            break
    if value:
        try:
            message = ctx.message.content
            try:
                name = re.split( r' ' , message , maxsplit=1 )
                print(name)
                name = re.split( r' - ' , name [ 1 ] , maxsplit=1 )
                print(name)
            except:
                await ctx.send( f'{author.mention}, ошибка в введенных данных, пример: "-create Привет - Пока"❗' )
                value = False


            question,answer = name[0],name[1]
            print(name)
            if value: #Проверяем есть ли данный вопрос в бд
                cursor.execute(f"SELECT question FROM Project1 WHERE question='{question}'")
                print(cursor.fetchall())
                cursor.execute( f"INSERT INTO Project1(question,answer) VALUES ('{question}','{answer}')" )
                conn.commit()
                cursor.execute(f"SELECT question,answer FROM Project1 WHERE question = '{question}'")
                m = f"{author.mention}, твой запрос успешно выполнен ✅"
                for i in cursor.fetchall():
                    print(i)
                    m += f"\n{i[0]} - {i[1]}"

                await ctx.send( m )
        except Exception as err:
            await ctx.send( f"❗ {author.mention}, что-то произошло не так, попробуй в другой раз❗ " )
    else :
        await ctx.send( f"{author.mention}, отказанно в доступе!" )

@bot.command('remove')
async def remove (ctx):
    author = ctx.message.author
    value = False
    cursor.execute( f"SELECT user_id FROM admins" )
    arr = cursor.fetchall()
    for i in arr :
        if author.id == i [ 0 ] :
            value = True
            break
    if value:
        message = ctx.message.content

        try :
            text = re.split( r' ' , message , maxsplit=1 )
        except :
            await ctx.send( f'{author.mention}, ошибка в веденных данных, пример: "-remove Привет - Пока❗" ' )
            value = False

        try :
            data = re.split( r' - ' , text[1] , maxsplit=1 )
        except :
            await ctx.send( f'{author.mention}, ошибка в веденных данных, пример: "-remove Привет - Пока❗" ' )
            value = False

        if value:
            cursor.execute(f"SELECT * FROM Project1 WHERE question='{data[0]}' and answer='{data[1]}'")
            if cursor.fetchall() != []:
                cursor.execute(f"DELETE FROM Project1 WHERE question='{data[0]}' and answer='{data[1]}'")
                conn.commit()
                await ctx.send(f"{author.mention}, данный 'вопрос-ответ' был успешно удален ✅")
            else:
                await ctx.send( f"{author.mention}, данный 'вопрос-ответ' не был найден ❗" )
    else :
        await ctx.send( f"{author.mention}, отказанно в доступе!" )

@bot.command('list')
async def list(ctx):
    author = ctx.message.author
    value = False
    cursor.execute( f"SELECT user_id FROM admins" )
    arr = cursor.fetchall()
    for i in arr :
        if author.id == i [ 0 ] :
            value = True
            break
    if value:
        cursor.execute(f"SELECT * FROM Project1")
        m = "Ваши 'вопрос-ответ':"
        arr = cursor.fetchall()
        if arr != []:
            for data in arr:
                m += f"\n{data[0]} - {data[1]}"
            await ctx.send( m )
        else:
            await ctx.send( "Ты еще не создал 'вопрос-ответ'❗" )
    else :
        await ctx.send( f"{author.mention}, отказанно в доступе!" )

@bot.command('?')
async def commands(ctx):
    author = ctx.message.author
    value = False
    cursor.execute( f"SELECT user_id FROM admins" )
    arr = cursor.fetchall()
    for i in arr :
        if author.id == i [ 0 ] :
            value = True
            break
    if value:
        await ctx.send(f"{author.mention}, команды: \n"
                       f"-create     - создает 'вопрос-ответ'\n"
                       f"-remove  - убирает выбранный 'вопрос-ответ'\n"
                       f"-list           - список всех 'вопрос-ответ'")
    else :
        await ctx.send( f"{author.mention}, отказанно в доступе!" )

@bot.command('admin')
async def admin(ctx):
    cursor.execute(f"SELECT * FROM admins")
    arr = cursor.fetchall()
    author = ctx.message.author
    value = False
    for i in arr:
        if author.id == i[0]:
            value = True
            break

    if value:
        await ctx.send(f"{author.mention}, вы являетесь администратором!")
    elif arr == []:
        cursor.execute(f"INSERT INTO admins(user_id) VALUES ({author.id})")
        conn.commit()
        await ctx.send(f"{author.mention}, теперь вы имеете доступ к админке!")

@bot.command('admin_add')
async def admin_add(ctx):
    cursor.execute(f"SELECT user_id FROM admins")
    arr = cursor.fetchall()
    message = ctx.message.content
    author = ctx.message.author
    value = False
    print(arr)
    for i in arr:
        if author.id == i[0]:
            value = True
            break

    if value:
        try:
            data = re.split(r' ', message, maxsplit=1)[1]
        except:
            value = False
            await ctx.send(f'{author.mention}, неправильно введенны данные: используйте "-admin_add ID-Пользователя"\n'
                           f'Если не знаете что такое ID-Пользователя то:\n'
                           f'1. Зайдите в Настройки пользователя -> Моя учетная запись\n'
                           f'2. Находите троеточие около вашего #ID и копируете цифровой ID')
    else:
        await ctx.send(f"{author.mention}, отказанно в доступе!")

    if value :
        if data not in arr :
            cursor.execute( f"INSERT INTO admins(user_id) VALUES ({data})" )
            conn.commit()
            await ctx.send( f"{author.mention}, вы добавили нового администратора!" )
        else:
            await ctx.send( f"{author.mention}, данный администратор уже добавлен!")

@bot.command('admin_remove')
async def admin_add(ctx):
    cursor.execute(f"SELECT user_id FROM admins")
    arr = cursor.fetchall()
    message = ctx.message.content
    author = ctx.message.author
    value = False
    for i in arr:
        if author.id == i[0]:
            value = True
            break

    if value :
        try :
            data = re.split( r' ' , message , maxsplit=1 ) [ 1 ]
            data = int(data)
        except :
            value = False
            await ctx.send( f'{author.mention}, неправильно введенны данные: используйте "-admin_add ID-Пользователя"\n'
                            f'Если не знаете что такое ID-Пользователя то:\n'
                            f'1. Зайдите в Настройки пользователя -> Моя учетная запись\n'
                            f'2. Находите троеточие около вашего #ID и копируете цифровой ID' )
    else:
        await ctx.send( f"{author.mention}, отказанно в доступе!" )

    if value:
        c = False
        for i in arr :
            if int(data) == i [ 0 ] :
                c = True
                break
        if c:
            cursor.execute( f"DELETE FROM admins WHERE user_id = {data}" )
            conn.commit()
            await ctx.send( f"{author.mention}, вы успешно удалили администратора!" )
        else:
            await ctx.send( f"{author.mention}, данный администратор не найден!")

@bot.command('admin_list')
async def admin_list(ctx):
    cursor.execute( f"SELECT user_id FROM admins" )
    arr = cursor.fetchall()
    message = ctx.message.content
    author = ctx.message.author
    value = False
    cursor.execute( f"SELECT user_id FROM admins" )
    for i in arr :
        if author.id == i [ 0 ] :
            value = True
            break

    if value:
        m = "Список администраторов:"
        for i in arr:
            m += f"\n{i[0]}"
        await ctx.send(m)
    else :
        await ctx.send( f"{author.mention}, отказанно в доступе!" )


bot.run(settings['token'])
