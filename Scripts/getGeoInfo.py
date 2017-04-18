import json
import urllib2
import re
from math import radians, cos, sin, asin, sqrt  
from haversine import haversine
import googlemaps

gmaps = googlemaps.Client(key='AIzaSyCnXTXPt3cXDjVmP-PLcA3dvhlIC9KPs_E')

def get_coordinate_and_disance(address, cityCoordinateDict, localityDict, community = []):
	addressUrl = address.replace(' ', '+')
	locality = "washington"
	if community != []:
		for item in community:
			if item.lower() in localityDict and item.lower() != "groupten" and item.lower() != "agnes":
				locality = localityDict[item]
				break

	if community != [] and community != ["agnes"] and locality == "" and "usgbc" not in community:
		print address
		print community
		raw_input("community error")
	components = {'locality':locality}
	comaQuantity = 0
	for char in address:
		if char == ",":
			comaQuantity += 1
	if comaQuantity == 1:
		coordinate = gmaps.geocode(address = address, components = components)
	else:
		coordinate = gmaps.geocode(address = address)
	if coordinate == []:
		latitude = ""
		longitude = ""
		distance = ""
	else:
		coordinate = coordinate[0] #choose the first reason
		latitude = coordinate["geometry"]["location"]["lat"]
		longitude = coordinate["geometry"]["location"]["lng"]
		if "bounds" in coordinate["geometry"]:
			northeast = coordinate["geometry"]["bounds"]["northeast"]
			southwest = coordinate["geometry"]["bounds"]["southwest"]
		elif "viewport" in coordinate["geometry"]:
			northeast = coordinate["geometry"]["viewport"]["northeast"]
			southwest = coordinate["geometry"]["viewport"]["southwest"]
		distance = haversine((northeast["lng"],northeast["lat"]), (southwest["lng"],southwest["lat"]), miles=True)
		if distance > 3:
			latitude = ""
			longitude = ""
			distance = ""

		if longitude != "" and latitude != "":
			cityLongitude = -77.0368707
			cityAltitude = 38.9071923
			if community != [] and "usgbc" not in community:
				for item in community:
					if item.lower() in cityCoordinateDict and item.lower() != "groupten" and item.lower() != "agnes":
						location = cityCoordinateDict[item]
						cityLongitude = float(location.split(",")[1])
						cityAltitude = float(location.split(",")[0])
						break

			if cityLongitude != "" and cityAltitude != "":
				cityEventDistance = haversine((longitude, latitude),(cityLongitude, cityAltitude), miles=True)
				if cityEventDistance > 25:
					latitude = ""
					longitude = ""
					distance = ""
				elif distance != "" and distance > 3:
					latitude = ""
					longitude = ""
					distance = ""
		
	return latitude, longitude, distance

def get_place(locationName, cityCoordinateDict, community):
	locationName = locationName.replace(" ", "+")
	query = locationName
	location = ""
	cityLongitude = -77.0368707
	cityAltitude = 38.9071923
	if community != [] and "usgbc" not in community:
		for item in community:
			if item.lower() in cityCoordinateDict and item.lower() != "agnes" and item.lower() != "groupten":
				location = cityCoordinateDict[item]
				cityLongitude = float(location.split(",")[1])
				cityAltitude = float(location.split(",")[0])
				break
	if community != [] and community != ["agnes"] and location == "" and "usgbc" not in community:
		print community
		raw_input("community error")

	radius = "50000"
	API_Key="AIzaSyCnXTXPt3cXDjVmP-PLcA3dvhlIC9KPs_E"
	if location != "":
		requrl = "https://maps.googleapis.com/maps/api/place/textsearch/json?query="+query+"&location="+location+"&radius="+radius+"&key="+API_Key
	else:
		requrl = "https://maps.googleapis.com/maps/api/place/textsearch/json?query="+query+"&key="+API_Key
	req = urllib2.Request(requrl)
	res_data = urllib2.urlopen(req)
	res = res_data.read()
	dic = json.loads(res)
	latitude = ""
	longitude = ""
	distance = ""
	if dic["status"] == "OK":
		address = dic["results"][0]["formatted_address"]
		geometry = dic["results"][0]["geometry"]
		latitude = geometry["location"]["lat"]
		longitude = geometry["location"]["lng"]
		if "bounds" in geometry:
			northeast = geometry["bounds"]["northeast"]
			southwest = geometry["bounds"]["southwest"]
			distance = haversine((northeast["lng"],northeast["lat"]), (southwest["lng"],southwest["lat"]), miles=True)
		elif "viewport" in geometry:
			northeast = geometry["viewport"]["northeast"]
			southwest = geometry["viewport"]["southwest"]
			distance = haversine((northeast["lng"],northeast["lat"]), (southwest["lng"],southwest["lat"]), miles=True)
		else:
			distance = ""

		# consider usgbc situation
		if "usgbc" not in community:
			cityEventDistance = haversine((longitude, latitude),(cityLongitude, cityAltitude), miles=True)
			print "distance: " + str(cityEventDistance)
			if cityEventDistance > 25:
				latitude = ""
				longitude = ""
				distance = ""
			elif distance != "" and distance > 3:
				latitude = ""
				longitude = ""
				distance = ""
	return latitude, longitude, distance

def getGeoInfo(location, community, cityCoordinateDict, localityDict):
	latitude, longitude, distance = get_coordinate_and_disance(location, cityCoordinateDict, localityDict, community)
	if latitude == "":
		print "No data from get_coordinate_and_disance"
		latitude, longitude, distance = get_place(location, cityCoordinateDict, community)
	return latitude, longitude, distance

def getGeoInfoWithRawOffset(location, community):
	latitude, longitude, distance = get_coordinate_and_disance(location, community)
	if latitude == "":
		latitude, longitude, distance = get_place(location, community)
	rawOffset = getTimeZone(latitude, longitude, community)['rawOffset']
	return latitude, longitude, distance, rawOffset
