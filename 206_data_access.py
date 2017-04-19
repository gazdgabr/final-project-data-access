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




#Write a function called get_twitter_user that goes to Twitter, gets data about a Twitter user, and dumps it in the cache. 

def get_twitter_user(desiredUser):
	if desiredUser + "_user" in cache_dictionary:
		userInfo = cache_dictionary[desiredUser + "_user"]
	else:
		User = api.get_user(desiredUser)
		userInfo = [User["id"], User["screen_name"], User["favourites_count"], User["followers_count"]]
		cache_dictionary[desiredUser + "_user"] = userInfo

		f = open(cache_filename,'w')
		f.write(json.dumps(cache_dictionary))
		f.close()
	return userInfo


# Write a function called get_twitter_term that goes to Twitter, gets tweets associated with a search term, and dumps them in the cache.

def get_twitter_term(keyPhrase):
	if keyPhrase + "_tweets"  in cache_dictionary:
		results = cache_dictionary[keyPhrase + "_tweets"]
	else:
		results = api.search(q=keyPhrase, count=10)
		cache_dictionary[keyPhrase + "_tweets"] = results
		
		f = open(cache_filename,'w')
		f.write(json.dumps(cache_dictionary))
		f.close()
	return results



# Write a function called get_OMDB_info that goes to the OMDB API, gets data about a specified movie, and dumps the result in the cache.

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

	return results



	'''
	These should be in the movie constructor
	title = results["Title"]
	director = results["Director"]
	IMDB = results["imdbRating"]
	actors = results["Actors"].split(", ")
	results = [title, director, IMDB, actors, numLang]
	#numLang is not right
	numLang = len(results["Language"])

	'''





# Create a class to handle Twitter users, call it twitterUsers. This will contain variables to store the user's ID, screen name, favorites count,
# and followers count. 

	# Define a constructor which takes in a dictionary representing a twitter user, and stors the pertinent data in the proper variables

	# Define a method that returns a the id of the user

	# Define a method that returns a list in this format: [screenname, favorites count, followers count]


# make a class to handle the Movie data, called Movie. This will contain variables to store its title, its director, its imdb rating, a list of actors,
# and the number of languages in the movie.

	# Define a constructor which takes in a dictionary representing a Movie, and stors the pertinent data in the proper variables

	# Define a _str_ method that returns the name of the movie

	# Define a method called infoList which returns a list in this format: [director, imdb rating, list of actors, number of languages]

# make a list containing the names of three movies
threeMovies = ["logan", "get out", "fate of the furious"]

# invoke the get_OMDB_info() function on all three of these movies
threeMovieDictions = []
for movie in threeMovies:
	threeMovieDictions.append(get_OMDB_info(movie))

# Using threeMovieDiction, create a Movie instance class for each of the three movies

# invoke the get_twitter_term() function for each of those three movies, store the resulting dictionaries in a list
MovieTweets = [get_twitter_term("fate of the furious"), get_twitter_term("logan"), get_twitter_term("get out")]

# Gather data about each user in the neighborhood of these tweets.
	# Iterate through all of the tweets in MovieTweets and store the screenname of each tweets author, and also the screen name of each
	# mentioned user. Store all of these screen names in a list called neighborhood

	#iterate across the neighborhood list and create an instance of TwitterUsers for each screenName in this list.

# Create a database file called finalproject.db. It should have three tables: Tweets, Users, and Movies. Each table should be laid out as follows:

# Tweets, with these columns:
	# tweet_text - the text in the tweet
	# tweet_id - the INTEGER PRIMARY KEY, with the string ID of the tweet from Twitter
	# user - the ID string that represents the user - references the Users table
	# movie - the string of the movie search the tweet came from; it will reference the Movies table
	# favorites - integer that represents the number of favorites that the tweet has
	# retweets - integer that represents the number of retweets that the tweet has

# Users, with these columns:
	# user_id - the INTEGER PRIMARY KEY, with the string ID of the Twitter user
	# screen_name - a string with the Twitter handle of the person who tweeted this tweet
	# user_favs - integer that represents the number of favorites the user has
	# followers - integer that represents the number of followers the user has

# Movies, with these columns:
	# movie_id - INTEGER PRIMARY KEY, with the string ID of the movie in the OMDB
	# title - string title of the movie
	# director - string name of the movie's director
	# languages - integer that represents the number of languages the movie is in
	# rating - string that represents the movie's IMDB rating
	# top_actor - string name of the top billed actor in the movie



conn = sqlite3.connect('finalproject.db')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Tweets')
cur.execute('DROP TABLE IF EXISTS Users')
cur.execute('DROP TABLE IF EXISTS Movies')

statement = 'CREATE TABLE IF NOT EXISTS '
statement += 'Tweets (tweet_text TEXT, tweet_id INTEGER PRIMARY KEY, user TEXT, movie TEXT, favorites INTEGER, retweets INTEGER)'
cur.execute(statement)

statement = 'CREATE TABLE IF NOT EXISTS '
statement += 'Users (user_id INTEGER PRIMARY KEY, screen_name TEXT, user_favs INTEGER, followers INTEGER)'
cur.execute(statement)

statement = 'CREATE TABLE IF NOT EXISTS '
statement += 'Movies (movie_id INTEGER PRIMARY KEY, title TEXT, director TEXT, languages INTEGER, rating TEXT, top_actor TEXT)'
cur.execute(statement)


userList = [get_twitter_user("TheRock"), get_twitter_user("RealHughJackman"), get_twitter_user("JordanPeele")]


#the following is adapted from lab 3
element_list = []
for maBoi in userList:
		user_id_item = maBoi[0]
		screen_name_item = maBoi[1]
		user_favs_item = maBoi[2]
		followers_item = maBoi[3]
		element_list.append((user_id_item, screen_name_item, user_favs_item, followers_item))

statement = 'INSERT INTO Users VALUES (?, ?, ?, ?)'    
for element in element_list:
	cur.execute(statement, element)

conn.commit()

# make some data base queries to find out interesting information
	# has a user tweeted about multiple movies?
	# has a user retweeted a director of one of the movies?
	# has an actor been in multiple of these movies?
# create an output

# Put your tests here, with any edits you now need from when you turned them in with your project plan.

# Testing cache loading: 
get_OMDB_info("waterworld")
get_OMDB_info("elf")
get_OMDB_info("ghostbusters")
get_OMDB_info("the exorcism")
get_OMDB_info("the princess bride")



class DatabaseTests(unittest.TestCase):

	def test_db_tweets(self):
		conn = sqlite3.connect('final_project_tweets.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Tweets');
		dis = cur.fetchall()
		conn.close()
		self.assertTrue(len(dis)>=3)

	def test_db_movies(self):
		conn = sqlite3.connect('final_project_tweets.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Movies');
		dat = cur.fetchall()
		conn.close()
		self.assertTrue(len(dat)>=3)
'''
class TwitterTests(unittest.TestCase):

	def test

class OMDBtests(unittest.TestCase):

	def test
'''

# Remember to invoke your tests so they will run! (Recommend using the verbosity=2 argument.)
if __name__ == "__main__":
	unittest.main(verbosity=2)