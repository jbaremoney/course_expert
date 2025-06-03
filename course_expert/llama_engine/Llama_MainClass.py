from together import Together
import os
from dotenv import load_dotenv
import sqlite3
load_dotenv()


class MainClass:
    def __init__(self, user_prompt):
        self.user_prompt = user_prompt
        self.client = Together(api_key=os.getenv("TOGETHER_API_KEY"))
        self.context_required_bool = False
        self.context_required_list = []
        self.course_db_path = './data_cleaning/courseDatabase.db' #DON'T CHANGE UNLESS FILE STRUCTURE CHANGES
        self.sql_query = None
        self.context = None
        self.final_response = None

    @staticmethod
    def get_course_table_schema():
        return """
        Table: courses_table
        Columns:
          - code TEXT
          - name TEXT
          - description TEXT
          - credits TEXT
          - prerequisites TEXT
          - corequisites TEXT
          - offered TEXT
          - repeatable TEXT
        """

    def generate_sql_query(self):
        table_schema = self.get_course_table_schema()
        system_prompt = f"""
             You are a helpful assistant. The user wants to query a database with the following schema:
            {table_schema}
            Only generate a valid SQL statement (no additional text) that answers the user's question.
            Use correct table/column names. Use correct table/column names. Make sure your query is syntactically 
            correct for SQLite.
             If you cannot be certain, make an educated guess. I will be running your query and passing you the context
             you grab in order to help the user's question with context.

             The user may not input course names in the correct format, if they do not, infer what the course code 
             should be.
             The course codes are standard letter codes in ALL CAPS followed by 3 numbers. ie compsci 160 has the code
             CSCI 160
             """
        response = self.client.chat.completions.create(
            model="meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
            messages=[{"role": "system", "content": system_prompt},
                      {"role": "user", "content": self.user_prompt}],
        )

        self.sql_query = response.choices[0].message.content
        return self.sql_query

    def run_sql(self):

        print(self.course_db_path)
        conn = sqlite3.connect(self.course_db_path)
        cursor = conn.cursor()
        try:
            cursor.execute(self.sql_query)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            self.context = [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            self.context = f"SQL Error: {e}"
        finally:
            conn.close()
        return self.context



    def generate_final_response(self):
        if self.context:
            messages = [
                {"role": "system", "content": f"Answer this prompt: {self.user_prompt} ... END OF USER PROMPT."
                                              f"Here is thecontext you retrieved:"
                                              f" {self.context}"
                                              f"If there was an error in the query result, or you are unsure, tell the user"
                                              f" you don't know. "
                                              f"Don't answer any questions that aren't related to academics and advising"}
            ]
        else:
            messages = [
                {"role": "system", "content": f"Answer the user's prompt like an academic advisor. Do not answer "
                                              f"any questions not related to this. If the user is asking important"
                                              f"questions regarding classes, be sure to default to an academic advisor"
                                              f"and let user know that you are uncertain."}
            ]
        res = self.client.chat.completions.create(model="meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8", messages=messages)
        self.final_response = res.choices[0].message.content
        return self.final_response

    def run(self):
        self.generate_sql_query()
        self.run_sql()
        return self.generate_final_response()
