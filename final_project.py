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
    def __init__(self,metaData,data, runningAvg, minYear, maxYear):
        self.stationlist = metaData;
        self.temperatures = data;
        self.runningAvg = runningAvg;
        self.minYear = minYear
        self.maxYear = maxYear
    def GetTemperature(self, station_id, year, month):
        if station_id in self.temperatures:
            temperatures = self.temperatures[station_id];
            if (month,year) in temperatures:
                return temperatures[(month,year)];
            else:
                return -99.99;
        else:
            return -99.99;
    def GetRunningAvg(self, station_id, year, month):
        if station_id in self.runningAvg:
            avgs = self.runningAvg[station_id]
            date = (month, year)
            if date in avgs:
                return avgs[date]
            else:
                return -99.99
        else:
            return -99.99
        
        
# Load GHCN Data
# Creates a GHCN_DataSet Object, populates its member variables and returns it 
############################
def LoadGHCNData(metadata_filename, data_filename):
    maxYear = -9999
    minYear = 9999
    
    # Collect Station Data
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

    # Collect temperatures, keyed by station ids, keyed by date tuple (month, year)
    stationTemps = dict() #indexed by station_id
    minYear = 3000
    maxYear = 0
    for line in open(data_filename, 'r'):
       
        _id = line[0:11];
        year = int(line[11:15]);
        if minYear > year:
            minYear = year
        if maxYear < year:
            maxYear = year
        
        element = line[15:19];
        temp = [];
        index = 19;
        
        if maxYear < year:
            maxYear = year
        if minYear > year:
            minYear = year
        
        # Years collect monthly data for each station by year
        if _id in stationTemps:
            monthlyTemps = stationTemps[_id];
        else:
            monthlyTemps = dict();    
        
        while index < 109:
            temp.append(line[index:index+5]);
            temp.append(line[index+5]);
            temp.append(line[index+6]);
            temp.append(line[index+7]);
            index = index+8;

        for i in xrange(0,len(temp)-3,4):
            month = i / 4
            temperature = float(temp[i]) / 100
            if temperature != -99.99: 
                monthlyTemps[(month,year)] = temperature;
        
        stationTemps[_id] = monthlyTemps;
        
    # Calculate avgs, keyed by id, keyed by date tuple (month, year)
    stationAvgs = dict()
    for _id in stationTemps:
        monthlyAvgs = dict()
        monthly = stationTemps[_id]
        for month in range(0,12):
            rTotal = 0
            rCount = 0
            for year in range(minYear,maxYear+1):               
                date = (month, year)
                if date in monthly:
                    data = monthly[date]
                    rTotal = rTotal + data
                    rCount = rCount + 1
                    monthlyAvgs[date] = float(rTotal) / rCount
        stationAvgs[_id] = monthlyAvgs
        

    return GHCN_DataSet(stationlist,stationTemps,stationAvgs, minYear, maxYear);

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
    data = GHCNGlypher.GetPointData()
    if point_id in StationIDs:
        _id = StationIDs[point_id];
        station = GHCN_Avg_raw.stationlist[_id];
        avg = GHCN_Avg_raw.GetRunningAvg(_id,CUR_YEAR,CUR_MONTH);
        temp = GHCN_Avg_raw.GetTemperature(_id,CUR_YEAR,CUR_MONTH);
        # print "temp: {0}, avg: {1}".format(temp,avg)
        if avg != -99.99:
            if temp != -99.99:    
                radius = 2
                if temp > avg:
                    radius = 2 + abs(float(temp)-float(avg)) # Radius is bigger by units of celcius
                else:
                    radius = 2 - abs(float(avg)-float(temp))/2
                ball.SetCenter(station.longitude,station.latitude,0.01);
                ball.SetRadius(radius)
            else:
                ball.SetRadius(0.0)
        else:
            ball.SetRadius(0.0)
    else:
        ball.SetRadius(0.0)
# MAIN
##############################################################
ren = vtkRenderer()
renwin = vtkRenderWindow()
iren = vtkRenderWindowInteractor()
camera = vtkCamera()
writer = vtkPNGWriter()

ren.SetBackground(0,0,0.2);
renwin.AddRenderer(ren);
renwin.SetSize(1000,500);
iren.SetRenderWindow(renwin);

# Use a ball to represent each station
ball = vtkSphereSource();
ball.SetRadius(0.2);
ball.SetThetaResolution(8)
ball.SetPhiResolution(8)
ball.Update();

##############
# LOAD DATA
##############
#########
## GHCN Data
############################
GHCN_Avg_raw = LoadGHCNData(GHCN_FILENAMES[0][0],GHCN_FILENAMES[0][1])
num_stations = len(GHCN_Avg_raw.stationlist)
minYear = GHCN_Avg_raw.minYear
maxYear = GHCN_Avg_raw.maxYear

# GENERATE EARTH MAP
###############################################################
# Setup data reader
earth_image = "1_world.topo.bathy.200403.3x5400x2700.jpg";
reader = vtkJPEGReader(); 
reader.SetFileName(earth_image);
reader.Update();

# Map of the Earth
mapPlane = vtkPlaneSource();
mapPlane.SetResolution(1800,900);
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
mapActor = vtkActor()
mapActor.SetMapper(mapMapper)
mapActor.SetTexture(mapTexture)

## Lookup Table
rg = 256
ball_lut = vtkLookupTable()
ball_lut.SetRampToSQRT()
ball_lut.SetNumberOfColors(rg)
# ball_lut.SetHueRange(.65,.99)
# ball_lut.SetValueRange(.4,.5)
# ball_lut.SetSaturationRange(1,1)

for i in range(rg):
    frac = float(i)/rg
    r = frac
    g = 0
    b = 1 - frac*frac
    ball_lut.SetTableValue( i, r,g,b, 1.0 )

ball_lut.Build()

kb1 = vtkSphereSource();
kb1.SetRadius(2);
kb1.SetThetaResolution(8)
kb1.SetPhiResolution(8)
kb1.Update();

kb2 = vtkSphereSource();
kb2.SetRadius(3);
kb2.SetThetaResolution(8)
kb2.SetPhiResolution(8)
kb2.Update();

kb_5 = vtkSphereSource();
kb_5.SetRadius(1);
kb_5.SetThetaResolution(8)
kb_5.SetPhiResolution(8)
kb_5.Update();

# Color Map and Ball scale
#######################
barActor = vtkScalarBarActor()
barActor.SetLookupTable(ball_lut)
barActor.SetTitle("Temperature in Degrees Celcius")
barActor.SetNumberOfLabels(5)
barActor.SetOrientationToHorizontal()
barActor.SetWidth(0.4)
barActor.SetHeight(0.05)
barActor.SetPosition(.32,.13)

kbMap1 = vtkPolyDataMapper()
kbMap1.SetInput(kb1.GetOutput())
kbMap2 = vtkPolyDataMapper()
kbMap2.SetInput(kb2.GetOutput())
kbMap_5 = vtkPolyDataMapper()
kbMap_5.SetInput(kb_5.GetOutput())

kbActor1 = vtkActor()
kbActor1.SetMapper(kbMap1)
kbActor1.GetProperty().SetColor(0,1,0)
kbActor1.SetPosition( -170, -65, 0.01 )
kbActor2 = vtkActor()
kbActor2.SetMapper(kbMap2)
kbActor2.GetProperty().SetColor(0,1,0)
kbActor2.SetPosition( -170, -75, 0.01 )
kbActor_5 = vtkActor()
kbActor_5.SetMapper(kbMap_5)
kbActor_5.GetProperty().SetColor(0,1,0)
kbActor_5.SetPosition( -170, -55, 0.01 )

kbTextActor1 = vtkTextActor()
kbTextActor1.SetInput("Average Temperature")
kbTextActor1.SetPosition(100, 179)
kbTextActor1.GetTextProperty().SetFontSize(35)
kbTextActor1.GetTextProperty().SetColor(.8,.8,.9)
kbTextActor1.GetTextProperty().ShadowOn()
kbTextActor1.GetTextProperty().SetShadowOffset(2,2)
kbTextActor2 = vtkTextActor()
kbTextActor2.SetInput("Avg  -1 deg C")
kbTextActor2.SetPosition(100, 258)
kbTextActor2.GetTextProperty().SetFontSize(35)
kbTextActor2.GetTextProperty().ShadowOn()
kbTextActor2.GetTextProperty().SetShadowOffset(2,2)
kbTextActor2.GetTextProperty().SetColor(.8,.8,.9)
kbTextActor_5 = vtkTextActor()
kbTextActor_5.SetInput("Avg  +1 deg C")
kbTextActor_5.SetPosition(100, 92)
kbTextActor_5.GetTextProperty().SetFontSize(35)
kbTextActor_5.GetTextProperty().SetColor(.8,.8,.9)
kbTextActor_5.GetTextProperty().ShadowOn()
kbTextActor_5.GetTextProperty().SetShadowOffset(2,2)

monthTextActor = vtkTextActor()
monthTextActor.SetPosition(120, 440)
monthTextActor.GetTextProperty().SetFontSize(90)
monthTextActor.GetTextProperty().SetColor(.8,.8,.9)
monthTextActor.GetTextProperty().ShadowOn()
monthTextActor.GetTextProperty().SetShadowOffset(2,2)

yearTextActor = vtkTextActor()
yearTextActor.SetPosition(170, 350)
yearTextActor.GetTextProperty().SetFontSize(90)
yearTextActor.GetTextProperty().SetColor(.8,.8,.9)
yearTextActor.GetTextProperty().ShadowOn()
yearTextActor.GetTextProperty().SetShadowOffset(2,2)


for CUR_YEAR in range(minYear,1735):
    for CUR_MONTH in range(0,13):

        ren.RemoveAllViewProps()       
        
        if CUR_MONTH == 0:
            mth = "January"
        elif CUR_MONTH == 1:
            mth = "February"
        elif CUR_MONTH == 2:
            mth = "March"
        elif CUR_MONTH == 3:
            mth = "April"
        elif CUR_MONTH == 4:
            mth = "May"
        elif CUR_MONTH == 5:
            mth = "June"
        elif CUR_MONTH == 6:
            mth = "July"
        elif CUR_MONTH == 7:
            mth = "August"
        elif CUR_MONTH == 8:
            mth = "September"
        elif CUR_MONTH == 9:
            mth = "October"
        elif CUR_MONTH == 10:
            mth = "November"
        elif CUR_MONTH == 11:
            mth = "December"    
        
        yr = "_ {0} _".format(CUR_YEAR) #Some reason, this textactor gets screwed up. The formatting just masks the issue
        monthTextActor.SetInput(mth)
        yearTextActor.SetInput(yr)
         
        GHCN_StationPts = vtkPoints()
        GHCN_StationPts.SetNumberOfPoints(num_stations)

        poly_vertex = vtkPolyVertex()
        poly_vertex.GetPointIds().SetNumberOfIds(num_stations)

        StationIDs = dict() ## Used to map PointIds back to StationIds

        ## Get spatial data (station coordinates) set up
        i=0
        minC = 10000
        maxC = -10000
        temperatures = vtkFloatArray()

        for index in GHCN_Avg_raw.stationlist:
            station = GHCN_Avg_raw.stationlist[index]
            temp = GHCN_Avg_raw.GetTemperature(index,CUR_YEAR,CUR_MONTH)
            if temp != -99.99:
                celc = temp
                if celc < minC:
                    minC = celc
                if celc > maxC:
                    maxC = celc
                temperatures.InsertNextValue(celc)
                poly_vertex.GetPointIds().SetId(i, i)
                GHCN_StationPts.InsertPoint(i, station.longitude, station.latitude, .01)
                StationIDs[i] = index
                i=i+1
                
        if minC == 10000:
            continue
        if maxC == -10000:
            continue
        
        print "Max: {0}, Min: {1}".format(maxC,minC)

        ## Unstructured Grid Data
        grid = vtkUnstructuredGrid();
        grid.Allocate(1,1);
        grid.InsertNextCell(poly_vertex.GetCellType(), poly_vertex.GetPointIds());
        grid.SetPoints(GHCN_StationPts);
        grid.GetCellData().SetScalars(temperatures)
        grid.Update()

        ## Programmable glypher g   ives us a callback for drawing the glyphs
        GHCNGlypher = vtkProgrammableGlyphFilter();
        GHCNGlypher.SetInput(grid);
        GHCNGlypher.SetSource(ball.GetOutput());
        GHCNGlypher.SetColorModeToColorByInput();
        GHCNGlypher.SetGlyphMethod(GlyphGHCN);

        ## PolyMapper
        glyphmapper = vtkPolyDataMapper();
        glyphmapper.SetInput(GHCNGlypher.GetOutput());
        glyphmapper.SetScalarRange(-18,35)
        glyphmapper.SetLookupTable(ball_lut)

        ## Actor
        glyphactor = vtkActor();
        glyphactor.SetMapper(glyphmapper);

        ren.AddActor(glyphactor);

        # Render Window
        ############################
        ren.AddActor(mapActor)
        ren.AddActor(barActor)
        ren.AddActor(kbActor1)
        ren.AddActor(kbActor2)
        ren.AddActor(kbActor_5)
        ren.AddActor(kbTextActor1)
        ren.AddActor(kbTextActor2)
        ren.AddActor(kbTextActor_5)
        ren.AddActor(monthTextActor)
        ren.AddActor(yearTextActor)

        camera.SetPosition(0,0,337)
        camera.SetFocalPoint(0,0,0)
        ren.SetActiveCamera(camera)

        renwin.Render();

        imgFilter = vtkWindowToImageFilter()
        imgFilter.SetInput(renwin)
        imgFilter.SetMagnification(3)
        imgFilter.SetInputBufferTypeToRGBA()
        imgFilter.Update()

        writer.SetFileName("output/{1}_{0}.png".format(CUR_MONTH, CUR_YEAR))
        writer.SetInput(imgFilter.GetOutput())
        writer.Write()