import requests
import tokenInfo #frick off haCkeRZZSZ you aint getting our token 
from videoGenerator import generator
import os
import random

def main():
	generator()
	graph = facebook.GraphAPI(tokenInfo.ACCESSTOKEN)
	message = f"Apollo 11 Mission Log #{random.randint(0,1000)}"
	path="nice.mp4"
	with open(os.path.realpath(path),"rb") as f:
		files={'file':f}
		url=f'https://graph-video.facebook.com/v4.0/me/videos?access_token={token}&description={message}'
		flag=requests.post(url, files=files).json()
		print(f"Succesfully posted {message} with id"+flag["id"])

if __name__ == '__main__':
	# print(tokenInfo.ACCESSTOKEN)
	main()