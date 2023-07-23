import os, os.path
import random
# import sqlite3
import mariadb
import string
import time
from dotenv import dotenv_values
import redis
import datetime

import asyncio
import websockets

import jwt

import cherrypy_cors
cherrypy_cors.install()

# from cherrypy.websocket import WebSocket

secrets=dotenv_values(".env")

import cherrypy
cherrypy.config.update({'server.socket_host': secrets["cherrypy_host"], 'server.socket_port': int(secrets["cherrypy_port"]), 'cors.expose.on': True,})

redis = redis.Redis(secrets["redis_host"], port=int(secrets["redis_port"]), decode_responses=True, password=secrets["redis_password"])

DB_STRING = "my.db"

def authenticate(username, password):
    if username == "admin" and password == "password":
        # Create a JWT token with a subject claim "admin" and an expiration time of 1 hour
        payload = {"sub": "admin", "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)}
        token = jwt.encode(payload, secrets["jwt_secret"], algorithm="HS256")
        return token
    else:
        return None

print (authenticate("admin", "password"))

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

# async def hello(websocket):
#     name = await websocket.recv()
#     print(f"<<< {name}")

#     greeting = f"Hello {name}!"

#     await websocket.send(greeting)
#     print(f">>> {greeting}")

# async def main():
#     async with websockets.serve(hello, "192.168.1.191", 8765):
#         await asyncio.Future()  # run forever

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

    # def POST(self, user="user", password="password"):
    #     token = user + password
    #     return token

    def POST(self, *args, **kwargs):

        length = kwargs.get("length", None)
        if length == None:
            length = 8
        print("length is: ",length)
        
        user = kwargs.get("user", None)
        
        password = kwargs.get("password", None)
        
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

    def DELETE(self):
        with mariadbconn.cursor() as c:
            print('DELETE ', redis.get('timestamp'))
            c.execute("DELETE FROM user_string WHERE session_id=?",
                     [redis.get('timestamp')])
        mariadbconn.commit()

    @cherrypy.expose
    def websocket(self, **kwargs):
        ws = websockets.connect('ws://192.168.1.191:8099/websocket')
        print("New websocket connection")
        while True:
            message = ws.recv()
            print("Received message: " + message)
            ws.send("Hello, client!")

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

    # asyncio.run(main())

    # cherrypy.engine.subscribe('start', setup_database)
    # cherrypy.engine.subscribe('stop', cleanup_database)

    webapp = StringGenerator()
    webapp.generator = StringGeneratorWebService()
    cherrypy.quickstart(webapp, '/', conf)

    # asyncio.run(main())