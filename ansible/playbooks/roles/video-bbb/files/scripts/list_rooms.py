#! /usr/bin/python3
 
from slugify import slugify
import json
import os
import re
import sys
import wget
import xml.etree.ElementTree as ET 



penta_url = 'https://fosdem.org/2021/schedule/xml'        
print("Checking if we have the schedule...")
if os.path.isfile(os.path.basename(penta_url)):
  penta = os.path.basename(penta_url)
else:
  print("Getting the schedule...")
  penta = wget.download(penta_url)

print("Parsing the schedule file...")
pentaparse = ET.parse(penta).getroot()
'''Match only devrooms, keynotes, lightning talks, main tracks'''
pattern='^[D,K,L,M]'
fullrooms=sorted(list(set([r.get('name') for r in pentaparse.findall('.//room') if r.get('name') and re.match(pattern,r.get('name')) ])))

rooms=sorted(list(set([slugify(r.get('name'),separator='') for r in pentaparse.findall('.//room') if r.get('name') and re.match(pattern,r.get('name')) ])))

output=''

print('Creating ansible host entries')
for r in rooms:
    output += r+'-vocto.video.fosdem.org\n'

f = open('/tmp/ansible_hosts_voctos', 'w')
f.write(output)
f.close()

output=''
print('Creating ansible group_vars/video.yml')
for r in rooms:
    output += '- ' + r + '\n'

f = open('/tmp/video.yml', 'w')
f.write(output)
f.close()

output=''
print('Creating live.fosdem.org mappings')
for r in fullrooms:
    output += "\t\t'"+ slugify(r,separator='') + "' => '" + r +"',\n"

f = open('/tmp/config.php', 'w')
f.write(output)
f.close()


