from datetime import datetime
import pytz


def get_current_time():

    # Define the timezone for Sri Lanka
    sri_lanka_tz = pytz.timezone("Asia/Colombo")

    # Get the current time in Sri Lanka
    sri_lanka_time = datetime.now(sri_lanka_tz)

    # Format and print the date and time for Sri Lanka
    formatted_time = sri_lanka_time.strftime("%Y-%m-%d %I:%M:%S %p")
    return f"Current date and time in Hotel: {formatted_time} "
