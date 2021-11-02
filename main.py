
import sys
#import os
from os import name, environ, getenv
from flask import Flask, jsonify, request
from flask_restful import Api, Resource, abort, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_cors import CORS, cross_origin
from werkzeug.utils import cached_property
from sqlalchemy.orm import sessionmaker
from safrs import SAFRSBase, SAFRSAPI
from dotenv import load_dotenv
from healthcheck import HealthCheck
from sqlalchemy.types import Text

load_dotenv()

# create a Flask app
app = Flask(__name__)

# Allows CORS
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

api = Api(app)

# Connect to postgresql db
db_host = getenv('DB_HOST')
db_port = getenv('DB_PORT') or 5432
db_user = getenv('DB_USER') or 'postgres'
db_pass = getenv('DB_PASS')
database_uri = "postgresql+psycopg2://{}:{}@{}:{}/promofeeds".format(db_user, db_pass, db_host, db_port)
engine = create_engine(database_uri)
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

# App IP 
server_name = getenv('SERVER_NAME')
server_port = getenv('SERVER_PORT') or 5000
if server_name:
    app.config['SERVER_NAME'] = "{}:{}".format(server_name, server_port)

# create a configured "Session" class
Session = sessionmaker(bind=engine)

# create a Session
session = Session()
db = SQLAlchemy(app)

# create Table for Feeds with FeedID, URL, and TrackingGroup
class FeedModel(db.Model):
    __tablename__ = "promofeeds"
    feedid = db.Column(db.Integer)
    url = db.Column(db.String(100), nullable=False)
    trackinggroup = db.Column(db.Integer, primary_key=True, nullable=False)
    
    def __repr__(self):
         return f"FeedID = {feedid}, trackingGroup = {trackinggroup}, partnerURL = {url}"

# Create table
db.create_all()  
   
class ArticleModel():
    feedid = fields.Integer
    url = fields.String
    trackinggroup = fields.Integer
    thumbnail = fields.String
    
    def __repr__(self):
         return f"FeedID = {feedid}, trackingGroup = {trackinggroup}, partnerURL = {url}"
        
# CRUD args for Put call 
feed_put_args = reqparse.RequestParser()
feed_put_args.add_argument("feedid", type=int, help="id is missing", required=True)
feed_put_args.add_argument("url", type=str, help="URL of Feed", required=True)

#CRUD for Update call
feed_update_args = reqparse.RequestParser()
feed_update_args.add_argument("feedid", type=int, help="partnerTrackingGroup is missing")
feed_update_args.add_argument("url", type=str, help="URL of Feed")

resource_fields = {
    "feedid": fields.Integer,
    "url": fields.String,
    "trackinggroup": fields.Integer,
    "thumbnail": fields.String
    
}
feeds = {}

# Class for FeedModel CRUD Query
class Feed(Resource):
    @marshal_with(resource_fields)
    def get(self, trackinggroup):
        result = FeedModel.query.filter_by(trackinggroup=trackinggroup).first()
        if not result:
            abort(404, message="no feed with that trackingGroup")
        return result

    @marshal_with(resource_fields)
    def put(self, trackinggroup):
        args = feed_put_args.parse_args()
        result = FeedModel.query.filter_by(trackinggroup=trackinggroup).first()
        if result:
            abort(409, message="already a feed for trackingGroup")
        feed = FeedModel(trackinggroup=trackinggroup, url=args['url'], feedid=args['feedid'])

        db.session.add(feed)
        db.session.commit()
        return feeds, 201

    @marshal_with(resource_fields)
    def patch(self, trackinggroup):
        args = feed_update_args.parse_args()
        result = FeedModel.query.filter_by(trackinggroup=trackinggroup).first()
        if not result:
            abort(404, message="no feed exists")

        if args['url']:
            result.url = args['url']
        
        db.session.commit()
        
        return result

    def delete(self, trackinggroup):
        #abort_if_no_feed_exists(trackingGroup)
        del feeds[trackinggroup]
        return '', 204

resource_fields_article = {
    "feedid": fields.Integer,    
    "url": fields.String,
    "link": fields.String,
    "thumbnail": fields.String    
}
# Return Feed URL to use for parser
class Returnurl(Resource):
    @marshal_with(resource_fields_article)
    def get(self, trackinggroup):
        result = FeedModel.query.filter_by(trackinggroup=trackinggroup).first()
        rssFeedURL = result.url.replace("\\","")
        return rssFeedURL

# Parse url since \\ gets added
class parseURL(Resource):
    @marshal_with(resource_fields_article)
    def get(self, trackinggroup):
        result = FeedModel.query.filter_by(trackinggroup=trackinggroup).first()
        rssFeedURL = result.url.replace("\\","")
        #print('rssFeedURL: ' + rssFeedURL)        


#def getPartnerFeedUrl(trackinggroup):
#    result = FeedModel.query.filter_by(trackinggroup=trackinggroup).first()
#    return result

def create_api(app, host="localhost", port=5000, api_prefix=""):
    api = SAFRSAPI(app, host=host, port=port, prefix=api_prefix)
    api.expose_object(User)
    api.expose_object(Book)
    print(f"Created API: http://{host}:{port}/{api_prefix}")

# Parse URL from giving URL 
# "rssFeedURL": feed URL from parseURL
#
def parseurl(rssFeedURL):
    # if there is a URL then proceed
    if rssFeedURL is not None:
        
        import feedparser # type: ignore
        import json
        
        # parsing partner feed
        partner_feed = partner_feed = feedparser.parse(rssFeedURL)
        
        # getting lists of partner entries via .entries
        posts = partner_feed.entries
        
        #init list
        post_list = []
        
        # iterating over individual posts        
        for post in posts:
            temp = dict()
            
            # if any post doesn't have information then throw error.
            try:    
                temp["title"] = post.title
                temp["link"] = post.link
                temp["imageSrc"] = post.media_thumbnail                

            except:
                pass
            
            post_list.append(temp)

    # return the response as json   
    response = jsonify(post_list)    
    return response

# Healthcheck
health = HealthCheck(app, "/healthcheck")
def database_available():
    working = True
    output = "database is functioning"
    try:
        session.execute('SELECT 1')
    except Exception as e:
        output = str(e)
        working = False
    return working, output

health.add_check(database_available)

def main():
    import requests
    from flask import Flask, jsonify
    from flask_sqlalchemy import SQLAlchemy
    from markupsafe import escape   
        
    # add resouce for returning feed info givin the trackinggroup
    api.add_resource(Feed, "/feed/<int:trackinggroup>", endpoint="feed")

    @app.route("/")
    @cross_origin()
    
    # get the list of items givin a tracking group - returns as json
    @app.route('/articles/<trackinggroup>', endpoint="articles")
    def gettrackinggroup(trackinggroup):
        data = requests.get(request.url_root + "feed/" + trackinggroup)
        data = data.json()
        feedURLfromData = data["url"]
        rssFeedURL = feedURLfromData.replace("\\","")
        return parseurl(rssFeedURL)

    app.run(host="0.0.0.0", port=server_port, debug=True)

# init main()
if __name__ == "__main__":
    main()
