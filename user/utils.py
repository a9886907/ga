#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import asyncio
import datetime
import os
import re
import traceback

from .. import chat_id, jdbot, logger, LOG_DIR, TOKEN

bot_id = int(TOKEN.split(":")[0])


async def execute(msg, info, exectext):
    """
    æ§è¡å½ä»¤
    """
    try:
        info += f'\n\nð£å¼å§æ§è¡èæ¬ð£\n\n'
        msg = await msg.edit(info)
        try:
            from ..diy.diy import start
            await start()
        except:
            pass
        p = await asyncio.create_subprocess_shell(exectext, shell=True, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, env=os.environ)
        res_bytes, res_err = await p.communicate()
        try:
            from ..diy.diy import end
            await end()
        except ImportError:
            pass
        res = re.findall(r".*ð£==============\n(.*)", res_bytes.decode('utf-8'), re.S)[0]
        if len(res) == 0:
            info += '\nå·²æ§è¡ï¼ä½è¿åå¼ä¸ºç©º'
            await msg.edit(info)
            return
        else:
            try:
                logtime = f'æ§è¡æ¶é´ï¼' + re.findall(r'èæ¬æ§è¡- åäº¬æ¶é´.UTC.8.ï¼(.*?)=', res, re.S)[0] + '\n'
                info += logtime
            except Exception as e:
                pass
            errinfo = '\n\n**âââ¼éè¯¯ä»£ç 493ï¼IPå¯è½é»äºâ¼ââ**\n' if re.search('Response code 493', res) else ''
            if len(info + res + errinfo) <= 4000:
                await msg.edit(info + res + errinfo)
            elif len(info + res + errinfo) > 4000:
                tmp_log = f'{LOG_DIR}/bot/{exectext.split("/")[-1].split(".js")[0].split(".py")[0].split(".sh")[0].split(".ts")[0].split(" ")[-1]}-{datetime.datetime.now().strftime("%H-%M-%S.%f")}.log'
                with open(tmp_log, 'w+', encoding='utf-8') as f:
                    f.write(res)
                await msg.delete()
                await jdbot.send_message(chat_id, f'{info}\næ§è¡ç»æè¾é¿ï¼è¯·æ¥çæ¥å¿{errinfo}', file=tmp_log)
                os.remove(tmp_log)
    except Exception as e:
        title = "ãð¥éè¯¯ð¥ã"
        name = "æä»¶åï¼" + os.path.split(__file__)[-1].split(".")[0]
        function = "å½æ°åï¼" + e.__traceback__.tb_frame.f_code.co_name
        details = "éè¯¯è¯¦æï¼ç¬¬ " + str(e.__traceback__.tb_lineno) + " è¡"
        tip = 'å»ºè®®ç¾åº¦/è°·æ­è¿è¡æ¥è¯¢'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\néè¯¯åå ï¼{str(e)}\n{details}\n{traceback.format_exc()}\n{tip}")
        logger.error(f"éè¯¯--->{str(e)}")