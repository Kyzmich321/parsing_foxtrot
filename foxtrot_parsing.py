import bs4
import openpyxl
import requests
import time
from openpyxl.styles import Font, Alignment


def foxtrot(link_sales):
    data = ('Name Smartphone', 'Price Smartphone', 'Link Smartphone', 'Link Site') # Заголовки колонок
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.append(data)
    variable = 1
    n = 1
    while n < variable + 1:
        res = requests.get(link_sales + f'?page={n}')
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        name_smartphone = soup.select('.card__title')
        price_smartphone = soup.select('.card-price')
        link_smartphone = soup.select('.card__body>a')
        if variable == 1:
            number_pages = soup.select('ul li[data-page]')
            pages_list = [int(number_pages[i].getText()) for i in range(len(number_pages) - 1)] # Список номерів сторінок
            variable = max(pages_list)
        for i in range(len(name_smartphone)):
            all_data = (name_smartphone[i].getText(), price_smartphone[i].getText(),
                        f"https://www.foxtrot.com.ua/{link_smartphone[i].get('href')}", 'https://www.foxtrot.com.ua/')
            sheet.append(all_data)
        n += 1
    fontObj1 = Font(name='Times New Roman', bold=True)
    for column in sheet['A1:D1']:
        for cell in column:
            cell.font = fontObj1
            cell.alignment = Alignment(horizontal='center')
    sheet.column_dimensions['A'].width = 85
    sheet.column_dimensions['B'].width = 40
    sheet.column_dimensions['C'].width = 130
    sheet.column_dimensions['D'].width = 27
    sheet.freeze_panes = 'A2'
    wb.save('xlsx/Foxtrot.xlsx')
    print('Successfully completed')


foxtrot_link = 'https://www.foxtrot.com.ua/uk/shop/mobilnye_telefony_samsung_smartfon.html'
start = time.time()
foxtrot(foxtrot_link)
finish = time.time()
print(finish - start)
