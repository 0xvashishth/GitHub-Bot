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

    #url for the comment reaction api
    url = event.data['issue']['url']
    main_url = url + "/assignees"

    #comment url
    url_comment = event.data['issue']['comments_url']

    #assignee check
    assinee = event.data['issue']['assignee']

    #issue body from the issue comment
    comment_body = event.data['comment']['body']

    #finding owner to not react on that comment
    issue_owner = event.data['issue']['user']['login']

    #finding author of the comment
    author = event.data['comment']['user']['login']

    #message for not assigning
    message = "We cannot assign this issue to you as it already assigned to someone ! Thanks !";
    message = "We cannot assign this issue to you as you are not owner of this issue ! Thanks !";

    if(comment_body == '/assign') :
        if(assinee) :
            await gh.post(url_comment, data={
                'body': message,
            },
            oauth_token=installation_access_token["token"]
                 )
        else:
            if(author == issue_owner) :
                await gh.post(main_url, data={
                    'assignees' : [author],
                },
                oauth_token=installation_access_token["token"]
                     )
            else:
                await gh.post(url_comment, data={
                    'body': message1,
                },
                oauth_token=installation_access_token["token"]
                     )