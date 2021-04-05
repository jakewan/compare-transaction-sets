class TransactionDefinition:
    def __init__(self, defn_config) -> None:
        self.__series_name = defn_config["name"]
        self.__from_def = DefinitionPart(defn_config["from"])
        self.__to_def = DefinitionPart(defn_config["to"])

    def __repr__(self):
        return f"TransactionDefinition(from={self.__from_def!r},to={self.__to_def!r})"

    @property
    def from_def(self):
        return self.__from_def

    @property
    def to_def(self):
        return self.__to_def

    @property
    def series_name(self):
        return self.__series_name


class DefinitionPart:
    def __init__(self, part_config):
        self.__spreadsheet_id = part_config["spreadsheetId"]
        self.__sheet_name = part_config["sheetName"]
        self.__range = part_config.get("range", None)
        if self.__range is None:
            self.__range = "A:I"
        self.__filter = []
        f = part_config["filter"]
        for i in range(2):
            self.__filter.append(
                {
                    "type": "columnName",
                    "columnName": f["names"][i],
                    "value": f["values"][i],
                }
            )
        self.__date_column_name = part_config["dateColumn"]
        self.__value_column_name = part_config["valueColumn"]

    def __repr__(self):
        return (
            "DefinitionPart("
            f"spreadsheet_id={self.__spreadsheet_id},"
            f"sheet_name={self.__sheet_name},"
            f"date_column={self.__date_column_name},"
            f"value_column={self.__value_column_name},"
            f"range={self.__range},"
            f"filter={self.__filter!r})"
        )

    @property
    def spreadsheet_id(self):
        return self.__spreadsheet_id

    @property
    def sheet_name(self):
        return self.__sheet_name

    @property
    def range(self):
        return self.__range

    @property
    def filter(self):
        return self.__filter

    @property
    def date_column(self):
        return self.__date_column_name

    @property
    def value_column(self):
        return self.__value_column_name
