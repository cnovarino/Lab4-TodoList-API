from flask_cors import CORS

from helper import (add_to_list, delete_item,
                    update_status, get_item, get_all_items, start_db)
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
api = Api(app)

# Parser
parser = reqparse.RequestParser()
parser.add_argument('task')
parser.add_argument('completed')


def abort_if_todo_doesnt_exist(todo_id):
    abort(404, message="Todo {} doesn't exist".format(todo_id))


# Makeing first URL
@app.route('/')
def hello_world():
    return 'Api Restful <b>(Really!)</b>'


# Todo
# shows a single todo item and lets you delete/delete a todo item
class Todo(Resource):
    def get(self, todo_id):
        item = get_item(todo_id)
        if not item:
            abort_if_todo_doesnt_exist(todo_id)
        return item

    def delete(self, todo_id):
        item = get_item(todo_id)
        if not item:
            abort_if_todo_doesnt_exist(todo_id)
        delete_item(todo_id)
        return get_all_items()

    def put(self, todo_id):
        item = get_item(todo_id)
        if not item:
            abort_if_todo_doesnt_exist(todo_id)
        args = parser.parse_args()
        status = args.get('completed')
        if status and update_status(todo_id, status):
            item = get_item(todo_id)
            return item
        return {'Fail': 'No status Parse. Please, use one of {}'}


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        return get_all_items()

    def post(self):
        args = parser.parse_args()
        add_to_list(args.get('task'))
        return get_all_items()


##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/api/todos')
api.add_resource(Todo, '/api/todos/<todo_id>')

if __name__ == '__main__':
    start_db()
    app.run(debug=True, port=5001)
