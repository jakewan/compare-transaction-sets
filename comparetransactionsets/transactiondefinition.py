from comparetransactionsets import parse_date


class TransactionDefinition:
    def __init__(self, series_name, series_config, outer_config):
        self.__series_name = series_name
        try:
            start_date = parse_date(series_config["startDate"])
        except KeyError:
            start_date = None
        self.__from_def = DefinitionPart(
            series_config["from"], outer_config, start_date
        )
        self.__to_def = DefinitionPart(series_config["to"], outer_config, start_date)

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
    def __init__(self, part_config, outer_config, start_date):
        view = outer_config["views"][part_config["view"]]
        view_profile = outer_config["viewProfiles"][view["profile"]]
        spreadsheet = outer_config["spreadsheets"][view_profile["spreadsheet"]]
        self.__spreadsheet_id = spreadsheet["spreadsheetId"]
        self.__sheet_name = view["sheet"]
        self.__range = view.get("range", None)
        if self.__range is None:
            self.__range = "A:I"
        self.__start_date = start_date
        self.__filter = []
        for i in range(2):
            try:
                value_config = part_config["filter"][i]
            except IndexError:
                value_config = ""

            self.__filter.append(
                {
                    "type": "columnName",
                    "columnName": view_profile["filter"][i],
                    "value": value_config,
                }
            )
        self.__date_column_name = view_profile["dateColumn"]
        self.__value_column_name = view["valueColumn"]

    def __repr__(self):
        return (
            "DefinitionPart("
            f"spreadsheet_id={self.__spreadsheet_id},"
            f"sheet_name={self.__sheet_name},"
            f"date_column={self.__date_column_name},"
            f"value_column={self.__value_column_name},"
            f"range={self.__range},"
            f"filter={self.__filter!r}),"
            f"start_date={self.__start_date!r}"
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

    @property
    def start_date(self):
        return self.__start_date
