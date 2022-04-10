# Copyright (C) 2022 Man-Userbot
# PocongUserbot < https://github.com/poocong/PocongUserbot
# Recode by @Gojo_satoru44

from datetime import datetime


from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP

USER_AFK = {}
afk_time = None
last_afk_message = {}
last_afk_msg = {}
afk_start = {}


@pocong_handler(outgoing=True)
async def _(event):
    global USER_AFK
    global afk_time
    global last_afk_message
    global afk_start
    global afk_end
    user = await event.client.get_me()
    owner = user.first_name
    back_alive = datetime.now()
    afk_end = back_alive.replace(microsecond=0)
    if afk_start != {}:
        total_afk_time = str((afk_end - afk_start))
    current_message = event.message.message
    if "afk" not in current_message and "yes" in USER_AFK:
        try:
            if pic.endswith((".tgs", ".webp")):
                shite = await event.client.send_message(event.chat_id, file=pic)
                shites = await event.client.send_message(
                    event.chat_id,
                    f"**{owner} Kembali Online Untuk Parming**\n**Dari AFK :** `{total_afk_time}` **Yang Lalu**",
                )
            else:
                shite = await event.client.send_message(
                    event.chat_id,
                    f"**{owner} Pengangguran sok Sibuk Balik Lagi!**\n**Dari AFK :** `{total_afk_time}` **Yang Lalu**",
                    file=pic,
                )
        except BaseException:
            shite = await event.client.send_message(
                event.chat_id,
                f"**{owner} Kembali Online**\n**Dari AFK :** `{total_afk_time}` **Yang Lalu**",
            )

        await asyncio.sleep(6)
        await shite.delete()
        try:
            await shites.delete()
        except BaseException:
            pass
        USER_AFK = {}
        afk_time = None

        await bash("rm -rf *.webp")
        await bash("rm -rf *.tgs")

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
