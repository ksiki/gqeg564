import json
from datetime import datetime

from django.db import transaction

from .models import Record


def process_json_file(file):
    try:
        data = json.load(file)
    except json.JSONDecodeError:
        return False, "JSON file isn't valid"

    if not isinstance(data, list):
        return False, "A list of JSON objects was expected"

    valid_records = []

    for index, item in enumerate(data):
        if "name" not in item or "date" not in item:
            return (
                False,
                f"Error in the #{index + 1} element: The 'name' or 'date' key is missing",
            )

        name = item.get("name")
        date_str = item.get("date")

        if not isinstance(name, str):
            return (
                False,
                f"Error in the #{index + 1} element: The 'name' key must be a string",
            )

        if len(name) >= 50:
            return (
                False,
                f"Error in the #{index + 1} element: Length of 'name' ({len(name)} sim.) exceeds the limit (less than 50)",
            )

        try:
            parsed_date = datetime.strptime(date_str, "%Y-%m-%d_%H:%M")
        except (ValueError, TypeError):
            return (
                False,
                f"Error in the #{index + 1} element: Invalid date format '{date_str}'. Expected YYYY-MM-DD_HH:MM",
            )
        valid_records.append(Record(name=name, date=parsed_date))

    if not valid_records:
        return False, "The JSON file is empty"

    try:
        with transaction.atomic():
            Record.objects.bulk_create(valid_records)

        return True, f"Successfully uploaded {len(valid_records)} records"

    except Exception as e:
        return False, f"Error when saving: {str(e)}"
