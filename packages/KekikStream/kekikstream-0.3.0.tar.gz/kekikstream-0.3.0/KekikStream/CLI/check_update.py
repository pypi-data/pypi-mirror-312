# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from .             import konsol
from rich.panel    import Panel
from pkg_resources import get_distribution
from requests      import get
from subprocess    import check_call
import sys

def check_and_update_package(package_name: str):
    """Paketi kontrol et ve gerekirse güncelle."""
    try:
        # Mevcut sürümü al
        current_version = get_distribution(package_name).version
        konsol.print(Panel(f"[cyan]Yüklü sürüm:[/cyan] [bold yellow]{current_version}[/bold yellow]"))

        # PyPI'den en son sürümü al
        response = get(f"https://pypi.org/pypi/{package_name}/json")
        if response.status_code == 200:
            latest_version = response.json()["info"]["version"]
            konsol.print(Panel(f"[cyan]En son sürüm:[/cyan] [bold green]{latest_version}[/bold green]"))

            # Eğer güncel değilse güncelle
            if current_version != latest_version:
                konsol.print(f"[bold red]{package_name} güncelleniyor...[/bold red]")
                check_call([sys.executable, "-m", "pip", "install", "--upgrade", package_name, "--break-system-packages"])
                konsol.print(f"[bold green]{package_name} güncellendi![/bold green]")
            else:
                konsol.print(f"[bold green]{package_name} zaten güncel.[/bold green]")
        else:
            konsol.print("[bold red]PyPI'ye erişilemiyor. Güncelleme kontrolü atlanıyor.[/bold red]")
    except Exception as e:
        konsol.print(f"[bold red]Güncelleme kontrolü sırasında hata oluştu: {e}[/bold red]")