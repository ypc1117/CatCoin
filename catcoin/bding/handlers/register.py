#-*- coding:utf-8 -*-
import logging
import traceback
import json
import asyncio
import aiohttp
from aiohttp import web


logger = logging.getLogger('register')


async def register(username):
    privkey,xpub = generate_keypairs()

    x_signature = generate_signature(privkey,url)
    signature = Signature(x_signature.r,x_signature.s)  
    if generate_verfication(xpub,url,signature):
        sin = generate_sin(xpub)
            ##insert into database
    else:
        print "INVAILD SIGNATURE"                 



async def handle_register(request):
    try:
        params = await request.json()
        username = params['username']
        return web.Response(text=json.dumps(await register(username)))

    except Exception as ex:
        logger.error(traceback.print_exc())
        return web.Response(text=json.dumps({
            'status': 'failture',
            'errmsg': '服务器未知错误'
        }))
