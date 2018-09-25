import numpy as np
import pandas as pd
import glob
import errno


path = '/Users/jeromemayaud/Downloads/matrices/traveltime_matrix_*.csv'
input_file = '/Users/jeromemayaud/Documents/University/BritishColumbia/Modelling/OpenTripPlanner/Surrey/points_surrey.csv'
files_list = glob.glob(path)

#Time threshold you set as maximum time somebody should travel (in mins - it is multiplied to seconds lower in the script)
time_threshold = 60

#Tables and parameters to work out lengths of files, number of origins etc.
points_table = np.genfromtxt(input_file,delimiter=',') #Convert CSV to numpy array
points_table = np.delete(points_table, (0), axis=0) #Delete first row ('NaNs' due to column titles from CSV file)
number_of_origins = int(np.nanmax(points_table, axis=0)[0]) #Find number of origin points by finding max in first column (ignoring NaNs)
number_of_files = len(files_list)
    
averages_table = np.zeros((number_of_origins,2))

file_number_counter = 0

for file_name in files_list:
    print("Working on file ", file_name)
    file_identifier_string = files_list[file_number_counter]
    file_identifier_string = file_identifier_string.replace('/Users/jeromemayaud/Downloads/matrices/traveltime_matrix_','')
    file_identifier_string = file_identifier_string.replace('.csv','')
    
    traveltime_matrix = np.genfromtxt(file_name,delimiter=',')
    traveltime_matrix = np.delete(traveltime_matrix, (0), axis=0) #Delete first row ('NaNs' due to column titles from CSV file)
    
    number_of_rows = len(traveltime_matrix)
    summing_table = np.zeros((number_of_origins, 2)) #Create empty matrix with same number of rows as matrix, and 2 columns
    summing_table[:,0] = np.arange(1, (number_of_origins+1)) #Populate first column with numbers from 1 to total number of origins

    a = 1
    b = 0
    below_threshold_counter = 0
    
    while a <= number_of_origins:
        if b >= len(traveltime_matrix): #Don't want to index out of bounds
            break
        if traveltime_matrix[b,2] == a:
            if traveltime_matrix[b,5] <= (time_threshold*60):
                below_threshold_counter += 1
            b += 1
        else:
            summing_table[(a-1),1] = ((below_threshold_counter/number_of_origins)*100) #Put number of counts into the summing table, as proportion of total potential destinations, in the 2nd column
            a += 1
            b += 1
            below_threshold_counter = 0
    
    np.savetxt('Analysed_traveltimematrix_Surrey_' + str(time_threshold) + "mins_Walk+Transit_19Sep2017_" + file_identifier_string + '.csv', summing_table, delimiter=",")
    file_number_counter += 1

    averages_table += summing_table

final_averages_table = averages_table
final_averages_table = final_averages_table[:,1]/number_of_files

np.savetxt('Analysed_traveltimematrix_Surrey_' + str(time_threshold) + "mins_Walk+Transit_19Sep2017_ALLTIMES.csv", final_averages_table, delimiter=",")
    