#compare the previous top posts to the current ones.

import os, time
from stat import *
from datetime import datetime, timedelta
import math
global math
import sys

#file to save changes in position of top posts, and time in which change occurred
postVelocity = open('postVelocity.txt', 'a')

#MAKE RUN FREQUENTLY WITHOUT FILLING ALLTOPPOSTS WITH REPEATED ENTRIES

def main():
	#if there is no top posts file, tell the user, 
    try:
        #get metadata about topPosts.txt
        prevPosts = 'latestTopPosts.txt'
        prevPostsInfo = os.stat(prevPosts)

        #time when top posts were last checked
        then =prevPostsInfo[ST_MTIME]

        #the time is now:
        now = time.time()
        #check for differences between old and current top posts
        postDiff(then, now, prevPosts)		
    except IOError:
        print('No top posts file exists.  Try running redReader.py first.')
        return

def postDiff(then, now, prevPosts):
    #how old is the current topPosts?
    lastTime = timeDiff(then, now)
    elapsedTime = now - then
    #how many of the top 25 posts have changed since then?
    numPostChanges = 0
	#how have the rankings of the posts changed?
    rankChanges = []

    #read in old data
    oldList = []
    for line in open(prevPosts):
        oldList.append(line)
    oldList = oldList[::3]

    #generate and read in new data
    os.system('redReader.py')
    newList = []
    for line in open('latestTopPosts.txt'):
        newList.append(line)
    newList = newList[::3]

    #count how many differences between old and new posts
    for post in newList:
	    #posts that fell out of top 25
        if post not in oldList:
	        numPostChanges += 1
        #difference in rank in posts still in (positive means they moved up)
        else:
            prevRank = oldList.index(post)
            newRank = newList.index(post)
            change = prevRank - newRank
            rankChanges.append(change)

    #write data on how much rankings changed in given time
    velocity = (rankChanges, elapsedTime)
    postVelocity.write(str(velocity)+'\n')

    if numPostChanges != 1:
        print('\n' + 'There have been', numPostChanges, 'changes in the top 25 posts in the past', lastTime)
    else:
        print('\n' + 'There has been', numPostChanges, 'change in the top 25 posts in the past', lastTime)

#organize the time into days, hours, minutes, and seconds
def timeDiff(earlier, later):
    diff = later - earlier

    #calculate units and remainders
    days = math.floor(diff/(60*60*24))
    diff -= days*(60*60*24)

    hours = math.floor(diff/(60*60))
    diff -= hours*(60*60)

    minutes = math.floor(diff/(60))
    diff -= minutes*(60)

    seconds = int(diff)

    timeList = [(days,'days'), (hours,'hours'), (minutes,'minutes'), (seconds,'seconds')]
    
    #get rid of zero values
    timeList = [x for x in timeList if x[0] != 0]
	
	#Create a string to return
	#MAKE TIME UNIT SINGULAR IF # OF UNITS = 1
    timeString = ''
    for t in timeList:
        timeString += (str(t[0]) + ' ' + t[1] + ' ')
    return timeString

#get the show started
if __name__ == '__main__':
    main()

