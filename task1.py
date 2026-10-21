import csv
from urllib.parse import urljoin, urlparse
import time
import requests
from bs4 import BeautifulSoup

start_url = 'https://www.musashino-u.ac.jp'
base_domain = urlparse(start_url).netloc

urls_to_visit = [start_url]
visited_urls = set()
sitemap = {}

MAX_PAGES = 20  # 動作確認・テスト用に20ページ制限

while urls_to_visit and len(sitemap) < MAX_PAGES:
    current_url = urls_to_visit.pop(0)

    if current_url in visited_urls:
        continue

    # 必須指示：アクセス前に負荷軽減のスリープを挟む
    time.sleep(1)

    try:
        res = requests.get(current_url, timeout=5)
        visited_urls.add(current_url)

        if res.status_code != 200:
            continue

        soup = BeautifulSoup(res.text, 'html.parser')
        title_tag = soup.find('title')
        title_text = title_tag.string.strip() if title_tag and title_tag.string else "タイトルなし"
        sitemap[current_url] = title_text

        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            full_url = urljoin(current_url, href).split('#')[0]

            if urlparse(full_url).netloc == base_domain and full_url not in visited_urls:
                if full_url not in urls_to_visit:
                    urls_to_visit.append(full_url)

    except Exception as e:
        print(f"エラー ({current_url}): {e}")

# 1. 辞書型変数を表示
print("【取得した辞書型データ】")
print(sitemap)

# 2. 辞書をもとにCSVファイルへ保存
with open('sitemap.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(['URL', 'Title'])
    for url, title in sitemap.items():
        writer.writerow([url, title])

print("\nsitemap.csv に正常に保存されました！")