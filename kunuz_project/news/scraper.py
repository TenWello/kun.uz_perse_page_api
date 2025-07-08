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

        main_block = soup.find("div", class_="main-news__left-hero")
        if main_block:
            a_tag = main_block.find("a", href=True)
            title_tag = main_block.find("h3", class_="main-news__left-hero-title")
            img_tag = main_block.find("img", src=True)

            if a_tag and title_tag:
                link = "https://kun.uz" + a_tag["href"]
                title = title_tag.get_text(strip=True)
                image = img_tag["src"] if img_tag else ""

                News.objects.update_or_create(
                    link=link,
                    defaults={
                        "title": title,
                        "description": "",
                        "image": image,
                        "type": "main",
                        "category": "",
                    }
                )

        latest_list = soup.find("div", class_="latest-news__list")
        if latest_list:
            for item in latest_list.find_all("a", class_="latest-news__item"):
                title = item.get_text(strip=True)
                link = "https://kun.uz" + item.get("href")

                category = ""
                gray_div = item.find_next("div", class_="gray-text")
                if gray_div:
                    p = gray_div.find("p")
                    if p:
                        cat_text = p.get_text(strip=True)
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
