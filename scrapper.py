import json

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from rich import box
from rich.console import Console
from rich.progress import track
from rich.table import Table

URL = 'https://tech.floripa.br/'

console = Console()


def fetch_html():
    console.print(f'🌐 Acessando [cyan]{URL}[/cyan]...', style='bold')
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL)
        page.wait_for_selector('#event-timeline', timeout=10000)
        html = page.content()
        browser.close()
    return html


def parse_events(html: str) -> list[dict]:
    soup = BeautifulSoup(html, 'html.parser')
    events = []

    for section in soup.select('div.event-date-section'):
        data_header = section.select_one('h3.event-date')
        data = data_header.text.strip() if data_header else ''

        # Adiciona barra de progresso para os eventos daquela seção
        for item in track(section.select('div.event-item'), description=f'Extraindo eventos em {data}'):
            horario = item.select_one('p.event-time strong')
            formato = item.select_one('p.event-time span.event-type')
            preco = item.select_one('p.event-time span.event-price')
            titulo = item.select_one('h4.event-title')
            local = item.select_one('p.event-location')
            descricao = item.select_one('p.event-description')
            tags = [tag.text.strip() for tag in item.select('div.event-tags span.tag-badge')]

            events.append({
                'data': data,
                'horario': horario.text.strip() if horario else '',
                'formato': formato.text.strip() if formato else '',
                'preco': preco.text.strip() if preco else '',
                'titulo': titulo.text.strip() if titulo else '',
                'local': local.text.strip() if local else '',
                'descricao': descricao.text.strip() if descricao else '',
                'tags': tags,
            })

    return events


def save_to_json(data, filename='events.json'):
    console.print(f'💾 Salvando em [green]{filename}[/green]...', style='bold')
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def show_summary(events_data):
    table = Table(title='📋 Eventos encontrados', box=box.ROUNDED, show_lines=True)
    table.add_column('Data', style='cyan', no_wrap=True)
    table.add_column('Horário', style='green')
    table.add_column('Formato', style='blue')
    table.add_column('Título', style='magenta')

    for evento in events_data:
        table.add_row(evento['data'], evento['horario'], evento['formato'], evento['titulo'])

    console.print(table)


def get_tech_floripa_events():
    html = fetch_html()
    events_data = parse_events(html)
    save_to_json(events_data)
    show_summary(events_data)


if __name__ == '__main__':
    get_tech_floripa_events()
