from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster

cluster = Cluster(['127.0.0.1'], port=9042)
session = cluster.connect()

session.set_keyspace('twitter')

from cassandra.encoder import Encoder
encoder_object = Encoder()
# parsedstring = encoder_object.cql_encode_str((string).encode('utf-8'))

from datetime import datetime, timedelta
# (datetime.strptime(string, "%Y-%m-%d").date() - timedelta(7)).isoformat()

# Queries in the assignment
query1 = "select * from table1 where author_screen_name=%s;"
query2 = "select * from table2 where keyword_processed=%s;"
query3 = "select * from table3 where hashtag=%s;"
query4 = "select * from table4 where mention=%s;"
query5 = "select * from table5 where date=%s;"
query6 = "select * from table6 where location=%s;"
query7 = "select * from table7 where date>=%s and date<=%s ALLOW FILTERING;"
query8 = "delete from table5 where date=%s;"


from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
	if(request.method=='GET'):
		return render_template('index.html')
	else:
		index = request.form["index"]
		string = encoder_object.cql_encode_str((request.form["name"]).encode('utf-8'))
		
		if (string and string!='NULL' and string!='""' and string!="''" and index!='clear'):
			if index=='1':
				data = session.execute(query1 % string)

				output = "<table class='table table-hover'><thead>"
				header = ['datetime', 'location', 'tid', 'tweet_text', 'author_screen_name', 'author_id', 'lang']
				for jj in header:
					output += "<th>" + str(jj) + "</th>"
				output += "</thead><tbody>"
				for row in data:
					output += "<tr>"
					li = [row.datetime.isoformat(), row.location, row.tid, row.tweet_text, row.author_screen_name, row.author_id, row.lang]
					for bla in li:
						# output += "<td>" + str(bla).replace('\n', ' ').replace('\'', '\\\'').replace('\"', '\\\"').replace('\t',' ').replace('\r', ' ') + "</td>"
						# output += "<td>" + bla + "</td>"
						output += "<td>" + bla.replace('\n', ' ').replace('\'', '\\\'').replace('\"', '\\\"').replace('\t',' ').replace('\r', ' ') + "</td>"
					output += "</tr>"
				output += "</tbody></table>"

			elif index=='2':
				data = session.execute(query2 % string)

				output = "<table class='table table-hover'><thead>"
				header = ['like_count', 'tweet_text', 'keyword_processed']
				for jj in header:
					output += "<th>" + str(jj) + "</th>"
				output += "</thead><tbody>"
				for row in data:
					output += "<tr>"
					li = [str(row.like_count), row.tweet_text, row.keyword_processed]
					for bla in li:
						# output += "<td>" + str(bla).replace('\n', ' ').replace('\'', '\\\'').replace('\"', '\\\"').replace('\t',' ').replace('\r', ' ') + "</td>"
						# output += "<td>" + bla + "</td>"
						output += "<td>" + bla.replace('\n', ' ').replace('\'', '\\\'').replace('\"', '\\\"').replace('\t',' ').replace('\r', ' ') + "</td>"
					output += "</tr>"
				output += "</tbody></table>"

			elif index=='3':
				data = session.execute(query3 % string)

				output = "<table class='table table-hover'><thead>"
				header = ['hashtag', 'datetime', 'tweet_text']
				for jj in header:
					output += "<th>" + str(jj) + "</th>"
				output += "</thead><tbody>"
				for row in data:
					output += "<tr>"
					li = [row.hashtag, row.datetime.isoformat(), row.tweet_text]
					for bla in li:
						# output += "<td>" + str(bla).replace('\n', ' ').replace('\'', '\\\'').replace('\"', '\\\"').replace('\t',' ').replace('\r', ' ') + "</td>"
						# output += "<td>" + bla + "</td>"
						output += "<td>" + bla.replace('\n', ' ').replace('\'', '\\\'').replace('\"', '\\\"').replace('\t',' ').replace('\r', ' ') + "</td>"
					output += "</tr>"
				output += "</tbody></table>"

			elif index=='4':
				data = session.execute(query4 % string)

				output = "<table class='table table-hover'><thead>"
				header = ['datetime', 'tweet_text', 'mention']
				for jj in header:
					output += "<th>" + str(jj) + "</th>"
				output += "</thead><tbody>"
				for row in data:
					output += "<tr>"
					li = [row.datetime.isoformat(), row.tweet_text, row.mention]
					for bla in li:
						# output += "<td>" + str(bla).replace('\n', ' ').replace('\'', '\\\'').replace('\"', '\\\"').replace('\t',' ').replace('\r', ' ') + "</td>"
						# output += "<td>" + bla + "</td>"
						output += "<td>" + bla.replace('\n', ' ').replace('\'', '\\\'').replace('\"', '\\\"').replace('\t',' ').replace('\r', ' ') + "</td>"
					output += "</tr>"
				output += "</tbody></table>"

			elif index=='5':
				data = session.execute(query5 % string)

				output = "<table class='table table-hover'><thead>"
				header = ['date', 'like_count', 'tweet_text']
				for jj in header:
					output += "<th>" + str(jj) + "</th>"
				output += "</thead><tbody>"
				for row in data:
					output += "<tr>"
					li = [str(row.date), str(row.like_count), row.tweet_text]
					for bla in li:
						# output += "<td>" + str(bla).replace('\n', ' ').replace('\'', '\\\'').replace('\"', '\\\"').replace('\t',' ').replace('\r', ' ') + "</td>"
						# output += "<td>" + bla + "</td>"
						output += "<td>" + bla.replace('\n', ' ').replace('\'', '\\\'').replace('\"', '\\\"').replace('\t',' ').replace('\r', ' ') + "</td>"
					output += "</tr>"
				output += "</tbody></table>"

			elif index=='6':
				data = session.execute(query6 % string)

				output = "<table class='table table-hover'><thead>"
				header = ['location', 'tweet_text']
				for jj in header:
					output += "<th>" + str(jj) + "</th>"
				output += "</thead><tbody>"
				for row in data:
					output += "<tr>"
					li = [row.location, row.tweet_text]
					for bla in li:
						# output += "<td>" + str(bla).replace('\n', ' ').replace('\'', '\\\'').replace('\"', '\\\"').replace('\t',' ').replace('\r', ' ') + "</td>"
						# output += "<td>" + bla + "</td>"
						output += "<td>" + bla.replace('\n', ' ').replace('\'', '\\\'').replace('\"', '\\\"').replace('\t',' ').replace('\r', ' ') + "</td>"
					output += "</tr>"
				output += "</tbody></table>"

			elif index=='7':
				string_l7 = encoder_object.cql_encode_str(((datetime.strptime(string, "'%Y-%m-%d'").date() - timedelta(7)).isoformat()).encode('utf-8'))
				data = session.execute(query7 % (string_l7, string))

				dct = {}
				for row in data:
					if row.hashtag not in dct:
						dct[row.hashtag] = row.count
					else:
						dct[row.hashtag] += row.count

				lst = [[h, dct[h]] for h in dct]
				lst.sort(key=lambda x: x[1], reverse=True)

				if len(lst) <= 20:
					datalst = lst
				else:
					datalst = lst[:20]

				output = "<table class='table table-hover'><thead>"
				header = ['hashtag', 'count']
				for jj in header:
					output += "<th>" + str(jj) + "</th>"
				output += "</thead><tbody>"
				for row in datalst:
					output += "<tr>"
					li = [row[0], str(row[1])]
					for bla in li:
						# output += "<td>" + str(bla).replace('\n', ' ').replace('\'', '\\\'').replace('\"', '\\\"').replace('\t',' ').replace('\r', ' ') + "</td>"
						# output += "<td>" + bla + "</td>"
						output += "<td>" + bla.replace('\n', ' ').replace('\'', '\\\'').replace('\"', '\\\"').replace('\t',' ').replace('\r', ' ') + "</td>"
					output += "</tr>"
				output += "</tbody></table>"
			elif index=='8':
				session.execute(query8 % string)
				output = 'Successfully Done'

		elif index=='0':
			output = ''
		else:
			output = 'Enter the name.'

		return render_template('index.html', out=output)

if __name__ == '__main__':
	app.run(debug=True, host='127.0.0.1')
