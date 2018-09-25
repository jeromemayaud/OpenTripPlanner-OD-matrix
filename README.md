# OpenTripPlanner-OD-matrix
A series of scripts to calculate an origin-destination (OD) matrix across a study area using OpenTripPlanner. This can be run for a single time of the day (using 'python_script.py') or looping through several times in the day (using 'python_script_loopHM.py'). Also included are scripts to further analyse the OD matrices.

These functions were used to analyse OD-matrices in the following publications:

Mayaud, J. R., Tran, M., Pereira, R. H. M. & Nuttall, R. (2018). Future access to essential services in a growing smart city: The case of Surrey, British Columbia. Computers, Environment and Urban Systems.

These scripts are based on the wonderful reproducible example provided by Rafa Pereira: https://github.com/rafapereirabr/otp-travel-time-matrix

# Running the code
1.	Download the following files from chosen city, and add in a city-specific folder in your ‘OpenTripPlanner’ folder:
a.	GTFS (General Transit Feed Specification) data, as a zipped file
b.	OpenStreetMap (OSM) data, as a .pbf file (e.g. available from Mapzen Metro extract: https://mapzen.com/data/metro-extracts/)

2.	Download a Shape File of your city boundary and add in a city-specific folder (e.g. city administrative boundaries can be found at http://global.mapit.mysociety.org/)

3.	Download the Shape File of Routes and Stops of your city from its Transit Department website, and add in your city-specific folder.

4.	In the Terminal, run following scripts to run the matrix building files: 

a. First, set the directory to your OTP folder:

cd/Users/jeromemayaud/Documents/University/BritishColumbia/Modelling/OpenTripPlanner  (<-- 

b. Second, build the graph:

java -Xmx8G -jar otp-1.2.0-shaded.jar --cache /Users/jeromemayaud/Documents/University/BritishColumbia/Modelling/OpenTripPlanner --basePath /Users/jeromemayaud/Documents/University/BritishColumbia/Modelling/OpenTripPlanner --build /Users/jeromemayaud/Documents/University/BritishColumbia/Modelling/OpenTripPlanner

5.	Move the graph to a sub-folder within your main folder, which should be called ‘graph_folder’ 

6.	In R, run ‘MakingHexagonalMaps'. This outputs a CSV file (e.g. ‘points.csv’) to be used below.

7.	Move 'points.csv' into your OpenTripPlanner folder.

8.	In the Terminal, run the matrix-building python file. 'python_script.py' script (or 'python_script_loopHM.py' script if you want to loop the matrix-building file several times in the day):

/Users/jeromemayaud/jython2.7.0/bin/jython -J-XX:-UseGCOverheadLimit -J-Xmx8G -Dpython.path=otp-1.2.0-shaded.jar python_script.py

Make sure that: 
- The ‘Otps entry point’ has the same folder as where your graph is located 
- The working directory is still set to your city folder 
- The req.setDateTime is set to the right date for your particular GTFS data

This outputs ‘traveltime_matrix.csv’.

9.	Run the ‘traveltime_matrix_analyser.py’ script. If you have run the matrix-building file for several times in the day (i.e. using 'python_script_loopHM.py'), and need to collapse all these into an average, run ‘traveltime_matrix_analyser_MULTIPLE.py’ in Python.s

This outputs ‘Analysed_traveltimematrix.csv’.
