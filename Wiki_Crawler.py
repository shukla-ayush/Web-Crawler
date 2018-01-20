# Implementing focused web crawler

# Importing the URL Library
import urllib.request, urllib.parse

# Importing BeautifulSoup
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import ssl
import time

c = ssl.create_default_context()
c.check_hostname = False
c.verify_mode = ssl.CERT_NONE


# to keep track of the links that has been visited
links_visited = list()


# to ensure no more than 1000 URL's are crawled
url_counter = 1000

# to open the file for writing
urlfile = open('Focused_crawling.txt', "a")


def web_crawler ():

   global url_counter, keyword

    # this list will store URL's present at the same depth
   current_list = list()

   # this url will store URL's present at the depth next to current depth
   next_list = list()
   final_list = list()

   seed = input("Enter URL: ")
   keyword = input("Enter keyword: ")

   current_list.append(seed)

   depth = 1
   print("URL at Depth 1: ")
   # checks whichever condition occurs first
   while url_counter > 0 and depth < 7 :
        if len(current_list) > 0:

             # to push out 1st element of the list
             url = current_list.pop(0)
             link_extract(url, next_list, keyword)

             # will show url and decreasing values of URL from 1000 to 1
             print(url, url_counter)
             url_counter = url_counter - 1

        elif len(current_list)==0:
            depth = depth + 1
            print("URL's at Depth:", depth)
            for links in next_list:
               current_list.append(next_list.pop(0))

   # to ensure no dupliacte entries are made into the text file
   for i in links_visited:
       if i not in final_list:
           final_list.append(i)

   urlfile.write("Seed link: ")
   for j in final_list:
       urlfile.write("-" + j + "\n")


# to extract the URL's using BeautifulSoup
def link_extract (url, next_list, keyword):

   global url_counter
    # to ensure politeness policy
   time.sleep(1)

   web_page = urllib.request.urlopen(url, context=c).read()
   soup_object = BeautifulSoup(web_page, 'html.parser')
   tags = soup_object('a')
   links_visited.append(url)

   # call to process URL
   url_processing(tags, next_list, keyword)


# to process the URL's as per the given constraints
def url_processing (tags, next_list, keyword):

   for tag in tags:
      url_updated = tag.get('href')
      if url_updated is None :
         continue

      # empty url condition
      if len(url_updated) < 1 :
         continue

      # handling of administrative links
      pos_of_colon = url_updated.find(':');
      if pos_of_colon > 5:
         continue

      # handling of hyperlinks on same page
      pos_of_hash = url_updated.find('#')
      if pos_of_hash >1 :
         url_updated = url_updated[:pos_of_hash]

      # non textual media ignored

      if url_updated.endswith('.mp3') or url_updated.endswith('.jpg') or url_updated.endswith('.png') or url_updated.endswith('.pdf'):
          continue

      # handling of relative URL's
      if url_updated.startswith('/'):
        url_updated = urljoin("https://en.wikipedia.org/wiki", url_updated)

      # prefix condition
      if not url_updated.startswith("https://en.wikipedia.org/wiki"):
          continue

      # Removing Main Page of Wikipedia
      if url_updated == "https://en.wikipedia.org/wiki/Main_Page":
          continue

      # Removing random article
      if "/wiki/Special:Random" in url_updated:
          continue

      if not (url_updated.startswith("https://en.wikipedia.org/wiki/" + keyword[0].upper() + keyword[1:]) or "_" + keyword in url_updated or " " + keyword in tag.get_text()):
          continue

      # duplicate URL's in next_list
      if url_updated in next_list:
           continue

      # duplicate links in already parsed list
      if url_updated in links_visited:
          continue

      # call storelinks to append URL's in file and ist
      storelinks (next_list, url_updated)

def storelinks (next_list, url_updated):

      next_list.append(url_updated)


# function call
web_crawler()
