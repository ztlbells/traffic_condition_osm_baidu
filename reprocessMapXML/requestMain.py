# This script is to request baidu direction service to obtain traffic_condition, distance & duration

import json
import urllib2
import httplib
import csv
import sys
import time

#developer key
ak 						= '&ak=tzWqf1kD8Gd6l6tGm9rOyoVs5Q4jXQoZ'

csv_file_path      		= './ways_lat_lon_dis.csv' #sys.argv[1]
output_csv 				= './output_' + str(time.localtime()) + '.csv'
start_time				= time.time()

#srt_pnt_lat			= str(31.030302)
#srt_pnt_lon			= str(121.4426264)
#end_pnt_lat			= str(31.0300714)
#end_pnt_lon			= str(121.4427271)

########### conversion part ###################
# lat&lon should be converted to baidu ver.
#http://api.map.baidu.com/geoconv/v1/?coords=121.4272715,31.0289643&from=1&to=5&ak=urkey

def attain_baidu_coords(lat, lon):
	url 	= 'http://api.map.baidu.com/geoconv/v1/?'
	coords 	= 'coords=' + lon + ',' + lat
	url 	= url + coords + '&from=1&to=5' + ak

	temp = urllib2.urlopen(url)
	hjson = json.loads(temp.read())
	return hjson['result']


########### request traffic condition part #######################
# request example 
# http://api.map.baidu.com/direction/v1?mode=driving&origin=39.921673,116.484644&destination=39.9231,
# 116.484669&origin_region=%E5%8C%97%E4%BA%AC&destination_region=%E5%8C%97%E4%BA%AC&ak=
# tzWqf1kD8Gd6l6tGm9rOyoVs5Q4jXQoZ

def request_baidu_dir(srt_pnt_lat, srt_pnt_lon, end_pnt_lat, end_pnt_lon, org_distance):
	url 				= 'http://api.map.baidu.com/direction/v1?'
	mode 				= 'mode=driving'


	srt_pnt = attain_baidu_coords(srt_pnt_lat, srt_pnt_lon)[0]
	end_pnt = attain_baidu_coords(end_pnt_lat, end_pnt_lon)[0]

	origin 				= '&origin=' 		+ str(srt_pnt['y']) + ',' + str(srt_pnt['x']) #+ srt_pnt_lat + ',' + srt_pnt_lon #
	destination 		= '&destination=' 	+ str(end_pnt['y']) + ',' + str(end_pnt['x']) #+ end_pnt_lat + ',' + end_pnt_lon #
	origin_region 		= '&origin_region=%%E5%%8C%%97%%E4%%BA%%AC' 
	destination_region	= '&destination_region=%%E5%%8C%%97%%E4%%BA%%AC'
	output				= '&output=json'
	coord_type			= '&coord_type=gcj02'
 


	url = url + mode + origin + destination + origin_region + destination_region + output + coord_type + ak
	print url
	temp = urllib2.urlopen(url)
	hjson = json.loads(temp.read())

	traffic_condition 	= hjson['result']['traffic_condition']
	steps 				= hjson['result']['routes'][0]['steps'][0]
	distance			= hjson['result']['routes'][0]['distance']
	duration			= hjson['result']['routes'][0]['duration']

	if len(steps) > 1:
		# if the number of 'content' > 1, we need the average value of duration / distance
		ratio			= float(duration) / float(distance)
		duration 		= float(org_distance) * ratio
		return (traffic_condition, org_distance, str(duration))
	else :
		#print 'cond', traffic_condition, 'dis', distance, 'dur', duration
		return (traffic_condition, distance, duration)

########### reading csv part ##################
ways_csv_file = file (csv_file_path,"r")
reader = csv.reader(ways_csv_file)

csv_file = file (output_csv,"w")
writer = csv.writer(csv_file, quoting = csv.QUOTE_ALL)
writer.writerow(['way_id', 'trfc_cdt', 'distance', 'duration'])
counter = 0
for line in reader :

    if line[0] != 'way_id':

    	#print line
    	result = request_baidu_dir(line[1], line[2], line[3], line[4], line[5])
    	writer.writerow([line[0], result[0], result[1], result[2]])
    	counter += 1
    	print counter, "running time:", time.time() - start_time

csv_file.close()

print "running time:", time.time() - start_time, "ways:", counter




