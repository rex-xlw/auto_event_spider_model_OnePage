import datetime
############################################################
#fetch server date info to construct the start url
currentTime = datetime.datetime.now()
#startTime = currentTime + datetime.timedelta(days=-3)
startTime = currentTime
startTimeStr = startTime.strftime('%Y-%m-%d')

endTime = currentTime + datetime.timedelta(weeks=8)
endTimeStr = endTime.strftime('%Y-%m-%d')

startTimeList = startTimeStr.split("-")
endTimeList = endTimeStr.split("-")

startYear = startTimeList[0]
startMonth = startTimeList[1]
startDate = startTimeList[2]

endYear = endTimeList[0]
endMonth = endTimeList[1]
endDate = endTimeList[2]
###############################################################


#input xpath
evtname = ''
evtdesc = ''
starttime = '' #only contain starttime
startdate = '' #only fill it with enddate
endtime = '' #only contain endtime
enddate = '' #only fill it with startdate
date = '' #only contain date without time
time = '' #contain the starttime and/or entime without date
tags = ''
dateAndTime = ''
location = ''

#timezone information: 'US/Alaska', 'US/Aleutian', 'US/Arizona', 'US/Central', 'US/East-Indiana', 'US/Eastern', 'US/Hawaii', 'US/Indiana-Starke', 'US/Michigan', 'US/Mountain', 'US/Pacific', 'US/Pacific-New', 'US/Samoa'
## "US/Eastern" #EST EDT
## "US/Central" #CST CDT
## "US/Mountain" #MST MDT
## "US/Pacific" #PST PDT
## "US/Alaska" #AKST AKMT
## "US/Hawaii" #HST HST
## "US/Arizona" #No dayling saving time there exception for Navajo Nation
timezoneName = 'US/Eastern'

#all the picurl should be included in the src tag
picurl = ''

#input url #format: "http(s)://xx.xxx.edu(com/net)/xxx/xxx/xxx" The domain name should be the same
mainUrlList = [
				'',
			]
				
#input a list of regular expression #format: "http(s)://xx.xxx.edu(com/net)/xxx""
#
urlREList = [
				'',
			]

#remove url partial pattern
subUrlList = []

#element modify list
evtnameModifiedList = []
evtdescModifiedList = []
locationModifiedList = []

#input specific location, can ignore
specificLocation = ""

#input a list of half regualr experssion
urlPrefixList = []

#input addtional tags for the crawlers
additionalTags = []

#input domain, can ignore
domain = ""

#input evtsource, can ignore
source = ""

#Preset parameter
filterElementList = [".jpg", ".css", ".png", ".js", ".ico", ".pdf", ".docx", ".jpeg"]