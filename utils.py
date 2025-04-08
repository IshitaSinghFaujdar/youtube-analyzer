import isodate

def convert_duration_to_minutes(duration):
    try:
        parsed_duration = isodate.parse_duration(duration)
        return parsed_duration.total_seconds() / 60
    except Exception:
        return 0
