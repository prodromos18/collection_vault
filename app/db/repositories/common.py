OP_MAPPING = {
    "eq": lambda column, value: column == value,
    "gte": lambda column, value: column >= value,
    "lte": lambda column, value: column <= value,
    "contains": lambda column, value: column.contains(value),
}