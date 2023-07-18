import os, os.path
import random
# import sqlite3
import mariadb
import string
import time
from dotenv import dotenv_values
import redis

import cherrypy_cors
cherrypy_cors.install()

secrets=dotenv_values(".env")

import cherrypy
cherrypy.config.update({'server.socket_host': secrets["cherrypy_host"], 'server.socket_port': int(secrets["cherrypy_port"]), 'cors.expose.on': True,})

redis = redis.Redis(secrets["redis_host"], port=int(secrets["redis_port"]), decode_responses=True, password=secrets["redis_password"])

DB_STRING = "my.db"

try:
    mariadbconn = mariadb.connect(
        user=secrets["user"],
        password=secrets["password"],
        host=secrets["host"],
        port=int(secrets["port"]),
        database=secrets["database"]
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

mariadbcur = mariadbconn.cursor()

try:
    test = mariadbcur.execute("SELECT session_id FROM user_string;")
except:
    print("Tabela user_string nie istnieje")
    print("Tworzę")
    mariadbcur.execute("CREATE TABLE `python_test`.`user_string` (`session_id` TEXT NOT NULL , `value` TEXT NOT NULL ) ENGINE = InnoDB;")

class StringGenerator(object):
    @cherrypy.expose
    def index(self):
        return open('index.html')

# @cherrypy_cors.tools.preflight(allowed_methods=['GET', 'POST', 'DELETE'])
@cherrypy.expose
# @cherrypy.tools.json_out()
# @cherrypy.tools.json_in(force=False)
class StringGeneratorWebService(object):

    @cherrypy_cors.tools.preflight(allowed_methods=["GET", "DELETE", "PUT"])
    def OPTIONS(self):
        redisTS = redis.get('timestamp')
        print('redis test options ', redisTS)
        # pass

    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        redis.set('timestamp', time.time())
        with mariadbconn.cursor() as c:
            print('GET ', redis.get('timestamp'))
            r = c.execute("SELECT value FROM user_string WHERE session_id=?",
                          [redis.get('timestamp')])
        mariadbconn.commit()
        return r.fetchone()

    def POST(self, length=8):
        redis.set('timestamp', time.time())
        some_string = ''.join(random.sample(string.hexdigits, int(length)))
        with mariadbconn.cursor() as c:
            print('POST ', redis.get('timestamp'))
            c.execute("INSERT INTO user_string (session_id, value) VALUES (?, ?)",
                      [redis.get('timestamp'), some_string])
        mariadbconn.commit()
        return some_string

    def PUT(self, another_string):
        with mariadbconn.cursor() as c:
            cherrypy.session['ts'] = time.time()
            print('PUT ', redis.get('timestamp'))
            c.execute("UPDATE user_string SET value=? WHERE session_id=?",
                      [another_string, redis.get('timestamp')])
        mariadbconn.commit()

    # @cherrypy_cors.tools.preflight(allowed_methods=['GET', 'POST', 'DELETE'])
    def DELETE(self):
        with mariadbconn.cursor() as c:
            print('DELETE ', redis.get('timestamp'))
            c.execute("DELETE FROM user_string WHERE session_id=?",
                     [redis.get('timestamp')])
        mariadbconn.commit()


# def setup_database():
#     """
#     Create the `user_string` table in the database
#     on server startup
#     """
#     with sqlite3.connect(DB_STRING) as con:
#         con.execute("CREATE TABLE user_string (session_id, value)")


# def cleanup_database():
#     """
#     Destroy the `user_string` table from the database
#     on server shutdown.
#     """
#     with sqlite3.connect(DB_STRING) as con:
#         con.execute("DROP TABLE user_string")

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/generator': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }

    # cherrypy.engine.subscribe('start', setup_database)
    # cherrypy.engine.subscribe('stop', cleanup_database)

    webapp = StringGenerator()
    webapp.generator = StringGeneratorWebService()
    cherrypy.quickstart(webapp, '/', conf)