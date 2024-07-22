from flask import Blueprint, request, Response
from .data.search_data import USERS
import json

bp = Blueprint("search", __name__, url_prefix="/search")

@bp.route("")
def search():
    return search_users(request.args.to_dict()), 200

def search_users(args):
    """Search users database

    Parameters:
        args: a dictionary containing the following search parameters:
            id: string
            name: string
            age: string
            occupation: string

    Returns:
        a list of users that match the search parameters
    """

    search_id = args.get('id')
    search_name = args.get('name')
    search_age = int(args.get('age'))
    search_occupation = args.get('occupation')

    def matches(user):
        if search_id and user.get('id') == search_id:
            return True
        if search_name and search_name.lower() in user.get('name', '').lower():
            return True
        if search_age and user.get('age'):
            # Check if user_age is equal to search_age or search_age + 1 or - 1
            if search_age in {search_age, search_age + 1, search_age - 1}:
                return True
        if search_occupation and search_occupation.lower() in user.get('occupation', '').lower():
            return True
        return False

    # BONUS CHALLENGE

    matched_users = [user for user in USERS if matches(user)]
    json_output = json.dumps(matched_users, indent=4)

    # new lines
    json_lines = json_output.split('\n')
    new_json_output = '\n'.join(json_lines)
    return Response(
        response=new_json_output,
        status=200,
        mimetype='application/json'
    )
