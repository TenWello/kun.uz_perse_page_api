from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
from news.models import News

class Command(BaseCommand):
    help = "Kun.uz yangiliklarini tortib keladi"

    def handle(self, *args, **kwargs):
        url = "https://kun.uz/news"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # main news (kategoriya yo'q, lekin qo'shib ketamiz, null bo'ladi)
        main_block = soup.find("div", class_="main-news")
        if main_block:
            main_link = main_block.find("a")
            main_title = main_block.find("div", class_="news-title")
            main_desc = main_block.find("div", class_="news-desc")
            main_img = main_block.find("img")
            if main_link and main_title:
                News.objects.update_or_create(
                    link="https://kun.uz" + main_link["href"],
                    defaults={
                        "title": main_title.text.strip(),
                        "description": main_desc.text.strip() if main_desc else "",
                        "image": main_img["src"] if main_img else "",
                        "type": "main",
                        "category": "",  # main uchun category bo'sh
                    }
                )

        # right side news latest
        latest_list = soup.find("div", class_="latest-news__list")
        if latest_list:
            for item in latest_list.find_all("a", class_="latest-news__item"):
                title = item.get_text(strip=True)
                link = "https://kun.uz" + item.get("href")

                # categoryni olish uchun: keyingi "div.gray-text > p"
                category = ""
                gray_div = item.find_next("div", class_="gray-text")
                if gray_div:
                    p = gray_div.find("p")
                    if p:
                        cat_text = p.get_text(strip=True)
                        # Masalan: "O‘zbekiston | 14:11"
                        if "|" in cat_text:
                            category = cat_text.split("|")[0].strip()
                        else:
                            category = cat_text.strip()

                News.objects.update_or_create(
                    link=link,
                    defaults={
                        "title": title,
                        "type": "latest",
                        "category": category,
                    }
                )
        self.stdout.write(self.style.SUCCESS("news uploaded"))
