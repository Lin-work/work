import feedparser
import pandas as pd
import urllib.parse
from datetime import datetime
from googletrans import Translator

translator = Translator()

keywords = ["climate change", "ESG", "sustainability", "SBTi", "IFRS", "TCFD", "碳定價", "永續", "氣候變遷"]
base_url = "https://news.google.com/rss/search?q="

all_articles = []

for keyword in keywords:
    encoded_keywords = urllib.parse.quote_plus(keyword)
    feed = feedparser.parse(base_url + encoded_keywords)
    for entry in feed.entries:
        try:
            published_time = datetime(*entry.published_parsed[:6])
        except:
            published_time = None
        all_articles.append({
            "keyword" : keyword,
            "Title": entry.title,
            "Source": entry.source.title if 'source' in entry else "Google News",
            "Link": entry.link,
            "Publish Time": published_time,

        })

df_en = pd.DataFrame(all_articles)
df_en = df_en.sort_values(by="Publish Time", ascending=False)
df_top5 = df_en.groupby("keyword").head(5).reset_index(drop=True)

translated_title = []
for idx, row in df_top5.iterrows():
    try:
        title_zh = translator.translate(row['Title'], src='en', dest='zh-tw').text
    except:
        title_zh = ""
    translated_title.append(title_zh)

df_zh = pd.DataFrame({
            "關鍵字" : df_top5["keyword"],
            "標題": translated_title,
            "Source": df_top5["Source"],
            "Link": df_top5["Link"],
            "Publish Time":  df_top5["Publish Time"],
        })


with pd.ExcelWriter("20250630.xlsx", engine='openpyxl') as writer:
    df_top5.to_excel(writer, sheet_name = '英文', index = False)
    df_zh.to_excel(writer, sheet_name = '中文', index = False)
