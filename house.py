#################
# GIMME SHELTER #
#################
import feedparser
import argparse
import os.path
import hashlib
from termcolor import colored, cprint

# grab the craigslist feed
def getFeed(args):
	tmp = getHashes()
	old_links = tmp.split("\n")
	new_links = []
	#if hood.len > 1: 
	#	url = "https://%s.craigslist.org/search/%s/%s?query=%s&sale_date=&maxAsk=%i&format=rss" % (args.city, args.hood, args.type, args.keywords, args.max_amt)
	#else:
	url = "https://%s.craigslist.org/search/%s?query=%s&sale_date=&maxAsk=%i&format=rss" % (args.city, args.type, args.keywords, args.max_amt)
	last = getLastMod();
	feed = feedparser.parse(url,modified=last)
	if feed.status == 304:
		print "Nothing has changed!"
	else:
		cprint("Fetching new ads ...",'green')
		setLastMod(feed.modified)
		for item in feed.entries:
			#
			i = hashlib.md5(item.link).hexdigest();
			if doesMatch(i,old_links):
				text=colored('New Ad!','red',attrs=['blink'])
				print "%s date: %s title: %s, url: %s" % (text,item.date,item.title,item.link)
			else:
				cprint("Old Ad title: %s, url: %s" % (item.title,item.link),'grey')
			new_links.append(i)

		#print 'old links', old_links
		#print 'new links', new_links
		writeHashes("\n".join(sorted(new_links)))
# setup args
def setupArgs():
	parser = argparse.ArgumentParser(description='Find some housing on Craigslist!');
	parser.add_argument('--search',dest='keywords',type=str,default='',help="Keywords you'd like to search for")
	parser.add_argument('--city',dest='city',type=str,default='nyc',help="City to search in, defaults to NYC. See CL for abbreviations")
	parser.add_argument('--neighborhood',dest='hood',type=str,default='',help="Your neighborhood")
	parser.add_argument('--type',dest='type',type=str,default='sub',help="Type of listing to search for, defaults to sublet")
	parser.add_argument('--max',dest='max_amt',type=int,help="Maximum amount you want to pay")
	return parser.parse_args()


# fetch last modified
def getLastMod():
	#if file exists
	if os.path.isfile('last_mod'):
		f = open('last_mod','r')
		return f.read()
	else:
		return 0

# write last modified date out
def setLastMod(date):
	f = open('last_mod','w')
	f.write(date)

def getHashes():
	#if file exists
	if os.path.isfile('hashes'):
		f = open('hashes','r')
		return f.read()
	else:
		return '\n'

def writeHashes(data):
	f = open('hashes','w')
	f.write(data)

def doesMatch(item,hashes):
	for h in hashes:
		if item == h:
			return False
	return True	

def intro():
	print "\n"
	cprint("+++++++++++++++++++++++++++++++++++++",'red')
	cprint(" ,-.  .  . ,--. ,    ,---. ,--. ,-. ",'blue')
	cprint("(   ` |  | |    |      |   |    |  )",'blue')
	cprint(" `-.  |--| |-   |      |   |-   |-< ",'blue')
	cprint(".   ) |  | |    |      |   |    |  \\",'blue')
	cprint(" `-'  '  ' `--' `--'   '   `--' '  '",'blue')
	cprint("+++++++++++++++++++++++++++++++++++++",'red')
	print "\n"


def main():
	intro()
	args = setupArgs()
	return getFeed(args)

main()