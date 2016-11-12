# This script is to create a table to store all ways' information (id; start & end (lat, lon))
# xml files needed: map.xml & output.xml

# sys argvs
ways_xml                    = './xml/output.xml' #sys.argv[1]
map_xml         			= './xml/map.xml' #sys.argv[2]
output_csv_xml          	= 'ways_lat_lon_dis.csv'#sys.argv[3]

import xmltodict
import csv 
import math

def node_info(node_id, node_list) :
	match = 0
	for node in node_list :
		if node_id == node['@id'] :
			match = 1
			return (node['@lat'], node['@lon'])
	if match == 0:
		return (0.0, 0.0)

def getDistance(srt_pnt, end_pnt):
        #radius of Earth
        R = 6378137 
        PI = math.pi
        srt_pnt_lat = float(srt_pnt[0]) * PI / 180.0 
        end_pnt_lat = float(end_pnt[0]) * PI / 180.0 

        lat_dif = srt_pnt_lat - end_pnt_lat;  
        lon_dif = (float(srt_pnt[1]) - float(end_pnt[1])) * PI / 180.0 

        sin_lat = math.sin(lat_dif / 2.0);  
        sin_lon = math.sin(lon_dif / 2.0);  

        distance = 2 * R  * math.asin(\
        					math.sqrt(sin_lat * sin_lat + math.cos(lat_dif) * math.cos(lon_dif) * (sin_lon**2))\
        							)
        return distance

# read ways
ways_doc = open(ways_xml,'r')
ways_org_doc = ways_doc.read()
ways_obj = xmltodict.parse(ways_org_doc)

ways = ways_obj['osm']['way']
len_of_ways = len(ways)

# read nodes
node_doc = open(map_xml,'r')
node_org_doc = node_doc.read()
node_obj = xmltodict.parse(node_org_doc)

nodes = node_obj['osm']['node']
len_of_nodes = len(nodes)

print 'number of ways:', len_of_ways, \
	' number of nodes:', len_of_nodes

# create a table 
csv_file = file (output_csv_xml,"w")
writer = csv.writer(csv_file, quoting = csv.QUOTE_ALL)
writer.writerow(['way_id', 'srt_pnt_lat', 'srt_pnt_lon', \
							'end_pnt_lat', 'end_pnt_lon', 'distance'])

for way in ways :
	nds = len(way['nd'])

	start_nd = way['nd'][0]['@ref']
	end_nd = way['nd'][nds - 1]['@ref']

	start_nd_info = node_info(start_nd, nodes)
	end_nd_info	= node_info(end_nd, nodes)

	total_distance = 0
	for counter in range(0, len(way['nd']) - 1) :
		start_nd = way['nd'][counter]['@ref']
		end_nd   = way['nd'][counter + 1]['@ref']
		total_distance += getDistance(node_info(start_nd, nodes),node_info(end_nd, nodes))

	writer.writerow([way['@id'], start_nd_info[0], start_nd_info[1],\
								end_nd_info[0], end_nd_info[1], \
								str(total_distance) ])

csv_file.close()

#print obj['osm']['way'][0]['nd'][0]['@ref']

