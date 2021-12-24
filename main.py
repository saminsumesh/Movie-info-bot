import os
import json
import requests
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client, filters
from request.utils import reqoute_uri

API = "https://api.sumanjay.cf/watch/query="


Bot = Client(
"Movie info bot",
bot_token = os.environ.get("BOT_TOKEN"),
api_id = int(os.environ.get("API_ID")),
api_hash = os.environ.get("API_HASH")
)

START_TXT = """Hey {} , Iam an simple movie info bot , You can search any movie with me and i will provide you with correct and accurate details.

• This bot is an opensource project , So Please consider giving a start to the repo

• For more details hit /help
"""

HELP_TXT = """
***Here is my help section you can find your help from here**

• /movie - To get the info of movie
• /about - Something about me 

"""
ABOUT_TXT = """
**🤖 Name** = Movie Info Bot
**😎 Creator** = [PaulWalker](https://t.me/paulwalker_TG")
**📚 Framework** = [Pyrogram](https://pyrogram.org)
😍 **Source Code** = [Click Here](https://github.com/saminsumesh/Movie-Info-Bot)
📡 **Server** = [Heroku](https://heroku.com)
📣 **XD Botz** = [XD Botz](https://t.me/XD_Botz)
👥 **Support Chat** = [XD Botz Support](https://t.me/xd_botzsupport")
"""

START_BUTTONS = InlineKeyboardMarkup(
     [[
     InlineKeyboardButton('Updates', url="https://t.me/XD_Botz"),
     InlineKeyboardButton('Support', url="https://t.me/xd_botzsupport")
     ],[
     InlineKeyboardButton('Help', callback_data='help'),
     InlineKeyboardButton('About', callback_data='about')
     ],[
     InlineKeyboardButton('Close', callback_data='close')
     ]]
)


HELP_BUTTON = InlineKeyboardButton(
[[
InlineKeyboardButton('Home', callback_data="home"),
InlineKeyboardButton('About', callback_data="about")
],[
InlineKeyboardButton('Close', callback_data="close")
]]
)




@Bot.on_callback_query()
async def cb_handler(bot, update):
    
    if update.data == "home":
        await update.message.edit_text(
            text=START_TXT.format(update.from_user.mention),
            reply_markup=START_BUTTON,
            disable_web_page_preview=True
        )
    
    elif update.data == "help":
        await update.message.edit_text(
            text=HELP_TXT,
            reply_markup=HELP_BUTTON,
            disable_web_page_preview=True
        )
    
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TXT.format((await bot.get_me()).username),
            reply_markup=ABOUT_BUTTON,
            disable_web_page_preview=True
        )
    
    else:
        await update.message.delete()



@Bot.on_callback_query()
async def callback(bot, update):
    data = update.data
    if data == "close":
       update.message.delete()


@Bot.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    await update.reply_text(
    text=START_TXT.format(update.from_user.mention),
    reply_markup=START_BUTTON,
    disable_web_preview=True
    )
    
@Bot.on_message(filters.private & filters.command(["help"]))
async def help(bot, update):
    await update.reply_text(
    text=HELP_TXT.format(update.from_user.mention),
    reply_markup=HELP_BUTTON,
    disable_web_preview=True
    )
    
@Bot.on_message(filters.private & filters.command(["about"]))
async def about(bot, update):
    await update.reply_text(
    text=ABOUT_TXT.format(update.from_user.mention),
    reply_markup=ABOUT_BUTTON,
    disable_web_preview=True
    )
    
@Bot.on_message(filters.command(["movie"]), group=2)
async def get_command(bot, update):
    movie = requote_uri(update.text.split(" ", 1)[1])
    username = (await bot.get_me()).username
    keyboard = [
        InlineKeyboardButton(
            text="Click here",
            url=f"https://telegram.me/{username}?start={movie}"
        )
    ]
    await update.reply_text(
        text=f"**Click the button below**",
        reply_markup=InlineKeyboardMarkup([keyboard]),
        disable_web_page_preview=True,
        quote=True
    )


@Bot.on_message(filters.private & filters.text & ~filters.via_bot & ~filters.edited)
async def get_movie_name(bot, update):
    if update.text.startswith("/"):
        return
    await get_movie(bot, update, update.text)


async def get_movie(bot, update, name):
    movie_name = requote_uri(name)
    movie_api = API + movie_name
    r = requests.get(movie_api)
    movies = r.json()
    keyboard = []
    number = 0
    for movie in movies:
        number += 1
        switch_text = movie_name + "+" + str(number)
        try:
            keyboard.append(
                [
                    InlineKeyboardButton(
                        text=description(movie),
                        switch_inline_query_current_chat=switch_text
                    )
                ]
            )
        except:
            pass
    keyboard.append(JOIN_BUTTONS)
    await update.reply_text(
        text="Select required option",
        reply_markup=InlineKeyboardMarkup(keyboard),
        disable_web_page_preview=True,
        quote=True
    )


def description(movie):
    set = []
    if movie['title']:
        set.append(movie['title'])
    if movie['type']:
        set.append(movie['type'].capitalize())
    if movie['release_year']:
        set.append(str(movie['release_year']))
    description = " | ".join(set)
    return description


def info(movie):
    info = f"**Title:** `{movie['title']}`\n"
    try:
        info += f"**Type:** `{movie['type'].capitalize()}`\n"
    except:
        pass
    try:
        info += f"**Release Date:** `{str(movie['release_date'])}`\n"
    except:
        pass
    try:
        info += f"**Release Year:** `{movie['release_year']}`\n"
    except:
        pass
    try:
        if movie['score']:
            scores = movie['score']
            info += "**Score:** "
            score_set = []
            for score in scores:
                score_set.append(f"{score.upper()} - `{str(scores[score])}`")
            info += " | ".join(score_set) + "\n"
    except:
        pass
    try:
        if movie['providers']:
            info += "**Providers:** "
            providers = movie['providers']
            provider_set = []
            for provider in providers:
                provider_set.append(f"<a href={providers[provider]}>{provider.capitalize()}</a>")
            info += " | ".join(provider_set)
    except:
        pass
    return info


def thumb(movie):
    thumbnail = movie['movie_thumb'] if movie['movie_thumb'] else None
    return thumbnail
    
    Bot.run()
