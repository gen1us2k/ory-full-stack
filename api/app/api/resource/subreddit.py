from flask import request, abort, session
from flask_restful import Resource
from app.common import paginate
from app.api.schema import SubRedditSchema
from app.extensions import db
from app.models import SubReddit
from app.common import AccessControlMixin


class SubRedditResource(Resource, AccessControlMixin):
    def get(self, subreddit_id):
        schema = SubRedditSchema()
        subreddit = SubReddit.query.get_or_404(subreddit_id)
        return {"subreddit": schema.dump(subreddit)}

    def put(self, subreddit_id):
        user_id = session.get("user_id")
        if not self.is_allowed("groups", "admin", "member", user_id):
            return abort(403)

        schema = SubRedditSchema()
        subreddit = SubReddit.query.get_or_404(subreddit_id)
        subreddit = schema.load(request.json, instsance=subreddit)

        db.session.commit()

        return {"subreddit": schema.dump(subreddit)}

    def delete(self, subreddit_id):
        if not self.is_allowed("groups", "admin", "member", user_id):
            return abort(403)

        subreddit = SubReddit.get_by_id(subreddit_id)
        subreddit.delete()
        return None, 204


class SubRedditList(Resource):
    def get(self):
        schema = SubRedditSchema(many=True)
        query = SubReddit.query
        return paginate(query, schema)

    def post(self):
        if not self.is_allowed("groups", "admin", "member", user_id):
            return abort(403)

        schema = SubRedditSchema()
        subreddit = schema.load(request.json)
        subreddit.save()
        return {"subreddit": schema.dump(subreddit)}, 201

