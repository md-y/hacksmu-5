import requests

URL = "https://us-central1-sendsms-399304.cloudfunctions.net/function-2"

PARAMS = {'message':'Youre app is failing!'}
 
# sending get request and saving the response as response object
requests.get(url = URL, params = PARAMS)
