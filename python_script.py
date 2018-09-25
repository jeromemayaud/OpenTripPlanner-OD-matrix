#

from org.opentripplanner.scripting.api import OtpsEntryPoint

# Instantiate an OtpsEntryPoint
otp = OtpsEntryPoint.fromArgs(['--graphs', '.',
                               '--router', 'graph_folder'])

# Start timing the code
import time
start_time = time.time()

# Get the default router
router = otp.getRouter('graph_folder')
points_file = 'points_surrey.csv' #Set the file from which you will take points

# Create a default request for a given departure time
req = otp.createRequest()
req.setDateTime(2017, 9, 19, 10, 00, 00)  # set departure time (year, month, day, hour, minute, sec)
req.setMaxTimeSec(3600)                   # set a limit to maximum travel time (seconds)
req.setModes('CAR, WALK')             # define transport mode
#req.setSearchRadiusM(500)                 # set max snapping distance to connect trip origin to street network (Does this parameter even exist??)
#req.maxWalkDistance = 500                 # set maximum walking distance ( kilometers ?)
#req.walkSpeed = walkSpeed                 # set average walking speed ( meters ?)
#req.bikeSpeed = bikeSpeed                 # set average cycling speed (miles per hour ?)

# Read Points of Destination - The file points.csv contains the columns GEOID, ID, X and Y.
points = otp.loadCSVPopulation(points_file, 'Y', 'X')
dests = otp.loadCSVPopulation(points_file, 'Y', 'X')

# Create a CSV output
matrixCsv = otp.createCSVOutput()
matrixCsv.setHeader([ 'origin', 'destination', 'walk_distance', 'travel_time', 'boardings' ])

# Start Loop
for origin in points:
  print "Processing origin:", origin
  req.setOrigin(origin)
  spt = router.plan(req)
  if spt is None: continue

  # Evaluate the SPT for all points
  result = spt.eval(dests)
  
  # Add a new row of result in the CSV output
  for r in result:
    matrixCsv.addRow([ origin.getStringData('GEOID'), r.getIndividual().getStringData('GEOID'), r.getWalkDistance() , r.getTime(),  r.getBoardings() ])
    
# Save the result
matrixCsv.save('traveltime_matrix.csv')

# Stop timing the code
print("Elapsed time was %g seconds" % (time.time() - start_time))
