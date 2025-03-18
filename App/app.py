import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from pymongo import MongoClient
from dotenv import load_dotenv
from mongoengine import connect
from flask_restx import Api, Resource, fields
from Modules.Teams.Team import Team  # Import the Team model

# Load environment variables from .env file
load_dotenv()

# Get the MongoDB URI from the environment variables
mongo_uri = os.getenv('MONGO_URI')

# Initialize the Flask application
app = Flask(__name__)

# Connect to MongoDB using mongoengine
connect(host=mongo_uri)

# Initialize Flask-RESTx
api = Api(app, version='1.0', title='Soccer AI API',
          description='API for accessing soccer team data',
          doc='/swagger')

# Create a namespace for teams
teams_ns = api.namespace('teams', description='Teams operations')

# Define the model for Swagger documentation
match_stats_model = api.model('MatchStats', {
    'wins': fields.Integer(description='Number of wins'),
    'losses': fields.Integer(description='Number of losses'),
    'draws': fields.Integer(description='Number of draws'),
    'total_goal_scored': fields.Integer(description='Total goals scored'),
    'total_goal_suffered': fields.Integer(description='Total goals suffered'),
    'goal_difference': fields.Integer(description='Goal difference')
})

previous_match_model = api.model('PreviousMatch', {
    'opponent': fields.String(description='Opponent team ID'),
    'result': fields.String(description='Match result (1, X, 2)')
})

team_model = api.model('Team', {
    'id': fields.String(description='Team ID'),
    'tenant': fields.String(description='Tenant identifier'),
    'competition': fields.String(description='Competition name'),
    'name': fields.String(description='Team name'),
    'current_position': fields.Integer(description='Current position in the league'),
    'matches_stats': fields.Nested(match_stats_model),
    'next_match': fields.String(description='Next match opponent ID'),
    'previous_match': fields.Nested(previous_match_model)
})

teams_response_model = api.model('TeamsResponse', {
    'teams': fields.List(fields.Nested(team_model))
})

@teams_ns.route('')
class TeamList(Resource):
    @teams_ns.doc('get_teams')
    @teams_ns.response(200, 'Success', teams_response_model)
    def get(self):
        """Get all teams"""
        teams = Team.objects()
        teams_list = []
        
        for team in teams:
            team_dict = team.to_mongo().to_dict()
            if '_id' in team_dict:
                team_dict['id'] = str(team_dict.pop('_id'))
            teams_list.append(team_dict)
            
        return {"teams": teams_list}

if __name__ == '__main__':
    app.run(debug=True)