class MismatchedTransaction:
    def __init__(self, date, name, description, value):
        self.__date = date
        self.__name = name
        self.__description = description
        self.__value = value

    def __repr__(self):
        return (
            f"MismatchedTransaction("
            f"date={self.__date},"
            f"name={self.__name},"
            f"description={self.__description},"
            f"value={self.__value})"
        )

    @property
    def date(self):
        return self.__date

    @property
    def name(self):
        return self.__name

    @property
    def description(self):
        return self.__description

    @property
    def value(self):
        return self.__value
