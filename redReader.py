#get top 25 links and titles; overwrite latestTopPosts and append to allTopPosts
#this script is set to run daily with windows task scheduler


import urllib.request
from urllib.error import HTTPError,URLError
from bs4 import BeautifulSoup, SoupStrainer

#get info from /r/all
url = 'http://reddit.com/r/all'

#overwrite this file with new posts
latestTopPosts = open('latestTopPosts.txt', 'w')
#append new posts to this file
allTopPosts = open('allTopPosts.txt', 'a')



#opens up the web page using urllib
#if the page can't open due to an http error, print a message saying open failed
try:
    #use Firefox user agent so site won't treat script as bot
    request = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11' })
    page = urllib.request.urlopen(request)

    #create a soup of the page
    soup = BeautifulSoup(page)


    #find All of the post links and store them in posts
    posts = []
    for anchor in soup.find_all('a'):
        if 'class' in anchor.attrs and anchor['class'] == ['title', '']:
            posts.append(anchor)
    
    #overwrite titles and links in latestTopPosts, and append them to allTopPosts
    for post in posts:
        url = post['href']
        title = post.get_text()
        latestTopPosts.write(title+'\n'+url+'\n'+'\n')
        allTopPosts.write(title+'\n'+url+'\n'+'\n')

    print('Successfully got top posts!')

except HTTPError as e:   
    #if error occurs, say what type
   print('Page open failed. Error code is : ', e)
