import urllib2
from lxml import etree
import socket
import time
from random import randrange
import random

def process_url_to_file(noindex, urlcdiscount):
	urlcdiscount=urlcdiscount.rstrip();
	urlse="https://www.google.fr/search?hl=fr&safe=off&num=100&q="+urlcdiscount
	print(urlse)
	user_agent_list = ['Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0', 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36']
	user_agent = random.choice(user_agent_list)
	print("User agent choisi : "+user_agent)
	headers = { 'User-Agent' : user_agent }
	request = urllib2.Request(urlse,None,headers)
	proxy_support = urllib2.ProxyHandler({"http":"http://localhost:3128"})
	opener = urllib2.build_opener(proxy_support)
	urllib2.install_opener(opener)
	data = urllib2.urlopen(request).read()
	tree = etree.HTML(data)
	urlgg = tree.xpath('//div[@id="ires"]//a/@href')
	# getting all the elements in the list that contain cdiscount
	matching = [s for s in urlgg if "cdiscount" in s]
	print 'We found '+str(len(matching)) + 'URLs in SERP containing Cdiscount'
	matching = [s for s in urlgg if "cdiscount" in s]
	print 'We found '+str(len(matching)) + 'URLs in SERP containing Cdiscount'
	if urlcdiscount in matching:
		print 'URL in index'
		noindex.write(urlcdiscount+"\n")
	else:
		print 'URL not in index'

def main():
	fichierurl = open("/home/sduprey/My_Data/My_Indexation_Checker_Data/urllist.txt", "r")
	urllist = fichierurl.readlines()
	noindex = open("/home/sduprey/My_Data/My_Indexation_Checker_Data/noindex.txt", "w")
	for urlcdiscount in urllist:
		try:
			process_url_to_file(noindex, urlcdiscount)
			randomtimer = randrange(5, 30)
			print("Mise en pause : "+str(randomtimer)+" secondes...")
			time.sleep(randomtimer)
		except socket.timeout, e:
			print("socket timeout")
		except urllib2.HTTPError:
			time.sleep(3600)
			process_url_to_file(noindex, urlcdiscount)
		except KeyboardInterrupt:
			print("W: interrupt received, proceeding…")
			fichierurl.close()
			noindex.close()
	
	fichierurl.close()
	noindex.close()

if __name__ == "__main__":
	main()
