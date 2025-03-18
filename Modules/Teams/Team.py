from mongoengine import Document, EmbeddedDocument, fields


class MatchStats(EmbeddedDocument):
    wins = fields.IntField(default=0)
    losses = fields.IntField(default=0)  
    draws = fields.IntField(default=0)
    total_goal_scored = fields.IntField(default=0)
    total_goal_suffered = fields.IntField(default=0)
    goal_difference = fields.IntField(default=0)

class PreviousMatch(EmbeddedDocument):
    opponent = fields.ReferenceField('Team')  
    result = fields.StringField(choices=['1', 'X', '2'])  

class Team(Document):
    tenant = fields.StringField(required=True)
    competition = fields.StringField(required=True)
    name = fields.StringField(required=True)
    current_position = fields.IntField(required=True)
    matches_stats = fields.EmbeddedDocumentField(MatchStats)
    next_match = fields.ReferenceField('Team')  
    previous_match = fields.EmbeddedDocumentField(PreviousMatch)



















