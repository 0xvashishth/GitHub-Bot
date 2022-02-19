import asyncio
import os
import sys
import traceback
import aiohttp
from aiohttp import web
from gidgethub import aiohttp as gh_aiohttp
from gidgethub import routing
from gidgethub import sansio
from gidgethub import apps

router = routing.Router()

@router.register("issue_comment", action="created")
async def issue__comment_create_event(event, gh, *args, **kwargs):


    installation_id = event.data["installation"]["id"]

    installation_access_token = await apps.get_installation_access_token(
        gh,
        installation_id=installation_id,
        app_id=os.environ.get("GH_APP_ID"),
        private_key=os.environ.get("GH_PRIVATE_KEY")
    )


    url = event.data['comment']['reactions']['url']

    repo_owner = event.data['repository']['owner']['login']

    #finding author of the comment
    author = event.data['comment']['user']['login']


    if(author != repo_owner and author != 'pygithub-bot-app[bot]') :

        message = 'heart'

        await gh.post(url, data={
            'content': message,
        },
        oauth_token=installation_access_token["token"]
                 )

@router.register("issue_comment", action="edited")
async def issue__comment_edit_event(event, gh, *args, **kwargs):

    installation_id = event.data["installation"]["id"]

    installation_access_token = await apps.get_installation_access_token(
        gh,
        installation_id=installation_id,
        app_id=os.environ.get("GH_APP_ID"),
        private_key=os.environ.get("GH_PRIVATE_KEY")
    )
    url = event.data['comment']['reactions']['url']

    repo_owner = event.data['repository']['owner']['login']

    author = event.data['comment']['user']['login']


    if(author != repo_owner and author != 'pygithub-bot-app[bot]') :

        message = 'eyes'

        await gh.post(url, data={
            'content': message,
        },
        oauth_token=installation_access_token["token"]
                 )