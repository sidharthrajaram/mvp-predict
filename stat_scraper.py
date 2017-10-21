import pprint
from googleapiclient.discovery import build

api_key = 'AIzaSyDnFvuTtCa7DqCQ1zdJrCGr8JO9LxX32us'
cse_id = '009205659464253359167:mus4plss10w'

def google_search(search_term, api_key, cse_id, **kwargs):
	service = build("customsearch", "v1", developerKey=api_key)
	res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
	return res['items']

if __name__ == '__main__':

	player = 'LeBron James'

	results = google_search(player, api_key, cse_id, num=1)
	prelim_url = results[0]["formattedUrl"]
	print(prelim_url)