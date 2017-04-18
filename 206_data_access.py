###### INSTRUCTIONS ###### 

# An outline for preparing your final project assignment is in this file.

# Below, throughout this file, you should put comments that explain exactly what you should do for each step of your project. 
# You should specify variable names and processes to use. For example, "Use dictionary accumulation with the list you just created 
# to create a dictionary called tag_counts, where the keys represent tags on flickr photos and the values represent frequency of 
# times those tags occur in the list."

# You can use second person ("You should...") or first person ("I will...") or whatever is comfortable for you, as long as you are 
# clear about what should be done.

# Some parts of the code should already be filled in when you turn this in:
# - At least 1 function which gets and caches data from 1 of your data sources, and an invocation of each of those functions to 
# show that they work 
# - Tests at the end of your file that accord with those instructions (will test that you completed those instructions correctly!)
# - Code that creates a database file and tables as your project plan explains, such that your program can be run over and over 
# again without error and without duplicate rows in your tables.
# - At least enough code to load data into 1 of your database tables (this should accord with your instructions/tests)

######### END INSTRUCTIONS #########

# Put all import statements you need here.
import json
import requests
import re
import tweepy
import twitter_info
import collections 
import sqlite3
import unittest
import itertools
import random

## Tweepy setup code borrowed from code given by Professor Cohen this semester.
##### TWEEPY SETUP CODE:

consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

##### END TWEEPY SETUP CODE

## Caching pattern:

cache_filename = "206_final_project_cache.json"

try:
	cache_file = open(cache_filename,'r')
	cache_stuff = cache_file.read()
	cache_file.close()
	cache_dictionary = json.loads(cache_stuff)

except:
	cache_dictionary = {}




# Begin filling in instructions....

def get_twitter_user(desiredUser):
	if desiredUser in cache_dictionary:
		userInfo = cache_dictionary[desiredUser]
	else:
		User = api.get_user(desiredUser)
		userInfo = [User["id"], User["screen_name"], User["favourites_count"], User["followers_count"]]
		cache_dictionary[desiredUser] = userInfo

		f = open(cache_filename,'w')
		f.write(json.dumps(cache_dictionary))
		f.close()
	return userInfo



def get_twitter_term(keyPhrase):
	if keyPhrase in cache_dictionary:
		results = cache_dictionary[keyPhrase]
	else:
		results = api.search(q=keyPhrase, count=10)
		cache_dictionary[keyPhrase] = results
		
		f = open(cache_filename,'w')
		f.write(json.dumps(cache_dictionary))
		f.close()
	return results

#def get_twitter_user():

def get_OMDB_info(movie):
	if movie in cache_dictionary:
		results = cache_dictionary[movie]
	else:
		baseurl = "http://www.omdbapi.com/?t="
		request = baseurl + movie

		results = requests.get(request)
		results = json.loads(results.text)


		cache_dictionary[movie] = results


		f = open(cache_filename,'w')
		f.write(json.dumps(cache_dictionary))
		f.close()

	print(results.keys())
	title = results["Title"]
	director = results["Director"]
	IMDB = results["imdbRating"]
	actors = results["Actors"].split(", ")
	#numLang is not right
	numLang = len(results["Language"])

	results = [title, director, IMDB, actors, numLang]
	print(results)
	return results



# Put your tests here, with any edits you now need from when you turned them in with your project plan.
get_OMDB_info("waterworld")

# Remember to invoke your tests so they will run! (Recommend using the verbosity=2 argument.)
if __name__ == "__main__":
	unittest.main(verbosity=2)