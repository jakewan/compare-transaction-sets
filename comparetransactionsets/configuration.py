from comparetransactionsets.transactiondefinition import TransactionDefinition


class Configuration:
    def __init__(self, raw_dict):
        self.__series_defs = []
        for series_name, series_config in raw_dict["series"].items():
            self.__series_defs.append(
                TransactionDefinition(series_name, series_config, raw_dict)
            )

    @property
    def series_defs(self):
        return self.__series_defs
