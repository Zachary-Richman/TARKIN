import sqlite3

class Wrapper:
    def __init__(self, path):
        self.database_path = path
        self.connection = sqlite3.connect(self.database_path)

    def _generate_table(self, table_name, cols: dict[str, str]):
        """

        :param table_name:
        :param cols: dict[name, type + any init configurations (e.g., PRIMARY KEY)]
        :return:
        """
        if not cols: return ValueError("Must have at least one column.")

        cursor = self.connection.cursor()

        column_definitions = ", ".join(
            f"{name} {definition}"
            for name, definition in cols.items()
        )

        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_definitions})"
        cursor.execute(query)

