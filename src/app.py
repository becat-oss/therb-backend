from flask import Flask
from flask_cors import CORS
from flask_graphql import GraphQLView
from flask_sqlalchemy import SQLAlchemy
from src.database import init_db
#from src.schema import schema
from src.models.schema import schema
from src.models.models import db_session
#import src.models

# def create_app():
#     app = Flask(__name__)
#     app.config.from_object('src.config.Config')
#     init_db(app)

#     app.add_url_rule('/graphql', 
#         view_func=GraphQLView.as_view(
#             'graphql', 
#             schema=schema, 
#             graphiql=True
#         ))

#     return app

# app=create_app()

app = Flask(__name__)
app.debug = True

app.config.from_object('src.config.Config')
init_db(app)

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True  # GraphiQLを表示
    )
)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

# if __name__ == '__main__':
#     app.run()