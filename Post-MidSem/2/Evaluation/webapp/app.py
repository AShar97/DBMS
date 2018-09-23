from py2neo import Graph, Node, Relationship
g = Graph("bolt://localhost:7687", password="pass")

# Queries in the assignment
query3 = "MATCH (m1:User)<-[:MENTIONS]-(t:Tweet {location: '%s', ttype:'Tweet'})-[:MENTIONS]->(m2:User) WHERE m1.author_screen_name <= m2.author_screen_name RETURN DISTINCT t.location, m1.author_screen_name, m2.author_screen_name, collect(t.tid), count(*) as c ORDER BY c DESC LIMIT 3"
query9 = "MATCH (m:User {author_screen_name:'%s'})<-[:MENTIONS]-(t:Tweet {ttype:'Tweet'})-[:TAGS]->(h:Hashtag) RETURN DISTINCT m.author_screen_name, h.hashtag, collect(t.tid), count(*) as c ORDER BY c DESC LIMIT 3"

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
			if index=='3':
				data = g.data(query3 % string)

				output = "<table class='table table-hover'><thead>"
				header = ['Location', 'User-mention1', 'User-mention2', 'Tweet-ids where these usermentions co-occur', 'Co-occurrence count']
				for h in header:
					output += "<th>" + str(h) + "</th>"
				output += "</thead><tbody>"
				for row in data:
					output += "<tr>"
					li = [row[0], row[1], row[2], row[3], str(row[4])]
					for txt in li:
						output += "<td>" + str(txt).replace('\n', ' ').replace('\'', '\\\'').replace('\"', '\\\"').replace('\t',' ').replace('\r', ' ') + "</td>"
						# output += "<td>" + str(txt) + "</td>"
						# output += "<td>" + txt.replace('\n', ' ').replace('\'', '\\\'').replace('\"', '\\\"').replace('\t',' ').replace('\r', ' ') + "</td>"
					output += "</tr>"
				output += "</tbody></table>"

			elif index=='9':
				data = g.data(query9 % string)

				output = "<table class='table table-hover'><thead>"
				header = ['User-mention', 'hashtags', 'Tweet-ids where the user-mention and the hashtag co-occur', 'Co-occurrence count']
				for h in header:
					output += "<th>" + str(h) + "</th>"
				output += "</thead><tbody>"
				for row in data:
					output += "<tr>"
					li = [row[0], row[1], row[2], str(row[3])]
					for txt in li:
						output += "<td>" + str(txt).replace('\n', ' ').replace('\'', '\\\'').replace('\"', '\\\"').replace('\t',' ').replace('\r', ' ') + "</td>"
						# output += "<td>" + str(txt) + "</td>"
						# output += "<td>" + txt.replace('\n', ' ').replace('\'', '\\\'').replace('\"', '\\\"').replace('\t',' ').replace('\r', ' ') + "</td>"
					output += "</tr>"
				output += "</tbody></table>"

		elif index=='0':
			output = ''
		
		else:
			output = 'Enter the name.'

		return render_template('index.html', out=output)

if __name__ == '__main__':
	app.run(debug=True, host='127.0.0.1')
