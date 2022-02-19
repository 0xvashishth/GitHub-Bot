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

LABEL = 'review_needed' # label name

@router.register("issues", action="opened")
async def issue_opened_event(event, gh, *args, **kwargs):
    label = event.data['issue']['labels_url']

    installation_id = event.data["installation"]["id"]

    installation_access_token = await apps.get_installation_access_token(
        gh,
        installation_id=installation_id,
        app_id=os.environ.get("GH_APP_ID"),
        private_key=os.environ.get("GH_PRIVATE_KEY")
    )

    await gh.post(label, data=[LABEL],
        oauth_token=installation_access_token["token"]
                 ) #event post for key label