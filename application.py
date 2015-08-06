import os
import flask
import MySQLdb

application = flask.Flask(__name__)
application.debug = True

@application.route('/')
def hello_world():
  storage = Storage()
  storage.populate()
  score = storage.score()
  rank = score.ranking()
  return "ranking , %d!" % rank

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
    cur.execute("DROP TABLE IF EXISTS scores")
    cur.execute("CREATE TABLE scores(score INT)")
    cur.execute("DROP TABLE IF EXISTS ranking")
    cur.execute("CREATE TABLE ranking(rank INT,gravatar varchar(30),username varchar(30),name varchar(30),location varchar(30),language varchar(30),repos varchar(30),followers varchar(30),created varchar(30)")

  def populate(self):
    cur = self.db.cursor()
    cur.execute("INSERT INTO scores(score) VALUES(1234)")

  def score(self):
    cur = self.db.cursor()
    cur.execute("SELECT * FROM scores")
    row = cur.fetchone()
    return row[0]

  def saveRankingPerson(self):
    cur = self.db.cursor()
    cur.execute("INSERT INTO ranking('1','http://www.baidu.com/a.png','andyiac','summer','beijing','java','30','100','2014-10-10')")

  def ranking(self):
    cur = self.db.cursor()
    cur.execute("SELECT * FROM ranking")
    row = cur.fetchone()
    return row[0]  

if __name__ == "__main__":
  application.run(host='0.0.0.0', port=3000)
