import numpy as np
import pandas as pd

#Time threshold you set as maximum time somebody should travel (in mins - it is multiplied to seconds lower in the script)
time_threshold = 30

#This is the input traveltime_matrix
input_file = '/Users/jeromemayaud/Documents/University/BritishColumbia/Modelling/OpenTripPlanner/Vancouver/traveltime_matrices/traveltime_matrix_WalkTransit_19Sep2017.csv'
input_file2 = '/Users/jeromemayaud/Documents/University/BritishColumbia/Modelling/OpenTripPlanner/Vancouver/points_vancouver.csv'

traveltime_matrix = np.genfromtxt(input_file,delimiter=',') #Convert CSV to numpy array
traveltime_matrix = np.delete(traveltime_matrix, (0), axis=0) #Delete first row ('NaNs' due to column titles from CSV file)
points_table = np.genfromtxt(input_file2,delimiter=',') #Convert CSV to numpy array
points_table = np.delete(points_table, (0), axis=0) #Delete first row ('NaNs' due to column titles from CSV file)

number_of_rows = len(traveltime_matrix)
number_of_origins = int(np.nanmax(points_table, axis=0)[0]) #Find number of origin points by finding max in first column (ignoring NaNs)
summing_table = np.zeros((number_of_origins, 2)) #Create empty matrix with same number of rows as matrix, and 2 columns
summing_table[:,0] = np.arange(1, (number_of_origins+1)) #Populate first column with numbers from 1 to total number of origins

a = 1
b = 0
below_threshold_counter = 0

while a <= number_of_origins:
    if b >= len(traveltime_matrix): #Don't want to index out of bounds
        break
    if traveltime_matrix[b,0] == a:
        if traveltime_matrix[b,3] <= (time_threshold*60):
            below_threshold_counter += 1
        b += 1
    else:
        summing_table[(a-1),1] = ((below_threshold_counter/number_of_origins)*100) #Put number of counts into the summing table, as proportion of total potential destinations, in the 2nd column
        a += 1
        b += 1
        below_threshold_counter = 0

np.savetxt('Analysed_traveltimematrix_Seattle_' + str(time_threshold) + "mins_19Sep2017" + '.csv', summing_table, delimiter=",")
