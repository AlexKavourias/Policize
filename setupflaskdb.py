'''
Created on Sep 13, 2014
Sets up the master sqlite db that I eventually use for my queries in the actual
Flask app.
@author: Alex
'''

import sqlite3
from DataAnalysis import TwitterCorpus as tc

conn = sqlite3.connect('C:/users/alex/desktop/policize/MasterFlask.db')
curs = conn.cursor()

mconn = sqlite3.connect('C:/users/alex/desktop/MembersofCongress.sqlite3')
mcurs = mconn.cursor()

Hconn = sqlite3.connect('C:/users/alex/desktop/policize/CloudURLs.db')
hcurs = Hconn.cursor()

Iconn = sqlite3.connect('C:/users/alex/desktop/policize/IconURLs.db')
icurs = Iconn.cursor()

sql_direct = 'C:/users/alex/sirf/moc/%s.sqlite3'

sens = set(map(lambda x:x[0],mcurs.execute('select name from senate').fetchall()))
reps = set(map(lambda x:x[0],mcurs.execute('select name from house').fetchall()))
curs.execute('drop table if exists info')
for moc in tc.get_mocs():
    name = moc[0]
    handle = moc[1]
    
    if name in sens:
        title = 'Sen.'
    else:
        title = 'Rep.'
    try:    
        count = sqlite3.connect(sql_direct % handle).cursor().execute("select count(*) from tweets").fetchone()[0]
    except: 
        continue
    curs.execute('create table if not exists Info(title text,name text,party text,tweets int,icon_url text,ht_url text,district text,handle text)')
    fetch = mcurs.execute("select name,party,district from members where handle = '%s'" % moc[1]).fetchone()
    icon = icurs.execute("select url from links where name = '%s' COLLATE NOCASE" % handle).fetchone()[0]
    cloud = hcurs.execute("select url from links where name = '%s' COLLATE NOCASE " % handle).fetchone()

    if cloud is None:
        cloud = 'no cloud'
    else:
        cloud = cloud[0]
    curs.execute('insert into Info(title,name,party,tweets,icon_url,ht_url,district,handle) VALUES(?,?,?,?,?,?,?,?)',(title,
                                                                                     name,
                                                                                     fetch[1],
                                                                                     count,
                                                                                     icon,
                                                                                     cloud,
                                                                                     fetch[-1],
                                                                                     str(handle)))
conn.commit()
