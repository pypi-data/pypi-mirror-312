# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from .CLI      import konsol, cikis_yap, hata_yakala
from .Managers import PluginManager, ExtractorManager, UIManager, MediaManager
from .Core     import PluginBase, ExtractorBase, SeriesInfo
from asyncio   import run

class KekikStream:
    def __init__(self):
        self.plugin_manager            = PluginManager()
        self.extractor_manager         = ExtractorManager()
        self.ui_manager                = UIManager()
        self.media_manager             = MediaManager()
        self.current_plugin:PluginBase = None

    async def run(self):
        self.ui_manager.clear_console()
        konsol.rule("[bold cyan]KekikStream Başlatılıyor[/bold cyan]")
        if not self.plugin_manager.get_plugin_names():
            konsol.print("[bold red]Hiçbir eklenti bulunamadı![/bold red]")
            return

        try:
            await self.select_plugin()
        finally:
            await self.plugin_manager.close_plugins()

    async def handle_no_results(self):
        action = await self.ui_manager.select_from_list(
            message = "Ne yapmak istersiniz?",
            choices = ["Geri Git", "Ana Menü", "Çıkış"]
        )

        match action:
            case "Geri Git":
                await self.search_all()
            case "Ana Menü":
                await self.run()
            case "Çıkış":
                cikis_yap(False)

    async def select_plugin(self):
        plugin_name = await self.ui_manager.select_from_fuzzy(
            message = "Arama yapılacak eklentiyi seçin:",
            choices = ["Tüm Eklentilerde Ara", *self.plugin_manager.get_plugin_names()]
        )

        if plugin_name == "Tüm Eklentilerde Ara":
            await self.search_all()
        else:
            self.current_plugin = self.plugin_manager.select_plugin(plugin_name)
            await self.search_single_plugin()

    async def search_single_plugin(self):
        self.ui_manager.clear_console()
        konsol.rule(f"[bold cyan]{self.current_plugin.name} Eklentisinde Arama Yapın[/bold cyan]")

        query   = await self.ui_manager.prompt_text("Arama sorgusu girin:")
        results = await self.current_plugin.search(query)

        if not results:
            konsol.print("[bold red]Arama sonucu bulunamadı![/bold red]")
            return await self.handle_no_results()

        selected_result = await self.select_result(results)

        if selected_result:
            await self.show_details({"plugin": self.current_plugin.name, "url": selected_result})

    async def search_all(self):
        self.ui_manager.clear_console()
        konsol.rule("[bold cyan]Tüm Eklentilerde Arama Yapın[/bold cyan]")

        query   = await self.ui_manager.prompt_text("Arama sorgusu girin:")
        results = await self.search_all_plugins(query)

        if not results:
            return await self.handle_no_results()

        selected_result = await self.select_from_all_results(results)

        if selected_result:
            await self.show_details(selected_result)

    async def select_result(self, results):
        selected_url = await self.ui_manager.select_from_fuzzy(
            message = "İçerik sonuçlarından birini seçin:",
            choices = [{"name": res.title, "value": res.url} for res in results]
        )

        if selected_url:
            return selected_url

    async def show_details(self, selected_result):
        try:
            if isinstance(selected_result, dict) and "plugin" in selected_result:
                plugin_name = selected_result["plugin"]
                url         = selected_result["url"]

                self.current_plugin = self.plugin_manager.select_plugin(plugin_name)
            else:
                url = selected_result

            media_info = await self.current_plugin.load_item(url)
        except Exception as hata:
            konsol.log(selected_result)
            hata_yakala(hata)
            return

        self.media_manager.set_title(f"{self.current_plugin.name} | {media_info.title}")

        self.ui_manager.display_media_info(f"{self.current_plugin.name} | {media_info.title}", media_info)

        if isinstance(media_info, SeriesInfo):
            selected_episode = await self.ui_manager.select_from_fuzzy(
                message = "İzlemek istediğiniz bölümü seçin:",
                choices = [
                    {"name": f"{episode.season}. Sezon {episode.episode}. Bölüm - {episode.title}", "value": episode.url}
                        for episode in media_info.episodes
                ]
            )
            if selected_episode:
                links = await self.current_plugin.load_links(selected_episode)
                await self.show_options(links)
        else:
            links = await self.current_plugin.load_links(media_info.url)
            await self.show_options(links)

    async def show_options(self, links):
        if not links:
            konsol.print("[bold red]Hiçbir bağlantı bulunamadı![/bold red]")
            return await self.handle_no_results()

        mapping = self.extractor_manager.map_links_to_extractors(links)
        has_play_method = hasattr(self.current_plugin, "play") and callable(getattr(self.current_plugin, "play", None))    
        # ! DEBUG
        # konsol.print(links)
        if not mapping and not has_play_method:
            konsol.print("[bold red]Hiçbir Extractor bulunamadı![/bold red]")
            konsol.print(links)
            return await self.handle_no_results()

        if not mapping:
            selected_link = await self.ui_manager.select_from_list(
                message = "Doğrudan oynatmak için bir bağlantı seçin:",
                choices = [{"name": self.current_plugin.name, "value": link} for link in links]
            )
            if selected_link:
                await self.play_media(selected_link)
            return

        action  = await self.ui_manager.select_from_list(
            message = "Ne yapmak istersiniz?",
            choices = ["İzle", "Geri Git", "Ana Menü"]
        )

        match action:
            case "İzle":
                selected_link = await self.ui_manager.select_from_list(
                    message = "İzlemek için bir bağlantı seçin:", 
                    choices = [{"name": extractor_name, "value": link} for link, extractor_name in mapping.items()]
                )
                if selected_link:
                    await self.play_media(selected_link)

            case "Geri Git":
                await self.search_all()

            case _:
                await self.run()

    async def play_media(self, selected_link):
        if hasattr(self.current_plugin, "play") and callable(self.current_plugin.play):
            konsol.log(f"[yellow][»] Oynatılıyor : {selected_link}")
            await self.current_plugin.play(
                name      = self.current_plugin._data[selected_link]["name"],
                url       = selected_link,
                referer   = self.current_plugin._data[selected_link]["referer"],
                subtitles = self.current_plugin._data[selected_link]["subtitles"]
            )
            return

        extractor: ExtractorBase = self.extractor_manager.find_extractor(selected_link)
        if not extractor:
            konsol.print("[bold red]Uygun Extractor bulunamadı.[/bold red]")
            return

        try:
            extract_data = await extractor.extract(selected_link, referer=self.current_plugin.main_url)
        except Exception as hata:
            konsol.print(f"[bold red]{extractor.name} » hata oluştu: {hata}[/bold red]")
            await self.handle_no_results()
            return

        if isinstance(extract_data, list):
            selected_data = await self.ui_manager.select_from_list(
                message = "Birden fazla bağlantı bulundu, lütfen birini seçin:",
                choices = [{"name": data.name, "value": data} for data in extract_data]
            )
        else:
            selected_data = extract_data

        if selected_data.headers.get("Cookie"):
            self.media_manager.set_headers({"Cookie": selected_data.headers.get("Cookie")})

        self.media_manager.set_title(f"{self.media_manager.get_title()} | {selected_data.name}")
        self.media_manager.set_headers({"Referer": selected_data.referer})
        konsol.log(f"[yellow][»] Oynatılıyor : {selected_data.url}")
        self.media_manager.play_media(selected_data)

    async def search_all_plugins(self, query: str):
        all_results = []

        for plugin_name, plugin in self.plugin_manager.plugins.items():
            if not isinstance(plugin, PluginBase):
                konsol.print(f"[yellow][!] {plugin_name} geçerli bir PluginBase değil, atlanıyor...[/yellow]")
                continue

            konsol.log(f"[yellow][~] {plugin_name:<19} aranıyor...[/]")
            try:
                results = await plugin.search(query)
                if results:
                    all_results.extend(
                        [{"plugin": plugin_name, "title": result.title, "url": result.url, "poster": result.poster} for result in results]
                    )
            except Exception as hata:
                konsol.print(f"[bold red]{plugin_name} » hata oluştu: {hata}[/bold red]")

        if not all_results:
            konsol.print("[bold red]Hiçbir sonuç bulunamadı![/bold red]")
            await self.handle_no_results()
            return []

        return all_results

    async def select_from_all_results(self, results):
        choices = [
            {"name": f"{f'[{res["plugin"]}]':<21} » {res['title']}", "value": res}
                for res in results
        ]

        return await self.ui_manager.select_from_fuzzy(
            message = "Arama sonuçlarından bir içerik seçin:",
            choices = choices
        )

from .CLI import pypi_kontrol_guncelle

def basla():
    try:
        konsol.print("[bold cyan]Güncelleme kontrol ediliyor...[/bold cyan]")
        pypi_kontrol_guncelle("KekikStream")

        app = KekikStream()
        run(app.run())
        cikis_yap(False)
    except KeyboardInterrupt:
        cikis_yap(True)
    except Exception as hata:
        hata_yakala(hata)