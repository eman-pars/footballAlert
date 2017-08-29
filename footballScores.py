import urllib.request as ur
from bs4 import BeautifulSoup


URL = "http://www.espn.in/football/scoreboard/_/league/all/date/20170827"



# Do not use the system proxy
# Create custom proxyHandler with no proxies

proxy_handler = ur.ProxyHandler({})
opener = ur.build_opener(proxy_handler)
ur.install_opener(opener)





page = ur.urlopen(URL)

soup = BeautifulSoup(page)

print(soup.title)