from datetime import datetime, timedelta

def format_date(date_obj):
    return date_obj.strftime('%m/%d/%Y')

end_date = datetime.strptime('2024-09-08', '%Y-%m-%d')
start_date = datetime.strptime('2024-09-01', '%Y-%m-%d')

# Iterate from start_date to end_date, one day at a time
current_date = end_date
i=0
while current_date >= start_date:
    # Convert the date to the required format (mm/dd/yyyy)
    formatted_date = format_date(current_date)
    # Move to the previous day
    prev_day = current_date - timedelta(days=2)
    next_formatted_date = format_date(prev_day)
    print(f'Min date: {next_formatted_date}      max date: {formatted_date}')
    # Construct the URL for the Google search

    url = f'https://www.google.com/search?q=RealEstate+reddit&tbs=cdr:1,cd_min:{next_formatted_date},cd_max:{formatted_date}&as_sitesearch=reddit.com/r/RealEstate/'
    print(url)
    print()
    current_date = prev_day