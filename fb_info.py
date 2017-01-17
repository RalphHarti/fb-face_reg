# So far it only works if the last action was to post a new status update!!!!!
# Otherwise what comes after message in posts_person file is something else

import fbconsole
from fbconsole import graph_url
from urllib import urlretrieve
import re
import mmap
import json
import requests
import os
import shutil
import facebook


fbconsole.authenticate()

f = open('posts_person3.json', 'w+r+b')
a = open('all.txt','w+r+b')
json_file = open('json_info.txt', 'w')
t = open('.fb_access_token', 'r+b')  			# get the token retrieved by fbconcole.authenticate()
t.seek(18)
mt = mmap.mmap(t.fileno(), 0)
mt.seek(0) # reset file cursor
token_find = re.search('scope', mt)
token_end = token_find.end()
token_point = token_end - 27
#token = t.read(token_point)
token = ''
#print(token)

name = ''

newpath = 'data/' + name 
if not os.path.exists(newpath): os.makedirs(newpath)

#profile_pic = graph_url('/' + name + '/picture') #Request facebook profile pic
#filename = name + '.jpg'
#
#urlretrieve(profile_pic, filename)
#
#shutil.move('/Users/ralph/Desktop/' +filename, '/Users/ralph/Desktop/' + name )

last_activity = open('last_activity.txt' ,'w')
link = open('link.txt', 'w')

r = requests.get("https://graph.facebook.com/" + name + "/feed/" + '?access_token=' + token) 		# get the json file for the feed

raw = json.loads(r.text)
#json_file.write(r)
rawstr = str(raw)
a.write(rawstr)
try: 
 print(raw['data'][0]['story'])
 print(raw['data'][0]['from']['name'])
 print(raw['data'][0]['picture'])
 print(raw['data'][0]['link'])
 print('one')
 last_activity.write(raw['data'][0]['story'].encode('utf8')+'\n')
 last_activity.write(raw['data'][0]['from']['name'].encode('utf8')+'\n')
 last_activity.write(raw['data'][0]['picture'].encode('utf8')+'\n')
 last_activity.write(raw['data'][0]['description'].encode('utf8')+'\n')
 link.write(raw['data'][0]['link'].encode('utf8')+'\n')

except KeyError:
 try:
  print(raw['data'][0]['message'])
  print(raw['data'][0]['link'])
  print(raw['data'][0]['from']['name'])
  print('two')
  last_activity.write(raw['data'][0]['message'].encode('utf8')+'\n')
  last_activity.write(raw['data'][0]['link'].encode('utf8')+'\n')
  last_activity.write(raw['data'][0]['from']['name'].encode('utf8')+'\n')
  link.write(raw['data'][0]['link'].encode('utf8')+'\n')

 except KeyError:
  try:
   print(raw['data'][0]['message'])
   print(raw['data'][0]['from']['name'])
   last_activity.write(raw['data'][0]['message'].encode('utf8')+'\n')
   last_activity.write(raw['data'][0]['from']['name'].encode('utf8')+'\n')
   link.write(raw['data'][0]['link'].encode('utf8')+'\n')
   print('three')
  except KeyError:
      try:
           print(raw['data'][0]['picture'])
           print(raw['data'][0]['from']['name'])
           last_activity.write(raw['data'][0]['picture'].encode('utf8')+'\n')
           last_activity.write(raw['data'][0]['from']['name'].encode('utf8')+'\n')
           link.write(raw['data'][0]['link'].encode('utf8')+'\n')    
      except KeyError:
           print(raw['data'][0]['from']['name'])
           last_activity.write(raw['data'][0]['from']['name'].encode('utf8')+'\n')
         
        

#shutil.move('last_activity.txt', newpath )
#shutil.move('link.txt', newpath )

graph = facebook.GraphAPI(token) # Grants access

total = 0 # Count for number of posts
for post in fbconsole.iter_pages(graph.get_object('/callumkift/feed')): # Iterates over the feed and retrieves posts
    if ('message' in post): # Makes sure it is a post and not a 'like', comment etc.
        total += 1
        print total,':', post['updated_time'], '\n', post['message'], '\n' # Prints posts
        if total > 2: break # Limits to three, change 2-> 4 if you want the last 5 posts etc.

last_activity.close()
link.close()
f.close()
t.close()



