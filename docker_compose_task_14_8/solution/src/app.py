"""
Simple TODO API
"""

from bottle import Bottle, request, response, Response
import json
from todoservice import TODO
from os import environ
from sys import exit
import redis
import psycopg2
from sys import stderr


TODO_S = None
app = Bottle()



@app.get("/")
def say_hello():
    response.set_header("Content-Type", "application/json")
    json_str = json.dumps({"message": "oh hai de"})

    return json_str


@app.post("/todos")
def create_todo():
    response.set_header("Content-Type", "application/json")
    json_body = request.json
    try:
        todo = TODO_S.create_todo(json_body)
    except Exception as e:
        response.status = 500
        return json.dumps({"error": str(e)})

    response.status = 200
    return json.dumps(todo)


@app.get("/todos")
def get_all_todos():
    response.set_header("Content-Type", "application/json")
    all_todos = TODO_S.get_all_todos()

    return json.dumps(all_todos)


@app.get("/todos/<todo_id>")
def get_single_todo(todo_id: str):
    response.set_header("Content-Type", "application/json")
    todo = TODO_S.get_todo(todo_id)

    if todo is None:
        response.status = 404
        return json.dumps({error: "todo not found"})

    return json.dumps(todo)


@app.patch("/todos/<todo_id>")
def update_todo(todo_id: str):
    response.set_header("Content-Type", "application/json")
    json_body = request.json
    todo = TODO_S.update_todo(todo_id, json_body)

    if todo is None:
        response.status = 404
        return json.dumps({error: "todo not found"})

    return json.dumps(todo)

@app.delete("/todos/<todo_id>")
def delete_todo(todo_id: str):
    response.set_header("Content-Type", "application/json")
    res = TODO_S.delete_todo(todo_id)

    if todo is None:
        response.status = 404
        return json.dumps({error: "todo not found"})
    return json.dumps(res)


def main():
    global TODO_S

    redis_url = None
    postgres_url = None
    try:
        redis_url = environ["REDIS_URL"]
        postgres_db = environ["POSTGRES_DB"]
        postgres_pw = environ["POSTGRES_PASSWORD"]
        postgres_user = environ["POSTGRES_USER"]
        postgres_host = environ["POSTGRES_HOST"]

    except KeyError:
        print("Expected REDIS_URL/POSTGRES_URLs to be set. Exiting.")
        sys.exit(1)


    r = redis.Redis(host=redis_url, decode_responses=True)
    pg = psycopg2.connect(dbname=postgres_db, user=postgres_user,
                          password=postgres_pw, host=postgres_host)

    TODO_S = TODO(redis_db=r, postgres_db=pg)
    TODO_S.init_start()

    app.run(host="0.0.0.0", port=8080, debug=True)


if __name__ == '__main__':
    main()
