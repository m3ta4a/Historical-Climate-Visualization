######
#   Jake Van Alstyne
#   CS 6630
#   Scientific Visualization
#   Valerio Pascucci
######

import sys
import random
from vtk import *

US_STATION_DATA_FN = "data/ushcn-stations.txt";
US_DATA_FILENAMES = [  'data/9641C_201012_raw.avg',
                    'data/9641C_201012_raw.max',
                    'data/9641C_201012_raw.min',
                    'data/9641C_201012_raw.pcp',
                    'data/9641C_201012_tob.avg',
                    'data/9641C_201012_tob.max',
                    'data/9641C_201012_tob.min',
                    'data/9641C_201012_F52.avg',
                    'data/9641C_201012_F52.max',
                    'data/9641C_201012_F52.min',
                    'data/9641C_201012_F52.pcp'];
                    
            # List of 2-member lists of data-corresponding filenames, 
            # Within sublist, 1st is metadata, 2nd is actual data
GHCN_FILENAMES = [  ['data/GHCN/ghcnm.tavg.v3.1.0.20111121.qcu.inv','data/GHCN/ghcnm.tavg.v3.1.0.20111121.qcu.dat'],
                    ['',''],
                    ['',''],
                    ['',''],
                    ['',''],
                    ['',''],
                    ['',''],
                    ['',''],
                    ['',''],
                    ['','']    
                            ];

class US_Station:
    def __init__(self, coop_id, latitude, longitude, elevation,state,name,component_1,component_2,component_3,UTC_offset):
        self.coop_id = coop_id;
        self.latitude = latitude;
        self.longitude = longitude;
        self.elevation = elevation;
        self.state = state;
        self.name = name;
        self.component_1 = component_1;
        self.component_2 = component_2;
        self.component_3 = component_3;
        self.UTC_offset = UTC_offset;
    def __str__(self):
        return "Station ID: {0}, lat: {1}, long: {2}".format(self.coop_id, self.latitude, self.longitude);

class US_Data:
    def __init__(self, station_id, element, year, data):
        self.station_id = station_id;
        self.element = element;
        self.year = year;
        self.data = data;
    def __str__(self):
        return "ID: {0}, element: {1}, year: {2}, data[0]: {3},{4}".format(self.station_id, self.element, self.year, self.data[0], self.data[1]);

class GHCN_Data:
    def __init__(self, _id, year, element, values):
        self.station_id = _id;
        self.year = year;
        self.element = element;
        self.values = values;

class GHCN_Station:
    def __init__(self, _id, latitude, longitude, elevation, name, grelev, popcls, popsiz, topo, stveg, stloc, ocndis, airstn, towndis, grveg, popcss):
        self.station_id = _id;
        self.latitude = latitude;
        self.longitude = longitude;
        self.elevation = elevation;
        self.name = name;
    def __str__(self):
        return "Station Name: {3}, ID: {0}, lat: {1}, long: {2}".format(self.station_id, self.latitude, self.longitude, self.name);

class GHCN_DataSet:
    def __init__(self,metaData,data):
        self.stationlist = metaData;
        self.data = data;
    def GetTemperature(self, station_id, year, month):
        if station_id in self.data:
            data = self.data[station_id];
            if int(year) in data:
                months = data[int(year)];
                month = months[0];
                return month[0];
            else:
                return -9999;
        else:
            return -9999;

# Load GHCN Data
# Creates a GHCN_DataSet Object, populates its member variables and returns it 
############################
def LoadGHCNData(metadata_filename, data_filename):
    stationlist = dict();
    for line in open(metadata_filename,'r'):
        _id = line[0:11];
        latitude = float(line[12:20]);
        longitude = float(line[21:30]);
        elevation = float(line[31:37]);
        name = line[38:68];
        grelev = line[69:73];
        popcls = line[74];
        popsiz = line[75:79];
        topo = line[79:81];
        stveg = line[81:83];
        stloc = line[83:85];
        ocndis = line[85:87];
        airstn = line[88];
        towndis = line[88:90];
        grveg = line[90:106];
        popcss = line[107];
    
        station = GHCN_Station(_id,latitude,longitude,elevation,name,grelev,popcls,popsiz,topo,stveg,stloc,ocndis,airstn,towndis,grveg,popcss);
        stationlist[_id] = station;        

    datalist = dict(); #indexed by station_id
    for line in open(data_filename, 'r'):
        _id = line[0:11];
        year = int(line[11:15]);
        element = line[15:19];
        temp = [];
        index = 19;
        while index < 109:
            temp.append(line[index:index+5]);
            temp.append(line[index+5]);
            temp.append(line[index+6]);
            temp.append(line[index+7]);
            index = index+8;
        values = [];
        for i in xrange(0,len(temp)-3,4):
            value = [temp[i], temp[i+1], temp[i+2], temp[i+3]];
            values.append(value);
        # Years collect monthly data for each station by year
        if _id in datalist:
            years = datalist[_id];
        else:
            years = dict();    
        years[year] = values;
        datalist[_id] = years;

    return GHCN_DataSet(stationlist,datalist);

# Appends each line from filename as instance of USData into the supplied listname
############################
def LoadUSData(filename, listname):
    for line in open(filename,'r'):
        station_id = int(line[0:6]);
        element = line[6];
        year = int(line[7:11]);
        values = line[12:];
        data = US_Data(station_id,element,year,values.split());
        listname.append(data);

# GHCN Glyph Callback
##########################
def GlyphGHCN():
    point_id = GHCNGlypher.GetPointId();
    if point_id in StationIDs:
        _id = StationIDs[point_id];
        station = GHCN_Avg_raw.stationlist[_id];
        temp = GHCN_Avg_raw.GetTemperature(_id,1983,0);
        if temp != -9999:
            celcius = float(temp) / 100
            kelvin = celcius + 273.15
            radius = (kelvin - 200) / 100 # Hard coded values, can do better.
            ball.SetCenter(station.longitude,station.latitude,0.01);
            ball.SetRadius(radius)
        else:
            ball.SetRadius(0.0)
    else:
        ball.SetRadius(0.0)
# MAIN
##############################################################
ren = vtkRenderer();   

# Use a ball to represent each station
ball = vtkSphereSource();
ball.SetRadius(0.2);
ball.SetThetaResolution(8)
ball.SetPhiResolution(8)
ball.Update();

year = 1983
month = 0

##############
# LOAD DATA
##############
#########
## GHCN Data
############################
GHCN_Avg_raw = LoadGHCNData(GHCN_FILENAMES[0][0],GHCN_FILENAMES[0][1])
num_stations = len(GHCN_Avg_raw.stationlist)

GHCN_StationPts = vtkPoints()
GHCN_StationPts.SetNumberOfPoints(num_stations)

poly_vertex = vtkPolyVertex()
poly_vertex.GetPointIds().SetNumberOfIds(num_stations)

StationIDs = dict() ## Used to map PointIds back to StationIds

print("number of stations:")
print(num_stations)

i=0
temperatures = vtkFloatArray()
for index in GHCN_Avg_raw.stationlist:
    station = GHCN_Avg_raw.stationlist[index]
    temp = GHCN_Avg_raw.GetTemperature(index,year,month)
    if int(temp) != -9999:
        celc = float(temp) / 100.0
        val  = (celc + 50) / 100
        temperatures.InsertNextValue(val)
        poly_vertex.GetPointIds().SetId(i, i)
        GHCN_StationPts.InsertPoint(i, station.longitude, station.latitude, .01)
        StationIDs[i] = index
        i=i+1

grid = vtkUnstructuredGrid();
grid.Allocate(1,1);
grid.InsertNextCell(poly_vertex.GetCellType(), poly_vertex.GetPointIds());
grid.SetPoints(GHCN_StationPts);
grid.GetCellData().SetScalars(temperatures)
grid.Update();

ball_lut = vtkLookupTable()
ball_lut.SetNumberOfColors(256)
for i in range(256):
    ball_lut.SetTableValue( i, float(i)/255.0, 0.0, 1 - float(i)/255.0, 1.0 )
#ball_lut.SetValueRange(0,1)
#ball_lut.SetSaturationRange(1.0, 1.0)
#ball_lut.SetHueRange(.8,1.0)
#ball_lut.SetRampToLinear()
#ball_lut.Build()

GHCNGlypher = vtkProgrammableGlyphFilter();
GHCNGlypher.SetInput(grid);
GHCNGlypher.SetSource(ball.GetOutput());
GHCNGlypher.SetColorModeToColorByInput();
GHCNGlypher.SetGlyphMethod(GlyphGHCN);

glyphmapper = vtkPolyDataMapper();
glyphmapper.SetInput(GHCNGlypher.GetOutput());
glyphmapper.SetLookupTable(ball_lut)

glyphactor = vtkActor();
glyphactor.SetMapper(glyphmapper);

ren.AddActor(glyphactor);

# GENERATE EARTH MAP
###############################################################
# Setup data reader
earth_image = "1_world.topo.bathy.200403.3x5400x2700.jpg";
reader = vtkJPEGReader(); 
reader.SetFileName(earth_image);
reader.Update();

# Map of the Earth
mapPlane = vtkPlaneSource();
mapPlane.SetResolution(1000,500);
mapPlane.SetNormal(0,0,1);
mapPlane.SetOrigin(-180,-90,0.01);
mapPlane.SetPoint1(180,-90,0.01);
mapPlane.SetPoint2(-180,90,0.01);

# Mapper for the map
mapMapper = vtkPolyDataMapper();
mapMapper.SetInput(mapPlane.GetOutput());

# Texture for the map
mapTexture = vtkTexture();
mapTexture.SetInput(reader.GetOutput());

#Set up the actor, apply texture
mapActor = vtkActor();
mapActor.SetMapper(mapMapper);
mapActor.SetTexture(mapTexture);

# Render Window
############################
ren.AddActor(mapActor);

renwin = vtkRenderWindow();
renwin.AddRenderer(ren);
iren = vtkRenderWindowInteractor();
iren.SetRenderWindow(renwin);
ren.SetBackground(0,0,0.2);
renwin.SetSize(1480,1480);

renwin.Render();
ren.ResetCamera();

iren.Initialize();
iren.Start();



# FOR NOW DONT CARE ABOUT US ONLY DATA
# U.S. DATA
############################
#US_F52_MaxData = []; # F52 ->
#US_F52_MinData = [];
#US_F52_AvgData = [];
#US_F52_PCPData = [];
#US_tob_MaxData = []; # tob ->
#US_tob_MinData = [];
#US_tob_AvgData = [];
#US_raw_MaxData = []; # raw -> 
#US_raw_MinData = [];
#US_raw_AvgData = [];
#US_raw_PCPData = [];

# LoadUSData(US_DAA_FILENAMES[0],US_raw_AvgData);
# LoadUSData(US_DATA_FILENAMES[1],US_raw_MaxData);
# LoadUSData(US_DATA_FILENAMES[2],US_raw_MinData);
# LoadUSData(US_DATA_FILENAMES[3],US_raw_PCPData);
# LoadUSData(US_DATA_FILENAMES[4],US_tob_AvgData);
# LoadUSData(US_DATA_FILENAMES[5],US_tob_MaxData);
# LoadUSData(US_DATA_FILENAMES[6],US_tob_MinData);
# LoadUSData(US_DATA_FILENAMES[7],US_F52_AvgData);
# LoadUSData(US_DATA_FILENAMES[8],US_F52_MaxData);
# LoadUSData(US_DATA_FILENAMES[9],US_F52_MinData);
# LoadUSData(US_DATA_FILENAMES[10],US_F52_PCPData);

# for item in US_F52_MaxData:
#     print(US_StationData[item.station_id]);
#     print(item);

# LOAD STATION INFORMATION FROM DISK
###############################################################
# US_StationData = dict();
# for line in open(US_STATION_DATA_FN,'r'):
#     coop_id = int(line[0:6]);
#     latitude = float(line[7:15]);
#     longitude = float(line[16:25]);
#     elevation = line[26:32];
#     state = line[33:35];
#     name = line[36:66];
#     component_1 = line[67:73];
#     component_2 = line[74:80];
#     component_3 = line[81:87];
#     UTC_offset = line[88:90];
#     station = US_Station(coop_id,latitude,longitude,elevation,state,name,component_1,component_2,component_3,UTC_offset);
#     US_StationData[coop_id] = station;
# 
# # Show U.S. stations on map
# ##########################
# num_stations = len(US_StationData);
# US_StationPoints = vtkPoints();
# US_StationPoints.SetNumberOfPoints(num_stations);
# 
# poly_vertex = vtk.vtkPolyVertex();
# poly_vertex.GetPointIds().SetNumberOfIds(num_stations);
# 
# i=0;
# for index, item in US_StationData.iteritems():
#     poly_vertex.GetPointIds().SetId(i, index)
#     US_StationPoints.InsertPoint(i,float(item.longitude),float(item.latitude), .01);
#     i=i+1;
#         
# grid = vtkUnstructuredGrid();
# grid.Allocate(1,1);
# grid.InsertNextCell(poly_vertex.GetCellType(), poly_vertex.GetPointIds());
# grid.SetPoints(US_StationPoints);
# grid.Update();

# RenderData(grid,ren);

