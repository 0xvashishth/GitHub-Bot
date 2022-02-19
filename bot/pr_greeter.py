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


@router.register("pull_request", action="opened")
async def opened_pr(event, gh, *arg, **kwargs):

    installation_id = event.data["installation"]["id"]

    installation_access_token = await apps.get_installation_access_token(
        gh,
        installation_id=installation_id,
        app_id=os.environ.get("GH_APP_ID"),
        private_key=os.environ.get("GH_PRIVATE_KEY")
    )

    author = event.data['pull_request']['user']['login']
    ur = event.data['pull_request']['comments_url']

    messag = f"<br><table><tbody><tr><td>Thanks for opening the pull request @{author}! I will look into it ASAP!\n Till then you can improve your code & you can show your love by staring my repos 😋.</td></tr></tbody></table>"
    await gh.post(ur, data={
        'body': messag,
        },
        oauth_token=installation_access_token["token"]
                 )
            