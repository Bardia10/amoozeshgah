from datetime import datetime, timedelta
from khayyam import JalaliDate 

def get_jalali(time,day:int,week_delta:int):
    # Get today's time, like give me the timestamp of today when the clock is 13:44
    now = datetime.now()
    today_time = now.replace(
        hour=time.hour,  # Extract the hour directly from the `time` object
        minute=time.minute,  # Extract the minute directly from the `time` object
        second=0, 
        microsecond=0
    )
    # Get today's day, like is it Tuesday or what, then convert it to a number when Saturday is 1 and Friday is 7
    today_day = (now.weekday() + 2) % 7 + 1  # Adjust to make Saturday = 1 and Friday = 7

    # Timestamp + day delta to get this week day time
    target_day_timestamp = today_time + timedelta(days=(day - today_day))

    # Timestamp + delta week to get the actual timestamp
    final_timestamp = target_day_timestamp + timedelta(weeks=week_delta)

    # Convert to Jalali date
    jalali_date = JalaliDate(final_timestamp)

    # Format the Jalali date as yyyy/mm/dd
    formatted_jalali_date = f"{jalali_date.year}/{jalali_date.month:02}/{jalali_date.day:02}"
    return {"jalali":formatted_jalali_date,"timestamp":final_timestamp}
