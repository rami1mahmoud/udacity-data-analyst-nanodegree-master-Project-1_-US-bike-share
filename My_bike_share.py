import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv', 'new york city': 'new_york_city.csv', 'washington': 'washington.csv' }
city_number, filter_type, month, day_number = 0, "", "",0
def get_filters():
    print('Hello, let\'s exploer bike share in the US \n')
    print("Which city do you like to see its data?\n")
    # getting city
    print(" "+"For Chicago press: 1 \n", "For New York press: 2 \n", "For Washington press: 3")
    while  True:
        city_number = int(input("I chose city: "))
        if city_number in [1, 2, 3]:
            break       
        print('Please enter a valid number for your city of choice.')   
    # getting filter type
    print("Would you like to filter data by month, day, both, or not at all? Type none for no time filter." )
    while  True:
        filter_type = input("I chose to filter by: \n").lower()
        if filter_type in ['month', 'day', 'both', 'none']:
            break       
        print('Please enter a valid choice to filter by.')  
    if filter_type == 'day':   
    # getting day   
        while  True:
            day_number = int(input("Ok, which day?  (e.g.  1 = Saturday)\n" ))
            if day_number in [1, 2, 3, 4, 5, 6, 7]:
                month = '0'
                break       
            print('Please enter a valid day number.')
    elif filter_type == 'month':
        while  True:
            month = str(input("Ok, which month? (Chose from January till June.)\n" ).lower())
            if month in ['january', 'february', 'march', 'april', 'may', 'june']:
                day_number = 0
                break       
            print('Please enter a valid choice for month.')
    elif filter_type == 'both':
        while  True:
            day_number = int(input("Ok, which day?  (e.g.  1 = Saturday)\n" ))
            if day_number in [1, 2, 3, 4, 5, 6, 7]:
                break       
            print('Please enter a valid day number.')
        while  True:
            month = str(input("Ok, which month? (Chose from January till June.)\n" ).lower())
            if month in ['january', 'february', 'march', 'april', 'may', 'june']:
                break       
            print('Please enter a valid choice for month.')
    elif  filter_type == 'none':
        month  = ''
        day_number = 0
        city_number = city_number
    print('--'*40)
    return city_number, filter_type, month, day_number
def load_data(city_number, filter_type, month, day_number): 
    days = {1:'Saturday', 2:'Sunday', 3:'Monday', 4:'Tuesday', 5:'Wednesday', 6:'Thursday', 7:'Friday'} 
    cal_data = pd.read_csv(list(CITY_DATA.values())[city_number - 1])
    if filter_type == 'month':
        cal_data = cal_data[pd.to_datetime(cal_data['Start Time']).dt.month_name()== month.title()].copy()        
    elif filter_type == 'day':
        cal_data = cal_data[pd.to_datetime(cal_data['Start Time']).dt.day_name() == days[day_number]].copy()   
    elif filter_type == 'both':
        cal_data = cal_data[(pd.to_datetime(cal_data['Start Time']).dt.month_name() == month.title()) & (pd.to_datetime(cal_data['Start Time']).dt.day_name()== days[day_number])].copy()     
    elif filter_type == 'none':
        cal_data = pd.read_csv(list(CITY_DATA.values())[city_number - 1])          
    return cal_data 

def time_stats(cal_data, filter_type):
    print('Calculating the first statistic ..............')
    cal_data['St_hour'] = pd.to_datetime(cal_data["Start Time"]).dt.hour
    start_time = time.time()
    print('Most popular hour: ', str(cal_data['St_hour'].mode()[0]), '        ', 'Count: ', str( (cal_data[cal_data['St_hour'] == cal_data['St_hour'].mode()[0]].shape)[0] ), '        Filter: ', filter_type)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('--'*40)

def station_stats(cal_data, filter_type):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip............\n')
    start_time = time.time()
    print('Start station:  ', str(cal_data['Start Station'].mode()[0]), '         Count:  ',  str( (cal_data[cal_data['Start Station'] == cal_data['Start Station'].mode()[0]].shape)[0] ))
    print('End staion: ', str(cal_data['End Station'].mode()[0]),  '         Count:  ',  str( (cal_data[cal_data['End Station'] == cal_data['End Station'].mode()[0]].shape)[0] ), '    Filter: ', filter_type )
    # display most frequent combination of start station and end station trip
    cal_data1 = cal_data.loc[(cal_data['Start Station'] == cal_data['Start Station'].mode()[0]) & (cal_data['End Station']==cal_data['End Station'].mode()[0])].copy()
    if cal_data1.shape[0] != 0:  
        print('\n The most popular combination between stations:\n ')  
        print('The combination is between, start station:  ', str(cal_data1['Start Station'].iloc[0]), '      and end station:  ', str(cal_data1['End Station'].iloc[0]), '    Count: ', str((cal_data1.shape)[0]) ,'  Filter:  ', filter_type)
        print("\nThis took %s seconds." % (time.time() - start_time))
    print('--'*40)

def trip_duration_stats(cal_data, filter_type):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
        # display total travel time
    print('Total duration: ', str(cal_data['Trip Duration'].sum(skipna=True)), '       Count: ',  str((cal_data['Trip Duration'].shape)[0]),'        Average duration: ', str(cal_data['Trip Duration'].mean(skipna=True)), '     Filter: ', filter_type)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('--'*40)

def user_stats(cal_data, filter_type):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()
        # Display counts of user types
    '''After checking the data, I find that both Chicago and New York has nan values in 'Gender' and 'Birth Year' columns.
        New York has also nan values in 'User Type' column
        Washington hasn't any nan values in its columns
    '''
    cal_data1 = cal_data[cal_data['User Type'].notna()].copy() # to get rows that is not nan
    print('Calculating user types statistics..........\n', 'Subscribers: ',str((cal_data1[(cal_data1['User Type']== 'Subscriber')].shape)[0]), '       Customers: ', str((cal_data1[cal_data1['User Type'] == 'Customer' ].shape)[0]), '      Filter: ', filter_type)
    if city_number in [1, 2]:
        # Display counts of gender
        cal_data2 = cal_data[cal_data['Gender'].notna()].copy() # to get rows that is not nan
        print('\nCalculating Gender statistics..........\n', 'Male: ',str((cal_data2[cal_data2['Gender'] == 'Male'].shape)[0]), '       Female: ', str((cal_data2[cal_data2['Gender'] == 'Female' ].shape)[0]), '      Filter: ', filter_type)
        # Display earliest, most recent, and most common year of birth
        cal_data3 = cal_data[cal_data['Birth Year'].notna()].copy() # to get rows that is not nan
        print('\nCalculating birth year statistics..........\n', 'Earliest year: ',str(cal_data3['Birth Year'].min()), '       Recent: ', str(cal_data3['Birth Year'].max()), '        Most common year: ', str(cal_data3['Birth Year'].mode()[0]),'      Filter: ', filter_type)
        print("\nThis took %s seconds." % (time.time() - start_time))
    print('--'*40)
        
def main():
    while True:
        #get_filters()
        city_number, filter_type, month, day_number = get_filters()
        df = load_data(city_number, filter_type, month, day_number)
        time_stats(df, filter_type)
        station_stats(df, filter_type)
        trip_duration_stats(df, filter_type)
        user_stats(df, filter_type)
        while True:   
            answer = str(input('Would you like to see a sample, that consists of five rows, of the users\' data? Please type yes or no. \n')).lower()
            if answer in ['yes', 'no']:
                if answer =='yes':
                    start, end = 0,0
                    while answer == 'yes' and end <= df.shape[0]:
                        end += 5
                        print(df.iloc[start:end-1].to_dict(orient='records'))
                        start = end
                        while  True:
                            answer = str(input('Would you like to see another sample of five rows? Type yes to continue or no to stop.\n')).lower()
                            if answer in ['yes', 'no']:
                                break
                            print('Please type yes or no only.')
                elif  answer == 'no':
                    print('thank you')
                break
            print('Please enter a valid answer only yes to continue or no to stop.')                       
        while True:
            restart = input('\nWould you like to restart to see another city? Enter yes or no.\n')
            if restart.lower() in ['yes', 'no']: 
                break   
            print ('Please type yes to see another city data or no to terminate.')
        if restart == 'no':
            print('Thank you.')
            break 
        else:
            continue
if  __name__ == "__main__":            
    main() 
                        
#except:
#print('Have a good day!')
             