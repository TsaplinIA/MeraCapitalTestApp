import re


def parse_duplicate_key_error(error_string: str) -> tuple[str, str, str]:
    # Split the error string into sections
    sections = error_string.split("\n")

    # Extract table name from the SQL statement
    sql_statement = sections[2]
    table_name_match = re.search(r'(?:UPDATE|INSERT INTO|DELETE FROM) (\w+)', sql_statement)
    if table_name_match:
        table_name = table_name_match.group(1)
    else:
        table_name = None

    # Extract column name and value from the DETAIL section
    detail_section = sections[1]
    column_name_match = re.search(r'Key \((.*?)\)=', detail_section)
    value_match = re.search(r'Key \(.*?\)=\((.*?)\)', detail_section)
    if column_name_match and value_match:
        column_name = column_name_match.group(1)
        value = value_match.group(1)
    else:
        column_name = None
        value = None

    return table_name, column_name, value
