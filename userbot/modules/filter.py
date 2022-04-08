import re

from telethon import events
from telethon.utils import get_display_name
from userbot import BLACKLIST_CHAT, BOTLOG_CHATID
from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, bot
from userbot.events import poci_cmd
from userbot.modules.sql_helper.filter_sql import (
    add_filter,
    get_filters,
    remove_all_filters,
    remove_filter,
)
from userbot.utils import edit_delete, edit_or_reply


@bot.on(events.NewMessage(incoming=True))
async def filter_incoming_handler(event):
    name = event.raw_text
    filters = get_filters(event.chat_id)
    if not filters:
        return
    a_user = await event.get_sender()
    chat = await event.get_chat()
    me = await event.client.get_me()
    if event.sender_id == me.id:
        return
    title = get_display_name(await event.get_chat()) or "this chat"
    participants = await event.client.get_participants(chat)
    count = len(participants)
    mention = f"[{a_user.first_name}](tg://user?id={a_user.id})"
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    first = a_user.first_name
    last = a_user.last_name
    fullname = f"{first} {last}" if last else first
    username = f"@{a_user.username}" if a_user.username else mention
    userid = a_user.id
    my_first = me.first_name
    my_last = me.last_name
    my_fullname = f"{my_first} {my_last}" if my_last else my_first
    my_username = f"@{me.username}" if me.username else my_mention
    for trigger in filters:
        pattern = r"( |^|[^\w])" + re.escape(trigger.keyword) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            file_media = None
            filter_msg = None
            if trigger.f_mesg_id:
                msg_o = await event.client.get_messages(
                    entity=BOTLOG_CHATID, ids=int(trigger.f_mesg_id)
                )
                file_media = msg_o.media
                filter_msg = msg_o.message
                link_preview = True
            elif trigger.reply:
                filter_msg = trigger.reply
                link_preview = False
            await event.reply(
                filter_msg.format(
                    mention=mention,
                    title=title,
                    count=count,
                    first=first,
                    last=last,
                    fullname=fullname,
                    username=username,
                    userid=userid,
                    my_first=my_first,
                    my_last=my_last,
                    my_fullname=my_fullname,
                    my_username=my_username,
                    my_mention=my_mention,
                ),
                file=file_media,
                link_preview=link_preview,
            )


@bot.on(poci_cmd(outgoing=True, pattern="filter (.*)"))
async def add_new_filter(event):
    if event.chat_id in BLACKLIST_CHAT:
        return await edit_or_reply(
            event, "**❌Perintah ini Dilarang digunakan di Group ini❌**"
        )
    value = event.pattern_match.group(1).split(None, 1)
    keyword = value[0]
    try:
        string = value[1]
    except IndexError:
        string = None
    msg = await event.get_reply_message()
    msg_id = None
    if msg and msg.media and not string:
        if BOTLOG_CHATID:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"**#FILTER\nID OBROLAN:** {event.chat_id}\n**TRIGGER:** `{keyword}`"
                "\n\n**Pesan Berikut Disimpan Sebagai Data Balasan Filter Untuk Obrolan, Mohon Jangan Menghapusnya**",
            )
            msg_o = await event.client.forward_messages(
                entity=BOTLOG_CHATID,
                messages=msg,
                from_peer=event.chat_id,
                silent=True,
            )
            msg_id = msg_o.id
        else:
            await edit_or_reply(
                event,
                "**Untuk menyimpan media ke filter membutuhkan** `BOTLOG_CHATID` **untuk disetel.**",
            )
            return
    elif msg and msg.text and not string:
        string = msg.text
    elif not string:
        return await edit_or_reply(event, "Apa yang harus saya lakukan ?")
    success = "**Berhasil {} Filter** `{}` **Disini**"
    if add_filter(str(event.chat_id), keyword, string, msg_id) is True:
        return await edit_or_reply(event, success.format("Menyimpan", keyword))
    remove_filter(str(event.chat_id), keyword)
    if add_filter(str(event.chat_id), keyword, string, msg_id) is True:
        return await edit_or_reply(event, success.format("Mengupdate", keyword))
    await edit_or_reply(event, f"**ERROR saat menyetel filter untuk** `{keyword}`")


@bot.on(poci_cmd(outgoing=True, pattern="filters$"))
async def on_snip_list(event):
    OUT_STR = "**Tidak Ada Filter Apapun Disini.**"
    filters = get_filters(event.chat_id)
    for filt in filters:
        if OUT_STR == "**❌Tidak Ada Filter Apapun Disini.❌**":
            OUT_STR = "**✥✔ Daftar Filter Yang Aktif Disini✔:**\n"
        OUT_STR += "• `{}`\n".format(filt.keyword)
    await edit_or_reply(
        event,
        OUT_STR,
        caption="✔Daftar Filter Yang Aktif Disini✔",
        file_name="filters.text",
    )


@bot.on(poci_cmd(outgoing=True, pattern="stop ([\s\S]*)"))
async def remove_a_filter(event):
    filt = event.pattern_match.group(1)
    if not remove_filter(event.chat_id, filt):
        await event.edit("**Filter** `{}` **Tidak Ada Disini**.".format(filt))
    else:
        await event.edit("**🗑Berhasil Menghapus Filter🗑** `{}` **Disini**".format(filt))


@bot.on(poci_cmd(outgoing=True, pattern="rmallfilters$"))
async def on_all_snip_delete(event):
    filters = get_filters(event.chat_id)
    if filters:
        remove_all_filters(event.chat_id)
        await edit_delete(
            event, "**🗑Berhasil Menghapus semua filter yang ada dalam obrolan ini🗑**"
        )
    else:
        await edit_delete(event, "**❌Tidak Ada Filter Apapun Disini❌.**")


CMD_HELP.update(
    {
        "filter": f"**Plugin : **`filter`\
        \n\n  •  **Syntax :** `{cmd}filters`\
        \n  •  **Function : **Melihat filter userbot yang aktif di obrolan.\
        \n\n  •  **Syntax :** `{cmd}filter` <keyword> <balasan> atau balas ke pesan ketik `.filter` <keyword>\
        \n  •  **Function : **Membuat filter di obrolan, Bot Akan Membalas Jika Ada Yang Menyebut 'keyword' yang dibuat. Bisa dipakai ke media/sticker/vn/file.\
        \n\n  •  **Syntax :** `{cmd}stop` <keyword>\
        \n  •  **Function : **Untuk Nonaktifkan Filter yang terpasang di grup.\
        \n\n  •  **Syntax :** `{cmd}rmallfilters`\
        \n  •  **Function : **Menghapus semua filter yang ada di grup.\
    "
    }
)
