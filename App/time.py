import datetime


def get_current_timestamp():
    # get current time
    current_datetime = datetime.datetime.now()

    # print  "dd/mm/yyyy"

    # formatted_date = current_datetime.strftime('%d/%m/%Y')
    # print("Current time:", formatted_date)

    # get time in timestamp format
    current_timestamp = current_datetime.timestamp()

    return current_timestamp


timestamp_value = get_current_timestamp()

print("Timestamp:", timestamp_value)
