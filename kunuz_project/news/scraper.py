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

        # main news
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
                        "type": "main"
                    }
                )

        # right side news latest
        latest_list = soup.find("div", class_="news-list")
        if latest_list:
            for item in latest_list.find_all("a", class_="news__title"):
                title = item.text.strip()
                link = "https://kun.uz" + item.get("href")
                News.objects.update_or_create(
                    link=link,
                    defaults={
                        "title": title,
                        "type": "latest"
                    }
                )
        self.stdout.write(self.style.SUCCESS("news uploaded"))
