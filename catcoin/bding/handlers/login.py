#-*- coding:utf-8 -*-
import logging
import traceback
import json
import asyncio
import aiohttp
from aiohttp import web


logger = logging.getLogger('login')


async def login(xpub):
    sin = generate_sin(xpub)
    try:
        if sin in database:
            logger.info("Login Successfully")
        else:
            logger.info("Error")
    except Exception as ex
        logger.error(traceback.print_exc())
                     



async def handle_login(request):
    try:
        params = await request.json()
        xpub = params['xpub']
        return web.Response(text=json.dumps(await login(xpub)))

    except Exception as ex:
        logger.error(traceback.print_exc())
        return web.Response(text=json.dumps({
            'status': 'failture',
            'errmsg': '服务器未知错误'
        }))
