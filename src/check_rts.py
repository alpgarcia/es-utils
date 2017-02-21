
import elasticsearch as es
import elasticsearch_dsl as dsl

def main():

    db =  {
        'es_hosts' : ["es_host"],
        'dbname' : 'logstash_index_name'
    }
    client = es.Elasticsearch(db['es_hosts'])

    rts = 0
    ts = 0
    with open('missing_ids.txt', 'r') as f:
        for line in f:
            s = dsl.Search(using=client, index=db['dbname'])
            s = s.query('match', id_str=line)
            for hit in s.execute():
                if 'retweeted_status' in hit:
                    rts += 1
                else:
                    ts += 1

                print('TWEETS: ' + str(ts) + ' RTs: ' + str(rts), end='\r')

    print('TWEETS   : ', ts )
    print('RETWEETS : ', rts)

if __name__ == '__main__':
    main()
