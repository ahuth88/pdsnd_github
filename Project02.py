#!/usr/bin/env python
# coding: utf-8

# In[162]:


import math
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate


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

    # get user input for city (chicago, new york city, washington) and check for correct spelling
    city = input("Name the city you would like to analyse: ").lower()
    while city not in CITY_DATA:
        print("Sorry, this City is not supported. Please check your spelling and choose a supported city from the list below")
        for key, value in CITY_DATA.items():
            print (key.title())
        city = input("\nTry again and enter the city you would like to analyse: ").lower()

    # get user input for month (all, january, february, ... , june) and check for correct spelling
    months = ["all", "january", "february", "march", "april", "may", "june"]
    month = input("Which month would you like to analyse ('all' or between January and June): ").lower()
    while month not in months:
        print("Sorry, I didn´t get this. Please check your spelling and choose a month between January and June or type all.")
        month = input("Try again and enter the month (or all):")

    # get user input for day of week (all, monday, tuesday, ... sunday) and check for correct spelling
    days = ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    day = input("Which day of the week would you like to analyse ('all' or any day Monday to Sunday): ").lower()
    while day not in days:
        print("Sorry, I didn´t get this. Please check your spelling and choose a day between Monday and Sunday or type all for the entire week.")
        day = input("Try again and enter the day (or all):")

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
    df['day_of_week'] = df['Start Time'].dt.weekday

    # filter by month if applicable
    if month != 'all':

        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower()) + 1

        # filter by month to create the new dataframe
        df = df[df['month']==month]

    # filter by day of week if applicable
    if day != 'all':
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day.lower())

        # filter by day of week to c reate the new dataframe
        df = df[df['day_of_week']==day]

    return df



def time_stats(df, month, day):
    """
    Displays statistics on the most frequent times of travel.

    Args:
        (dataframe) df - pre-filtered dataframe
        (string) month - name of the filtered month
        (string) day - name of the filtered day

    returns:
        displays the most common month, day and start hour in discriptive sentences
        and additional graphics (bar charts) if month and/or day is set to 'all'.
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()


    #available attributes
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


    # determine the most common month with its name and total count of rentals in this month
    common_month = df['month'].mode()[0]
    name_month = months[common_month-1].title()
    count_month = df['month'].value_counts()[common_month]
    count_all_month = df['month'].value_counts()

    # in case month is not filtered (set to 'all') create bar chart
    if month == "all":

        print("The most common month for bike rentals (considering the filtered day(s): {}) is:\n\n{}, with total rentals of: {}.\n".format(day, name_month, count_month))

        bars_month=[]
        titles_month=[]

        #create data for bar chart
        for i in range(6):
            bars_month.append(count_all_month[i+1])
            titles_month.append(months[i].title())

        #show bar chart
        fig_month = plt.figure()
        ax = fig_month.add_axes([0,0,1,1])
        ax.bar(titles_month, bars_month)
        plt.xlabel('Month')
        plt.ylabel('Rentals')
        plt.title('Rentals per Month')
        plt.show()

    # if month is filtered return statistics for this month
    else:
        print("In {} {} rentals took place for the selected day(s)(in this case '{}'). To compare with other months restart and choose filter 'all'.\n".format(name_month, count_month, day.title()))


    # determine the most common day with its name and total count of rentals on this day
    common_day = df['day_of_week'].mode()[0]
    name_day = days[common_day].title()
    count_day = df['day_of_week'].value_counts()[common_day]
    count_all_day = df['day_of_week'].value_counts()

    # in case day is not filtered (set to 'all') create bar chart
    if day == "all":

        print("\nThe most common day for rentals in month(s) '{}' is {} with total rentals of {}.\n".format(month.title(), name_day, count_day))

        #create data for bar chart
        bars_day=[]
        titles_day=[]
        for x in range(7):
            titles_day.append(days[x].title())
        for y in range(7):
            bars_day.append(count_all_day[y])

        #show bar chart
        fig_day = plt.figure()
        ax = fig_day.add_axes([0,0,1,1])
        ax.bar(titles_day, bars_day)
        plt.xlabel('Day')
        plt.ylabel('Rentals')
        plt.title('Rentals per Day')

        plt.show()

    # if day is filtered return statistics for this day
    else:
        print("On all {}´s in month(s) '{}' {} rentals took place.\nTo compare with other days restart and choose 'all' as filter.\n".format(day.title(), month.title(), count_day))


    # create new column with hours pulled from 'Start Time'
    df['hour'] = df['Start Time'].dt.hour

    # determine and display most common rental hours
    common_hour = df['hour'].mode()[0]
    count_hour = df['hour'].value_counts()[common_hour]
    count_hour_all = df['hour'].value_counts().sort_index()
    count_hour_list = df['hour'].value_counts().keys().tolist()

    print("\nMost common hour for bike rentals and the selcted filters is: {} o'clock with {} rentals.".format(common_hour, count_hour))

    #create horizontal bar chart
    bars_hour = count_hour_all.tolist()
    titles_hour = count_hour_all.keys().tolist()
    y_pos = np.arange(len(titles_hour))
    plt.barh(y_pos, bars_hour, align='center', alpha=1)
    plt.yticks(y_pos, titles_hour)
    plt.xlabel('Rentals')
    plt.ylabel('Start Hour')
    plt.title('Rentals per Start Hour')

    plt.show()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.

    Args:
        (dataframe) df - pre-filtered dataframe

    Returns:
        Most common Start Station, End Station and combination of Start and End Station in discriptive sentences,
        as well as a top ten list of the most common combinations.
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print("\nThe most common start station is: {}.".format(common_start))

    # display most commonly used end station
    common_end = df['End Station'].mode()[0]

    print("\nThe most common end station is: {}.".format(common_end))

    # display most frequent combination of start station and end station trip
    # create sub data frame with pairing and grouping Start and End Station
    df_sub = df[["Start Station", "End Station"]]
    df_sub = df_sub.dropna()
    df_sub = df_sub.groupby(['Start Station','End Station']).size().reset_index().rename(columns={0:'Tours'})

    # sort sub data frame for creating top ten list
    df_sub = df_sub.sort_values(by='Tours', ascending=False).reset_index()

    #print results
    print("\nMost frequent combination of start-end station is '{}' to '{}' with in total {} tours, \nwhereas the top ten combinations can be found in the following:\n".format(df_sub["Start Station"][0], df_sub["End Station"][0], df_sub["Tours"][0]))
    print(df_sub.head(10))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def sec_to_h (sec):
    """
    Converts given amount of seconds into hours, minutes and seconds and returns three values (hours, minutes, seconds).

    Args:
        (int) sec - seconds as integer

    Returns:
        (int) hours, (int) minutes, (int) seconds
    """
    hours = int(sec / 3600)
    minutes = int((sec % 3600) / 60)
    seconds = int((sec % 3600) % 60)

    return hours, minutes, seconds



def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.

    Args:
        df - pre filtered data frame

    Returns:
        Discriptive sentences with the sum of trips, the average duration and the longest trip in hours, minutes and seconds.
        Additional a histogram is plotted showing the distribution of trips in minutes.
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travel_total = df['Trip Duration'].sum()

    print("\nThe total travel time is {} hours {} minutes and {} seconds.".format(sec_to_h(travel_total)[0], sec_to_h(travel_total)[1], sec_to_h(travel_total)[2]))

    # display mean travel time
    travel_mean = round(df['Trip Duration'].mean(), 4) 

    print("\nThe mean trip duration is exactly {} seconds or in other words around {} hours {} minutes and {} seconds.".format(travel_mean, sec_to_h(int(travel_mean))[0], sec_to_h(int(travel_mean))[1], sec_to_h(int(travel_mean))[2]))

    # display max travel time
    travel_max = df['Trip Duration'].max()

    print("\nThe longest trip took {} hours {} minutes and {} seconds.\n".format(sec_to_h(travel_max)[0], sec_to_h(travel_max)[1], sec_to_h(travel_max)[2]))

    # create and display a histogram for trips in min
    print("The distribution of trip duration can be seen in the following histogram. Please mind that all trips greater 2 hours are capped to 2 hours (120 min).\n")

    trip_in_min = []
    tripmin = 0
    for trip in df['Trip Duration']:
        #cap all trips longer than 120 min to 120 min (for reason of visualization)
        if (trip/60)> 120:
            tripmin = 120
        else:
            tripmin = int(trip/60)
        trip_in_min.append(tripmin)

    bins = np.linspace(math.ceil(min(trip_in_min)), math.floor(max(trip_in_min)), 50) # fixed number of bins
    plt.xlim([min(trip_in_min)-5, max(trip_in_min)+5])
    plt.hist(trip_in_min, bins=bins, alpha=0.5)
    plt.title('Distribution of trips in minutes')
    plt.xlabel('minutes')
    plt.ylabel('count')

    plt.show()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def user_stats(df):
    """
    Displays statistics on bikeshare users.

    Args:
        df - pre filtered data frame

    Returns:
        a table with the statistics for the user profiles with preset attributes:
        User Type: Subscriber, Customer, Dependent
        Gender: Male, Female
        Birth Year: most recent, earliest and most common
        """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Count user types for pre-set attributes (set 0 if attribute not available)
    try:
        subscriber = df['User Type'].value_counts()["Subscriber"]
    except KeyError:
        subscriber = 0

    try:
        customer = df['User Type'].value_counts()["Customer"]
    except KeyError:
        customer = 0

    try:
        dependent = df['User Type'].value_counts()["Dependent"]
    except KeyError:
        dependent = 0

    # Count gender for pre-set attributes (set 'na' if attribute not available)
    try:
        male = df['Gender'].value_counts()["Male"]
    except KeyError:
        male = "na"

    try:
        female = df['Gender'].value_counts()["Female"]
    except KeyError:
        female = "na"

    # Determine earliest, most recent, and most common year of birth. if Birth Year is not avaliable return 'na'.
    try:
        birth_recent = int(df['Birth Year'].max())
        birth_earliest = int(df['Birth Year'].min())
        birth_common = int(df['Birth Year'].mode()[0])
    except KeyError:
        birth_recent = "na"
        birth_earliest = "na"
        birth_common = "na"

    #create data for table
    data = [["Subscriber", subscriber],
        ["Customer", customer],
        ["Dependent", dependent],
        ["Male", male], ["Female", female],
        ["Most recent Birth Year", birth_recent],
        ["Earliest Birth Year", birth_earliest],
        ["Most common Birth Year", birth_common]]

    #define header names for table
    col_names = ["User Info", "Count / Year"]

    #display table
    print("\nUser profile looks like in following table:\n")
    print(tabulate(data, headers=col_names, tablefmt="fancy_grid"))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def display_raw (df):
    """While loop to slice through raw data."""
    raw = input("\nDo you wish to see the raw data? Enter y (for yes) or n.\n")
    while raw.lower() != "n" and raw.lower() != "y":
        raw = input("\nI din´t get this. Please try again and enter y or n:")

    i = 0
    while raw.lower() == "y":
        print(df[i:i+5])
        raw = input("\nDo you wish to see the next lines of raw data? Enter y (for yes) or n.\n")
        i +=5



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        display_raw(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        while restart.lower() != "no" and raw.lower() != "yes":
            restart = input("\nI din´t get this. Pleas try again and enter yes or no:")
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
