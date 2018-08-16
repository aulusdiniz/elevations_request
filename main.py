import csv, json
import urllib2
# import time

str_locations = "locations="
api_token = "&key=[HERE YOU API TOKEN]"
batch =200
batch_req = 2
batch_size = 0
count = 0
input_name = 'data.csv'

with open(input_name) as csvfile:
    batch_size = len(csvfile.readlines()) % batch
    csvfile.close()

try:
    with open(input_name) as csvfile:
        reader = csv.DictReader(csvfile)
        # start batch operation
        batch_count = 1
        for row in reader:
            count = count + 1
            str_locations = str_locations + str(row['Latitude'])+","+str(row['Longitude'])+"|"
            if(count>(batch*batch_count)):
                url_request = "https://maps.googleapis.com/maps/api/elevation/json?" + str_locations[:-1] + api_token
                str_locations = "locations="
                # print url_request
                req = urllib2.Request(url_request)
                content = (urllib2.urlopen(req).read())
                batch_count = batch_count + 1
                print batch_count
                # time.sleep(1)

                with open('output.csv', 'a') as csvoutput:
                    writer = csv.DictWriter(csvoutput, fieldnames=["Latitude", "Longitude", "Elevation"])
                    for x in range(len((json.loads(content).get('results')))):
                        writer.writerow({
                            'Latitude': json.loads(content).get('results')[x].get('location').get('lat'),
                            'Longitude': json.loads(content).get('results')[x].get('location').get('lng'),
                            'Elevation': json.loads(content).get('results')[x].get('elevation')
                        })
                    csvoutput.close()
        csvfile.close()
except:
        print count
        cfile = open('count.txt', 'w')
        cfile.write(str(count))
        cfile.close()
