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
query4 = "select * from table4 where date=%s;"
query8 = "select * from table8 where date=%s;"

from bs4 import BeautifulSoup
import csv

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
			if index=='4':
				data = session.execute(query4 % string)

				output = "<table class='table table-hover'><thead>"
				header = ['Date', 'UserID', 'Number of times the userID has posted a tweet on that date']
				for jj in header:
					output += "<th>" + str(jj) + "</th>"
				output += "</thead><tbody>"

				i = 0
				for row in data:
					i += 1
					output += "<tr>"
					li = [str(row.date), row.author_id, str(row.count)]
					for bla in li:
						# output += "<td>" + str(bla).replace('\n', ' ').replace('\'', '\\\'').replace('\"', '\\\"').replace('\t',' ').replace('\r', ' ') + "</td>"
						# output += "<td>" + bla + "</td>"
						output += "<td>" + bla.replace('\n', ' ').replace('\'', '\\\'').replace('\"', '\\\"').replace('\t',' ').replace('\r', ' ') + "</td>"
					output += "</tr>"
				output += "</tbody></table>"

				output += "The total number of such rows obtained is <b>%d</b>." % i

				# soup = BeautifulSoup(output)
				# table = soup.select_one("table.table-hover")
				# headers = [th.text.encode("utf-8") for th in table.select("tr th")]

				# with open("4.csv", "w") as f:
				# 	wr = csv.writer(f)
				# 	wr.writerow(headers)
				# 	wr.writerows([[td.text.encode("utf-8") for td in row.find_all("td")] for row in table.select("tr + tr")])

			elif index=='8':
				data = session.execute(query8 % (string))

				output = "<table class='table table-hover'><thead>"
				header = ['Date', 'hashtag', 'mention', 'Number of times the hashtag-mention pair is cooccurring on this date']
				for jj in header:
					output += "<th>" + str(jj) + "</th>"
				output += "</thead><tbody>"

				i = 0
				for row in data:
					i += 1
					output += "<tr>"
					li = [str(row.date), row.hashtag, row.mention, str(row.count)]
					for bla in li:
						# output += "<td>" + str(bla).replace('\n', ' ').replace('\'', '\\\'').replace('\"', '\\\"').replace('\t',' ').replace('\r', ' ') + "</td>"
						# output += "<td>" + bla + "</td>"
						output += "<td>" + bla.replace('\n', ' ').replace('\'', '\\\'').replace('\"', '\\\"').replace('\t',' ').replace('\r', ' ') + "</td>"
					output += "</tr>"
				output += "</tbody></table>"

				output += "The total number of such rows obtained is <b>%d</b>." % i

				# soup = BeautifulSoup(output)
				# table = soup.select_one("table.table-hover")
				# headers = [th.text.encode("utf-8") for th in table.select("tr th")]

				# with open("4.csv", "w") as f:
				# 	wr = csv.writer(f)
				# 	wr.writerow(headers)
				# 	wr.writerows([[td.text.encode("utf-8") for td in row.find_all("td")] for row in table.select("tr + tr")])

		elif index=='0':
			output = ''
		else:
			output = 'Enter the name.'

		return render_template('index.html', out=output)

if __name__ == '__main__':
	app.run(debug=True, host='127.0.0.1')
