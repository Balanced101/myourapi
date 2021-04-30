import json
import sqlite3


class DatabaseController:
    def __init__(self):
        self.db = None
        self.cursor = None
        try:
            self.db = sqlite3.connect('api_db.sqlite')
            self.db.row_factory = sqlite3.Row
            self.cursor = self.db.cursor()

        except sqlite3.Error:
            print("Error open db.\n")

    def __del__(self):
        self.db.close()

    def run_query(self, query_string, arguments):

        query_type = query_string.split(' ')[0].upper()

        if query_type == "INSERT":
            return self.run_insert(query_string, arguments)
        else:
            return self.run_select(query_string, arguments)

    def run_insert(self, query_string, arguments):
        try:
            self.cursor.execute(query_string, arguments)
            self.db.commit()

            return '{"results": ["Insert successful"]}'

        except sqlite3.OperationalError as e:
            return "{'sqlerror': '" + e.args[0] + "'}"

    def run_select(self, query_string, arguments):
        try:
            self.cursor.execute(query_string, arguments)

            query_result = self.cursor.fetchall()
            rows = []
            results = {'results': rows}
            for row in query_result:
                results['results'].append(dict(row))

            return json.dumps(results)

        except sqlite3.OperationalError as e:
            return "{'sqlerror': '" + e.args[0] + "'}"
