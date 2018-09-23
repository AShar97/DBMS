from py2neo import Graph, Node, Relationship
g = Graph("bolt://localhost:7687", password="pass")

# from datetime import datetime, timedelta
# # (datetime.strptime(string, "%Y-%m-%d").date() - timedelta(7)).isoformat()

# Queries in the assignment
query1 = "MATCH (u:User {author_screen_name:'%s'})-[:POSTS]->(t:Tweet) RETURN u.author_screen_name, t.datetime, t.tid, t.tweet_text, t.location, t.lang ORDER BY t.datetime DESC"
query2 = "MATCH (u:User {author_screen_name:'%s'})-[:POSTS]->(t:Tweet)-[:MENTIONS]->(m:User) RETURN DISTINCT u.author_screen_name, m.author_screen_name"
query3 = "MATCH (h1:Hashtag)<-[:TAGS]-(t:Tweet)-[:TAGS]->(h2:Hashtag) where h1.hashtag>=h2.hashtag RETURN DISTINCT h1.hashtag, h2.hashtag, count(*) as c ORDER BY c DESC LIMIT 20"
query4 = "MATCH (h:Hashtag {hashtag:'%s'})<-[:TAGS]-(t:Tweet)-[:MENTIONS]->(m:User) RETURN DISTINCT h.hashtag, m.author_screen_name, count(*) as c ORDER BY c DESC LIMIT 20"
query5 = "MATCH (t:Tweet {location:'%s'})-[:TAGS]->(h:Hashtag) RETURN DISTINCT t.location, h.hashtag"
query6 = "MATCH (u1:User)-[:POSTS]->(t:Tweet)-[:RETWEETS]->(rt:Tweet)<-[:POSTS]-(u2:User) RETURN DISTINCT u1.author_screen_name, u2.author_screen_name, count(*) as c ORDER BY c DESC LIMIT 5"
query7 = "MATCH (u1:User)-[:POSTS]->(t:Tweet)-[:REPLY]->(rt:Tweet)<-[:POSTS]-(u2:User) RETURN DISTINCT u1.author_screen_name, u2.author_screen_name, count(*) as c ORDER BY c DESC LIMIT 5"
query8 = "MATCH (u:User {author_screen_name:'%s'})-[p:POSTS]->(t:Tweet) DETACH DELETE p"


from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
	if(request.method=='GET'):
		return render_template('index.html')
	else:
		index = request.form["index"]
		string = request.form["name"]
		
		if (string and string!='NULL' and string!='""' and string!="''"):
			if index=='1':
				data = g.data(query1 % string)

				output = "<table class='table table-hover'><thead>"
				header = ['datetime', 'author_screen_name', 'tid', 'tweet_text', 'location', 'lang']
				for h in header:
					output += "<th>" + str(h) + "</th>"
				output += "</thead><tbody>"
				for row in data:
					output += "<tr>"
					# li = [row['t.datetime'], row['u.author_screen_name'], row['t.tid'], row['t.tweet_text'], row['t.location'], row['t.lang']]
					li = [row[1], row[0], row[2], row[3], row[4], row[5]]
					for txt in li:
						# output += "<td>" + str(txt).replace('\n', ' ').replace('\'', '\\\'').replace('\"', '\\\"').replace('\t',' ').replace('\r', ' ') + "</td>"
						output += "<td>" + txt + "</td>"
						# output += "<td>" + txt.replace('\n', ' ').replace('\'', '\\\'').replace('\"', '\\\"').replace('\t',' ').replace('\r', ' ') + "</td>"
					output += "</tr>"
				output += "</tbody></table>"

			elif index=='2':
				data = g.data(query2 % string)

				output = "<table class='table table-hover'><thead>"
				header = ['Given User', 'Mentioned User']
				for h in header:
					output += "<th>" + str(h) + "</th>"
				output += "</thead><tbody>"
				for row in data:
					output += "<tr>"
					# li = [row['u.author_screen_name'], row['m.author_screen_name']]
					li = [row[0], row[1]]
					for txt in li:
						# output += "<td>" + str(txt).replace('\n', ' ').replace('\'', '\\\'').replace('\"', '\\\"').replace('\t',' ').replace('\r', ' ') + "</td>"
						output += "<td>" + txt + "</td>"
						# output += "<td>" + txt.replace('\n', ' ').replace('\'', '\\\'').replace('\"', '\\\"').replace('\t',' ').replace('\r', ' ') + "</td>"
					output += "</tr>"
				output += "</tbody></table>"

			elif index=='4':
				data = g.data(query4 % string)

				output = "<table class='table table-hover'><thead>"
				header = ['Given Hashtag', 'Mentioned User', 'Frequency']
				for h in header:
					output += "<th>" + str(h) + "</th>"
				output += "</thead><tbody>"
				for row in data:
					output += "<tr>"
					# li = [row['h.hashtag'], row['m.author_screen_name'], row['c']]
					li = [row[0], row[1], str(row[2])]
					for txt in li:
						# output += "<td>" + str(txt).replace('\n', ' ').replace('\'', '\\\'').replace('\"', '\\\"').replace('\t',' ').replace('\r', ' ') + "</td>"
						output += "<td>" + txt + "</td>"
						# output += "<td>" + txt.replace('\n', ' ').replace('\'', '\\\'').replace('\"', '\\\"').replace('\t',' ').replace('\r', ' ') + "</td>"
					output += "</tr>"
				output += "</tbody></table>"

			elif index=='5':
				data = g.data(query5 % string)

				output = "<table class='table table-hover'><thead>"
				header = ['Given Location', 'Hashtag']
				for h in header:
					output += "<th>" + str(h) + "</th>"
				output += "</thead><tbody>"
				for row in data:
					output += "<tr>"
					# li = [row['t.location'], row['h.hashtag']]
					li = [row[0], row[1]]
					for txt in li:
						# output += "<td>" + str(txt).replace('\n', ' ').replace('\'', '\\\'').replace('\"', '\\\"').replace('\t',' ').replace('\r', ' ') + "</td>"
						output += "<td>" + txt + "</td>"
						# output += "<td>" + txt.replace('\n', ' ').replace('\'', '\\\'').replace('\"', '\\\"').replace('\t',' ').replace('\r', ' ') + "</td>"
					output += "</tr>"
				output += "</tbody></table>"

			elif index=='8':
				g.run(query8 % string)
				output = 'Successfully Done.'

		elif index=='0':
			output = ''
		
		else:
			if index=='3':
				data = g.data(query3)

				output = "<table class='table table-hover'><thead>"
				header = ['Hashtag 1', 'Hashtag 2', 'Frequency']
				for h in header:
					output += "<th>" + str(h) + "</th>"
				output += "</thead><tbody>"
				for row in data:
					output += "<tr>"
					# li = [row['h1.hashtag'], row['h2.hashtag'], row['c']]
					li = [row[0], row[1], str(row[2])]
					for txt in li:
						# output += "<td>" + str(txt).replace('\n', ' ').replace('\'', '\\\'').replace('\"', '\\\"').replace('\t',' ').replace('\r', ' ') + "</td>"
						output += "<td>" + txt + "</td>"
						# output += "<td>" + txt.replace('\n', ' ').replace('\'', '\\\'').replace('\"', '\\\"').replace('\t',' ').replace('\r', ' ') + "</td>"
					output += "</tr>"
				output += "</tbody></table>"

			elif index=='6':
				data = g.data(query6)

				output = "<table class='table table-hover'><thead>"
				header = ['Retweeter - User', 'Orginal Tweet Poster - User', 'Frequnecy']
				for h in header:
					output += "<th>" + str(h) + "</th>"
				output += "</thead><tbody>"
				for row in data:
					output += "<tr>"
					# li = [row['u1.author_screen_name'], row['u2.author_screen_name'], row['c']]
					li = [row[0], row[1], str(row[2])]
					for txt in li:
						# output += "<td>" + str(txt).replace('\n', ' ').replace('\'', '\\\'').replace('\"', '\\\"').replace('\t',' ').replace('\r', ' ') + "</td>"
						output += "<td>" + txt + "</td>"
						# output += "<td>" + txt.replace('\n', ' ').replace('\'', '\\\'').replace('\"', '\\\"').replace('\t',' ').replace('\r', ' ') + "</td>"
					output += "</tr>"
				output += "</tbody></table>"

			elif index=='7':
				data = g.data(query7)

				output = "<table class='table table-hover'><thead>"
				header = ['Replier - User', 'Orginal Tweet Poster - User', 'Frequnecy']
				for h in header:
					output += "<th>" + str(h) + "</th>"
				output += "</thead><tbody>"
				for row in data:
					output += "<tr>"
					# li = [row['u1.author_screen_name'], row['u2.author_screen_name'], row['c']]
					li = [row[0], row[1], str(row[2])]
					for txt in li:
						# output += "<td>" + str(txt).replace('\n', ' ').replace('\'', '\\\'').replace('\"', '\\\"').replace('\t',' ').replace('\r', ' ') + "</td>"
						output += "<td>" + txt + "</td>"
						# output += "<td>" + txt.replace('\n', ' ').replace('\'', '\\\'').replace('\"', '\\\"').replace('\t',' ').replace('\r', ' ') + "</td>"
					output += "</tr>"
				output += "</tbody></table>"

			else:
				output = 'Enter the name.'

		return render_template('index.html', out=output)

if __name__ == '__main__':
	app.run(debug=True, host='127.0.0.1')
