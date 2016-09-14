'''
Created on 2016年9月9日

@author: zhengwei
'''

from actions.actionList import action
import datetime

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")[:10]
print("---")
print("---")
print(now + "[run]")
print("---")
print("---")
for actor in action:
    actor()
print("---")
print("---")
print(now + "[finish]")
print("---")
print("---")
