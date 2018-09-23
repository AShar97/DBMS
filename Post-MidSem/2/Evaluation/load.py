### Reading the data
import json
import os
# data = {}
# dirname = "./workshop_dataset1"
# for filename in os.listdir(dirname):
# 	with open(dirname+'/'+filename) as f:
# 		data.update(json.load(f))
# 		f.close()

data = json.load(open("./dataset.json"))

### Creating the graph

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
# media_list : map<text, map<text,text>> ##
# quoted_source_id : text
# url_list : set<text> ##
# tweet_text : text
# author_profile_image : text
# author_screen_name : text
# author_id : text
# lang : text
# keywords_processed_list : set<text>
# retweet_source_id : text
# mentions : set<text>
# replyto_source_id : text

from py2neo import Graph, Node, Relationship
g = Graph("bolt://localhost:7687", password="pass")
tx = g.begin()

g.run("CREATE CONSTRAINT ON (u:User) ASSERT u.author_screen_name IS UNIQUE")
g.run("CREATE CONSTRAINT ON (t:Tweet) ASSERT t.tid IS UNIQUE")
g.run("CREATE CONSTRAINT ON (h:Hashtag) ASSERT h.hashtag IS UNIQUE")

i = 0
for d in data:
	i += 1
	if i%100 is 0:
		tx.commit()
		tx = g.begin()
		print("\n",i)

	u = Node("User",
			 # verified=data[d]["verified"],
			 # author=data[d]["author"],
			 # author_profile_image=data[d]["author_profile_image"],
			 author_screen_name=data[d]["author_screen_name"],
			 # author_id=data[d]["author_id"]
			 )
	tx.merge(u, primary_label="User", primary_key="author_screen_name")
	# g.merge(u, label="User")
	
	u["verified"] = data[d]["verified"]
	u["author"] = data[d]["author"]
	u["author_profile_image"] = data[d]["author_profile_image"]
	u["author_id"] = data[d]["author_id"]
	
	# u.push()
	tx.push(u)
	# g.push(u)
	
	t = Node("Tweet",
			 # quote_count=data[d]["quote_count"],
			 # reply_count=data[d]["reply_count"],
			 # datetime=data[d]["datetime"],
			 # date=data[d]["date"],
			 # like_count=data[d]["like_count"],
			 # sentiment=data[d]["sentiment"],
			 # location=data[d]["location"],
			 tid=data[d]["tid"],
			 # retweet_count=data[d]["retweet_count"],
			 # ttype=data[d]["type"],
			 # tweet_text=data[d]["tweet_text"],
			 # lang=data[d]["lang"]
			 )
	tx.merge(t, primary_label="Tweet", primary_key="tid")
	# tx.create(t)
	# g.merge(t, label="Tweet")
	
	t["quote_count"] = data[d]["quote_count"]
	t["reply_count"] = data[d]["reply_count"]
	t["datetime"] = data[d]["datetime"]
	t["date"] = data[d]["date"]
	t["like_count"] = data[d]["like_count"]
	t["sentiment"] = data[d]["sentiment"]
	t["location"] = data[d]["location"]
	t["retweet_count"] = data[d]["retweet_count"]
	t["ttype"] = data[d]["type"]
	t["tweet_text"] = data[d]["tweet_text"]
	t["lang"] = data[d]["lang"]
	
	# t.push()
	tx.push(t)
	# g.push(t)

	POSTS = Relationship(u, "POSTS", t)

	tx.create(POSTS)
	# g.create(POSTS)
	
	if data[d]["quoted_source_id"]:
		quoted = Node("Tweet",
					 tid=data[d]["quoted_source_id"]
					 )
		tx.merge(quoted, primary_label="Tweet", primary_key="tid")
		# g.merge(quoted, label="Tweet")

		QUOTES = Relationship(t, "QUOTES", quoted)

		tx.create(QUOTES)
		# g.create(QUOTES)
	
	if data[d]["retweet_source_id"]:
		retweet = Node("Tweet",
					   tid=data[d]["retweet_source_id"]
					   )
		tx.merge(retweet, primary_label="Tweet", primary_key="tid")
		# g.merge(retweet, label="Tweet")

		RETWEETS = Relationship(t, "RETWEETS", retweet)

		tx.create(RETWEETS)
		# g.create(RETWEETS)
	
	if data[d]["replyto_source_id"]:
		replyto = Node("Tweet",
					   tid=data[d]["replyto_source_id"]
					   )
		tx.merge(replyto, primary_label="Tweet", primary_key="tid")
		# g.merge(replyto, label="Tweet")

		REPLY = Relationship(t, "REPLY", replyto)

		tx.create(REPLY)
		# g.create(REPLY)
	
	if (data[d]["keywords_processed_list"]
		and
		data[d]["keywords_processed_list"]!='NULL'
		and
		data[d]["keywords_processed_list"]!="''"
		and
		data[d]["keywords_processed_list"]!='""'
		):
		for k in data[d]["keywords_processed_list"]:
			if (k and k!='NULL' and k!='""' and k!="''"):
				keyword = Node("Keyword", keyword=k)
				
				tx.merge(keyword, primary_label="Keyword", primary_key="keyword")
				# g.merge(keyword, label="Keyword")

				HAS = Relationship(t, "HAS", keyword)

				tx.create(HAS)
				# g.create(HAS)

	if (data[d]["hashtags"]
		and
		data[d]["hashtags"]!='NULL'
		and
		data[d]["hashtags"]!="''"
		and
		data[d]["hashtags"]!='""'
		):
		for h in data[d]["hashtags"]:
			if (h and h!='NULL' and h!='""' and h!="''"):
				hashtag = Node("Hashtag", hashtag=h)
				
				tx.merge(hashtag, primary_label="Hashtag", primary_key="hashtag")
				# g.merge(hashtag, label="Hashtag")

				TAGS = Relationship(t, "TAGS", hashtag)

				tx.create(TAGS)
				# g.create(TAGS)

	if (data[d]["mentions"]
		and
		data[d]["mentions"]!='NULL'
		and
		data[d]["mentions"]!="''"
		and
		data[d]["mentions"]!='""'
		):
		for m in data[d]["mentions"]:
			if (m and m!='NULL' and m!='""' and m!="''"):
				mention = Node("User", author_screen_name=m)
				
				tx.merge(mention, primary_label="User", primary_key="author_screen_name")
				# g.merge(mention, label="User")

				MENTIONS = Relationship(t, "MENTIONS", mention)

				tx.create(MENTIONS)
				# g.create(MENTIONS)

	print(".", end="")

# print("\nLoaded.")

tx.commit()

print("\nDone.")