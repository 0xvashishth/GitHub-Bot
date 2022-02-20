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

@router.register("workflow_run", action="completed")
async def workflow_job(event, gh, *arg, **kwargs):

	installation_id = event.data["installation"]["id"]

	installation_access_token = await apps.get_installation_access_token(
		gh,
		installation_id=installation_id,
		app_id=os.environ.get("GH_APP_ID"),
		private_key=os.environ.get("GH_PRIVATE_KEY")
	)

	status = event.data['workflow_run']['conclusion']
	ur = event.data['pull_request']['comments_url']
	link // we can set link acording to our convenience !!
	# pass
	if(status == "success"):
		messag = f"succeed"
		await gh.post(link, data={
			'body': messag,
			},
            oauth_token=installation_access_token["token"]
                 )

	elif(status == "failure"):
		messag = f"Failure"
		await gh.post(link, data={
			'body': messag,
			},
            oauth_token=installation_access_token["token"]
                 )
	else:
		return
