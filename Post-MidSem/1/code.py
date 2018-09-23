### Reading the data
import json
import os
data = {}
dailyhashcount = {}
dirname = "./workshop_dataset1"
for filename in os.listdir(dirname):
	dailyhashcount[filename[:-5]] = {}
	with open(dirname+'/'+filename) as f:
		data.update(json.load(f))
		f.close()

### Creating the table

# quote_count : int
# reply_count : int
# hashtags : set<text>
# datetime : timestamp
# date : date
# like_count : int
# verified : boolean
# sentiment : tinyint
# author : text
# location : text
# tid : text
# retweet_count : int
# type : text
# media_list : map<text, map<text,text>>
# quoted_source_id : text
# url_list : set<text>
# tweet_text : text
# author_profile_image : text
# author_screen_name : text
# author_id : text
# lang : text
# keywords_processed_list : set<text>
# retweet_source_id : text
# mentions : set<text>
# replyto_source_id : text

from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster

cluster = Cluster(['127.0.0.1'], port=9042)
session = cluster.connect()

querydb = "create keyspace if not exists twitter with replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' };"
session.execute(querydb)
session.set_keyspace('twitter')

try:
	# query_t = "truncate tweets if exists;"
	query_1 = "truncate table1 if exists;"
	query_2 = "truncate table2 if exists;"
	query_3 = "truncate table3 if exists;"
	query_4 = "truncate table4 if exists;"
	query_5 = "truncate table5 if exists;"
	query_6 = "truncate table6 if exists;"
	query_7 = "truncate table7 if exists;"

	# session.execute(query_t)
	session.execute(query_1)
	session.execute(query_2)
	session.execute(query_3)
	session.execute(query_4)
	session.execute(query_5)
	session.execute(query_6)
	session.execute(query_7)

except:
	# query_t = "create table if not exists tweets (quote_count int, reply_count int, hashtags set<text>, datetime timestamp, date date, like_count int, verified boolean, sentiment tinyint, author text, location text, tid text, retweet_count int, type text, media_list map<text, map<text,text>>, quoted_source_id text, url_list set<text>, tweet_text text, author_profile_image text, author_screen_name text, author_id text, lang text, keywords_processed_list set<text>, retweet_source_id text, mentions set<text>, replyto_source_id text, PRIMARY KEY (tid));"
	query_1 = "create table if not exists table1 (datetime timestamp, location text, tid text, tweet_text text, author_screen_name text, author_id text, lang text, PRIMARY KEY (author_screen_name, datetime, tid)) with clustering order by (datetime desc);"
	query_2 = "create table if not exists table2 (like_count int, tid text, tweet_text text, keyword_processed text, PRIMARY KEY (keyword_processed, like_count, tid)) with clustering order by (like_count desc);"
	query_3 = "create table if not exists table3 (hashtag text, datetime timestamp, tid text, tweet_text text, PRIMARY KEY (hashtag, datetime, tid)) with clustering order by (datetime desc);"
	query_4 = "create table if not exists table4 (datetime timestamp, tid text, tweet_text text, mention text, PRIMARY KEY (mention, datetime, tid)) with clustering order by (datetime desc);"
	query_5 = "create table if not exists table5 (date date, like_count int, tid text, tweet_text text, PRIMARY KEY (date, like_count, tid)) with clustering order by (like_count desc);"
	query_6 = "create table if not exists table6 (location text, tid text, tweet_text text, PRIMARY KEY (location, tid));"
	query_7 = "create table if not exists table7 (hashtag text, date date, count int, PRIMARY KEY (date));"

	# session.execute(query_t)
	session.execute(query_1)
	session.execute(query_2)
	session.execute(query_3)
	session.execute(query_4)
	session.execute(query_5)
	session.execute(query_6)
	session.execute(query_7)

### Inserting the data

from cassandra.encoder import Encoder
encoder_object = Encoder()
# parsedstring = encoder_object.cql_encode_str((string).encode('utf-8'))


query1 = "insert into table1 (datetime, location, tid, tweet_text, author_screen_name, author_id, lang) values (%s, %s, %s, %s, %s, %s, %s);"
query2 = "insert into table2 (like_count, tid, tweet_text, keyword_processed) values (%d, %s, %s, %s);"
query3 = "insert into table3 (hashtag, datetime, tid, tweet_text) values (%s, %s, %s, %s);"
query4 = "insert into table4 (datetime, tid, tweet_text, mention) values (%s, %s, %s, %s);"
query5 = "insert into table5 (date, like_count, tid, tweet_text) values (%s, %d, %s, %s);"
query6 = "insert into table6 (location, tid, tweet_text) values (%s, %s, %s);"
query7 = "insert into table7 (hashtag, date, count) values (%s, %s, %d);"

i = 0

for d in data:
	if (data[d]["location"]):
		location = encoder_object.cql_encode_str((data[d]["location"]).encode('utf-8'))
	else:
		location = 'NULL'
	tweet_text = encoder_object.cql_encode_str((data[d]["tweet_text"]).encode('utf-8'))

	datetime = encoder_object.cql_encode_str((data[d]["datetime"]).encode('utf-8'))
	tid = encoder_object.cql_encode_str((data[d]["tid"]).encode('utf-8'))
	author_screen_name = encoder_object.cql_encode_str((data[d]["author_screen_name"]).encode('utf-8'))
	author_id = encoder_object.cql_encode_str((data[d]["author_id"]).encode('utf-8'))
	lang = encoder_object.cql_encode_str((data[d]["lang"]).encode('utf-8'))

	# like_count = encoder_object.cql_encode_str((data[d]["like_count"]).encode('utf-8'))
	date = encoder_object.cql_encode_str((data[d]["date"]).encode('utf-8'))

	session.execute(query1 % (datetime, location, tid, tweet_text, author_screen_name, author_id, lang))

	if (data[d]["keywords_processed_list"] and data[d]["keywords_processed_list"]!='NULL' and data[d]["keywords_processed_list"]!="''" and data[d]["keywords_processed_list"]!='""'):
		for k in data[d]["keywords_processed_list"]:
			if (k and k!='NULL' and k!='""' and k!="''"):
				keyword_processed = encoder_object.cql_encode_str((k).encode('utf-8'))
				session.execute(query2 % (data[d]["like_count"], tid, tweet_text, keyword_processed))

	if (data[d]["hashtags"]):
		for h in data[d]["hashtags"]:
			hashtag = encoder_object.cql_encode_str((h).encode('utf-8'))
			session.execute(query3 % (hashtag, datetime, tid, tweet_text))

			if hashtag not in dailyhashcount[data[d]["date"]]:
				dailyhashcount[data[d]["date"]][hashtag] = 1
			else:
				dailyhashcount[data[d]["date"]][hashtag] += 1

	if (data[d]["mentions"]):
		for m in data[d]["mentions"]:
			mention = encoder_object.cql_encode_str((m).encode('utf-8'))
			session.execute(query4 % (datetime, tid, tweet_text, mention))

	session.execute(query5 % (date, data[d]["like_count"], tid, tweet_text))

	if (location and location!='NULL' and location!=''):
		session.execute(query6 % (location, tid, tweet_text))

	i+=1
	if i%1000==0:
		print(i)

for d in dailyhashcount:
	for h in dailyhashcount[d]:
		date = encoder_object.cql_encode_str((d).encode('utf-8'))

		session.execute(query7 % (h, date, dailyhashcount[d][h]))

	i+=1
	if i%1000==0:
		print(i)

