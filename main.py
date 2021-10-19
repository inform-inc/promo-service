from os import name
from flask import Flask, jsonify
from flask_restful import Api, Resource, abort, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_cors import CORS, cross_origin
from werkzeug.utils import cached_property

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

api = Api(app)
engine = create_engine('postgresql+psycopg2://postgres:Mj3nH5@db:5432/promofeeds')
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://postgres:Mj3nH5@db:5432/promofeeds"
app.config['SERVER_NAME'] = "0.0.0.0:5000"
db = SQLAlchemy(app)

class FeedModel(db.Model):
    feedid = db.Column(db.Integer)
    url = db.Column(db.String(100), nullable=False)
    trackinggroup = db.Column(db.Integer, primary_key=True, nullable=False)
    
    def __repr__(self):
         return f"FeedID = {feedid}, trackingGroup = {trackinggroup}, partnerURL = {url}"
db.create_all()     
class ArticleModel():
    feedid = fields.Integer
    url = fields.String
    trackinggroup = fields.Integer
    thumbnail = fields.String
    
    def __repr__(self):
         return f"FeedID = {feedid}, trackingGroup = {trackinggroup}, partnerURL = {url}"
        


feed_put_args = reqparse.RequestParser()
feed_put_args.add_argument("feedid", type=int, help="id is missing", required=True)
feed_put_args.add_argument("url", type=str, help="URL of Feed", required=True)

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

class Feed(Resource):
    @marshal_with(resource_fields)
    def get(self, trackinggroup):
        print(trackinggroup)
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

class Returnurl(Resource):
    @marshal_with(resource_fields_article)
    def get(self, trackinggroup):
        result = FeedModel.query.filter_by(trackinggroup=trackinggroup).first()
        rssFeedURL = result.url.replace("\\","")
        return rssFeedURL


class parseURL(Resource):
    @marshal_with(resource_fields_article)
    def get(self, trackinggroup):
        result = FeedModel.query.filter_by(trackinggroup=trackinggroup).first()
        rssFeedURL = result.url.replace("\\","")
        print('rssFeedURL: ' + rssFeedURL)        


def getPartnerFeedUrl(trackinggroup):
    result = FeedModel.query.filter_by(trackinggroup=trackinggroup).first()
    return result

def parseurl(rssFeedURL):
    if rssFeedURL is not None:
        #print("rssfeedurl is not none")
        import feedparser # type: ignore
        import json
        
        # parsing partner feed
        partner_feed = partner_feed = feedparser.parse(rssFeedURL)
        
        # getting lists of partner entries via .entries
        posts = partner_feed.entries
        
        post_list = []
        
        # iterating over individual posts        
        for post in posts:
            temp = dict()
            
            # if any post doesn't have information then throw error.
            try:    
                temp["title"] = post.title
                temp["link"] = post.link
                temp["imageSrc"] = post.media_thumbnail
                # temp["author"] = post.author
                # temp["time_published"] = post.published

            except:
                pass
            
            post_list.append(temp)
       
    response = jsonify(post_list)    
    return response

def main():
    import requests
    from flask import Flask, jsonify
    from flask_sqlalchemy import SQLAlchemy
    from markupsafe import escape   
         
    BASE = "http://0.0.0.0:5000/"

    api.add_resource(Feed, "/feed/<int:trackinggroup>", endpoint="feed")

    @app.route("/")
    @cross_origin()
    
    @app.route('/articles/<trackinggroup>', endpoint="articles")
    def gettrackinggroup(trackinggroup):
        data = requests.get(BASE + "feed/" + trackinggroup)
        data = data.json()
        feedURLfromData = data["url"]
        rssFeedURL = feedURLfromData.replace("\\","")
        return parseurl(rssFeedURL)

    app.run(host="0.0.0.0", debug=True)


if __name__ == "__main__":
    main()