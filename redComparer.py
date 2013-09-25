#compare the previous top posts and their ranks to the current ones.

import os, time
from stat import *
from datetime import datetime, timedelta
import math
global math
import sys

#file to save changes in position of top posts, and time in which change occurred
postVelocity = open('postVelocity.txt', 'a')
postChanges = open('postChanges.txt', 'a')


#MAKE RUN FREQUENTLY WITHOUT FILLING ALLTOPPOSTS WITH REPEATED ENTRIES; for now just delete repeats

def main():
	#if there is no top posts file, tell the user, 
    try:
        #get metadata about topPosts.txt
        prevPosts = 'latestTopPosts.txt'
        prevPostsInfo = os.stat(prevPosts)

        #time when top posts were last checked
        then =prevPostsInfo[ST_MTIME]

        #the time is now seconds since epoch
        now = time.time()
        #check for differences between old and current top posts
        postDiff(then, now, prevPosts)		
    except IOError:
        print('No top posts file exists.  Try running redReader.py first.')
        return

def postDiff(then, now, prevPosts):
    #how old is the current topPosts in seconds?
    elapsedTime = now - then
    #get a readable time format
    lastTime = timeDiff(elapsedTime)

    #how many of the top 25 posts have changed since then?
    numPostChanges = 0

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

    if numPostChanges != 1:
        print('\n' + 'There have been', numPostChanges, 'changes in the top 25 posts in the past', lastTime)
        postChanges.write('There have been '+str(numPostChanges)+' changes in the top 25 posts in the past '+str(lastTime)+'\n')
    else:
        print('\n' + 'There has been', str(numPostChanges), 'change in the top 25 posts in the past', lastTime)
        postChanges.write('There has been '+str(numPostChanges)+' change in the top 25 posts in the past '+str(lastTime)+'\n')
    postVel(oldList, newList, elapsedTime)


#prints array of changes in rank, time since last update to postVelocity.txt
def postVel(oldList, newList, elapsedTime):
    #get the time of day
    time = datetime.now()
    timeTup = time.timetuple()
    currHour = timeTup[3]
    #keep track of how posts ranks have changed
    rankChanges = []
   
    #find the changes in post ranks
    for post in newList:
        #of the posts still in the top 25
        if post in oldList:
            prevRank = oldList.index(post)
            newRank = newList.index(post)
            change = prevRank - newRank
            rankChanges.append(change)
        else:
            rankChanges.append('new')
			
    #write data on how much rankings changed in given time
    velocity = (rankChanges, elapsedTime, currHour)
    postVelocity.write(str(velocity)+'\n')
        
#organize the time into days, hours, minutes, and seconds
def timeDiff(elapsedTime):
    diff = elapsedTime

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

