# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from KekikStream.Core import PluginBase, SearchResult, SeriesInfo, Episode
from Kekik.Sifreleme  import CryptoJS
from parsel           import Selector
import re, urllib.parse, base64

class DiziBox(PluginBase):
    name     = "DiziBox"
    main_url = "https://www.dizibox.plus"

    async def search(self, query: str) -> list[SearchResult]:
        self.oturum.cookies.update({
            "LockUser"      : "true",
            "isTrustedUser" : "true",
            "dbxu"          : "1722403730363"
        })
        istek  = await self.oturum.get(f"{self.main_url}/?s={query}")
        secici = Selector(istek.text)

        return [
            SearchResult(
                title  = item.css("h3 a::text").get(),
                url    = self.fix_url(item.css("h3 a::attr(href)").get()),
                poster = self.fix_url(item.css("img::attr(src)").get()),
            )
            for item in secici.css("article.detailed-article")
        ]

    async def load_item(self, url: str) -> SeriesInfo:
        istek  = await self.oturum.get(url)
        secici = Selector(istek.text)

        title       = secici.css("div.tv-overview h1 a::text").get()
        poster      = self.fix_url(secici.css("div.tv-overview figure img::attr(src)").get())
        description = secici.css("div.tv-story p::text").get()
        year        = secici.css("a[href*='/yil/']::text").re_first(r"(\d{4})")
        tags        = secici.css("a[href*='/tur/']::text").getall()
        rating      = secici.css("span.label-imdb b::text").re_first(r"[\d.,]+")
        actors      = [actor.css("::text").get() for actor in secici.css("a[href*='/oyuncu/']")]

        episodes = []
        for sezon_link in secici.css("div#seasons-list a::attr(href)").getall():
            sezon_url    = self.fix_url(sezon_link)
            sezon_istek  = await self.oturum.get(sezon_url)
            sezon_secici = Selector(sezon_istek.text)

            for bolum in sezon_secici.css("article.grid-box"):
                ep_title   = bolum.css("div.post-title a::text").get()
                ep_href    = self.fix_url(bolum.css("div.post-title a::attr(href)").get())
                ep_season  = bolum.css("div.post-title a::text").re_first(r"(\d+)\. ?Sezon")
                ep_episode = bolum.css("div.post-title a::text").re_first(r"(\d+)\. ?Bölüm")

                if ep_title and ep_href:
                    episodes.append(Episode(
                        season  = ep_season,
                        episode = ep_episode,
                        title   = ep_title.strip(),
                        url     = ep_href,
                    ))

        return SeriesInfo(
            url         = url,
            poster      = poster,
            title       = title,
            description = description,
            tags        = tags,
            rating      = rating,
            year        = year,
            episodes    = episodes,
            actors      = actors,
        )

    async def _iframe_decode(self, name:str, iframe_link:str, referer:str) -> list[str]:
        results = []

        if "/player/king/king.php" in iframe_link:
            print(name, iframe_link)
        elif "/player/moly/moly.php" in iframe_link:
            print(name, iframe_link)
        elif "/player/haydi.php" in iframe_link:
            okru_url = base64.b64decode(iframe_link.split("?v=")[-1]).decode("utf-8")
            results.append(okru_url)

        return results

    async def load_links(self, url: str) -> list[str]:
        istek  = await self.oturum.get(url)
        secici = Selector(istek.text)

        iframes = []
        main_iframe  = secici.css("div#video-area iframe::attr(src)").get()
        if main_iframe:
            if decoded := await self._iframe_decode(self.name, main_iframe, url):
                iframes.extend(decoded)

        for alternatif in secici.css("div.video-toolbar option[value]"):
            alt_name = alternatif.css("::text").get()
            alt_link = alternatif.css("::attr(value)").get()

            if not alt_link:
                continue

            self.oturum.headers.update({"Referer": url})
            alt_istek = await self.oturum.get(alt_link)
            alt_istek.raise_for_status()

            alt_secici = Selector(alt_istek.text)
            alt_iframe = alt_secici.css("div#video-area iframe::attr(src)").get()

            if alt_iframe:
                if decoded := await self._iframe_decode(alt_name, alt_iframe, url):
                    iframes.extend(decoded)

        return iframes