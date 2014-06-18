#################
# GIMME SHELTER #
#################
import feedparser
import argparse
import os.path
import hashlib
import smtplib
from termcolor import colored, cprint
from email.mime.text import MIMEText

# grab the craigslist feed
def getFeed(args):
	tmp = getHashes()
	old_links = tmp.split("\n")
	new_links = []
	new_ads = []
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
			
		# if cmd line mode
			i = hashlib.md5(item.link).hexdigest();
			if isNewAd(i,old_links):					
				text=colored('New Ad!','red',attrs=['blink'])
				out= "%s title: %s, url: %s" % (text,item.title,item.link)
				print out
				new_ads.append(i)

			else:
				cprint("Old Ad title: %s, url: %s" % (item.title,item.link),'grey')
			
			new_links.append(i)
		#if email mode
			try: 
				if args.email:
					sendMsg(new_ads,args.email)
			except Exception, e:
				print e
				continue

		writeHashes("\n".join(sorted(new_links)))
# setup args
def setupArgs():
	parser = argparse.ArgumentParser(description='Find some housing on Craigslist!');
	parser.add_argument('--search',dest='keywords',type=str,default='',help="Keywords you'd like to search for")
	parser.add_argument('--city',dest='city',type=str,default='nyc',help="City to search in, defaults to NYC. See CL for abbreviations")
	parser.add_argument('--neighborhood',dest='hood',type=str,default='',help="Limit search to neighborhood (not yet implemented)")
	parser.add_argument('--type',dest='type',type=str,default='sub',help="Type of listing to search for, defaults to sublet")
	parser.add_argument('--new',dest='max_amt',type=bool,default=True,help="Defaults to True")
	parser.add_argument('--max',dest='max_amt',type=int,help="Maximum amount you want to pay")
	parser.add_argument('--email',dest='email',type=str,default=False,help="Send as email (not yet implemented)")

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

def isNewAd(item,hashes):
	for h in hashes:
		if item == h:
			return False
	return True	

def intro():
	# font shimrod, via http://www.kammerl.de/ascii/AsciiSignature.php
	print "\n"
	cprint("+++++++++++++++++++++++++++++++++++++",'red')
	cprint(" ,-.  .  . ,--. ,    ,---. ,--. ,-. ",'blue')
	cprint("(   ` |  | |    |      |   |    |  )",'blue')
	cprint(" `-.  |--| |-   |      |   |-   |-< ",'blue')
	cprint(".   ) |  | |    |      |   |    |  \\",'blue')
	cprint(" `-'  '  ' `--' `--'   '   `--' '  '",'blue')
	cprint("+++++++++++++++++++++++++++++++++++++",'red')
	print "\n"

# not yet implemented
def sendMsg(body,to):
	myBody = MIMEText("\n".join(body))
	msg['Subject'] = 'New apartment ads'
	msg['From'] = 'apartmentfairy@yourcomputer.null'
	msg['To'] = to
	# envelope header.
	# python -m smtpd -n -c DebuggingServer localhost:1025
	s = smtplib.SMTP('localhost',1025)
	s.sendmail(msg['From'], to, myBody)
	s.quit();

def main():
	intro()
	args = setupArgs()
	return getFeed(args)

main()