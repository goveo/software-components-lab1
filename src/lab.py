import urllib.request
import re

with urllib.request.urlopen("http://www.example.com") as url:
	s = url.read()
print(s)