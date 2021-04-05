class DiffSet:
    def __init__(self, series_defn):
        self.__series_defn = series_defn
        self.__mismatched_values = []
        self.__mismatched_widthdrawals = []
        self.__mismatched_deposits = []

    def __repr__(self) -> str:
        return f"DiffSet(series_name={self.__series_defn!r})"

    @property
    def series_name(self):
        return self.__series_defn.series_name

    @property
    def from_def(self):
        return self.__series_defn.from_def

    @property
    def to_def(self):
        return self.__series_defn.to_def

    @property
    def contains_mismatches(self):
        return (
            0 < len(self.__mismatched_values)
            or 0 < len(self.__mismatched_widthdrawals)
            or 0 < len(self.__mismatched_deposits)
        )

    @property
    def mismatched_values(self):
        return self.__mismatched_values

    @property
    def mismatched_withdrawals(self):
        return self.__mismatched_widthdrawals

    @property
    def mismatched_deposits(self):
        return self.__mismatched_deposits
