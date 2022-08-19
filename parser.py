from requests_html import HTMLSession
from bs4 import BeautifulSoup
import config
import mysql.connector
from datetime import datetime

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
        soup = BeautifulSoup(article.text, 'html.parser')
        article = soup.find('article')
        span_list = BeautifulSoup(str(article), 'html.parser').find_all(
            "span", {"class": "typography__StyledTypography-owin6q-0 fUOSEs"})
        time = []
        time = ''
        for span in span_list:
            for i in span.contents:
                if (len(i) > 27):
                    if (i.startswith('Jan')):
                        time = i.replace("Jan", "1").replace(" ", "/",1).replace(", ", "/",1)
                        orderId = i.replace("Jan", "01").replace(" ", "/",1).replace(", ", "/",1).split(' ')[0]
                    elif (i.startswith('Feb')):
                        time = i.replace("Feb", "2").replace(" ", "/",1).replace(", ", "/",1)
                        orderId = i.replace("Feb", "02").replace(" ", "/",1).replace(", ", "/",1).split(' ')[0]
                    elif (i.startswith('Mar')):
                        time = i.replace("Mar", "3").replace(" ", "/",1).replace(", ", "/",1)
                        orderId = i.replace("Mar", "03").replace(" ", "/",1).replace(", ", "/",1).split(' ')[0]
                    elif (i.startswith('Apr')):
                        time = i.replace("Apr", "4").replace(" ", "/",1).replace(", ", "/",1)
                        orderId = i.replace("Apr", "04").replace(" ", "/",1).replace(", ", "/",1).split(' ')[0]
                    elif (i.startswith('May')):
                        time = i.replace("May", "5").replace(" ", "/",1).replace(", ", "/",1)
                        orderId = i.replace("May", "05").replace(" ", "/",1).replace(", ", "/",1).split(' ')[0]
                    elif (i.startswith('Jun')):
                        time = i.replace("Jun", "6").replace(" ", "/",1).replace(", ", "/",1)
                        orderId = i.replace("Jun", "06").replace(" ", "/",1).replace(", ", "/",1).split(' ')[0]
                    elif (i.startswith('Jul')):
                        time = i.replace("Jul", "7").replace(" ", "/",1).replace(", ", "/",1)
                        orderId = i.replace("Jul", "07").replace(" ", "/",1).replace(", ", "/",1).split(' ')[0]
                    elif (i.startswith('Aug')):
                        time = i.replace("Aug", "8").replace(" ", "/",1).replace(", ", "/",1)
                        orderId = i.replace("Aug", "08").replace(" ", "/",1).replace(", ", "/",1).split(' ')[0]
                    elif (i.startswith('Sep')):
                        time = i.replace("Sep", "9").replace(" ", "/",1).replace(", ", "/",1)
                        orderId = i.replace("Sep", "09").replace(" ", "/",1).replace(", ", "/",1).split(' ')[0]
                    elif (i.startswith('Oct')):
                        time = i.replace("Oct", "10").replace(" ", "/",1).replace(", ", "/",1)
                        orderId = i.replace("Oct", "10").replace(" ", "/",1).replace(", ", "/",1).split(' ')[0]
                    elif (i.startswith('Nov')):
                        time = i.replace("Nov", "11").replace(" ", "/",1).replace(", ", "/",1)
                        orderId = i.replace("Nov", "11").replace(" ", "/",1).replace(", ", "/",1).split(' ')[0]
                    elif (i.startswith('Dec')):
                        time = i.replace("Dec", "12").replace(" ", "/",1).replace(", ", "/",1)
                        orderId = i.replace("Dec", "12").replace(" ", "/",1).replace(", ", "/",1).split(' ')[0]
        if orderId[5] != '/':
            orderId = '0'.join(orderId.split('/',1)).replace('/','')
        else: orderId = orderId.replace('/','')
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
                sql = "INSERT INTO news (link, title, picture, time, content, orderId) VALUES (%s, %s, %s, %s, %s, %s)"
                val = (link, soup.title.text, picture, time, p[0], orderId)
                mycursor.execute(sql, val)
                mydb.commit()
                print(mycursor.rowcount, "record inserted.")
        except Exception as e:
            print(link)
            print(e)