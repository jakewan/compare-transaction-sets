class TransactionDirection:
    def __init__(self, from_or_to, defn):
        assert from_or_to in ["from", "to"]
        self.__from_or_to = from_or_to
        self.__defn = defn

    def get_left_date_column(self):
        if self.__from_or_to == "from":
            return self.__defn.from_def.date_column
        elif self.__from_or_to == "to":
            return self.__defn.to_def.date_column

    def get_right_date_column(self):
        if self.__from_or_to == "from":
            return self.__defn.to_def.date_column
        elif self.__from_or_to == "to":
            return self.__defn.from_def.date_column

    def get_left_column_name(self, idx):
        if self.__from_or_to == "from":
            return self.__defn.from_def.filter[idx]["columnName"]
        elif self.__from_or_to == "to":
            return self.__defn.to_def.filter[idx]["columnName"]

    def get_right_column_name(self, idx):
        if self.__from_or_to == "from":
            return self.__defn.to_def.filter[idx]["columnName"]
        elif self.__from_or_to == "to":
            return self.__defn.from_def.filter[idx]["columnName"]

    def get_left_value_column(self):
        if self.__from_or_to == "from":
            return self.__defn.from_def.value_column
        elif self.__from_or_to == "to":
            return self.__defn.to_def.value_column

    def get_right_value_column(self):
        if self.__from_or_to == "from":
            return self.__defn.to_def.value_column
        elif self.__from_or_to == "to":
            return self.__defn.from_def.value_column

    def _is_left_match(self, obj):
        if self.__from_or_to == "from":
            for i in range(1):
                col_name = self.__defn.from_def.filter[i]["columnName"]
                val = self.__defn.from_def.filter[i]["value"]
                if obj[col_name] != val:
                    return False
            return True
        for i in range(1):
            col_name = self.__defn.to_def.filter[i]["columnName"]
            val = self.__defn.to_def.filter[i]["value"]
            if obj[col_name] != val:
                return False
        return True

    def _is_right_match(self, obj):
        if self.__from_or_to == "from":
            for i in range(1):
                col_name = self.__defn.to_def.filter[i]["columnName"]
                val = self.__defn.to_def.filter[i]["value"]
                if obj[col_name] != val:
                    return False
            return True
        for i in range(1):
            col_name = self.__defn.from_def.filter[i]["columnName"]
            val = self.__defn.from_def.filter[i]["value"]
            if obj[col_name] != val:
                return False
        return True
