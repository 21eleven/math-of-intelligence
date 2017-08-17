import MySQLdb as db
import sys
import requests
from lxml import html
from bs4 import BeautifulSoup as bs
import re

try:
    # connect to mysql instance 
    conn = db.connect('localhost','user', 'password', 'db_name')
    mysql = conn.cursor()

    mysql.execute('DESCRIBE article_html')
    describe = mysql.fetchall()

    print(describe)
    
    # get list of article ids from database
    mysql.execute("select id from article_html where open = 1")
    ids = mysql.fetchall()
    print(len(ids))

    # iterate through list of article id
    for idx in range(len(ids)):
        _id = ids[idx][0]
        # select article html and metadata based on id
        get = 'select title, html, url, topic, journal, date, type from article_html where id = {}'.format(_id)
        mysql.execute(get)
        row = mysql.fetchall()[0]
        
        title = row[0]
        html = row[1]
        url = row[2]
        topic = row[3]
        journal = row[4]
        date = row[5]
        _type = row[6]

        print(title, '\n', url, '\n', topic, journal, date)
        try:
            # load html into beautiful soup
            soup = bs(html)
            # remove html tags
            text = soup.get_text()
            # cut string to only include text after 
            # 'Abstract' header and before 'References' header
            text = text.split('Abstract')[1]
            text = text.split('References')[0]
            try:
                text = text.split("Additional Information")[0]
            except:
                pass

            lines = text.split('\n')

            filtered = []
            
            for line in lines:
                # remove lines of text with few words,
                # these lines are mostly figure labels
                if len(line) > 9:
                    filtered.append(line)
            
            # preprocessing
            # make lowercase, remove reseach paper section header words
            # (ie introduction, discussion, conclusion, methods)
            # remove digits and special characters
            text = '\n'.join(filtered)
            text = text.lower()
            text = text.replace('introduction',' introduction ')
            text = text.replace('discussion',' discussion ')
            text = text.replace('conclusion',' conclusion ')
            text = text.replace('methods',' methods ')
            text = ''.join(c for c in text if not c.isdigit())
            text = re.sub('[^A-Za-z0-9]+', ' ', text)

            word_count = len(text.split(' '))
            print(word_count)
            
            # insert cleaned article text into articles tables 
            # along with metadata
            insert = "REPLACE INTO articles (title, text, url, topic, journal, date, type, wc) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)"

            mysql.execute(insert, (title, text, url, topic, journal, date, _type, word_count))
            conn.commit()

        except:
            pass
            

except e:
    print(e)

finally:
    conn.close()
