from io import StringIO
import os
from datetime import date
from databricks.sdk import WorkspaceClient

def write_file_to_delta_table(uploaded_file, table_name):

    if uploaded_file is not None:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        string_data = stringio.read()
        filename = uploaded_file.name
        todays_date = date.today()

        w = WorkspaceClient(host=os.getenv('DB_WORKSPACE_URL'), token=os.getenv('DB_WORKSPACE_TOKEN'))
        sql_query = f'INSERT INTO {table_name } VALUES ("{todays_date}-{filename}", "{string_data}", "{todays_date}","{filename}")'
        w.statement_execution.execute_statement(statement=sql_query, warehouse_id='e072e72d0a4864f2')


