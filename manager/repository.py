from sqlite3_wrapper import Wrapper as DatabaseWrapper
from datetime import datetime

class Repository:
    def __init__(self):
        self.database_path = "./simulations.db"
        self.table_name = "simulations"
        self.db_cols = {
            ["System_id", "TEXT"],
            ["Seed", "INTEGER"],
            ["N_planets", "INTEGER"],
            ["Condition", "TEXT"],  # no outer, has outer
            ["JSON", "BLOB"],
            ["Was_stable", "INTEGER"],  # 0, 1
            ["Instability_location", "INTEGER"],  # timestep
            ["Failed", "INTEGER"] # 0, 1
            ["Waiting", "INTEGER"], # 0, 1
            ["Creation_timestamp", "TEXT"],
            ["Finalization_timestamp", "TEXT"]
        }

        self.db = DatabaseWrapper(self.database_path, self.db_cols)

    def _create_database(self):
        self.db.generate_table(self.table_name)

    def write_initial_commits(self, sets: list[list[dict[str, str]]]) -> None:
        """
        Expected is,
        System_id
        Seed
        N_planets
        Condition
        JSON

        :param sets:
        :return:
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        for _set in sets:
            _set.extend(
                ["Was_stable", "-1"],
                ["Instability_location", "-1"],  # timestep
                ["Failed", "-1"]  # 0, 1
                ["Waiting", "1"],  # 0, 1
                ["Creation_timestamp", timestamp],
                ["Finalization_timestamp", " "]
            )

        self.db.write(self.table_name, sets)


