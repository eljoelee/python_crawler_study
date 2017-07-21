import json
from urllib.request import urlopen

response = urlopen("http://localhost:8000/dogs/?format=json").read().decode('utf-8')
resJson = json.loads(response)

for dog in resJson:
    # Dictionary
    print(dog['dogName']+'\n'+dog['dogInfo']+'\n')