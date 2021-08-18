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
    partnerTrackingGroup = db.Column(db.String(5), primary_key=True, nullable=False)
    partnerURL = db.column(db.String(100))

    def __repr__(self):
        return F"FeedId ="
        # return f"FeedID = {feedid}, trackingGroup = {partnerTrackingGroup}, partnerURL = {partnerURL}"
        # return f"Feed(feedid={feedid}, partnerTrackingGroup={partnerTrackingGroup}, partnerFeedURL={PartnerFeedURL})"

# db.create_all()

feed_put_args = reqparse.RequestParser()

feed_put_args.add_argument("partnerTrackingGroup", type=str, help="partnerTrackingGroup is missing")
feed_put_args.add_argument("partnerURL", type=str, help="URL of Feed", required=True)

feed_update_args = reqparse.RequestParser()
feed_update_args.add_argument("partnerTrackingGroup", type=str, help="partnerTrackingGroup is missing")
feed_update_args.add_argument("partnerURL", type=str, help="URL of Feed", required=True)

resource_fields = {
    "feedid": fields.Integer,
    "partnerURL": fields.String,
    "partnerTrackingGroup": fields.String
    
}
feeds = {}

class Feed(Resource):
    @marshal_with(resource_fields)
    def get(self, trackingGroup):
        result = FeedModel.query.filter_by(id=trackingGroup).first()
        if not result:
            abort(404, message="no feed with that trackingGroup")
        return result

    @marshal_with(resource_fields)
    def put(self, trackingGroup):
        args = feed_put_args.parse_args()
        result = FeedModel.query.filter_by(partnerTrackingGroup=trackingGroup).first()
        if result:
            abort(409, message="already a feed for trackingGroup")
        #feed = FeedModel(id=feedid, partnerURL=args[partnerURL], trackingGroup=args[partnerTrackingGroup])
        #db.session.add(feed)
        #db.session.commit()
        return feeds, 201

    def delete(self, trackingGroup):
        #abort_if_no_feed_exists(trackingGroup)
        del feeds[trackingGroup]
        return '', 204



api.add_resource(Feed, "/feed/<int:trackingGroup>")   


if __name__ == "__main__":
    app.run(debug=True)