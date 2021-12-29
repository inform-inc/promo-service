import sys
from os import name, environ, getenv
from flask import Flask, jsonify, request, make_response
from flask_restful import Api, Resource, abort, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_cors import CORS, cross_origin
from werkzeug.utils import cached_property
from sqlalchemy.orm import sessionmaker
from safrs import SAFRSBase, SAFRSAPI
from flask_healthz import Healthz
from flask_healthz import HealthError
from sqlalchemy.types import Text

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

# Parse URL from given URL 
# "rssFeedURL": feed URL from gettrackinggroup
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

# Health Checks
Healthz(app, no_log=True)
def liveness():
    pass
def readiness():
    try:
        session.execute('SELECT 1')
    except Exception:
        raise HealthError("Unable to connect to DB")
app.config.update(
    HEALTHZ = {
        "live": "main.liveness",
        "ready": "main.readiness"
    }
)

# main
def main():
    import requests
    from flask import Flask, jsonify
    from flask_sqlalchemy import SQLAlchemy
    from markupsafe import escape   
        
    # add resouce for returning feed info given the trackinggroup
    api.add_resource(Feed, "/feed/<int:trackinggroup>", endpoint="feed")
    
    @app.route("/")
    @cross_origin()
    
    # get the list of items givin a tracking group - returns as json    
    @app.route('/articles/<trackinggroup>', endpoint="articles")
    
    #gets trackinggroup from api uri, gets the feed from getURL and then sends it to the parser for display
    def gettrackinggroup(trackinggroup):
        rssFeedURL = getUrl(trackinggroup)                
        #print(rssFeedURL, file=sys.stderr)
        return parseurl(rssFeedURL)        
    
    # gets the url of the partner from the db
    def getUrl(trackinggroup):
        # data = requests.get(request.url_root + "feed/" + trackinggroup)
        results = engine.execute("select url from promofeeds where trackingGroup='"+trackinggroup+"'")        
        data = [i[0] for i in results]
        result = str(data)[2:-2]       #trims the list
        return result

    app.run(host="0.0.0.0", port=server_port, debug=True)

# init main()
if __name__ == "__main__":
    main()