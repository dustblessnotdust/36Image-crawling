import requests
from bs4 import BeautifulSoup

with open("urls.txt", "a") as f:
    for i in range(1,100):
        url = f"https://desk.3gbizhi.com/search/0-0-2-0/ai%E7%BE%8E%E5%A5%B3/index_{i}.html"
        r = requests.get(url)
        if "找不到相关图片，您可以换一个关键词试试" in r.text:
            break
        soup = BeautifulSoup(r.text, "html.parser")
        a=soup.find_all("a",attrs={"class":"imgw"})
        for i in a:
            url=i.get("href")
            print(url)
            f.write(url+"\n")
