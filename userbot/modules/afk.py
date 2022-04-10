# Copyright (C) 2022 Man-Userbot
# PocongUserbot < https://github.com/poocong/PocongUserbot
# Recode by @Gojo_satoru44

from datetime import datetime

from telethon.tl import functions, types

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, bot, owner
from userbot.utils import poci_cmd

USER_AFK = {}
afk_time = None
last_afk_message = {}
last_afk_msg = {}
afk_start = {}

@bot.on(poci_cmd(outgoing=True, pattern="afk(?: |$)(.*)"))
async def _(event):
    if event.fwd_from:
        return
    reply = await event.get_reply_message()
    global USER_AFK
    global afk_time
    global last_afk_message
    global last_afk_msg
    global afk_start
    global afk_end
    global reason
    global pic
    USER_AFK = {}
    afk_time = None
    last_afk_message = {}
    last_afk_msg = {}
    afk_end = {}
    start_1 = datetime.now()
    afk_start = start_1.replace(microsecond=0)
    reason = event.pattern_match.group(1)
    pic = await event.client.download_media(reply) if reply else None
    if not USER_AFK:
        last_seen_status = await bot(
            functions.account.GetPrivacyRequest(types.InputPrivacyKeyStatusTimestamp())
        )
        if isinstance(last_seen_status.rules, types.PrivacyValueAllowAll):
            afk_time = datetime.datetime.now()
        USER_AFK = f"yes: {reason} {pic}"
        if reason:
            try:
                if pic.endswith((".tgs", ".webp")):
                    await event.client.send_message(event.chat_id, file=pic)
                    await event.client.send_message(
                        event.chat_id,
                        f"\n ❏ 𝗔𝗙𝗞 !\n┌ {owner} 𝗟𝗮𝗴𝗶 𝗔𝗙𝗞! \n└ 𝗞𝗮𝗿𝗲𝗻𝗮 : `{reason}`",
                    )
                else:
                    await event.client.send_message(
                        event.chat_id,
                        f"\n ❏ 𝗔𝗙𝗞 !\n┌ {owner} 𝗟𝗮𝗴𝗶 𝗔𝗙𝗞! \n└ 𝗞𝗮𝗿𝗲𝗻𝗮 : `{reason}`",
                        file=pic,
                    )
            except BaseException:
                await event.client.send_message(
                    event.chat_id,
                    f"\n ❏ 𝗔𝗙𝗞 !\n┌ {owner} 𝗟𝗮𝗴𝗶 𝗔𝗙𝗞! \n└ 𝗞𝗮𝗿𝗲𝗻𝗮 : `{reason}`",
                )
        else:
            try:
                if pic.endswith((".tgs", ".webp")):
                    await event.client.send_message(event.chat_id, file=pic)
                    await event.client.send_message(
                        event.chat_id, f"**✘ {owner} Telah AFK ✘**"
                    )
                else:
                    await event.client.send_message(
                        event.chat_id,
                        f"**✘ {owner} Telah AFK ✘**",
                        file=pic,
                    )
            except BaseException:
                await event.client.send_message(
                    event.chat_id, f"**✘ {owner} Telah AFK ✘**"
                )
        await event.delete()
        try:
            if reason and pic:
                if pic.endswith((".tgs", ".webp")):
                    await event.client.send_message(BOTLOG_CHATID, file=pic)
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        f"\n ❏ 𝗔𝗙𝗞 !\n┌ {owner} 𝗟𝗮𝗴𝗶 𝗔𝗙𝗞! \n└ 𝗞𝗮𝗿𝗲𝗻𝗮 : `{reason}`",
                    )
                else:
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        f"\n ❏ 𝗔𝗙𝗞 !\n┌ {owner} 𝗟𝗮𝗴𝗶 𝗔𝗙𝗞! \n └ 𝗞𝗮𝗿𝗲𝗻𝗮 : `{reason}`",
                        file=pic,
                    )
            elif reason:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    f"\n ❏ 𝗔𝗙𝗞 !\n┌ {owner} 𝗟𝗮𝗴𝗶 𝗔𝗙𝗞! \n└ 𝗞𝗮𝗿𝗲𝗻𝗮 : `{reason}`",
                )
            elif pic:
                if pic.endswith((".tgs", ".webp")):
                    await event.client.send_message(BOTLOG_CHATID, file=pic)
                    await event.client.send_message(
                        BOTLOG_CHATID, f"\n**✘ {owner} Sedang AFK ✘**"
                    )
                else:
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        f"\n**✘ {owner} Sedang AFK ✘**",
                        file=pic,
                    )
            else:
                await event.client.send_message(
                    BOTLOG_CHATID, f"\n**✘ {owner} Sedang AFK ✘**"
                )
        except Exception as e:
            BOTLOG_CHATIDger.warn(str(e))


CMD_HELP.update(
    {
        "afk": f"**Plugin : **`afk`\
        \n\n  •  **Syntax :** `{cmd}afk` <alasan> bisa <sambil reply sticker/foto/gif/media>\
        \n  •  **Function : **Memberi tahu kalau Master sedang afk bisa dengan menampilkan media keren ketika seseorang menandai atau membalas salah satu pesan atau dm Anda.\
        \n\n  •  **Syntax :** `{cmd}off`\
        \n  •  **Function : **Memberi tahu kalau Master sedang OFFLINE, dan menguubah nama belakang menjadi 【 OFF 】 \
    "
    }
)
