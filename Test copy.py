import requests
from bs4 import BeautifulSoup

link = "https://www.timeshighereducation.com/hub/sinorbis"

res = requests.get(link)
if res.status_code == 200:
    soup = BeautifulSoup(res, 'html.parser')

# get the text content of the webpage
text = soup.get_text()

print(text)