# ********************************************************************************
#
#		Abaqus Standard 2016 Pre-Processing Script
#
#		Generates an ABAQUS model (.cae) file which performs load/unload simulations
# 		for parametric stent geometries
#
#		Author: Ross Blair
# 		Date:	18/02/17
#
# ********************************************************************************
#
from part import *
from material import *
from section import *
from optimization import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
import __main__
import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import step
import interaction
import load
import mesh
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior
#
# ********************************************************************************
# Material models
# ********************************************************************************
#
# PLLA
execfile('PLLA.py')
#
# PET
m = mdb.models['Model-1']
m.Material(name='PET')
mat = mdb.models['Model-1'].materials['PET']
mat.Density(table=((1.38e-09, ), ))
mat.Elastic(table=((2500.0, 0.4), ))
#
# ********************************************************************************
# Analysis procedure
# ********************************************************************************
#
# Step
time_period = 1
m.StaticStep(initialInc=0.1, maxInc=1, maxNumInc=10000, minInc=1e-5, name='INFLATE', 
nlgeom=ON, previous='Initial', timePeriod=time_period)
m.StaticStep(initialInc=0.1, maxInc=1, maxNumInc=10000, minInc=1e-5, name='RECOIL-2', 
nlgeom=ON, previous='INFLATE', timePeriod=time_period)
#
# ********************************************************************************
# Balloon geometry
# ********************************************************************************
#
blen = 7.0
bdia = 1.4
#
m.ConstrainedSketch(name='__profile__', sheetSize=20.0)
s = mdb.models['Model-1'].sketches['__profile__']
s.ConstructionLine(point1=(-10.0, 0.0), point2=(10.0, 0.0))
s.FixedConstraint(entity=s.geometry[2])
s.Line(point1=(blen/2, bdia/2), point2=(-blen/2, bdia/2))
s.HorizontalConstraint(addUndoState=False, entity=s.geometry[3])
m.Part(dimensionality=THREE_D, name='BALLOON', type=DEFORMABLE_BODY)
m.parts['BALLOON'].BaseShellRevolve(angle=360.0, 
flipRevolveDirection=OFF, sketch=s)
del s
#
# Reference points
p = m.parts['BALLOON']
p.ReferencePoint(point=(0.0, 0.0, 0.0))
#
# Sets (pre-mesh) and section assignment
p.Set(faces=p.faces.getByBoundingBox(-10,-10,-10,10,10,10), 
name='BODY', referencePoints=(p.referencePoints[2], ))
m.HomogeneousShellSection(idealization=NO_IDEALIZATION, 
integrationRule=SIMPSON, material='PET', name='BALLOON', numIntPts=5, 
poissonDefinition=DEFAULT, preIntegrate=OFF, temperature=GRADIENT, thickness=0.02, 
thicknessField='', thicknessModulus=None, thicknessType=UNIFORM, useDensity=OFF)
p.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE, region=
p.sets['BODY'], sectionName='BALLOON', thicknessAssignment=FROM_SECTION)
#
# Create surfaces
p.Surface(name='SURFACE', 
side1Faces=p.faces.getByBoundingBox(-10,-10,-10,10,10,10))
#
# ********************************************************************************
# Mesh
# ********************************************************************************
#
# Balloon
p = m.parts['BALLOON']
p.seedEdgeBySize(constraint=FINER, deviationFactor=0.1, edges=
p.edges.getByBoundingBox(-10,-10,-10,10,10,10), size=0.1)
m.parts['BALLOON'].generateMesh()
#
bnodemin = blen/2 - 0.05
bnodemax = blen/2 + 0.05
bnoderad = bdia + 0.05
#
p = m.parts['BALLOON']
p.Set(name='ALL NODES', 
nodes=p.nodes.getByBoundingBox(-10,-10,-10,10,10,10))
p.Set(name='END NODES 1', 
nodes=p.nodes.getByBoundingBox(
-bnodemax,-bnoderad,-bnoderad,-bnodemin,bnoderad,bnoderad))
p.Set(name='END NODES 2', 
nodes=p.nodes.getByBoundingBox(
bnodemin,-bnoderad,-bnoderad,bnodemax,bnoderad,bnoderad))
#
# ********************************************************************************
# Stent geometry
# ********************************************************************************
#
# Import .sat file 
mdb.openAcis('Stent.SAT',scaleFromFile=OFF)
m = mdb.models['Model-1']
m.PartFromGeometryFile(combine=False, dimensionality=THREE_D, 
geometryFile=mdb.acis, name='Multilink Stent (Half)-1', type=DEFORMABLE_BODY)
m.PartFromGeometryFile(bodyNum=2, combine=False, dimensionality=THREE_D, 
geometryFile=mdb.acis, name='MULTILINK-STENT', type=DEFORMABLE_BODY)
#
# Delete additional models generated by Abaqus
del m.parts['Multilink Stent (Half)-1']
#
# Calculate total number of vertices
p = m.parts['MULTILINK-STENT']
numbervertices = p.vertices[-1].index
#
p.DatumPlaneByThreePoints(
point1 = p.vertices[234], 
point2 = p.vertices[235], 
point3 = p.vertices[208])
p.DatumPlaneByThreePoints(
point1 = p.vertices[466], 
point2 = p.vertices[314], 
point3 = p.vertices[309])
p.DatumPlaneByThreePoints(
point1 = p.vertices[356], 
point2 = p.vertices[361], 
point3 = p.vertices[249])
p.DatumPlaneByThreePoints(
point1 = p.vertices[327], 
point2 = p.vertices[343], 
point3 = p.vertices[263])
p.DatumPlaneByThreePoints(
point1 = p.vertices[321], 
point2 = p.vertices[304], 
point3 = p.vertices[170])
p.DatumPlaneByThreePoints(
point1 = p.vertices[455], 
point2 = p.vertices[301], 
point3 = p.vertices[296])
p.DatumPlaneByThreePoints(
point1 = p.vertices[338], 
point2 = p.vertices[270], 
point3 = p.vertices[237])
p.DatumPlaneByThreePoints(
point1 = p.vertices[435], 
point2 = p.vertices[431], 
point3 = p.vertices[426])
p.DatumPlaneByThreePoints(
point1 = p.vertices[286], 
point2 = p.vertices[291], 
point3 = p.vertices[192])
#
p.DatumPlaneByThreePoints(
point1 = p.vertices[149], 
point2 = p.vertices[130], 
point3 = p.vertices[498])
p.DatumPlaneByThreePoints(
point1 = p.vertices[190], 
point2 = p.vertices[189], 
point3 = p.vertices[406])
p.DatumPlaneByThreePoints(
point1 = p.vertices[140], 
point2 = p.vertices[139], 
point3 = p.vertices[487])
p.DatumPlaneByThreePoints(
point1 = p.vertices[240], 
point2 = p.vertices[241], 
point3 = p.vertices[278])
p.DatumPlaneByThreePoints(
point1 = p.vertices[178], 
point2 = p.vertices[179], 
point3 = p.vertices[396])
p.DatumPlaneByThreePoints(
point1 = p.vertices[214], 
point2 = p.vertices[213], 
point3 = p.vertices[443])
#
p.DatumPlaneByThreePoints(
point1 = p.vertices[379], 
point2 = p.vertices[421], 
point3 = p.vertices[229])
p.DatumPlaneByThreePoints(
point1 = p.vertices[313], 
point2 = p.vertices[430], 
point3 = p.vertices[99])
#
p.DatumPlaneByPrincipalPlane(offset=0.0, principalPlane=XYPLANE)
plane_offset = fabs(p.vertices[285].pointOn[0][2]) - fabs(p.vertices[337].pointOn[0][2])
p.DatumPlaneByPrincipalPlane(offset=plane_offset, principalPlane=XYPLANE)
p.DatumPlaneByPrincipalPlane(offset=-plane_offset, principalPlane=XYPLANE)
p.DatumPlaneByThreePoints(
point1=p.InterestingPoint(p.edges[605], MIDDLE), 
point2=p.InterestingPoint(p.edges[372], MIDDLE), 
point3=p.InterestingPoint(p.edges[226], MIDDLE))
p.DatumPlaneByThreePoints(
point1=p.InterestingPoint(p.edges[222], MIDDLE), 
point2=p.InterestingPoint(p.edges[198], MIDDLE), 
point3=p.InterestingPoint(p.edges[595], MIDDLE))
p.DatumPlaneByPrincipalPlane(offset=0.0, principalPlane=YZPLANE)
#
# Partition cells using datum planes
numberdatumplanes = p.datums.keys()
for i in numberdatumplanes:
	p.PartitionCellByDatumPlane(
	cells=p.cells.getByBoundingBox(-10,-10,-10,10,10,10),datumPlane=p.datums[i])
#
# Reference Point
p.ReferencePoint(point=(0.0, 0.0, 0.0))
#
# Sets (pre-mesh) and section assignment
p.Set(cells=p.cells.getByBoundingBox(-10,-10,-10,10,10,10), name='BODY')
m.HomogeneousSolidSection(material='PLLA', name='STENT', thickness=None)
p.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE, region=
p.sets['BODY'], sectionName='STENT', thicknessAssignment=FROM_SECTION)
#
# Selecting surfaces of stent
# s = p.faces.findAt(((x_value, y_value, z_value), ))
innersurface = p.faces[585].getFacesByFaceAngle(angle=20.0)
p.Surface(name='INNER', side1Faces=innersurface)
outersurface = p.faces[512].getFacesByFaceAngle(angle=20.0)
p.Surface(name='OUTER', side1Faces=outersurface)
totalsurface = p.faces[512].getFacesByFaceAngle(angle=90.0)
p.Surface(name='TOTAL', side1Faces=totalsurface)
#
# Datum points
p.DatumPointByMidPoint(
point1=p.InterestingPoint(p.edges[571], MIDDLE), 
point2=p.InterestingPoint(p.edges[587], MIDDLE))
p.DatumPointByMidPoint(
point1=p.InterestingPoint(p.edges[234], MIDDLE), 
point2=p.InterestingPoint(p.edges[228], MIDDLE))
#
# ********************************************************************************
# Orientation
# ********************************************************************************
#
p.DatumCsysByThreePoints(coordSysType=CYLINDRICAL, name='CYLCSYS', 
origin=(0.0, 0.0, 0.0), point1=(1.0, 0.0, 0.0), point2=(1.0, 1.0, 0.0))
#
p.MaterialOrientation(additionalRotationField='', additionalRotationType=ROTATION_NONE, 
angle=0.0, axis=AXIS_3, fieldName='', localCsys=p.datums[55], orientationType=SYSTEM
, region=Region(cells=p.cells.getByBoundingBox(-10,-10,-10,10,10,10)), stackDirection=STACK_3)
#
# ********************************************************************************
# Stent mesh
# ********************************************************************************
#
# Mesh
p.seedEdgeBySize(constraint=FINER, deviationFactor=0.1, edges=
p.edges.getByBoundingBox(-10,-10,-10,10,10,10), size=0.035)
p.generateMesh()
#
# Sets (post-mesh)
p.Set(name='ALL NODES', 
nodes=p.nodes.getByBoundingBox(-10,-10,-10,10,10,10))
#
c1 = p.vertices[348]
c2 = p.vertices[362]
c3 = p.vertices[353]
n1 = c1.getNodes()
n2 = c2.getNodes()
n3 = c3.getNodes()
p.Set(name='CENTRE NODES', nodes=(n1, n2, n3))
c3coord = fabs(p.vertices[362].pointOn[0][0])+0.005
p.Set(name='INNER NODES', 
nodes=p.nodes.getByBoundingCylinder((0,0,-10),(0,0,10),c3coord))
#
n1 = p.nodes.getByBoundingSphere(center=(779.428E-03,449.991E-03,2.5), radius=0.0001)
n2 = p.nodes.getByBoundingSphere(center=(-779.418E-03,450.009E-03,2.5), radius=0.0001)
n3 = p.nodes.getByBoundingSphere(center=(0.0,-900.E-03,2.5), radius=0.0001)
p.Set(name='END NODES L PLANAR', nodes=(n1, n2, n3))
#
n1 = p.nodes.getByBoundingSphere(center=(900.E-03,0.0,-2.5), radius=0.0001)
n2 = p.nodes.getByBoundingSphere(center=(-450.E-03,779.423E-03,-2.5), radius=0.0001)
n3 = p.nodes.getByBoundingSphere(center=(-450.E-03,-779.423E-03,-2.5), radius=0.0001)
p.Set(name='END NODES R PLANAR', nodes=(n1, n2, n3))
#
zcoord = p.vertices[165].pointOn[0][2]
#
left1 = zcoord-0.0001
left2 = zcoord+0.0001
p.Set(nodes=p.nodes.getByBoundingCylinder((0,0,left1),(0,0,left2),10),
name='END NODES L')
#
right1 = -zcoord+0.0001
right2 = -zcoord-0.0001
p.Set(nodes=p.nodes.getByBoundingCylinder((0,0,right1),(0,0,right2),10),
name='END NODES R')
#
# ********************************************************************************
# Model generation
# ********************************************************************************
#
# Assembly
a = m.rootAssembly
a.DatumCsysByThreePoints(coordSysType=CYLINDRICAL, name='CYLCSYS', 
origin=(0.0, 0.0, 0.0), point1=(0.0, 0.0, -1.0), point2=(0.0, 1.0, -1.0))
a.Instance(dependent=ON, name='MULTILINK-STENT-1', part=p)
i = a.instances['MULTILINK-STENT-1']
a.ReferencePoint(point=i.datums[53])
a.ReferencePoint(point=i.datums[54])
p = m.parts['BALLOON']
a.Instance(dependent=ON, name='BALLOON-1', part=p)
a.ParallelEdge(fixedAxis=
a.instances['BALLOON-1'].edges[0], flip=ON, movableAxis=
a.instances['MULTILINK-STENT-1'].edges[3])
a.CoincidentPoint(fixedPoint=a.instances['BALLOON-1'].referencePoints[2]
, movablePoint=a.instances['MULTILINK-STENT-1'].referencePoints[48])
#
# Sets in assembly (post-mesh)
a.Set(name='CTRL R', referencePoints=(a.referencePoints[4], ))
a.Set(name='CTRL L', referencePoints=(a.referencePoints[5], ))
#
# Contact
m.ContactProperty('GENERAL')
#
m.SurfaceToSurfaceContactStd(adjustMethod=NONE, 
clearanceRegion=None, createStepName='INFLATE', datumAxis=None, 
initialClearance=OMIT, interactionProperty='GENERAL', 
master=a.instances['BALLOON-1'].surfaces['SURFACE'], name='INFLATE', 
slave=a.instances['MULTILINK-STENT-1'].surfaces['INNER'], 
sliding=SMALL, thickness=ON)
#
# Amplitudes
m.SmoothStepAmplitude(data=((0.0, 0.0), (time_period, 1.0), (2*time_period, 0.0)), 
name='INFLATION', timeSpan=TOTAL)
#
# Boundary conditions
m.DisplacementBC(amplitude=UNSET, createStepName='INFLATE', 
distributionType=UNIFORM, fieldName='', fixed=OFF, 
localCsys=a.datums[1], name='STENT BC', 
region=a.instances['MULTILINK-STENT-1'].sets['CENTRE NODES']
, u1=UNSET, u2=0.0, u3=0.0, ur1=UNSET, ur2=UNSET, ur3=UNSET)
#
m.DisplacementBC(amplitude='INFLATION', createStepName='INFLATE', 
distributionType=UNIFORM, fieldName='', fixed=OFF, 
localCsys=a.datums[1], name='BALLOON DISP', 
region=a.instances['BALLOON-1'].sets['ALL NODES']
, u1=1.05, u2=UNSET, u3=UNSET, ur1=UNSET, ur2=UNSET, ur3=UNSET)
#
m.DisplacementBC(amplitude=UNSET, createStepName='INFLATE', 
distributionType=UNIFORM, fieldName='', fixed=OFF, 
localCsys=a.datums[1], name='BALLOON BC', 
region=a.instances['BALLOON-1'].sets['ALL NODES']
, u1=UNSET, u2=0, u3=0, ur1=UNSET, ur2=UNSET, ur3=UNSET)
#
# ********************************************************************************
# Output data
# ********************************************************************************
#
# Job
mdb.Job(activateLoadBalancing=False, atTime=None, contactPrint=OFF, 
description='', echoPrint=OFF, explicitPrecision=SINGLE, historyPrint=OFF, 
memory=90, memoryUnits=PERCENTAGE, model='Model-1', modelPrint=OFF, 
multiprocessingMode=DEFAULT, name='RECOIL', nodalOutputPrecision=
SINGLE, numCpus=5, numDomains=5, parallelizationMethodExplicit=DOMAIN, 
queue=None, resultsFormat=ODB, scratch='', type=ANALYSIS, userSubroutine=''
, waitHours=0, waitMinutes=0)
#
# Field output
m.FieldOutputRequest(createStepName='INFLATE', name='F-Output-1', 
timeInterval=0.1, timeMarks=ON, 
variables=('S', 'PE', 'PEEQ', 'PEMAG', 'LE', 'U', 'RF', 'CF', 'CSTRESS', 'CDISP', 'COORD'))
#
# History output
m.HistoryOutputRequest(createStepName='INFLATE', name='H-Output-1', 
timeInterval=0.1, timeMarks=ON, 
variables=PRESELECT)
#
m.steps['INFLATE'].Restart(frequency=0, numberIntervals=0, overlay=OFF, timeMarks=OFF)
m.steps['RECOIL-2'].Restart(frequency=1, numberIntervals=0, overlay=ON, timeMarks=OFF)
#
# Node labels for assembly level set generation
m = mdb.models['Model-1']
a = m.rootAssembly
i = a.instances['MULTILINK-STENT-1']
p = m.parts['MULTILINK-STENT']
#
paramsFile = open('leftplanarnodes.txt','w')
leftendnodes = i.sets['END NODES L PLANAR'].nodes
for j in range(len(leftendnodes)):
	nodelabels = leftendnodes[j].label
	paramsFile.write(str(nodelabels) + ',')
paramsFile.close()
#
paramsFile = open('rightplanarnodes.txt','w')
leftendnodes = i.sets['END NODES R PLANAR'].nodes
for j in range(len(leftendnodes)):
	nodelabels = leftendnodes[j].label
	paramsFile.write(str(nodelabels) + ',')
paramsFile.close()
#
paramsFile = open('leftnodes.txt','w')
leftendnodes = i.sets['END NODES L'].nodes
for j in range(len(leftendnodes)):
	nodelabels = leftendnodes[j].label
	paramsFile.write(str(nodelabels) + ',')
paramsFile.close()
#
paramsFile = open('rightnodes.txt','w')
rightendnodes = i.sets['END NODES R'].nodes
for j in range(len(rightendnodes)):
	nodelabels = rightendnodes[j].label
	paramsFile.write(str(nodelabels) + ',')
paramsFile.close()
#
paramsFile = open('centrenodes.txt','w')
centrenodes = i.sets['CENTRE NODES'].nodes
for j in range(len(centrenodes)):
	nodelabels = centrenodes[j].label
	paramsFile.write(str(nodelabels) + ',')
paramsFile.close()
#
paramsFile = open('innernodes.txt','w')
innernodes = i.sets['INNER NODES'].nodes
for j in range(len(innernodes)):
	nodelabels = innernodes[j].label
	paramsFile.write(str(nodelabels) + ',')
paramsFile.close()
#
m = mdb.models['Model-1']
p = m.parts['MULTILINK-STENT']
a = m.rootAssembly
#
leftrp = p.datums[53].pointOn
x = leftrp[0]
y = leftrp[1]
z = leftrp[2]
paramsFile = open('leftrp.txt','w')
paramsFile.write(str(x)+ '\n' + str(y) + '\n' + str(z))
paramsFile.close()
#
rightrp = p.datums[54].pointOn
x = rightrp[0]
y = rightrp[1]
z = rightrp[2]
paramsFile = open('rightrp.txt','w')
paramsFile.write(str(x)+ '\n' + str(y) + '\n' + str(z))
paramsFile.close()
#
# Face label for assembly level surface generation
paramsFile = open('outersurfaceface.txt','w')
paramsFile.write(str(512))
paramsFile.close()
#
# Axial edge label for rigid plate orientation
paramsFile = open('axialedge.txt','w')
paramsFile.write(str(3))
paramsFile.close()
#
# Outer surface area of stent
surfaceAreaOuter = 0.0
surfaceAreaMatrix = a.instances['MULTILINK-STENT-1'].surfaces['OUTER'].faces
for i in range(len(surfaceAreaMatrix)):
	surfaceAreaOuter = surfaceAreaOuter + surfaceAreaMatrix[i].getSize()
#
paramsFile = open('surfaceAreaOuter.txt','w')
paramsFile.write(str(surfaceAreaOuter))
paramsFile.close()
#
# Total surface area of stent
surfaceAreaTotal = 0.0
surfaceAreaMatrix = a.instances['MULTILINK-STENT-1'].surfaces['TOTAL'].faces
for i in range(len(surfaceAreaMatrix)):
	surfaceAreaTotal = surfaceAreaTotal + surfaceAreaMatrix[i].getSize()
#
paramsFile = open('surfaceAreaTotal.txt','w')
paramsFile.write(str(surfaceAreaTotal))
paramsFile.close()
#
# Save .cae file for restart analysis
mdb.saveAs(pathName="RECOIL")
#
# Generate and submit input file
mdb.jobs['RECOIL'].writeInput(consistencyChecking=OFF)
# mdb.jobs['RECOIL'].submit(consistencyChecking=OFF)
# #
# # Wait for completion
# mdb.jobs['RECOIL'].waitForCompletion()
#
# ********************************************************************************
