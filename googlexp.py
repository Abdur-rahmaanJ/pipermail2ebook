# -*- coding: utf-8 -*-
"""

"""

import requests
from bs4 import BeautifulSoup

def html_start():
    return """
<!DOCTYPE html>
<html>
<head>
    <!--<link rel="stylesheet" type="text/css" href="style.css">-->
    <link href='https://fonts.googleapis.com/css?family=Raleway' rel='stylesheet' type='text/css'>
    <title></title>
    <style>
        
        pre{
            white-space: pre-wrap;
        }
        div{
            font-family: Raleway;
        }
        
        body{
            padding: 20px;
        }
        .author{
            color: orange;
            font-weight: bold;
        }
        .author > span{
            color: black;
        }
        
        .date{
            text-align: center;
        }
        .moreinfo{
            text-align: center;
        }
        
        .title{
            color: purple;
            font-weight: bold;
        }
        
        .response{
            color: green;
            font-weight: bold;
        }
    </style>
</head>
<body>"""

def html_info(date):
    return """
    <div class="date">{}</div>
    <div class="moreinfo">mailing-list as ebook, take a nice cup of coffee and enjoy</div>
    <div><a href='https://github.com/abdur-rahmaanj'>initiative of this person</a></div>
    <hr>""".format(date)

def html_end():
    return """
</body>
</html>
"""

def soup_content(url):
#url = "https://mail.python.org/pipermail/python-list/2018-July/736157.html"
    r = requests.get(url)
    r.encoding = 'utf-8'
    content = r.text
    # print(content)
    soup = BeautifulSoup(content, 'html.parser', from_encoding="utf-8")
    return {'soup':soup, 'content':content}

def title_author(soup):
    '''takes soup as arg'''
    title = soup.find_all('h1')[0].text
    author = soup.find_all('b')[0].text
    return {'title':title, 'author':author}

def next_prev(soup):
    '''takes soup as arg'''
    tags = soup.find_all('a')
    return {'next':tags[-6], 'prev':tags[-7]}
    
def extract_mail(content):
    '''takes raw html as text r.text, returns str'''
    listofcontent = content.split()
    
    target = []
    intake = 0
    
    for elem in listofcontent:
        if elem == '<!--beginarticle-->':
            intake = 1
            continue
        elif  elem == '<!--endarticle-->':
            break
        
        if intake:
            target.append(elem)
            
    return ' '.join(target)


def get_hrefs(soup, base_=''):
    tags = soup.find_all('a')
    links = []
    
    for tag in tags:
        try:
            links.append(base_+tag['href'])
        except KeyError:
            pass
        
    return links

def get_aumail(soup):
    tags = soup.find_all('a')
    return tags[0].text

def get_date(soup):
    tags = soup.find_all('I')
    return tags[0].text

def add_breaks(string):
    n = 120
    # credits : user dh from freebsd forum
    return '<br>'.join([string[i:i+n] for i in range(0, len(string), n)])

doc = open('doc.html', 'w+')

base = "https://mail.python.org/pipermail/python-list/2018-July/"

url = base+"thread.html"

main = soup_content(url)
soup = main['soup']
# print(get_hrefs(soup, base_=base))

c = 0

doc.write(html_start())
doc.write(html_info('2018-July'))

for link in get_hrefs(soup, base_=base):
    # if c == 10:
    #    break
    
    
    if link.endswith('.html'):
        try:
            sc = soup_content(link)
            #print(sc['content'])
            #print(title_author(sc['soup']))
            #print(extract_mail(sc['content']))
            doc.write('<div class="author">' + title_author(sc['soup'])['author'] + 
                      '<span> - '+get_aumail(sc['soup'])+'</span></div><br>\n')
            doc.write('<div class="title">' + title_author(sc['soup'])['title'] + 
                      '</div><br>\n')
            
            body = extract_mail(sc['content'].strip()).replace('<I>', 
                      '<br><I>').replace('</I>', '</I>\n')
            body_s = body.split('</I>')
            formatted = add_breaks(body_s[-1])
            body_s[-1] = '<div class="response">' + formatted + '</div>'
            # print(formatted)
            doc.write( '</I>'.join(body_s) + '<br>')
            doc.write('<hr>\n\n')
            doc.flush()
        except UnicodeEncodeError:
            pass
    
    # c += 1

doc.write(html_end()) 
doc.close()
print('program terminated')
    

#tags = soup.find_all('a')
#links = []
#
#for tag in tags:
#    try:
#        links.append(tag['href'])
#    except KeyError:
#        pass
#    
#c = 0
#for link in links:
#    if c == 2:
#        break
#    url = base+link
#    r = requests.get(url)
#    content = r.text
#    print(content)
#    c += 1

