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

LABEL1 = 'review_needed' # label name
LABEL2 = 'GSSoC22'
LABEL3 = 'CX'

@router.register("pull_request", action="opened")
async def issue_opened_event(event, gh, *args, **kwargs):

    installation_id = event.data["installation"]["id"]
    pull_body = event.data["pull_request"]["body"]

    installation_access_token = await apps.get_installation_access_token(
        gh,
        installation_id=installation_id,
        app_id=os.environ.get("GH_APP_ID"),
        private_key=os.environ.get("GH_PRIVATE_KEY")
    )

    is_url = event.data['pull_request']['issue_url']
    suffix = '/labels{/name}'
    label_url = is_url + suffix
    
    await gh.post(label_url, data=[LABEL1],
        oauth_token=installation_access_token["token"]) #event post for key label

    if(pull_body.find("GSSOC22") == -1):
        pass
    else:
        await gh.post(label_url, data=[LABEL2],
		oauth_token=installation_access_token["token"])

    if(pull_body.find("Community Exchange") == -1):
        pass
    else:
	    await gh.post(label_url, data=[LABEL3],
		oauth_token=installation_access_token["token"])
    # await gh.post(label_url, data=[LABEL2],
    #     oauth_token=installation_access_token["token"]
    #              )