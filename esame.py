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
            raise ExamException(f'{red}{bold}Error occurred when reading the file: "{e}"{reset}')

        # If I can open the file I start to read line by line 
        for line in my_file:

            elements = line.split(',')
            # I skip the first element which is the heading
            if elements[0] != 'date':

                # I set the date and the value
                try:
                    date = str(elements[0])

                    # Check if the date doesn't makes sens as a date , using the helper function that I have added to the class
                    if not self.is_date(date):
                        # Run if the output of is_date is False thus that is not a date, don't save the value and go to the next loop
                        continue

                    # If the element is a float pass to the next one and ignore it
                    try:
                        # Make the value an integer if it is not don't accept it 
                        value = int(elements[1])
                    except ValueError:
                        continue

                    # If value is a negative number don't accept it and continue,
                    if value < 0:
                        continue
                except:
                    # If other error occur go to the next loop without saving those data 
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

    # Check if time_series is a list, and first_year and last_year are string, else rise exceptions
    if not isinstance(time_series, list):
        raise ExamException(f'{bold}{red} Error: parameter "time_series" should be a list of lists, not "{type(time_series)}"{reset}')
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

    # Since we know the list is ordered we can check if the first and last years are in the list
    # We should keep in mind that we are making comparison between string but since they are made up of numbers
    # I use :4 to just take in consideration the numbers of the year and not the dash or the moth
    if(first_year < time_series[0][0][:4]):
        raise ExamException(f'{bold}{red}Error: first_year is not present in the data.csv file{reset}')

    if(last_year > time_series[-1][0][:4]):
        raise ExamException(f'{bold}{red}Error: last_year is not present in the data.csv file{reset}')

    # temporary variables
    counter = 0
    years = []

    # Iterate over the lists of list given until we reach the last_year to create a list with elements set to 0 if needed
    while True:

        # This is a variable to keep in mind in which year we are jut because it is useful
        current_year = time_series[counter][0][:4]
        # Flag to know if I have already incremented the counter 
        flag = 0

        # If we are at the right index for the first year or year is already filled with something we do the following
        if current_year == first_year or years:

            # Create a list with all the values of a year loop over the 12 months
            for i in range(1,13):
                # Check the right part of the time_series date to look if it exist also try to check with a zero for the months 01 02 ... to 09, 
                # i should be interpreted as a string but starting from 1 not from zero to be compared with the months
                # Since we might be at the last year I will have be to careful to avoid index error, 
                try:

                    # I check if the month is the same and fill with a zero in front if the number is less then 10
                    if time_series[counter][0][5:8] == str(i).zfill(2):

                        # Saving the value at the counter into the years list 
                        years.append(time_series[counter][1])

                        # Increment the number of element that I have processed to get to the next month 
                        try:
                            # If we are still in the current year increment and set flag to 1 to indicate you have incremented 
                            if (time_series[counter + 1][0][:4] == current_year):
                                counter += 1
                                flag = 1
                            else:
                                # Set the flag to 0 and do not increment
                                flag = 0

                        except IndexError:
                            # Set the flag to 0 we are probably in the last year and we tried to look at the year at counter + 1 
                            flag = 0
                    else:
                        # If the year is not inside the date we have to add a 0 in that position
                        years.append(0)
                        # since it is not inside we increment don't increment and thus set the flag to 0
                        flag = 0

                except IndexError:
                    # if this occurs it means there are no more values for the final year and thus I'll fill them with 0
                    years.append(0)

            # Increment the counter because we finished the for loop, only if we haven't already incremented the counter
            if(flag == 0):
                counter = counter + 1

            # We check: if the year we just did was the last (thus counter -1 since we have updated it already) then we exit the loop
            try:
                # Break if we reached the last year
                if time_series[counter - 1][0][:4] == last_year:
                    break
            except IndexError:
                # Break if the year went out of range
                break

        # If we are not in the first year and the value of years is still null we go to the next one and repeat
        else:
            counter = counter + 1;


    # Since every year has 12 month which is sure because I made them by filling them by zero if the month was non existent I can divided by 12 and always get an integer 
    years_size = int(len(years)/12)

    # Empty list to save the final result
    results = []

    # Loop over 12 months 
    for i in range(12):

        # Declare a variable for the sum which starts from zero at every loop
        years_sum = 0

        # Variable to count how many months don't have a value of zero
        not_zero_counter = years_size

        # Useful variable to keep in mind where the last position was and also relative to where the zero were
        current = 0
        old_position = None

        # If we are doing the calculation on only two years
        if(years_size == 2):
            # Sum every years by subtracting the current month value of the year from the one that cams after
            # The first iteration j start from 1 and thus we get i + 12 and i
            years_sum += (years[i + 12] - years[i])
            # If there are only two years an one of them has value zero the end result will be zero
            if years[i] == 0 or years[i + 12] == 0:
                years_sum = 0

        else:
            # Loop over years by using the years_size
            for j in range(years_size):

                # Set current= to the current year
                current = j*12

                # Check if the year at the current position is zero
                if(years[i + current] == 0):
                    # Decrees the counter because we found a zero
                    not_zero_counter -= 1

                # If the number is not zero we keep going
                else:
                    # If the old position is still not set we go to the next step 
                    if(old_position == None):
                        old_position = current
                    else:
                        # Compute the sum
                        years_sum += (years[i + (current)] - years[i + (old_position)])
                        old_position = current

        # If a months has less the two value 
        if not_zero_counter < 2:
            results.append(0)
        else:
            # append the i result of the sum divided it by the number of non zero years - 1, to the list
            results.append(years_sum/(not_zero_counter - 1))

    # Must return 12 elements
    return results

#==============================
# Main
#==============================

# time_series_file = CSVTimeSeriesFile(name="data.csv")

# time_series = time_series_file.get_data()

# print(time_series)

# results = compute_avg_monthly_difference(time_series,"1949","1951")

# print(results)
