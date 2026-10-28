import sqlite3

class Wrapper:
    def __init__(self, path, cols):
        self.database_path = path
        self.connection = sqlite3.connect(self.database_path)
        self.table_cols: dict[str, str] = cols

    def generate_table(self, table_name):
        """

        :param table_name:
        :param cols: dict[name, type + any init configurations (e.g., PRIMARY KEY)]
        :return:
        """
        if not self.table_cols: return ValueError("Must have at least one column.")

        cursor = self.connection.cursor()

        column_definitions = ", ".join(
            f"{name} {definition}"
            for name, definition in self.table_cols.items()
        )

        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_definitions})"
        cursor.execute(query)

        return self.connection.close(), cursor.close()

    def write_row(self, table_name: str, row: dict[str, str]):
        cursor = self.connection.cursor()

        # properly construct the column placeholders and values list
        columns = ", ".join(row.keys())
        placeholders = ", ".join(["?"] * len(row))
        values = list(row.values())

        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        cursor.execute(query, values)

        self.connection.commit()
        cursor.close()

    def write_row_batch(self, table_name: str, rows: list[list[dict[str, str]]]):
        # gemini constructed, not yet reviewed
        if not rows or not rows[0]:
            return

        # 1. Reconstruct each row into a single consolidated dictionary
        # Transforms [[{"a": "1"}, {"b": "2"}]] into [{"a": "1", "b": "2"}]
        parsed_rows = []
        for row in rows:
            combined_row = {}
            for pair in row:
                combined_row.update(pair)
            parsed_rows.append(combined_row)

        cursor = self.connection.cursor()

        # 2. Extract column names from the first consolidated row
        columns = ", ".join(parsed_rows[0].keys())
        placeholders = ", ".join(["?"] * len(parsed_rows[0]))

        # 3. Ensure values are extracted in the exact order of the columns
        column_order = list(parsed_rows[0].keys())
        values = [tuple(row[col] for col in column_order) for row in parsed_rows]

        # 4. Execute the batch insert
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        cursor.executemany(query, values)

        self.connection.commit()
        cursor.close()




