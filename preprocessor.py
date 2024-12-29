import re
import pandas as pd

def preprocess(data):

    pattern = r"(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2}\s?[APap][Mm]) - (.*)"

    matches = re.findall(pattern, data)

    if matches:
        df = pd.DataFrame(matches, columns=["Date", "Time", "Message"])
        print(df)
    else:
        print("No valid matches found.")


    df['Date'] = pd.to_datetime(df['Date'])

    df['Full_date'] = df['Date'].dt.date 
    df['Year'] = df['Date'].dt.year
    df['Month_name'] = df['Date'].dt.month_name()
    df['Month'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day
    df['Day_name'] = df['Date'].dt.day_name()
    df['Hour'] = df['Time'].str.extract(r'(\d{1,2}):')
    df['Minute'] = df['Time'].str.extract(r':(\d{2})')
    df['AM/PM'] = df['Time'].str.extract(r'(AM|PM)')

    df['Hour'] = df['Hour'].astype(int) # Convert str to int
    df['Minute'] = df['Minute'].astype(int) # Convert str to int

    period = []
    for hour, am_pm in zip(df['Hour'], df['AM/PM']):
        if hour == 12:
            next_hour = 1
        else:
            next_hour = hour + 1
        period.append(f"{hour}-{next_hour} {am_pm}")
        
    df['Period'] = period

    df.drop('Date', axis=1, inplace=True)

    users = []
    messages = []
    for msg in df['Message']:
        entry = re.split('([\w\W]+?):\s', msg) # patter fetch the user's message 
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('Group_notification')
            messages.append(entry[0])

    df['User'] = users
    df['Message'] = messages
    
    new_order = ["User", "Message", "Day", "Day_name","Month", "Month_name", "Year", "Full_date", "Time", "Hour", "Minute", "AM/PM", "Period"]
    df = df[new_order]

    return df