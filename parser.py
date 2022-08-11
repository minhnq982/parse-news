from requests_html import HTMLSession
from bs4 import BeautifulSoup
import config
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    port='33006',
    user="maria",
    password="123",
    database='nest',
)

mycursor = mydb.cursor()


class Parser():
    session = HTMLSession()
    coindesk = session.get(config.COINDESK)
    soup = BeautifulSoup(coindesk.text, 'html.parser')
    sections = soup.find_all("section")
    list_article = []
    for section in sections:
        link = BeautifulSoup(str(section), 'html.parser').find_all("a")
        for href in link:
            if (str(href.get('href')).startswith(
                ("/author", "/policy", "/newsletters", "/podcasts", "https",
                "/learn", "/reports","/sponsored-content")) == False and len(str(href.get('href')))
                    > len(config.COINDESK.split('/')[-1]) + 10):
                list_article.append(config.COINDESK + href.get('href'))
    for link in set(list_article):
        article = session.get(link)
        print(link)
        soup = BeautifulSoup(article.text, 'html.parser')
        article = soup.find('article')
        span_list = BeautifulSoup(str(article), 'html.parser').find_all(
            "span", {"class": "typography__StyledTypography-owin6q-0 fUOSEs"})
        time = []
        time = ''
        for span in span_list:
            for i in span.contents:
                if (len(i) > 27):
                    if (i.startswith('Jul')):
                        time = i.replace("Jul", "7").replace(" ", "/",1).replace(", ", "/",1)
                    elif (i.startswith('Aug')):
                        time = i.replace("Aug", "8").replace(" ", "/",1).replace(", ", "/",1)
        figure = soup.find('figure')
        img = BeautifulSoup(str(figure), 'html.parser')
        p = soup.find('h2').contents
        try :
            picture = img.find('img').get('src')
        except :
            picture = ''
        try:
            sql = 'SELECT * FROM news WHERE title ="'+soup.title.text+'"'
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            if(len(myresult)==0):
                sql = "INSERT INTO news (link, title, picture, time, content) VALUES (%s, %s, %s, %s, %s)"
                val = (link, soup.title.text, picture, time, p[0])
                mycursor.execute(sql, val)
                mydb.commit()
                print(mycursor.rowcount, "record inserted.")
        except Exception as e:
            print(link)
            print(e)