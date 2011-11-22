from vtk import *

# Setup data reader
earth_image = "1_world.topo.bathy.200403.3x5400x2700.jpg";
reader = vtkJPEGReader(); 
reader.SetFileName(earth_image);
reader.Update();

mapPlane = vtkPlaneSource();
mapPlane.SetResolution(1000,500);
mapPlane.SetNormal(0,0,1);
mapPlane.SetOrigin(-180,-90,-0.01);
mapPlane.SetPoint1(180,-90,-0.01);
mapPlane.SetPoint2(-180,90,-0.01);

mapMapper = vtkPolyDataMapper();
mapMapper.SetInput(mapPlane.GetOutput());

mapTexture = vtkTexture();
mapTexture.SetInput(reader.GetOutput());

mapActor = vtkActor();
mapActor.SetMapper(mapMapper);
mapActor.SetTexture(mapTexture);

ren = vtkRenderer();
ren.AddActor(mapActor);
renwin = vtkRenderWindow();
renwin.AddRenderer(ren);
iren = vtkRenderWindowInteractor();
iren.SetRenderWindow(renwin);
ren.SetBackground(0,0,0.2);
renwin.SetSize(720,720);

renwin.Render();
ren.ResetCamera();

iren.Initialize();
iren.Start();