# This is the flask application running the API which has endpoints for the CRUD operations
# in our Todo-list.
from flask import Flask, g, request, jsonify
import sqlite3

DATABASE = 'todolist.db'

app = Flask(__name__)
app.config.from_object(__name__)

@app.route("/api/items")
def get_items():
    db = get_db()
    cur = db.execute('SELECT what_to_do, due_date, status FROM entries')
    entries = cur.fetchall()
    tdlist = [dict(what_to_do=row[0], due_date=row[1], status=row[2]) for row in entries]
    return jsonify(tdlist)


@app.route("/api/mark", methods=['PUT'])
def mark_as_done():
    item = request.json.get('item')
    query = "UPDATE entries SET status='done' WHERE what_to_do='"+item+"'"
    db = get_db()
    db.execute(query)
    db.commit()
    resp = jsonify(success=True)
    return resp

@app.route("/api/delete", methods=['DELETE'])
def delete_entry():
    item = request.json.get('item')
    db = get_db()
    db.execute("DELETE FROM entries WHERE what_to_do='"+item+"'")
    db.commit()
    resp = jsonify(success=True)
    return resp

@app.route("/api/add", methods=['POST'])
def add_entry():
    data = request.json
    what_to_do = data.get('what_to_do')
    due_date = data.get('due_date')
    db = get_db()
    db.execute('insert into entries (what_to_do, due_date) values (?, ?)', [what_to_do, due_date])
    db.commit()
    resp = jsonify(success=True)
    return resp

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = sqlite3.connect(app.config['DATABASE'])
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)