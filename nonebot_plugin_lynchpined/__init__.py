from typing import Tuple
from nonebot import get_plugin_config, require, on_command, get_bot, get_driver, logger
from nonebot.plugin import PluginMetadata

from .config import Config
from requests import get, HTTPError
import time

require("nonebot_plugin_apscheduler")

from nonebot_plugin_apscheduler import scheduler


__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-lynchpined",
    description="A nonebot2 plugin to check Lynchpin progress.",
    usage="Get Lynchpin progress by sending 'lynchpin' command. Subscribe to daily Lynchpin progress by adding `lynchpined_user` or `lynchpined_group` in config",
    type="application",
    homepage="https://github.com/theTeamFuture/nonebot-plugin-lynchpined",
    supported_adapters={"~onebot.v11"},
    config=Config,
)

config = Config.parse_obj(get_driver().config)

LYNCHPIN_DEST = "https://ak.hypergryph.com/lynchpin/api/meta"

PATTERN = [0,4,12,15,24,33,34,35,35]
EPOCH = 1715529600

def get_progress()->int:
    response = get(LYNCHPIN_DEST)
    if response.status_code == 200:
        result = response.json()
        return result['data']['progress']
    else:
        raise HTTPError

def get_expected_progress(timestamp)->Tuple[int,int]:
    sec_diff = timestamp - EPOCH
    days = sec_diff // 86400
    days_in_period = days % len(PATTERN)
    return PATTERN[days_in_period], days_in_period

def get_msg()->str:
    progress = get_progress()
    t = int(time.time())
    expected_progress, days_in_period = get_expected_progress(t)
    comparison = 'Matched' if progress == expected_progress else 'UNMATCHED'
    msg = f'Lynchpin: {progress}%\nPattern {comparison}:\n'
    result = [f'{p:2}' if idx!=days_in_period else f'[{p:2}]' for idx,p in enumerate(PATTERN) ]
    msg += ' '.join(result)
    return msg

GET_LYNCHPINED = on_command("lynchpin", priority=10, block=True)

@GET_LYNCHPINED.handle()
async def show_progress(event, state):
    try:
        msg = get_msg()
        await GET_LYNCHPINED.send(msg)
    except HTTPError:
        await GET_LYNCHPINED.send('Lynchpin: HTTPError')


async def run_everyday():
    bot = get_bot()
    msg = get_msg()
    for group_id in config.lynchpined_group:
        await bot.send_group_msg(group_id=group_id, message=msg)
    
    for user_id in config.lynchpined_user:
        await bot.send_msg(user_id=user_id, message=msg)

    logger.info('Daily Lynchpin completed.')

    


scheduler.add_job(func=run_everyday,trigger="cron",second=3,minute=0,hour=0,id="lynchpin_subscribe")



