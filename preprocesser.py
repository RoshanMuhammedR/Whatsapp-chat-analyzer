import re
import pandas as pd


def preprocess(data):
    pattern = re.compile(r'(\d{2}/\d{2}/\d{2},\s\d{1,2}:\d{2}\s[APMapm]{2}\s-\s)(.*)') #re pattern
    matches = pattern.findall(data)

    dates = []
    messages = []

    for match in matches:
        date_time_part, msg_part = match
        temp_date = f"{date_time_part.strip()}"
        temp_date = temp_date.replace("\u202f", "")
        temp_msg = f"{msg_part.strip()}"
        dates.append(temp_date)
        messages.append(temp_msg)

    #creating dataframe

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    # convert message_date type
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M%p -')

    df.rename(columns={'message_date': 'date'}, inplace=True)

    #seperating users and msg

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)


    #spliting date and time.

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    df.sort_values(by='hour', inplace=True)

    return df
