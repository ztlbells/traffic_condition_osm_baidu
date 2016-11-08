# This script is to create a table to store all ways' information (id; start & end (lat, lon))
# xml files needed: map.xml & output.xml

# sys argvs
ways_xml                    = './xml/output.xml' #sys.argv[1]
map_xml         			= './xml/map.xml' #sys.argv[2]
output_csv_xml          	= 'ways_lat_lon.csv'#sys.argv[3]

import xmltodict
import csv 

def node_info(node_id, node_list) :
	match = 0
	for node in node_list :
		if node_id == node['@id'] :
			match = 1
			return (node['@lat'], node['@lon'])
	if match == 0:
		return (0.0, 0.0)

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
							'end_pnt_lat', 'end_pnt_lat'])

for way in ways :
	nds = len(way['nd'])

	start_nd = way['nd'][0]['@ref']
	end_nd = way['nd'][nds - 1]['@ref']

	writer.writerow([way['@id'], node_info(start_nd, nodes)[0], node_info(start_nd, nodes)[1],\
								node_info(end_nd, nodes)[0], node_info(end_nd, nodes)[1] ])

csv_file.close()

#print obj['osm']['way'][0]['nd'][0]['@ref']

