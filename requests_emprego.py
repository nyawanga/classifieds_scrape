#from requests_html import HTMLSession
import requests as rq
from bs4 import BeautifulSoup as bs
import html5lib
from fake_useragent import UserAgent
import re


#ession = HTMLSession()

def clean(text):
    patt = re.compile(r'[^\t\r\n]*')
    clean = re.search(patt, text)
    return clean.group()

ua = UserAgent()
url = 'https://en.emprego.mmo.co.mz'

def main_page(url):
	inner_links = []
	res = rq.get(url, headers = {'user-agent': str(ua)})
	soup = bs(res.content, 'html5lib')
	#tree = soup.prettify()
	jobs_table = soup.find('ol', {'class': 'jobs'})
	#jobs_list = jobs_table.find_all('li')
	jobs_pages = jobs_table.find_all('a', href = True)
	#jobs_pages = [i.find_all('a', href = True) for i in jobs_table]
	for i in jobs_pages:
		link = i.get('href')
		inner_links.append(link)
		print(link)
	return set(inner_links)

inner_url = 'https://en.emprego.mmo.co.mz/jobs/programme-specialist/'
def parse_job(url):
	details = {}
	res = rq.get(inner_url, headers = {'user-agent': str(ua)})
	soup = bs(res.content, 'html5lib')
	attribs = ['jobcategory', 'location', 'title', 'jobtype', 'content']
	for attrib in attribs:
		try:
			if attrib == 'jobcategory':
				details[attrib] = soup.find('span', {'class': 'job-type'}).text.strip()
			elif attrib == 'jobtype':
				details[attrib] = soup.find('p', {'class':'meta'}).find('a').text.strip()
			elif attrib == 'title':
				details[attrib] = soup.find('h1', {'class': 'title'}).text.strip()
			elif attrib == 'location':
				details[attrib] = soup.find('span', {'class': 'location'}).text.strip()
			elif attrib == 'content':
				content_string = []
				for child in soup.find('div', {'class': 'section_content'}).children: #.get_text(strip = True)#.strip()
				    if child.name == 'center':
				        continue
				    elif child.name == 'div' and child.find('div', {'class':'wpa'}): #re.search(r'wpcnt', "".join(child.get('class'))):
				    	#print("Found it %s" % "".join(child.get('class')) )
				    	break
				    elif child.string == None:
				        #print(child.get_text("\n", strip = True)) 
				        content_string.append(child.get_text("\n", strip = True))
				    else:
				    	#print(child.string, "\n")
				    	content_string.append(child.string.strip())
				details[attrib] = "\n".join(content_string)

		except AttributeError as e:
			details[attrib] = 'Not Found'
			print('AttributeError on {0} \n'.format(attrib))
		except TypeError as e:
			details[attrib] = 'Not Found'
			#raise
			print('TypeError on {0} \n {1}'.format(attrib, e))
		except Exception as e:
			details[attrib] = 'Not Found'
			print('UncaughtError on {0} \n {1}'.format(attrib, e))

	return details


print(parse_job(inner_url)['content'])
#print(jobcategory.text)

#print(jobs_pages)


