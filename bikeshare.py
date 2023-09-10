import time
import pandas as pd
import numpy as np 

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city =input("Please enter the name of the city you want to analyze(Chicago, New York City, Washington):").lower()
        if city not in CITY_DATA:
          print("Sorry, I didn't catch that. Try again.")
        else:
             break

    # get user input for month (all, january, february, ... , june)
    months_list=['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        month = input("Please enter the month you want to filter by (all, january, february, ..., june) or 'all' to apply no month filter: ").lower()
        if month not in months_list:
         print("Sorry, I didn't catch that. Try again.")
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days_list=['sunday','monday','tuesday','wednesday','thursday','friday','saturday', 'all']
    while True:
        day = input("Please enter the day of the week you want to filter by (Monday, Tuesday, ..., Sunday) or 'all' to apply no day filter: ").lower()
        if day in days_list:
            break
        else:
            print("Invalid day of the week. Please try again.")
   
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
     # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

   # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the month list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month= df['month'].mode().values[0]
    print("The most common month is:", most_common_month)

    # display the most common day of week
    most_common_day_of_week= df['day_of_week'].mode().values[0]
    print("The most common day of the week is:", most_common_day_of_week)

    # display the most common start hour
    df['hour']= df['Start Time'].dt.hour
    most_common_start_hour= df['hour'].mode()[0]
    print("The most common start hour is:", most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station= df['Start Station'].value_counts().idxmax()
    print("The most common start station is:", most_common_start_station)

    # display most commonly used end station
    most_common_end_station= df['End Station'].value_counts().idxmax()
    print("The most common end station is:", most_common_end_station)

    # display most frequent combination of start station and end station trip
    combinations_group = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('The most frequent combination of Start Station and End Station trip is:', combinations_group)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()
    print('total travel time is:', total_duration )

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('mean travel time is:', mean_travel_time)
   
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User Types in Data are:', df['User Type'].value_counts())

    # Gender and birth year columns aren't in washington data, we have to ensure the city is not washington
    if CITY_DATA != 'washington':
        # Check if 'Gender' column exists before using it
        if 'Gender' in df.columns:
            print(df['Gender'].value_counts())
        else:
            print("Gender data not available in this dataset.")

        # Check if 'Birth Year' column exists before using it
        if 'Birth Year' in df.columns:
        # Display earliest, most recent, and most common year of birth
            earliest = df['Birth Year'].min() 
            print('earliest Birth Year: ', int(earliest))
            most_recent = df['Birth Year'].max() 
            print('most recent Birth Year: ', int(most_recent))
            most_common = df['Birth Year'].mode()[0]
            print('Most Common Birth Year: ', int(most_common))
        else:
            print("Birth Year data not available in this dataset.")
    else:
        print("Gender and Birth Year data not available for Washington.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# view raw data to user of choosed city
def display_data(df):  
    print('\nRaw data is available to check..\n')

    index=0
    user_input=input('would you like to desplay 5 rows of raw data?, please type yes or no').lower()
    if user_input not in ['yes','no']:
        print('That\'s invalid choise, please type yes or no...')
    elif user_input !='yes':
        print('Thank you')

    else:
        while index+5 < df.shape[0]:
            print(df.iloc[index:index+5])
            index += 5
            user_input= input('would you like to display more 5 rows of raw data?').lower()
            if user_input != 'yes':
                print('Thank you')
                break
            
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        if restart.lower() != 'yes':
            print('Thank you')
            break


if __name__ == "__main__":
	main()


