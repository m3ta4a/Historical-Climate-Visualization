######
#   Jake Van Alstyne
#   CS 6630
#   Scientific Visualization
#   Valerio Pascucci
######

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
    def __init__(self, station_id, element, year):
        self.station_id = station_id;
        self.element = element;
        self.year = year;
    def __str__(self):
        return "ID: {0}, element: {1}, year: {2}, data[0]: {3},{4}".format(self.station_id, self.element, self.year, self.data[0], self.data[1]);
        
def LoadUSData(filename, listname):
    for line in open(filename,'r'):
        station_id = line[0:6];
        element = line[6];
        year = line[7:11];
        data = US_Data(station_id,element,year);
        values = line[12:];
        data.data = values.split();
        listname.append(data);

        
# LOAD STATION INFORMATION FROM DISK
###############################################################
US_StationData = dict();
i = 0;
for line in open(US_STATION_DATA_FN,'r'):
    coop_id = line[0:6];
    latitude = line[7:15];
    longitude = line[16:25];
    elevation = line[26:32];
    state = line[33:35];
    name = line[36:66];
    component_1 = line[67:73];
    component_2 = line[74:80];
    component_3 = line[81:87];
    UTC_offset = line[88:90];
    station = US_Station(coop_id,latitude,longitude,elevation,state,name,component_1,component_2,component_3,UTC_offset);
    US_StationData[coop_id] = station;
    i=i+1;

num_stations = len(US_StationData);
US_StationPoints = vtkPoints();
US_StationPoints.SetNumberOfPoints(num_stations);

poly_vertex = vtk.vtkPolyVertex();
poly_vertex.GetPointIds().SetNumberOfIds(num_stations);

i=0;
for item in US_StationData:
    poly_vertex.GetPointIds().SetId(i, i)
    US_StationPoints.InsertPoint(i,float(US_StationData[item].longitude),float(US_StationData[item].latitude), 1.0);
    i=i+1;
        
grid = vtkUnstructuredGrid();
grid.Allocate(1,1);
grid.InsertNextCell(poly_vertex.GetCellType(), poly_vertex.GetPointIds());
grid.SetPoints(US_StationPoints);

StationMapper = vtkDataSetMapper();
StationMapper.SetInput(grid);
StationActor = vtkActor();
StationActor.SetMapper(StationMapper);
StationActor.GetProperty().SetDiffuseColor(0,1,0);

##############
# LOAD DATA
##############
####
### U.S. DATA
US_F52_MaxData = []; # F52 ->
US_F52_MinData = [];
US_F52_AvgData = [];
US_F52_PCPData = [];
US_tob_MaxData = []; # tob ->
US_tob_MinData = [];
US_tob_AvgData = [];
US_raw_MaxData = []; # raw -> 
US_raw_MinData = [];
US_raw_AvgData = [];
US_raw_PCPData = [];
LoadUSData(US_DATA_FILENAMES[0],US_raw_AvgData);
LoadUSData(US_DATA_FILENAMES[1],US_raw_MaxData);
LoadUSData(US_DATA_FILENAMES[2],US_raw_MinData);
LoadUSData(US_DATA_FILENAMES[3],US_raw_PCPData);
LoadUSData(US_DATA_FILENAMES[4],US_tob_AvgData);
LoadUSData(US_DATA_FILENAMES[5],US_tob_MaxData);
LoadUSData(US_DATA_FILENAMES[6],US_tob_MinData);
LoadUSData(US_DATA_FILENAMES[7],US_F52_AvgData);
LoadUSData(US_DATA_FILENAMES[8],US_F52_MaxData);
LoadUSData(US_DATA_FILENAMES[9],US_F52_MinData);
LoadUSData(US_DATA_FILENAMES[10],US_F52_PCPData);

# for item in US_F52_MaxData:
#     print(US_StationData[item.station_id]);
#     print(item);



# GENERATE IMAGES
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

ren = vtkRenderer();
ren.AddActor(mapActor);
ren.AddActor(StationActor);
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