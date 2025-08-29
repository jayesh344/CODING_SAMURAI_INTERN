import requests
from bs4 import BeautifulSoup
import pandas as pd
from rich.console import Console
from rich.table import Table
from rich.progress import track
from rich.panel import Panel

console = Console()
base_url = "https://quotes.toscrape.com/"
page = requests.get(base_url)

if page.ok:
    soup = BeautifulSoup(page.text, "html.parser")
    records = []
    blocks = soup.find_all("div", class_="quote")

    for block in track(blocks, description="🔎 Collecting data..."):
        quote_txt = block.find("span", class_="text").get_text(strip=True)
        writer = block.find("small", class_="author").get_text(strip=True)
        tags_list = [x.get_text(strip=True) for x in block.find_all("a", class_="tag")]
        tags_text = ", ".join(tags_list) if tags_list else "No Tags"

        link = block.find("a")["href"]
        full_link = base_url.rstrip("/") + link
        detail_req = requests.get(full_link)

        if detail_req.ok:
            detail_soup = BeautifulSoup(detail_req.text, "html.parser")
            birth_date = detail_soup.find("span", class_="author-born-date").get_text(strip=True)
            birth_place = detail_soup.find("span", class_="author-born-location").get_text(strip=True)
            bio = detail_soup.find("div", class_="author-description").get_text(strip=True)
        else:
            birth_date, birth_place, bio = "N/A", "N/A", "N/A"

        records.append([quote_txt, writer, tags_text, birth_date, birth_place, bio])

    df = pd.DataFrame(records, columns=["Quote", "Author", "Tags", "DOB", "Place", "About"])
    df.to_csv("quotes_with_authors.csv", index=False, encoding="utf-8")

    console.print(Panel.fit(
        "✅ [bold green]Scraping finished successfully![/bold green]\n"
        "📁 File saved: [yellow]quotes_with_authors.csv[/yellow]",
        style="bold blue"
    ))

    table = Table(title="🌟 Quotes & Authors", show_lines=True)
    table.add_column("ID", justify="center", style="cyan")
    table.add_column("Quote", style="magenta")
    table.add_column("Author", style="yellow")
    table.add_column("Tags", style="green")
    table.add_column("Born", style="cyan")
    table.add_column("Place", style="blue")

    for idx, row in df.iterrows():
        table.add_row(
            str(idx + 1),
            row["Quote"][:50] + "...",
            row["Author"],
            row["Tags"],
            row["DOB"],
            row["Place"]
        )

    console.print(table)

else:
    console.print(f"❌ [red]Failed to connect[/red] (status code: {page.status_code})")

