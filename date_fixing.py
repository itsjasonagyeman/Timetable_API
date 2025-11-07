import pandas as pd

df = pd.read_excel('subjects.xlsx')
df['hour'] = pd.to_datetime(df['time']).dt.hour

data = pd.Series(df.time.values, index = df.name).to_dict()



hours = {hour: None for hour in range(24)}

week_schedule = {
    'Monday': hours.copy(),
    'Tuesday': hours.copy(),
    'Wednesday': hours.copy(),
    'Thursday': hours.copy(),
    'Friday': hours.copy(),
    'Saturday': hours.copy(),
    'Sunday': hours.copy(),
}

for _, row in df.iterrows():
    day = row['day']         
    hour = row['hour']  
    name = row['name']        

    if day in week_schedule and 0 <= hour < 24:
        week_schedule[day][hour] = name

print(week_schedule)