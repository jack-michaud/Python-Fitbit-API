import requests
import base64
import json
'''
Created by: Jack Michaud

----- Basic usage ----- 

from fitbitAPI import *

fbapi = FitBitAPI('<client_id>','<client_secret>')
URL = fbapi.get_auth_url('http://example.com', ['activity','heartrate','location'])

#Go to URL, log in, get CODE from URL

CODE = '#####'
fbapi.get_access_token(CODE, 'http://example.com')
fbapi.access_endpoint('https://api.fitbit.com/1/user/-/activities/steps/date/today/1m.json')

-----------------------

'''

class FitBitAPI:
	CLIENT_ID = ''
	CLIENT_SECRET = ''
	AUTHORIZATION_HEADER = ''

	Authorization_URL = 'https://www.fitbit.com/oauth2/authorize'
	Access_Token_Request_URL = 'https://api.fitbit.com/oauth2/token'

	'''
	The parameters are app specific. Register app here: https://dev.fitbit.com/

	'''
	def __init__(self, client_id, client_secret):
		self.CLIENT_ID = client_id
		self.CLIENT_SECRET = client_secret

	
	'''
	Fitbit Docs: https://dev.fitbit.com/docs/oauth2/#authorization-page

	required - Redirect URI: MUST BE MATCH. Where Fitbit should send the user after the user grants or denies consent.
	required - Scope: An array of the permissions you're requesting. (See https://dev.fitbit.com/docs/oauth2/#scope)
	optional - prompt: Specify if you need to force the Fitbit authentication or the OAuth 2.0 authorization page to be displayed.

	'''
	def get_auth_url(self, redirect_uri, scope, prompt="none"):
		querystring = {
			"response_type": "code",
			"client_id": self.CLIENT_ID,
			"redirect_uri": redirect_uri,
			"scope": " ".join(scope)
		}
		response = requests.get(self.Authorization_URL, params=querystring)
		
		return response.url

	'''
	Fitbit Docs: https://dev.fitbit.com/docs/oauth2/#access-token-request

	required - Code: The authorization code received in the redirect as a URI parameter.
	required - Redirect URI: Required if specified in the redirect to the authorization page. 

	'''
	def get_access_token(self, code, redirect_uri):
		payload = "grant_type=authorization_code&code={}&redirect_uri={}".format(code, redirect_uri)
		headers = {
		    'authorization': "Basic {}".format(base64.b64encode("{}:{}".format(self.CLIENT_ID, self.CLIENT_SECRET))),
		    'content-type': "application/x-www-form-urlencoded",
		    'cache-control': "no-cache",
		}

		response = requests.post(self.Access_Token_Request_URL, data=payload, headers=headers)
		
		info = json.loads(response.text)
		if info.get('access_token', None) is not None:
			self.AUTHORIZATION_HEADER = "{} {}".format(info.get('token_type'), info.get('access_token'))
			return info
		else:
			return "Failure. Maybe invalid code or check if redirect_uri is an exact match."

	'''
	Fitbit Docs: https://dev.fitbit.com/docs/

	required - URL: Any fitbit api url. 

	'''
	def access_endpoint(self, url):
		if AUTHORIZATION_HEADER is '':
			return "Must run get_access_token() first."

		headers = {
		    'authorization': AUTHORIZATION_HEADER,
		    'cache-control': "no-cache",
		}
		response = requests.get(url, headers=headers)

		return json.loads(response.text)


