import soundcloud
import sys
import json

CLIENT_ID = 'eb7c96d7bcda8e51a7ae96b186fe6109'

dataset = {}

def add_point(country):
    if country in dataset:
        dataset[country] = dataset[country] + 1
    else:
        dataset[country] = 1

def main():
    if sys.argv.__len__() != 2:
        print 'Usage: ./country_tag_heatmap_v1.py <tag>'
        exit()
    else:
        query = sys.argv[1]


    number_entries = 0
    total_attempts = 0

    client = soundcloud.Client(client_id=CLIENT_ID)

    tracks = client.get('/tracks', tags = query, limit=10)
    for track in tracks:
        print (track.title).encode('utf-8')
        comment_query = client.get('/tracks/'+str(track.id)+'/comments')
        for comment in comment_query:
            uid = client.get('/comments/'+str(comment.id)).user_id
            country = client.get('/users/'+str(uid)).country
            if country != None:
                add_point(country.encode('utf-8'))
                number_entries = number_entries + 1
            sys.stdout.write('\r' + str(total_attempts) + ' queries made.')
            sys.stdout.flush()
            total_attempts = total_attempts + 1
    print dataset
    print number_entries , ' actual data points.'
    print total_attempts , ' total queries.'
    print 'JSON VERSION:'
    print json.dumps(dataset)
    outfile = open(query+'.json', 'w')
    outfile.write(json.dumps(dataset, indent=1))
    outfile.close()

if __name__ == '__main__':main()



