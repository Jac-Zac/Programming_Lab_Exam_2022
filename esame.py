#!/usr/bin/env python3

# Import to check dates
from dateutil.parser import parse

#==============================
#  Colors 
#==============================
# colored text
reset='\033[0m'
bold='\033[01m'
underline='\033[04m'
red='\033[31m'
green='\033[32m'
yellow='\033[93m'

#==============================
#  Exception Class
#==============================

class ExamException(Exception):
    pass

#==============================
#  CSVTimeSeriesFile Class
#==============================

class CSVTimeSeriesFile:
    '''Class that can read a time series related to passengers on an airline.
    And that can compute the average variance for every month'''

    # Constructor that takes in the name of the file
    def __init__(self, name):

        # If name is not a string raise generate an error and get back to main 
        if not isinstance(name, str):
            raise ExamException(f'{bold}{red} Error: parameter "name" must be a string, not "{type(name)}"')

        # Set the name 
        self.name = name

    # I need this to check if the string is a date
    def is_date(self,string):
        """
        Return whether the string can be interpreted as a date.
        :param string: str, string to check for date
        """
        try:
            parse(string)
            return True

        except ValueError:
            return False

    # Function that returns lists of lists which date and passengers number
    def get_data(self):

        # Initialise an empty list to save all of the values
        complete_list = []

        # I try to open the file and get the data if it fails I raise and exception and abort. 
        try:
            my_file = open(self.name, 'r')
        except Exception as e:

            # Raise the exception 
            raise ExamException(f'{red}{bold}Error occurred when reading the file: "{e}"{reset}')

        # If I can open the file I start to read line by line 
        for line in my_file:

            # Comma separated split
            elements = line.split(',')

            # I skip the first element which is the heading
            if elements[0] != 'date':

                # I set the date and the value
                try:
                    date = str(elements[0])

                    # Check if the date doesn't makes sens as a date 
                    # Using the helper function that I have added to the class
                    if not self.is_date(date):
                        # Run if the output of is_date is False
                        # And go to the next loop
                        continue

                    # Make the value an integer if it is not don't accept it 
                    value = int(elements[1])

                    # If value is a negative number don't accept it and continue,
                    # we could have also decided to accept it and change it with abs but I'm following the instruction give by the teacher
                    if value < 0:
                        continue
                except:
                    continue

                # Check if the timestamps is a duplicate of any of the preview timestamps saved
                if len(complete_list) > 0:
                    # Loop through the preview timestamps 
                    for item in complete_list:
                        # Save the data value on the previews timestamp
                        prev_date = item[0]

                        if date == prev_date:
                            raise ExamException(f'{bold}{red}Timestamp is a duplicate.{reset}')

                # Check if the timestamp follow the one before
                    prev_date = complete_list[-1][0]
                    if date < prev_date:
                        raise ExamException(f'{bold}{red}Timestamp is not ordered.{reset}')

                # I append the date and value lists to the main list for every step
                complete_list.append([date,value])

        # Close the file
        my_file.close()

        # If the file is empty 
        if not complete_list:
            raise ExamException(f'{bold}{red}File is empty{reset}')

        return complete_list

# Function to compute the average 
def compute_avg_monthly_difference(time_series, first_year, last_year):

    # Check if time_series is a list
    if not isinstance(time_series, list):
        raise ExamException(f'{bold}{red} Error: parameter "time_series" should be a list of lists, not "{type(time_series)}"{reset}')

    # Check if fist and last_year are strings
    if not isinstance(first_year, str):
        raise ExamException(f'{bold}{red} Error: parameter "first_year" must be a string, not "{type(first_year)}"{reset}')

    if not isinstance(last_year, str):
        raise ExamException(f'{bold}{red} Error: parameter "last_year" must be a string, not "{type(last_year)}"{reset}')

    # If the two years given are the same
    if first_year == last_year:
        raise ExamException(f'{bold}{red} Error: the last and first year are the same{reset}')

    # If the two years are in the wrong order print a warning, I don't think it is needed but I'm doing it for good measures 
    if first_year > last_year:
        print(f'{yellow}{bold}Warning:{reset}{yellow} First and last year are not in the right order, I will switch them and continue{reset}')
        tmp = first_year
        first_year = last_year
        last_year = tmp

    # Since we know the list is ordered we can check if the first and last years
    # We should keep in mind that we are making comparison between string but since they are made up of numbers
    # I use :4 to just take in consideration the numbers of the year and not the dash or the moth
    if(first_year < time_series[0][0][:4]):
        raise ExamException(f'{bold}{red}Error: first_year is not present in the data.csv file{reset}')

    # We check in the last list of time_series in the position 0 which is the position of the date
    # If the last year is not in the time_series
    if(last_year > time_series[-1][0][:4]):
        raise ExamException(f'{bold}{red}Error: last_year is not present in the data.csv file{reset}')

    # Empty list to save the final result
    results = []

    # temporary variables
    counter = 0
    years = []

    # Iterate over the lists of list given until we reach the last_year
    while True:

        # If we are at the right index for the first year or year is already filled with something 
        # Thous we are in a year after the first we should do the following
        if time_series[counter][0][:4] == first_year or years != None:

            # Create a list with all the values of a year
            for i in range(12):
                # Check the right part of the time_series date to look if it exist also try to check with a zero for the months 01 02 ... to 09, 
                # i should be interpreted as a string but starting from 1 not from zero to be compared with the months
                # Since we might be at the last year I will have be to careful to avoid index error, 
                try:
                    if time_series[counter][0][5:8] == str(i + 1) or time_series[counter][0][5:8] == str(i + 1).zfill(2):
                        # Getting the data at the counter + the iteration number we are in
                        years.append(time_series[counter][1])
                        # Increment the number of element that I have processed to get to the next month 
                        counter = counter + 1
                    else:
                        # If the year is not inside the date we have to add a 0 in that position
                        years.append(0)
                        # We don't want to increment the counter if the year is missing
                except IndexError:
                    # if this occurs it means there are no more values for the final year and thus I'll fill them with 0
                    years.append(0)

            # We check: if the year we just did was the last (thus counter -1 since we have updated it already) then we exit the loop
            if time_series[counter - 1][0][:4] == last_year:
                break

    # Since every year has 12 month which is sure because I made them by filling them by zero if the month was non existent I can divided by 12 and always get an integer 
    years_size = int(len(years)/12)
    print(years)

    # Loop over 12 months 
    for i in range(12):

        # Declare a variable for the sum which starts from zero at every loop
        years_sum = 0

        # Variable to count how many not_zero value are present
        not_zero_counter = 2

        # Loop over years by using the years_size valuable and starting from one since we are multiplying 
        for j in range(1,years_size):

            # If we are doing the calculation on only two years
            if(years_size == 2):
                # Sum every years by subtracting the current mouth value of the year from the one that cams after
                # The first iteration j start from 1 and thus we get i + 12 and i
                years_sum += (years[i + (12*j)] - years[i + (12*(j-1))])
                # If there are only two years an one of them has value zero the end result will be zero
                if years[i] == 0 or years[i + 12] == 0:
                    years_sum = 0
            else:

                if years[i + (12*(j-1))] != 0:
                    years_sum += (years[i + (12*j)] - years[i + (12*(j-1))])
                else:
                    not_zero_counter -= 1

        # If a months has less the two value 
        if not_zero_counter < 2:
            results.append(0)
        else:
            # append the i result toe the list and divided it by the number of years - 1
            results.append(years_sum/(years_size-1))

    # Must return 12 elements
    return results

#==============================
# Main
#==============================
