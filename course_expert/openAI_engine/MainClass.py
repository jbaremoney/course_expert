from dotenv import load_dotenv
load_dotenv()
import os
from openai import OpenAI
import sqlite3

class Advisor:
    def __init__(self, user_prompt: str):
        self.user_prompt = user_prompt

        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.schema = self.get_table_schema()
        self.sql_query = None
        self.context = None
        self.final_response = None
        self.course_db_path = './data_cleaning/courseDatabase.db' #DON'T CHANGE UNLESS FILE STRUCTURE CHANGES

    def get_table_schema(self):
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
        table_schema = self.get_table_schema()
        system_prompt = f"""
             You are a helpful assistant. The user wants to query a database with the following schema:
            {table_schema}
            Only generate a valid SQL statement (no additional text) that answers the user's question.
            Use correct table/column names. Use correct table/column names. Make sure your query is syntactically correct for SQLite.
             If you cannot be certain, make an educated guess. I will be running your query and passing you the context
             you grab in order to help the user's question with context.

             The user may not input course names in the correct format, if they do not, infer what the course code should be.
             The course codes are standard 4 letter codes in ALL CAPS followed by 3 numbers. ie compsci 160 has the code CSCI 160
             """
        res = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": system_prompt},
                      {"role": "user", "content": self.user_prompt}],
            temperature=0
        )
        self.sql_query = res.choices[0].message.content
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
        messages = [
            {"role": "system", "content": f"You generated an sql query based on this prompt: {self.user_prompt} .... "
                                          f"Answer like an academic advisor given this context you retrieved: {self.context}"
                                          f"If there was an error in the query result, or you are unsure, tell the user you don't know. "
                                          f"Don't answer any questions that aren't related to academia"}
        ]
        res = self.client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
        self.final_response = res.choices[0].message.content
        return self.final_response

    def run(self):
        self.generate_sql_query()
        self.run_sql()
        return self.generate_final_response()

    def debugRun(self):
        query = self.generate_sql_query()
        context = self.run_sql()

        print(f"QUERY: {query}")
        print(f"CONTEXT: {context}")

        return self.generate_final_response()

user_prompt= 'What classes do I have to take before math 442?'
convo = Advisor(user_prompt)

sql_query = convo.generate_sql_query()
print(f"Generated query: {sql_query}")

context = convo.run_sql()
print(f"Generated context: {context}")

response = convo.run()
print(f"RESPONSE: {response}")