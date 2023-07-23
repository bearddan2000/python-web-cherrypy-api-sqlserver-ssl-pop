import cherrypy
import json
from cp_sqlalchemy import SQLAlchemyTool, SQLAlchemyPlugin

import settings
from model import Base, PopModel

class App:
    @property
    def db(self):
        return cherrypy.request.db

    @cherrypy.expose
    def index(self):
        pops = self.db.query(PopModel).all()
        results = [
            {
                "id": pop.id,
                "name": pop.name,
                "color": pop.color
            } for pop in pops]

        return json.dumps(results)

def run():
    cherrypy.tools.db = SQLAlchemyTool()

    global_config = {
        'global' : {
            'server.socket_host' : '0.0.0.0',
            'server.socket_port' : 8080
        }
    }

    app_config = {
        '/' : {
            'tools.db.on': True
        }
    }

    cherrypy.config.update(global_config)

    cherrypy.tree.mount(App(), '/', config=app_config)

    sqlalchemy_plugin = SQLAlchemyPlugin(
        cherrypy.engine, Base,
            '{engine}://{username}:{password}@{host}/{db_name}'.format(
                **settings.SQLSERVER
            ),
        echo=True
    )

    sqlalchemy_plugin.subscribe()
    sqlalchemy_plugin.create()

    cherrypy.engine.start()
    cherrypy.engine.block()

if __name__ == '__main__':
    run()
