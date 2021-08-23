import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # : get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Would you like to see data for Chicago, New York, or Washington?').lower()
    while city not in ['chicago', 'new york', 'washington']:
        city = input('City Name is INVALID!, PLease Enter Again. \n Would you like to see data for Chicago, New York, or Washington?').lower()
                     

    # : get user input for month (all, january, february, ... , june)
    month = input('For Which Month Would You Like to Filter ? \n Enter All for no filter ').lower()
    while month not in MONTHS and month != 'all':
        month = input('Month Name is INVALID!, PLease Enter Again. \n For Which Month Would You Like to Filter ? \n Enter All for no filter ')

    # : get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('For Which Day Would You Like to Filter ? \n Enter All for no filter ').lower()
    while day not in DAYS and day != 'all':
            day = input('Day Name is INVALID!, PLease Enter Again. \n For Which Day Would You Like to Filter ? \n Enter All for no filter ')


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
    #load data
    df = pd.read_csv("{}.csv".format(city.replace(" ","_")))
    
    # Convert the Start and End Time columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    #Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name
    
    #Filter by month if applicable
    if month != 'all':
        #Use the index of the months list to get the corresponding index
        month = MONTHS.index(month) + 1

        #Filter by month to create the new dataframe
        df = df[df['month'] == month]

    #Filter by day of week if applicable
    if day != 'all':
        #Filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]



    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # : display the most common month
    Most_Frequent_month = df['month'].mode()[0]
    print(f"Most Frequent Month is: {MONTHS[Most_Frequent_month-1]} \n")

    # : display the most common day of week
    Most_Frequent_day = df['day_of_week'].mode()[0]
    print(f"Most Frequent Day is: {Most_Frequent_day} \n")

    
    # : display the most common start hour
    #Extract hour from the Start Time column to create hour column
    df['hour'] = df['Start Time'].dt.hour
    Most_Frequent_StartHour= df['hour'].mode()[0]
    print(f"Most Frequent Start Hour is: {Most_Frequent_StartHour} \n")



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # : display most commonly used start station
    Most_Frequent_StartStation = df['Start Station'].mode()[0]
    print(f"Most Frequent Start Station is: {Most_Frequent_StartStation} \n")


    # : display most commonly used end station
    Most_Frequent_EndStation = df['End Station'].mode()[0]
    print(f"Most Frequent End Station is: {Most_Frequent_EndStation} \n")


    # : display most frequent combination of start station and end station trip
    #create Start to End column
    df['Start To End'] = df['Start Station'].str.cat(df['End Station'], sep=' To ')
    Most_Frequent_StartANDEndStation = df['Start To End'].mode()[0]
    print(f"Most Frequent Combination of Start Station & End Etation is: {Most_Frequent_StartANDEndStation} \n")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # : display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f"Total Trip Duration is: {total_travel_time} Second(s) \n")



    # : display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f"Mean Trip Duration is: {mean_travel_time} Second(s) \n")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(city, df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # : Display counts of user types
    user_types_count = df['User Type'].value_counts()
    print(f"Count of User Types is: {user_types_count} \n")


    # : Display counts of gender
    if city != 'washington':
        gender_count = df['Gender'].value_counts()
        print(f"Count of User Gender is: {gender_count} \n")


    # : Display earliest, most recent, and most common year of birth
    if city != 'washington':
        earliest_birth_year = df['Birth Year'].min()
        print(f"Earliest Year of Birth: {earliest_birth_year} \n")
        most_recent_birth_year = df['Birth Year'].max()
        print(f"Most Recent Year of Birth: {most_recent_birth_year} \n")
        most_common_birth_year = df['Birth Year'].mode()[0]
        print(f"Most Common Year of Birth: {most_common_birth_year} \n")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_rowData(df):
    """
    Display raw data of the CSV files per user requests.
    """
    startLoc = 0
    ifDisplay = input("Do you want to see 5 raw data ?:   yes/no ").lower()
    if ifDisplay == 'yes':
        while startLoc+5 <= df.shape[0] - 1:
            print(df.iloc[startLoc:startLoc+5,:])
            startLoc += 5
            continueDisplay = input("Do you want to continue?:   yes/no ").lower()
            if continueDisplay != 'yes':
                break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(city, df)
        display_rowData(df)


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
