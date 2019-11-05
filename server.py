from flask import Flask, escape, request
from elasticsearch import Elasticsearch
from datetime import datetime
from datetime import timedelta
es = Elasticsearch(host='localhost', port='9200')
app = Flask(__name__)
app_start_time = datetime.utcnow()


@app.route('/')
def hello() :
	elapsed_time = datetime.utcnow() - app_start_time

	doc = {
		'ip': request.args.get('ip'),
		'is_attacker': request.args.get('is_attacker'),
		# 'text': 'Elasticsearch: cool. bonsai cool.',
		'timestamp': app_start_time - timedelta(days=30) + elapsed_time * 600,
	}
	# print(request.args.get('ip'))
	res = es.index(index="log-attack-2", doc_type='log', body=doc)
	return request.args.get('ip')

app.run(port = '5000', host='localhost')
