from datetime import datetime
from datetime import timedelta
from elasticsearch import Elasticsearch
import numpy as np
import pandas as pd

es = Elasticsearch(host='localhost', port='9200')

all_data = []
start = datetime(year=2019,month=10,day=3)
i = 0
while True:
    today = start + timedelta(days=i)
    res = es.search(index="log-attack-2", body={
  "query": {
    "match": {
      "timestamp": str(today.date())
    }
  }, 
    "aggs" : {
        "count_over_time" : {
            "date_histogram" : {
                "field" : "timestamp",
                "calendar_interval" : "1m"
            },
            "aggs" : {
              "by_type" : {
                "terms" : {
                  "field" : "is_attacker.keyword"
                }
              }
            }
            
        }
    },
    "size" : 0
})
    if res["hits"]["total"]["value"] == 0:
        break
    for e in res["aggregations"]["count_over_time"]["buckets"]:
        timestamp = e["key_as_string"]
        total = e["doc_count"]
        aggs = {u["key"] : u["doc_count"] for u in e["by_type"]["buckets"]}
        users = aggs["False"] if "False" in aggs else 0
        attackers = aggs["True"] if "True" in aggs else 0
        all_data.append([timestamp,users,attackers,total])
    i+=1

df = pd.DataFrame(data=np.array(all_data), columns=["timestamp", "users", "attackers", "total"])
df.to_csv(index=False,path_or_buf="./data.csv")