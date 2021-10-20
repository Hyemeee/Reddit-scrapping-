import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}


def extract_posts(html,subreddit):
  votes=html.find("div",{"class":"_1rZYMD_4xY3gRcSS3p8ODO"})
  if votes:
    votes=votes.string
    if "k" in votes:
      votes=votes.replace("k","")
      votes=float(votes)*1000
  title=html.find("h3",{"class":"_eYtD2XCVieq6emjKBH3m"})
  if title:
    title=title.string
  link=html.find("a",{"class":"SQnoC3ObvgnGjWt90zD9Z _2INHSNB8V5eaWp4P0rY_mE"})
  if link:
    link=link["href"]
  if votes and title and link:
    return {'title':title,'votes':int(votes),'link':link,'subreddit':subreddit}
  else:
    return None
      


def extract_subreddit(subreddit):
  all_post=[]
  try:
    url = f"https://www.reddit.com/r/{subreddit}/top/?t=month"
    result=requests.get(url, headers=headers)
    soup=BeautifulSoup(result.text,"html.parser")
    container=soup.find("div",{"class":"rpBJOHq2PR60pnwJlUyP0"})
    if container:
      posts= container.find_all("div",{"class":None},recursive=False)
      for post in posts:
        extracted= extract_posts(post,subreddit)
        if extracted:
          all_post.append(extracted)
  except Exception:
    pass
  return all_post


      
def aggregate_subreddits(subreddits):
  aggregated=[]
  for subreddit in subreddits:
    posts=extract_subreddit(subreddit)
    aggregated= aggregated+posts
  return aggregated



#recursive가 True이면 findAll 함수는 매개변수에 일치하는 태그를 찾아 자식, 자식의 자식을 검색합니다. false이면 문서의 최상위 태그만 찾습니다. 기본적으로 findAll은 재귀적으로(recursive가 True) 동작합니다. 