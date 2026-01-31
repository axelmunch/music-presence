def format_ordinal(value):
    if value % 100 in (11, 12, 13):
        return f"{value}th"

    match value % 10:
        case 1:
            return f"{value}st"
        case 2:
            return f"{value}nd"
        case 3:
            return f"{value}rd"
        case _:
            return f"{value}th"
