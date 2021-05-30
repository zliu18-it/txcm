# coding = utf-8
# usr/bin/env python

'''
Author: Chuck
Email: zliu18@gmail.com

date: 30/10/2019 9:39 AM
desc:
'''
import requests
import os
from bs4 import BeautifulSoup
import time
import bs4


save_path = '/Users/zliu/downloads/txcm1/'
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36(KHTML, like Gecko)"
                             " Chrome", "Accept": "text/html,application/xhtml+xml,application/xml;q = 0.9, image "
                                                  "/ webp, * / *;q = 0.8"}
domain = 'https://www.biqubu.com/'


def get_page(herf):
    global headers
    # url = domain + str(herf) + '.html'
    url = herf
    response = requests.get(url, headers = headers)
    # content = response.content.decode('utf-8')
    return response.content


def save_to_file(html, title, page_number, length=3):
    rev_tmp_dir = save_path  # 定义文件存储临时目录
    if not os.path.exists(rev_tmp_dir):
        os.makedirs(rev_tmp_dir)
    while len(str(page_number)) < length:
        page_number = '0' + str(page_number)
    file_name = rev_tmp_dir + "" + str(page_number) + ' ' + title + '.txt'
    with open(file_name, "w", encoding="utf-8") as f:
        f.write('<h1>' + title + '</h1><p>')
        for i in range(0, len(html.contents)):
            f.write(str(html.contents[i]))
        f.write('</p>')
        f.close()


def parse(content):
    soup = BeautifulSoup(content, 'lxml')
    book_name = soup.find('div', {'class': 'bookname'})
    title = book_name.find('h1')
    # print(type(title))
    book_content = soup.find('div', {'id': 'content'})
    text = ''
    if book_content is not None:
        # print(type(book_content))
        # for i in range(0, len(book_content.contents)):
        #     if isinstance(book_content.contents[i], bs4.element.NavigableString):
        #         text = text + book_content.contents[i]
        #     else:
        #         text = text + '\n'
            # text = text + re.sub('<br/>', '\n', book_content.contents[i])
        # book_content = re.sub('<br/>', '\n', book_content)
        return [str(title.text).strip(), book_content]
    else:
        return None


def parse_menu(content):
    soup = BeautifulSoup(content, 'lxml')
    dd_list = soup.find('div', {'id':'list'})
    links = []
    if dd_list is not None:
        for dd in dd_list.find_all('dd'):
            if dd is not None:
                link = dd.find('a')
                # print(link.text + " " +link['href'])
                links.append(link)
    return links


def merge():
    with open(save_path+'output_file.md','wb') as wfd:
        for root, dirs, files in os.walk(save_path):
            for f in files:
                with open(save_path+f,'rb') as fd:
                        wfd.write(fd.read())


if __name__ == '__main__':
    link_list = parse_menu(get_page(domain + 'book_17532/'))
    for i in range(0, len(link_list)):
        if i > 208:
            chapter = parse(get_page(domain + link_list[i]['href']))
            if chapter is not None:
                save_to_file(chapter[1], chapter[0], i)
                print('{} done'.format(chapter[0]))
                time.sleep(1)

    merge()
    # for i in range(3102, 3547):
    #     chapter = parse(get_page(i))
    #     if chapter is not None:
    #         save_to_file(chapter[0], chapter[1], i)
    #         print('{} done'.format(chapter[0]))
    #         time.sleep(2)