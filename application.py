import os
import flask
import MySQLdb
import requests
import BeautifulSoup
import sys
reload(sys) 
sys.setdefaultencoding('utf8')

application = flask.Flask(__name__)
application.debug = True

@application.route('/')
def hello_world():
  storage = Storage()
#  storage.populate()
#  score = storage.score()
  storage.saveRankingPerson() 
  rank = score.ranking()
  return "ranking , %d!" % rank

@application.route('/crowler')
def crowler():
  return "this is crowler"


class Storage():
  def __init__(self):
    self.db = MySQLdb.connect(
      user   = os.getenv('MYSQL_USERNAME'),
      passwd = os.getenv('MYSQL_PASSWORD'),
      db     = os.getenv('MYSQL_INSTANCE_NAME'),
      host   = os.getenv('MYSQL_PORT_3306_TCP_ADDR'),
      port   = int(os.getenv('MYSQL_PORT_3306_TCP_PORT'))
    )

    cur = self.db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS ranking(rank varchar(20),gravatar varchar(30),username varchar(30),name varchar(30),location varchar(30),language varchar(30),repos varchar(30),followers varchar(30),created varchar(30))")

  def saveRankingPerson(self):
    cur = self.db.cursor()
    cur.execute("INSERT INTO ranking(rank,gravatar,username,name,location,language,repos,followers,created) VALUES('1','http://www.baidu.com/a.png','andyiac','summer','beijing','java','30','100','2014-10-10')")

  def ranking(self):
    cur = self.db.cursor()
    cur.execute("SELECT * FROM ranking")
    row = cur.fetchone()
    return row[0] 

  def crowler(self):
    # crawler ranking
    r = requests.get("http://githubrank.com")
    soup = BeautifulSoup(r.text)

    table = soup.find('table')
    for i in range(2,1000 + 2):
      rows = table.findAll('tr')[i]
      cols = rows.findAll('td')

      Rank = cols[0].string
      Gravatar = cols[1].img.get('src')
      username = cols[2].string
      name = cols[3].string
      location = cols[4].string
      language = cols[5].string
      repos = cols[6].string
      followers = cols[7].string
      created = cols[8].string

      values = [Rank,Gravatar,username,name,location,language,repos,followers,created]
      cur = self.db.cursor()
      cur.execute("INSERT INTO ranking(rank,gravatar,username,name,location,language,repos,followers,created) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",values)
      self.db.commit()
      cur.close()
      print "insert -->" + Rank
    self.db.close()

    return "true"
if __name__ == "__main__":
  application.run(host='0.0.0.0', port=3000)
