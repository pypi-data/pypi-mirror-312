import random
from typing import Annotated, Any

import nonebot
from nonebot import get_plugin_config
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.params import RegexGroup
from nonebot.plugin import PluginMetadata, on_regex

from .config import Config

global_config = nonebot.get_driver().config
plugin_config = get_plugin_config(Config)

__plugin_meta__ = PluginMetadata(
    name="选择困难症",
    description="选择困难症？Bot帮你选！",
    usage="发送选xx选xx即可触发",
    type="application",
    homepage="https://github.com/SherkeyXD/nonebot-plugin-make-choice",
    supported_adapters={"~onebot.v11"},
    config=Config,
)

choice = on_regex(r"^[选要](\S*)[选要](\S*)", priority=20, block=True)


@choice.handle()
async def make_choice(
    event: Event, match_group: Annotated[tuple[Any, ...], RegexGroup()]
):
    random_choice = random.choice(match_group)
    if random.random() < plugin_config.choose_both_chance:
        random_choice = "我全都要！"
    await choice.finish(
        MessageSegment.reply(id_=event.message_id)
        + MessageSegment.text(f"建议您选择：\n{random_choice}")
    )
