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



@router.register("pull_request", action="closed")
async def issue_opened_event(event, gh, *args, **kwargs):

    installation_id = event.data["installation"]["id"]

    installation_access_token = await apps.get_installation_access_token(
        gh,
        installation_id=installation_id,
        app_id=os.environ.get("GH_APP_ID"),
        private_key=os.environ.get("GH_PRIVATE_KEY")
    )

    #url for the comment url
    url = event.data['pull_request']['comments_url']
    
    #author of the issue creater
    author = event.data['pull_request']['user']['login']

    # avatar = event.data['issue']['user']['avatar_url']

    #sender of that event means who is altering the things
    sender = event.data['sender']['login']

    #finding owner to not react on that comment
    repo_owner = event.data['repository']['owner']['login']

    #check weather pull request is merged and closed or only closed
    pr_check = event.data['pull_request']['merged']

    #message to be posted
    message_c = f"<br><table><tbody><tr><td>Thanks for closing this pull_request and contributing to our repository @{author} ! We hope you loved to work with our repository 😋.</td></tr></tbody></table>"
    
    #message to be posted
    message_m = f"<br><table><tbody><tr><td>Hureeeeeeeh 🤩 ! Your Pull request has been merged 🥳 ! Thanks for contributing to our repository @{author} ! We hope you loved to work with our repository 😋.</td></tr></tbody></table>"
    

    #if pr check is true means it is merged
    if(pr_check):
        await gh.post(url, data={
        'body': message_m,
        },
        oauth_token=installation_access_token["token"]
                 )
    else:
        #if pr chech is false means it is not merged but only closed
        #it will only greet whenever pr closed by a user
        if(repo_owner != sender):
            await gh.post(url, data={
            'body': message_c,
            },
            oauth_token=installation_access_token["token"]
                 )
