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

        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # MAIN news block (left-hero)
        main_block = soup.find("div", class_="main-news__left-hero")
        if main_block:
            link_tag = main_block.find("a", href=True)
            title_tag = main_block.find("h3", class_="main-news__left-hero-title")
            desc_tag = main_block.find("p", class_="main-news__left-hero-text")
            img_tag = main_block.find("img", src=True)

            if link_tag:
                News.objects.update_or_create(
                    link="https://kun.uz" + link_tag["href"],
                    defaults={
                        "title": title_tag.get_text(strip=True) if title_tag else "",
                        "description": desc_tag.get_text(strip=True) if desc_tag else "",
                        "image": img_tag["src"] if img_tag else "",
                        "type": "main",
                        "category": "",  # category topilmadi
                    }
                )

        # LATEST news (right-side)
        sidebar = soup.find("div", class_="main-news__right")
        if sidebar:
            a_list = sidebar.find_all("a", href=True)
            for idx, a in enumerate(a_list):
                title = a.get_text(strip=True)
                link = "https://kun.uz" + a["href"]
                category = ""
                gray_divs = sidebar.find_all("div", class_="gray-text")
                if idx < len(gray_divs):
                    cat_text = gray_divs[idx].get_text(strip=True)
                    if "|" in cat_text:
                        category = cat_text.split("|")[0].strip()
                    else:
                        category = cat_text.strip()

                News.objects.update_or_create(
                    link=link,
                    defaults={
                        "title": title,
                        "description": "",
                        "image": "",
                        "type": "latest",
                        "category": category,
                    }
                )

        self.stdout.write(self.style.SUCCESS("news successfully uploaded"))
