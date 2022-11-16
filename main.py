from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
import bs4, json

url = "https://medium.com/_/graphql"


def make_request(url, headers=None, data=None):
  request = Request(url, headers=headers or {}, data=data)
  try:
    with urlopen(request, timeout=10) as response:
      charset = response.headers.get_content_charset()
      print(response.status)
      return response.read().decode(charset), response
  except HTTPError as error:
    print(error.status, error.reason)
  except URLError as error:
    print(error.reason)
  except TimeoutError:
    print("Request timed out")


def get_topics(soup):
  titles = soup.find_all("div", class_="meteredContent")
  for title in titles:
    article = title.find("a")
    print(article["href"])
    print(article.string)


headers = {
  "User-Agent":
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
}
with open("query.json", 'r') as query:
  queryObj = json.load(query)
  queryStr = json.dumps(queryObj)
  queryBytes = queryStr.encode("utf-8")
  data = queryBytes
body, response = make_request(url, headers, data)
print(body)
root = bs4.BeautifulSoup(body, "lxml")
get_topics(root)
