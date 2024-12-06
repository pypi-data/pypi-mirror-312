import argparse
import logging
from datetime import datetime, timedelta
from math import atan2, cos, radians, sin, sqrt

import pandas as pd
from pytz import all_timezones, timezone
from timezonefinder import TimezoneFinder

logger = logging.getLogger(__name__)

command_description = """
Investigate suspicious timezone changes and provide transposed times,
countries, and travel feasibility.
"""
long_description = """
Investigate suspicious timezone changes and provide contextual analysis like
countries in the given timezone, or a comparisons between local time
under each location before and after the change. It is possible to
provide a speed travel and to see if changes are physically possible.
"""


def add_arguments(parser):
    """
    Adds the argument options to the extract command parser.
    """
    parser.formatter_class = argparse.RawTextHelpFormatter
    parser.description = long_description

    parser.add_argument(
        "--file",
        type=str,
        default="inspect_results_changes.csv",
        help="Path to the CSV file containing suspicious changes (from `inspect`).",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="investigate_results.csv",
        help="Path to save the investigation results.",
    )
    parser.add_argument(
        "--speed",
        type=int,
        default=900,
        help="Average transport speed in km/h (default: 900 for flights).",
    )


def get_coordinates_from_timezone_offset(offset):
    """
    Retrieve representative coordinates (latitude, longitude) for a given timezone offset.

    Args:
        offset (str): Timezone offset in the format "+0800", "-0500", etc.

    Returns:
        tuple: Coordinates (latitude, longitude) for a typical location in the timezone.
    """
    # Initialize TimezoneFinder
    tz_finder = TimezoneFinder()

    # Normalize offset to hours and minutes
    offset_hours = int(offset[:3])
    offset_minutes = int(offset[0] + offset[3:])
    offset_total_minutes = offset_hours * 60 + offset_minutes

    # Current UTC time for determining timezone
    now_utc = datetime.utcnow()

    # Iterate through all timezones to match the offset
    for tz_name in all_timezones:
        tz = timezone(tz_name)
        local_time = now_utc.astimezone(tz)
        tz_offset_minutes = local_time.utcoffset().total_seconds() / 60

        if tz_offset_minutes == offset_total_minutes:
            # Get the first matching timezone and find its center
            coordinates = tz_finder.timezone_at(lat=0, lng=0)  # Placeholder
            if coordinates:
                return coordinates

    return None  # Return None if no match is found


def calculate_local_time(utc_date, timezone_offset):
    """
    Calculate the local time for a given UTC date and timezone offset.

    Args:
        utc_date (str): UTC date in string format.
        timezone_offset (str): Timezone offset in the format "+0100" or "-0500".

    Returns:
        str: Local time as a string.
    """

    # Parse UTC date
    utc_datetime = datetime.strptime(utc_date, "%Y-%m-%d %H:%M:%S")

    # Convert timezone offset to hours and minutes
    offset_hours = int(timezone_offset[:3])
    offset_minutes = int(
        timezone_offset[0] + timezone_offset[3:]
    )  # Handle negative offsets

    # Calculate local time
    local_datetime = utc_datetime + timedelta(
        hours=offset_hours, minutes=offset_minutes
    )
    return local_datetime.strftime("%Y-%m-%d %H:%M:%S")


def calculate_transposed_time(utc_date, source_offset, target_offset):
    """
    Calculate the time in a target timezone based on a source timezone's UTC date.

    Args:
        utc_date (str): UTC date in string format.
        source_offset (str): Source timezone offset in the format "+0100" or "-0500".
        target_offset (str): Target timezone offset in the format "+0100" or "-0500".

    Returns:
        str: Local time in the target timezone.
    """
    # Parse UTC date
    utc_datetime = datetime.strptime(utc_date, "%Y-%m-%d %H:%M:%S")

    # Calculate source offset in minutes
    source_hours = int(source_offset[:3])
    source_minutes = int(source_offset[0] + source_offset[3:])
    source_offset_minutes = source_hours * 60 + source_minutes

    # Calculate target offset in minutes
    target_hours = int(target_offset[:3])
    target_minutes = int(target_offset[0] + target_offset[3:])
    target_offset_minutes = target_hours * 60 + target_minutes

    # Calculate the difference between source and target offsets
    offset_difference_minutes = target_offset_minutes - source_offset_minutes

    # Adjust UTC date to the target timezone
    target_datetime = utc_datetime + timedelta(minutes=offset_difference_minutes)
    return target_datetime.strftime("%Y-%m-%d %H:%M:%S")


def find_countries_for_timezone(timezone_offset):
    """
    Find possible countries for a given timezone offset.

    Args:
        timezone_offset (str): Timezone offset in the format "+0100" or "-0500".
        tz_finder (TimezoneFinder): Instance of TimezoneFinder.

    Returns:
        list: List of country names.
    """
    offset_hours = int(timezone_offset[:3])
    offset_minutes = int(timezone_offset[0] + timezone_offset[3:])
    offset_total_minutes = offset_hours * 60 + offset_minutes

    # Current UTC time for comparison
    now_utc = datetime.utcnow()

    # Find all matching timezones
    matching_timezones = []
    for tz_name in all_timezones:
        tz = timezone(tz_name)
        local_time = now_utc.astimezone(tz)
        tz_offset_minutes = local_time.utcoffset().total_seconds() / 60
        if tz_offset_minutes == offset_total_minutes:
            matching_timezones.append(tz_name)

    # Extract countries/regions from timezone names
    countries = set()
    for tz_name in matching_timezones:
        try:
            country_or_region = tz_name.split("/")[
                0
            ]  # Example: "Europe/Berlin" -> "Europe"
            countries.add(country_or_region)
        except Exception:
            continue

    return list(countries)


def is_physically_possible(
    coord1,
    coord2,
    departure_time,
    arrival_time,
    source_offset,
    target_offset,
    transport_speed_kmh=900,
):
    """
    Determine if it is physically possible to travel between two coordinates in the given time.

    Args:
        coord1 (tuple): (latitude, longitude) of the departure location.
        coord2 (tuple): (latitude, longitude) of the arrival location.
        departure_time (str): Departure time in source timezone.
        arrival_time (str): Arrival time in target timezone.
        source_offset (str): Timezone offset of the departure location.
        target_offset (str): Timezone offset of the arrival location.
        transport_speed_kmh (int): Average speed of the transport (default: 900 km/h for flights).

    Returns:
        bool: True if the travel is physically possible, False otherwise.
    """

    def haversine_distance(coord1, coord2):
        R = 6371  # Earth's radius in kilometers
        lat1, lon1 = radians(coord1[0]), radians(coord1[1])
        lat2, lon2 = radians(coord2[0]), radians(coord2[1])

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        return R * c

    departure_utc = calculate_transposed_time(departure_time, source_offset, "+0000")
    arrival_utc = calculate_transposed_time(arrival_time, target_offset, "+0000")

    # Calculate duration available for travel in hours
    duration_seconds = (
        datetime.strptime(arrival_utc, "%Y-%m-%d %H:%M:%S")
        - datetime.strptime(departure_utc, "%Y-%m-%d %H:%M:%S")
    ).total_seconds()
    duration_hours = duration_seconds / 3600

    # Calculate distance and required time for travel
    distance_km = haversine_distance(coord1, coord2)
    required_time_hours = distance_km / transport_speed_kmh

    return duration_hours >= required_time_hours


def main(args):
    """
    Investigate suspicious timezone changes and provide transposed times,
    countries, and travel feasibility.
    """
    # Load the suspicious changes file
    df = pd.read_csv(
        args.file, dtype={"previous_timezone": str, "current_timezone": str}
    )

    # Filter only suspicious changes
    df = df[df["suspicious"] == True]

    # Prepare a list for storing results
    investigation_results = []

    for _, row in df.iterrows():
        # Extract the previous and current timezones
        previous_tz = row["previous_timezone"]
        current_tz = row["current_timezone"]

        # Calculate local times
        previous_local_time = calculate_local_time(row["previous_date"], previous_tz)
        current_local_time = calculate_local_time(row["current_date"], current_tz)

        # Calculate transposed times
        time_in_current_at_change = calculate_transposed_time(
            row["previous_date"], previous_tz, current_tz
        )
        time_in_previous_after_change = calculate_transposed_time(
            row["current_date"], current_tz, previous_tz
        )

        # Retrieve countries for timezones
        countries_previous = find_countries_for_timezone(previous_tz)
        countries_current = find_countries_for_timezone(current_tz)

        # Parse departure and arrival times into UTC
        departure_utc = calculate_transposed_time(
            row["previous_date"], previous_tz, "+0000"
        )
        arrival_utc = calculate_transposed_time(
            row["current_date"], current_tz, "+0000"
        )

        # Estimate coordinates (mock example, replace with actual coordinates lookup)
        coord_prev = (45.0, 90.0)  # Replace with actual lookup for `previous_tz`
        coord_curr = (50.0, 85.0)  # Replace with actual lookup for `current_tz`

        # Calculate time difference in hours
        time_difference_hours = (
            pd.to_datetime(row["current_date"]) - pd.to_datetime(row["previous_date"])
        ).total_seconds() / 3600

        # Check if travel is physically possible
        travel_feasibility = is_physically_possible(
            coord1=coord_prev,
            coord2=coord_curr,
            departure_time=departure_utc,
            arrival_time=arrival_utc,
            source_offset=previous_tz,
            target_offset=current_tz,
            transport_speed_kmh=args.speed,
        )

        # Append the investigation result
        previous_date = row["previous_date"]
        current_date = row["current_date"]
        investigation_results.append(
            {
                "date_of_change": previous_date,
                "previous_timezone": previous_tz,
                "countries_previous": ", ".join(countries_previous),
                "current_timezone": current_tz,
                "countries_current": ", ".join(countries_current),
                "departure": f"{previous_date} {previous_tz} (time at is {time_in_current_at_change} {current_tz})",
                "arrival": f"{current_date} {current_tz} (time at is {time_in_previous_after_change} {previous_tz})",
                "physically_possible": travel_feasibility,
            }
        )

    # Convert results to DataFrame
    investigation_df = pd.DataFrame(investigation_results)

    # Save to CSV
    investigation_df.to_csv(args.output, index=False)
    print(f"Investigation results saved to '{args.output}'.")
    print(investigation_df.head(5).to_string(index=False))
