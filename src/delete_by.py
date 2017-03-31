import argparse
import sys

import elasticsearch as es
import elasticsearch_dsl as dsl
from elasticsearch_dsl.query import Match

def main():

    args = parse_args()

    db =  {
        'es_hosts' : [args.es_host],
        'dbname' : args.index
    }
    client = es.Elasticsearch(db['es_hosts'])
    s = dsl.Search(using=client, index=db['dbname'])
    # don't get any fields in response, only get ids
    s = s.source([])

    # m = Match(origin={"query": args.origin, "operator": "and"})

    s = s.query('match', origin={'query': args.origin, 'operator': 'and'}) \
        .query('range', ** {'grimoire_creation_date': {'gt': args.date}})

    print(s.to_dict())

    #ids = [h.meta.id for h in s.scan()]
    i = 0
    for hit in s.scan():
        i += 1
        es.Elasticsearch(db['es_hosts']).delete(index=db['dbname'], doc_type='items', id=hit.meta.id)

    print("Deleted: ", str(i))


def parse_args():
    """Parse arguments from the command line"""

    parser = argparse.ArgumentParser(description='Fake delete by query')

    parser.add_argument('-e', '--elastic-search', dest='es_host', required=True,
                        help='ES host')
    parser.add_argument('-i', '--index', dest='index', required=True,
                        help='ES index')
    parser.add_argument('-o', '--origin', dest='origin',
                        required=True, help='origin value')
    parser.add_argument('-d', '--date', dest='date',
                        required=True, help='date')

    return parser.parse_args()

if __name__ == '__main__':
    main()
