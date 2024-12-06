# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from KekikStream.Core import ExtractorBase, ExtractResult
import re

class TurboImgz(ExtractorBase):
    name     = "TurboImgz"
    main_url = "https://turbo.imgz.me"

    async def extract(self, url, referer=None) -> ExtractResult:
        if referer:
            self.oturum.headers.update({"Referer": referer})

        istek = await self.oturum.get(url)
        istek.raise_for_status()

        video_match = re.search(r'file: "(.*)",', istek.text)
        if not video_match:
            raise ValueError("File not found in response.")

        video_link = video_match.group(1)

        return ExtractResult(
            name      = self.name,
            url       = video_link,
            referer   = referer or self.main_url,
            subtitles = []
        )