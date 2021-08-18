from os import name
from flask import Flask
from flask.scaffold import F 
from flask_restful import Api, Resource, abort, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

# from requests.api import delete

app = Flask(__name__)
api = Api(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql:/root:@127.0.0.1:5000/"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///tmp/database.db"
db = SQLAlchemy(app)

class FeedModel(db.Model):
    feedid = db.Column(db.Integer)
    url = db.Column(db.String(100), nullable=False)
    trackinggroup = db.Column(db.String(5), primary_key=True, nullable=False)
    
    def __repr__(self):
        #  F"FeedId ="
         return f"FeedID = {feedid}, trackingGroup = {trackinggroup}, partnerURL = {url}"
        # return f"Feed(feedid={feedid}, partnerTrackingGroup={partnerTrackingGroup}, partnerFeedURL={PartnerFeedURL})"

db.create_all()

feed_put_args = reqparse.RequestParser()
feed_put_args.add_argument("feedid", type=int, help="id is missing", required=True)
feed_put_args.add_argument("url", type=str, help="URL of Feed", required=True)

feed_update_args = reqparse.RequestParser()
feed_update_args.add_argument("feedid", type=int, help="partnerTrackingGr up is missing")
feed_update_args.add_argument("url", type=str, help="URL of Feed")

resource_fields = {
    "feedid": fields.Integer,
    "url": fields.String,
    "trackinggroup": fields.String
    
}
feeds = {}

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



api.add_resource(Feed, "/feed/<int:trackinggroup>")   


if __name__ == "__main__":
    app.run(debug=True)