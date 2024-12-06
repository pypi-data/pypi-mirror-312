# ! Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from KekikStream.Core import ExtractorBase, ExtractResult, Subtitle
import json

class VideoSeyred(ExtractorBase):
    name     = "VideoSeyred"
    main_url = "https://videoseyred.in"

    async def extract(self, url, referer=None) -> ExtractResult:
        if referer:
            self.oturum.headers.update({"Referer": referer})

        video_id = url.split("embed/")[1].split("?")[0]
        video_url = f"{self.main_url}/playlist/{video_id}.json"

        response = await self.oturum.get(video_url)
        response.raise_for_status()

        try:
            response_list = json.loads(response.text)
            if not response_list:
                raise ValueError("Empty response from VideoSeyred.")
            response_data = response_list[0]
        except (json.JSONDecodeError, IndexError) as e:
            raise RuntimeError(f"Failed to parse response: {e}")

        subtitles = []
        for track in response_data.get("tracks", []):
            if track.get("kind") == "captions" and track.get("label"):
                subtitles.append(
                    Subtitle(
                        name = track["label"],
                        url  = self.fix_url(track["file"])
                    )
                )

        video_links = []
        for source in response_data.get("sources", []):
            video_links.append(
                ExtractResult(
                    name      = self.name,
                    url       = self.fix_url(source["file"]),
                    referer   = self.main_url,
                    subtitles = subtitles
                )
            )

        if not video_links:
            raise ValueError("No video links found in the response.")

        # En yüksek kaliteli videoyu döndür (varsayılan olarak ilk video)
        return video_links[0] if len(video_links) == 1 else video_links