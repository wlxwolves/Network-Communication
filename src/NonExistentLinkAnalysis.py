# Author: 	Dexin Qi
# Email: 	qdxzzz@gmail.com
import FailureVerifier
import LinkMap
import LinkMapOld
from Utils import Utils



def nonExistentLinkAnalysis():
	''' Do something to analysis the non-existent links.  '''
	test = Utils()
	test.ReadFormatedPingDataIntoMemory()
	linkmap = LinkMap.LinkMap("../data/maps/links_new_format.txt")
	linkmapold = LinkMapOld.LinkMap("../data/maps/links_new_format.txt")

	#dataFile = open("NonExistentLinks_NotLast.txt",'w')
	logFile = open("LogQDX.txt",'w')
	p = FailureVerifier.PingFailureVerifier()
	count = set()
	countDest = set()
	countLink = set()
	countLinkNotLast = set()
	routeCount = set()
	for i in p.getNonExistentLinks():
		route = i[4]
		link = i[5][0]
		countDest.add(i[2])
		time = (float(i[0])+float(i[1]))/2
		linkroute1 = test.LookUp(link[0],'',time)
		linkroute2 = test.LookUp(link[1],'',time)
		if link[0] == '137.164.46.7' and link[1] == '137.164.35.47':
			print "Found!!!:"
			print linkroute1,linkroute2
		if linkroute1+":"+linkroute2 not in routeCount:
			logFile.write(linkroute1+"\t"+linkroute2+"\n")
			s1 = linkroute1.split(',')
			s2 = linkroute2.split(',')
			linkInfo = linkmapold.getValidTime(s1[0],s1[1],s2[0],s2[1])
			logFile.write(str(linkInfo)+"\n\n")
			routeCount.add(linkroute1+":"+linkroute2)
		countLink.add(link)
		for j in range(len(link)):
			if route[-(j+1)] != link[-(j+1)]:
				count.add(i[2])
				countLinkNotLast.add(link)
				#dataFile.write(str(i)+"\n")
				print route[-(j+1)] ,link,link[-(j+1)]
				#print route,link
				break
	print "All Data"
	print len(countDest)
	print countDest
	print "Not last hop data"
	print len(count)
	print count
	print "Links"
	print len(countLink)
	print countLink
	print "Links not last"
	print len(countLinkNotLast)
	print countLinkNotLast
	#dataFile.close()
	logFile.close()

	print "=================================================="
	for i in countLink:
#TODO: 
#1.Write code here to get the router information of the ip of link i,
# use that to look up in the link map to see if the router mentioned above
# exists, how long did they last, is it possible that they are just missed?
		

		links = linkmap.getLinks2(i)
		for j in links.items():
			print j
		print "--------------------------------------------"
	
nonExistentLinkAnalysis()
