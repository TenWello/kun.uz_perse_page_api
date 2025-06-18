from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
from news.models import News

class Command(BaseCommand):
    help = "Kun.uz bosh sahifasidan yangiliklarni tortib keladi"

    def handle(self, *args, **kwargs):
        url = "https://kun.uz/"
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }

        # kunuzni upload qilish
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # Left side Main news (html class: main-news__left)
        main_block = soup.find("div", class_="main-news__left")
        if main_block:
            a = main_block.find("a", href=True)
            img = main_block.find("img", src=True)
            if a:
                News.objects.update_or_create(
                    link="https://kun.uz" + a["href"],
                    defaults={
                        "title":       a.get_text(strip=True),
                        "description": "",  # kun uz homepageda description yoq
                        "image":       img["src"] if img else "",
                        "type":        "main"
                    }
                )

        # Right side latest news (main-news__right ichidagi <a> kun.uz html class)
        sidebar = soup.find("div", class_="main-news__right")
        if sidebar:
            for a in sidebar.find_all("a", href=True):
                title = a.get_text(strip=True)
                link  = "https://kun.uz" + a["href"]
                News.objects.update_or_create(
                    link=link,
                    defaults={
                        "title":       title,
                        "description": "",
                        "image":       "",
                        "type":        "latest"
                    }
                )

        self.stdout.write(self.style.SUCCESS("news successfully uploaded"))
