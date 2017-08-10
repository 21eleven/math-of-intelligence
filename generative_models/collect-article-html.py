import MySQLdb as db
import sys
import requests
from lxml import html

try:
    conn = db.connect('localhost','user', 'password', 'db_name')
    mysql = conn.cursor()

    mysql.execute('DESCRIBE article_html')
    describe = mysql.fetchall()

    print(describe)

    if len(sys.argv) == 2:
        topic=sys.argv[1]
    else:
        #topic = 'biotechnology'
        #topic = 'anatomy'
        #topic = 'anthropology'
        #topic = 'physics'
        #topic = 'psychology'
        #topic = 'mathematics-and-computing'
        #topic = 'computational-biology-and-bioinformatics'
        #topic = 'ecology'
        #topic = 'cell-biology'
        #topic = 'microbiology'
        #topic = 'biogeochemistry'
        #topic = 'biochemistry'
        #topic = 'zoology'
        #topic = 'climate-sciences'
        #topic = 'neuroscience'
        #topic = 'genetics'
        #topic = 'cancer'
        #topic = 'plant-sciences'
        #topic = 'immunology'
        #topic = 'chemical-biology'
        #topic = 'chemistry'
        #topic = 'evolution'
        #topic = 'stem-cells'
        #topic = 'ocean-sciences'
        #topic = 'diseases'
        #topic = 'molecular-medicine'
        #topic = 'engineering'
        #topic = 'materials-science'
        #topic = 'nanoscience-and-technology'
        #topic = 'drug-discovery'
        #topic = 'philosophy'
        #topic = 'business-and-industry'
        topic = 'developmental-biology'
    
    pages = 8
    print('===={}===='.format(topic))
    for i in range(1,pages+1):
        print('////// PAGE {} //////'.format(i))

        if i == 1:
            search_url = "https://www.nature.com/search?article_type=research,reviews,protocols&order=relevance&subject={}".format(topic)
        else:
            search_url = "https://www.nature.com/search?article_type=research,reviews,protocols&order=relevance&subject={}&page={}".format(topic,i)

        res = requests.get(search_url)
        results = html.fromstring(res.content) # string as byte string

        for x in range(1,26):
            link_xpath = '//*[@id="content"]/div/div/div/div[2]/div[2]/section/ol/li[{}]/div/h2/a/@href'.format(x)
            title_xpath = '//*[@id="content"]/div/div/div/div[2]/div[2]/section/ol/li[{}]/div/h2/a/text()'.format(x)
            open_xpath = '//*[@id="content"]/div/div/div/div[2]/div[2]/section/ol/li[{}]/p/span[3]/text()'.format(x)
            date_xpath = '//*[@id="content"]/div/div/div/div[2]/div[2]/section/ol/li[{}]/p/time/text()'.format(x)
            link_header_xpath = '//*[@id="content"]/div/div/div/div[2]/div[2]/section/ol/li[{}]/p/text()'.format(x)
            authors_xpath = '//*[@id="content"]/div/div/div/div[2]/div[2]/section/ol/li[{}]/div/ul/text()'.format(x)
            journal_xpath = '//*[@id="content"]/div/div/div/div[2]/div[2]/section/ol/li[{}]/div/div/div[1]/a/text()'.format(x)

            link = results.xpath(link_xpath)[0]
            title = results.xpath(title_xpath)
            if len(title) > 1:
                title = " ".join(title)
            else: 
                title = title[0]
            _open = results.xpath(open_xpath) # empty if not open
            date = results.xpath(date_xpath)[0]
            _type = results.xpath(link_header_xpath)[0] #research,protocol,reviews
            journal = results.xpath(journal_xpath)[0]

            article_html = requests.get(link)
            article_html = article_html.text.encode('ascii', 'ignore')

            print(link)
            print(title)
            if len(_open) == 0:
                _open = 0
            else:
                _open = 1
                print("open")
            print(journal, date, _type)
            print(len(article_html))

            insert = "REPLACE INTO nature.article_html (title, html, url, topic, journal, open, date, type) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)"
            mysql.execute(insert , (title,article_html,link,topic,journal,_open,date,_type))
            conn.commit()

except e:
    print(e)

finally:
    conn.close()
