
import elasticsearch as es
import elasticsearch_dsl as dsl

def main():
    db =  {
        'es_hosts' : ["es_host"],
        'dbname' : 'logstash_index_name'
    }
    client = es.Elasticsearch(db['es_hosts'])
    s = dsl.Search(using=client, index=db['dbname'])

    print(s.to_dict())

    ids_join = {}
    i = 0
    for hit in s.scan():
        ids_join[hit.id_str] = hit.text
        i += 1
        print('Read: ' + str(i), end='\r')

    print('Total items read for join index: ' + str(i))

    db['dbname'] = 'search_api_index_name'
    s = dsl.Search(using=client, index=db['dbname'])

    ids_api = {}
    i = 0
    for hit in s.scan():
        ids_api[hit.id_str] = hit.text
        i += 1
        print('Read: ' + str(i), end='\r')

    print('Total items read for API index: ' + str(i))

    with open('missing_ids.txt', 'w') as f:
        for id_str in ids_join.keys():
            if id_str not in ids_api:
                f.write(id_str + '\n')


if __name__ == '__main__':
    main()
