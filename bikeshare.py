import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months_list = ['all','january', 'february', 'march', 'april', 'may', 'june']
dow_list = ['all', 'monday', 'tuesday','wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    try:
        city = input ("Please indicate which city you want to look at (chicago, new york city, washington): ").lower()
        while city not in CITY_DATA:
            city = input("Please indicate which city you want to look at (chicago, new york city, washington): ").lower()
    except ValueError:
        print("That is not valid input.")
    except KeyboardInterrupt:
        print("No input taken.")
    try:
        month = input ("Please indicate if you want to look at all the month (all) or a specific month (january, february, ... , june)").lower()
        while month not in months_list:
            month = input("Please indicate if you want to look at all the month (all) or a specific month (january, february, ... , june)").lower()
    except ValueError:
        print("That is not valid input.")
    except KeyboardInterrupt:
        print("No input taken.")
    try:
        day = input ("Please indicate if you want to look at the whole week (all) or a specific day of the week (monday, tuesday, ... sunday)").lower()
        while day not in dow_list:
            day = input("Please indicate if you want to look at the whole week (all) or a specific day of the week (monday, tuesday, ... sunday)").lower()
    except ValueError:
        print("That is not valid input.")
    except KeyboardInterrupt:
        print("No input taken.")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    month_mode = df['month'].mode()[0]

    print('Most common month:', month_mode)
    dow_mode = df['day_of_week'].mode()[0]

    print('Most common day of week:', dow_mode)
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]

    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    st_station_mode = df['Start Station'].mode()[0]

    print('Most common start station:', st_station_mode)
    end_station_mode = df['End Station'].mode()[0]

    print('Most common end station:', end_station_mode)
    df['Start End'] = df['Start Station'].map(str) + ' & ' + df['End Station']
    popular_start_end = df['Start End'].value_counts().idxmax()

    print('Most common combination of start station and end station trip:\n',popular_start_end)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    sum_traveltime_sec = df['Trip Duration'].sum()
    sum_traveltime_min = sum_traveltime_sec/60
    sum_traveltime_hrs = sum_traveltime_min/60
    print('Total travel time (in seconds):', sum_traveltime_sec)
    print('Total travel time (in minutes):', sum_traveltime_min)
    print('Total travel time (in hours):', sum_traveltime_hrs)
    mean_traveltime_sec = df['Trip Duration'].mean()
    mean_traveltime_min = mean_traveltime_sec/60
    print('Mean travel time (in seconds):', mean_traveltime_sec)
    print('Mean travel time (in minutes):', mean_traveltime_min)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    ct_users = df['User Type'].value_counts()
    print('Count of user types:', ct_users)

    while True:
        try:
            #display counts of gender
            ct_gender = df['Gender'].value_counts()
            print('Count of gender:', ct_gender)
            #display earliest, most recent, and most common year of birth
            min_birth_year = df['Birth Year'].min()
            max_birth_year = df['Birth Year'].max()
            mode_birth_year = df['Birth Year'].mode()[0]
            print('Earliest year of birth:', min_birth_year)
            print('Most recent year of birth:', max_birth_year)
            print('Most common year of birth:', mode_birth_year)
            break
        except KeyError:
            print("\nUnfortunately, for Washington there is no data covering gender and year of birth.")
            break
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        raw_data_look = input('\nWould you like to see five rows of the raw data? Enter yes or no.\n').lower()
        start_loc = 0
        end_loc = 4
        while (raw_data_look == 'yes'):
            print(df.iloc[start_loc:end_loc])
            start_loc += 5
            end_loc += 5
            raw_data_look = input("Do you wish to continue?: ").lower()


if __name__ == "__main__":
	main()
