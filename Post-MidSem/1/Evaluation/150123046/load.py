### Reading the data
import json
import os

data = {}
dailyhashmentioncount = {}
dailyusercount = {}

dirname = "./workshop_dataset1"
for filename in os.listdir(dirname):

	dailyhashmentioncount[filename[:-5]] = {}
	dailyusercount[filename[:-5]] = {}

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
	query_4 = "truncate table4 if exists;"
	query_8 = "truncate table8 if exists;"

	# session.execute(query_t)
	session.execute(query_4)
	session.execute(query_8)

except:
	# query_t = "create table if not exists tweets (quote_count int, reply_count int, hashtags set<text>, datetime timestamp, date date, like_count int, verified boolean, sentiment tinyint, author text, location text, tid text, retweet_count int, type text, media_list map<text, map<text,text>>, quoted_source_id text, url_list set<text>, tweet_text text, author_profile_image text, author_screen_name text, author_id text, lang text, keywords_processed_list set<text>, retweet_source_id text, mentions set<text>, replyto_source_id text, PRIMARY KEY (tid));"
	query_4 = "create table if not exists table4 (date date, author_id text, count int, PRIMARY KEY (date, count, author_id)) with clustering order by (count desc);"
	query_8 = "create table if not exists table8 (date date, hashtag text, mention text, count int, PRIMARY KEY (date, count, hashtag, mention)) with clustering order by (count desc);"

	# session.execute(query_t)
	session.execute(query_4)
	session.execute(query_8)

### Inserting the data

from cassandra.encoder import Encoder
encoder_object = Encoder()
# parsedstring = encoder_object.cql_encode_str((string).encode('utf-8'))


query4 = "insert into table4 (date, author_id, count) values (%s, %s, %d);"
query8 = "insert into table8 (date, hashtag, mention, count) values (%s, %s, %s, %d);"

i = 0

for d in data:
	# author_screen_name = encoder_object.cql_encode_str((data[d]["author_screen_name"]).encode('utf-8'))
	author_id = encoder_object.cql_encode_str((data[d]["author_id"]).encode('utf-8'))
	# date = encoder_object.cql_encode_str((data[d]["date"]).encode('utf-8'))

	if author_id not in dailyusercount[data[d]["date"]]:
		dailyusercount[data[d]["date"]][author_id] = 1
	else:
		dailyusercount[data[d]["date"]][author_id] += 1

	if (data[d]["hashtags"] and data[d]["hashtags"]!='NULL' and data[d]["hashtags"]!="''" and data[d]["hashtags"]!='""'):
		for h in data[d]["hashtags"]:
			if (h and h!='NULL' and h!='""' and h!="''"):
				hashtag = encoder_object.cql_encode_str((h).encode('utf-8'))
				
				if (data[d]["mentions"] and data[d]["mentions"]!='NULL' and data[d]["mentions"]!="''" and data[d]["mentions"]!='""'):
					if hashtag not in dailyhashmentioncount[data[d]["date"]]:
						dailyhashmentioncount[data[d]["date"]][hashtag] = {}
					
					for m in data[d]["mentions"]:
						if (m and m!='NULL' and m!='""' and m!="''"):
							mention = encoder_object.cql_encode_str((m).encode('utf-8'))

							if mention not in dailyhashmentioncount[data[d]["date"]][hashtag]:
								dailyhashmentioncount[data[d]["date"]][hashtag][mention] = 1
							else:
								dailyhashmentioncount[data[d]["date"]][hashtag][mention] += 1

	i+=1
	if i%1000==0:
		print(i/1120," %")

for d in dailyusercount:
	date = encoder_object.cql_encode_str((d).encode('utf-8'))
	for u in dailyusercount[d]:
		session.execute(query4 % (date, u, dailyusercount[d][u]))

	i+=1
	if i%10==0:
		print(i/1120," %")

for d in dailyhashmentioncount:
	date = encoder_object.cql_encode_str((d).encode('utf-8'))
	for h in dailyhashmentioncount[d]:
		for m in dailyhashmentioncount[d][h]:
			session.execute(query8 % (date, h, m, dailyhashmentioncount[d][h][m]))

	i+=1
	if i%10==0:
		print(i/1120," %")

print(100," %")