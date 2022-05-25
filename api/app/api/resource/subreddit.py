from flask import request
from flask_restful import Resource
from app.common import paginate
from app.api.schema import SubRedditSchema
from app.extensions import db
from app.models import SubReddit


class SubRedditResource(Resource):
    def get(self, subreddit_id):
        schema = SubRedditSchema()
        subreddit = SubReddit.query.get_or_404(subreddit_id)
        return {"subreddit": schema.dump(subreddit)}

    def put(self, subreddit_id):
        schema = SubRedditSchema()
        subreddit = SubReddit.query.get_or_404(subreddit_id)
        subreddit = schema.load(request.json, instsance=subreddit)

        db.session.commit()

        return {"subreddit": schema.dump(subreddit)}

    def delete(self, subreddit_id):
        subreddit = SubReddit.get_by_id(subreddit_id)
        subreddit.delete()
        return None, 204


class SubRedditList(Resource):
    def get(self):
        schema = SubRedditSchema(many=True)
        query = SubReddit.query
        return paginate(query, schema)

    def post(self):
        schema = SubRedditSchema()
        subreddit = schema.load(request.json)
        subreddit.save()
        return {"subreddit": schema.dump(subreddit)}, 201

