from getGeoInfo import getGeoInfo
from dbConnection import conn
import pytz
from pytz import timezone
import dateutil.parser as dparser

Agnes = conn.Agnes
eventslowercase = Agnes.eventslowercase
groupslowercase = Agnes.groupslowercase

def convertTimetoGMT(time, timezoneName):
	timezoneInstance = timezone(timezoneName)
	locTime = timezoneInstance.localize(time)
	GMTTimeZoneInstance = timezone("GMT")
	gmtTime = locTime.astimezone(GMTTimeZoneInstance)
	return gmtTime

def getLowercase(field):
	if isinstance(field, str):
		newField = field.lower()
	elif isinstance(field, unicode):
		newField = field.encode('ascii', 'ignore').lower()
	elif isinstance(field, list):
		newField = []
		for item in field:
			item = getLowercase(item)
			newField.append(item)
	elif isinstance(field, dict):
		newField = {}
		for key, value in field.iteritems():
			newField[key.lower()] = getLowercase(value)
	else:
		newField = field
	return newField

def insertEventData(db, event, cityCoordinateDict, localityDict, timezoneName):
	latitude, longitude, distance = getGeoInfo(event["location"], event["community"], cityCoordinateDict, localityDict)
	# event["latitude"] = latitude
	# event["longitude"] = longitude
	if latitude != "" and longitude != "":
		event["geo"] = str(latitude) + "," + str(longitude)
	else:
		event["geo"] = ""
	event["maxdistance"] = distance
	event["other"]["currentDistance"] = ""
	event["attended"] = []
	event["attendedCount"] = 0
	event["thumbnail"] = ""

	event["starttime"] = convertTimetoGMT(event["starttime"], timezoneName)
	event["endtime"] = convertTimetoGMT(event["endtime"], timezoneName)
	event["createdate"] = convertTimetoGMT(event["createdate"], timezoneName)
	
	event["freqmatchedcr"] = 0
	event["freqmatchedcb"] = 0
	event["freqmatched"] = 0

	event["evtnamelowercase"] = getLowercase(event["evtname"])
	event["evtdesclowercase"] = getLowercase(event["evtdesc"])
	event["keywordslowercase"] = getLowercase(event["keywords"])
	event["otherlowercase"] = getLowercase(event["other"])

	if "groupten" not in event["community"]:
		event["community"].append("groupten")

	print event
	raw_input("pause")
	inserted_id = db.insert(event)
	insertEventForKazem(event, inserted_id)
	return True

def insertFilter(urlFilter, ele):
	urlFilter.insert(ele)

def checkEleFitlerExist(urlFilter, ele):
	isExist = False
	for flag in urlFilter.find(ele):
		isExist = True
	return isExist

def insertGroupData(db, group):
	group["thumbnail"] = ""

	group["grpnamelowercase"] = getLowercase(group["grpname"])
	group["grpdesclowercase"] = getLowercase(group["grpdesc"])
	group["keywordslowercase"] = getLowercase(group["keywords"])
	group["otherlowercase"] = getLowercase(group["other"])

	inserted_id = db.insert(group)
	insertGroupForKazem(group, inserted_id)
	return True

def insertEventForKazem(event, inserted_id):
	try:
		event["events_id"] = inserted_id
		event["evtname"] = event["evtname"].lower()
		event["url"] = event["url"].lower()
		event["location"] = event["location"].lower()
		event["evtdesc"] = event["evtdesc"].lower()
		tagList = []
		for tag in event["other"]["tags"]:
			tagList.append(tag.lower())
		event["other"]["tags"] = tagList
		eventslowercase.insert(event)
	except Exception as e:
		print e
		eventslowercase.insert(event)

def insertGroupForKazem(group, inserted_id):
	try:
		group["groups_id"] = inserted_id
		group["grpname"] = group["grpname"].lower()
		group["grpaddress"] = group["grpaddress"].lower()
		group["grpdesc"] = group["grpdesc"].lower()
		tagList = []
		for tag in group["other"]["tags"]:
			tagList.append(tag.lower())
		group["other"]["tags"] = tagList
		groupslowercase.insert(group)
	except Exception as e:
		print e
		groupslowercase.insert(group)
