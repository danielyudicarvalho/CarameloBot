import bs4
import urllib.request as urllib_request
import pandas
from urllib.request import urlopen
from bs4 import BeautifulSoup


url = 'https://adotar.com.br/animais.aspx?cc=1484&cn=ms-campo-grande&finalidade=Adocao&tipo=Cao&porte=Medio'

response = urlopen(url)

html = response.read()

soup = BeautifulSoup(html, 'html.parser')
res = soup.findAll('div', class_="listaAnimais")

try:
    for item in res:
                link = item.find('a')['href']
                link = 'https://adotar.com.br'+link
                responseLink = urlopen(link)
                htmlLink = responseLink.read()
                soupLink = BeautifulSoup(htmlLink, 'html.parser')
                contact = soupLink.find('a',{"id":"mailprop"})
                email = contact['href']
                phone = contact.findNextSibling().find('a').getText()
                image = item.find('img')['src'][2:]
                text = item.find('div',{'class':'listaAnimaisDados'})
                text = text.get_text().split()
                print(link)
                print(text[0])
                print(image)
                print(email)
                print(phone)
except:
    print('not found')