#Load libraries
library("rgdal")
library("rgeos")
library("downloader")

setwd("/Users/jeromemayaud/Documents/University/BritishColumbia/Modelling/RStudioProjects/MakingHexagonalMaps")

#Read shape file
urbanmetro_mal <- readOGR(dsn="/Users/jeromemayaud/Documents/University/BritishColumbia/Modelling/RStudioProjects/MakingHexagonalMaps/VancouverShapeFile", layer="VancouverShape")    

#################################################
#Read from internet if you have a Geojson file instead
#downloader::download(url = "http://global.mapit.mysociety.org/area/29746.geojson", destfile = "/Users/jeromemayaud/Downloads/paris.GeoJSON")
#urbanmetro_mal <- readOGR(dsn = "/Users/jeromemayaud/Downloads/paris.GeoJSON", layer = "OGRGeoJSON")
#################################################

#Assign projection in UTM, because HexGrid works in metres (zone 10 aligns with Vancouver area)
urbanmetro_mal <- spTransform(urbanmetro_mal, CRS("+proj=utm +zone=10 +ellps=GRS80 +units=m +no_defs"))

#* * * * * HEXAGONAL GRID FUNCTION * * * * 
HexGrid <- function(mycellsize, originlpolygon) { 
  
  #Define size of hexagon bins in meters to create points
  HexPts <- spsample(originlpolygon, type="hexagonal", offset=c(0,0), cellsize=mycellsize)
  
  #Create Grid - transform into spatial polygons
  HexPols <- HexPoints2SpatialPolygons(HexPts)
  
  # convert to spatial polygon data frame
  df <- data.frame(idhex = getSpPPolygonsIDSlots(HexPols))
  row.names(df) <- getSpPPolygonsIDSlots(HexPols)
  hexgrid <- SpatialPolygonsDataFrame(HexPols, data =df)
  return(hexgrid)
}

#* * * * * CREATE HEXAGONAL GRID * * * * 
#This makes the hexagons 500 meters in diameter
hex_got <- HexGrid(500, urbanmetro_mal)

#Find the centres of each grid cell in hexagonal grid (keep as a spatial points frame so can keep the centroid ID, which is needed in other scripts to link centroids back to relevant polygons)
grid_centres <- SpatialPointsDataFrame(gCentroid(hex_got, byid=TRUE), hex_got@data, match.ID=FALSE)

#Convert into a spatial points file, to convert from UTM to WGS84, and then from spatial points file back to dataframe
grid_centres <- as.data.frame(spTransform(grid_centres, CRS("+proj=longlat +datum=WGS84")))

#Add a column at the front for GEOIDs, numbered from 1 to the total number of rows, swap columns round to fit format of Python script later
grid_centres <- cbind(GEOID = 1:nrow(grid_centres), grid_centres)
colnames(grid_centres) <- c("GEOID","ID", "X", "Y")
grid_centres <- grid_centres[c("GEOID", "ID", "Y", "X")]

write.csv(grid_centres, "points.csv", row.names=FALSE) #Don't want row names, otherwise you get the IDs outputted as a separate column
