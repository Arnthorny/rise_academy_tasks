"""
TODO/Cache Service class
"""

from psycopg2.extras import RealDictCursor


class Cache:
    def __init__(self, redis_db):
        self._r = redis_db

        self._expire = 15 * 60 # Expire in 15mins


    def set(self, key: str, value: dict):
        success = self._r.hset(f"{key}", mapping=value)

        self._r.hexpire(key, self._expire, "id", "title", "description")

        return success

    def get(self, key):
        val = self._r.hgetall(f"{key}")

        if val:
            return val

        return None

    def delete(self, key):
        self._r.delete(key)


class TODO:
    def __init__(self, redis_db, postgres_db):
        self._pg = postgres_db
        self._cache = Cache(redis_db)
        self._valid_todo_fields = ["id", "title", "description"]



    def init_start(self):
        # Create table
        cur = self._pg.cursor()

        cur.execute("CREATE TABLE IF NOT EXISTS todos (\
                    id SERIAL PRIMARY KEY,\
                    title VARCHAR NOT NULL,\
                    description VARCHAR NOT NULL);")

        self._pg.commit()
        cur.close()


    def create_todo(self, body: dict):
        cur = self._pg.cursor()
        title, description = body.values()

        if not title or not description:
            raise Exception("`title` and `description` must be given.")

        cur.execute("INSERT INTO todos (title, description) VALUES (%s, %s)\
                    RETURNING id", (title, description))

        new_id = cur.fetchone()[0]

        new_obj = body.copy()
        new_obj['id'] = new_id

        cache_key = f"todo-{new_id}"

        self._cache.set(cache_key, new_obj)

        self._pg.commit()
        cur.close()

        return new_obj


    def get_all_todos(self):
        cur_dict = self._pg.cursor(cursor_factory=RealDictCursor)
        cur_dict.execute(f"SELECT * FROM todos;")

        all_todos = cur_dict.fetchall()

        all_todos = list(map(dict, all_todos))

        cur_dict.close()
        return all_todos

    def get_todo(self, todo_id: str):
        cache_key = f"todo-{todo_id}"

        todo = self._cache.get(cache_key)
        if todo:
            return todo

        cur_dict = self._pg.cursor(cursor_factory=RealDictCursor)

        cur_dict.execute("SELECT * FROM todos WHERE id=%s", (todo_id, ))

        todo_res = cur_dict.fetchone()

        cur_dict.close()
        if todo_res:
            tmp = dict(todo_res)
            self._cache.set(cache_key, tmp)
            return tmp

        return None

    def update_todo(self, todo_id: str, update_body: dict):
        cache_key = f"todo-{todo_id}"
        todo = self.get_todo(todo_id)

        if todo is None:
            return None

        new_todo = todo.copy()
        new_todo.update(update_body)


        cur = self._pg.cursor()
        cur.execute("UPDATE todos SET title = %s, description = %s WHERE id =\
                    %s", (new_todo['title'], new_todo['description'], todo_id))


        self._pg.commit()
        new_todo['id'] = todo_id
        new_todo_filtered = {key: new_todo[key] for key in
                             self._valid_todo_fields}


        self._cache.set(cache_key, new_todo_filtered)
        return new_todo_filtered

    def delete_todo(self, todo_id: str):
        cache_key = f"todo-{todo_id}"
        todo = self.get_todo(todo_id)

        if todo is None:
            return None

        cur = self._pg.cursor()
        cur.execute("DELETE FROM todos WHERE id=%s", (todo_id,))

        self._pg.commit()
        self._cache.delete(cache_key)


    def destroy(self):
        self._pg.close()
