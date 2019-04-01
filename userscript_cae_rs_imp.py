# ********************************************************************************
#
#		ABAQUS/Explicit (6.14) Pre-Processing Script
#
#		Generates an ABAQUS model (.cae) file to assess the radial stiffness of 
# 		parametric stent geometries
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
# Import .cae file
mdb.openAuxMdb(pathName='RECOIL.cae')
mdb.copyAuxMdbModel(fromName='Model-1', toName='Model-1')
mdb.closeAuxMdb()
#
# ********************************************************************************
# Crimp tool geometry
# ********************************************************************************
#
m = mdb.models['Model-1']
m.ConstrainedSketch(name='__profile__', sheetSize=20.0)
s = mdb.models['Model-1'].sketches['__profile__']
s.ConstructionLine(point1=(-10.0, 0.0), point2=(10.0, 0.0))
s.FixedConstraint(entity=s.geometry[2])
s.rectangle(point1=(4.0, 1.0), point2=(-4.0, -1.0))
m.Part(dimensionality=THREE_D, name='CRIMP TOOL', type=DISCRETE_RIGID_SURFACE)
m.parts['CRIMP TOOL'].BaseShell(sketch=s)
del s
#
# Reference points
p = m.parts['CRIMP TOOL']
p.ReferencePoint(point=(0.0, 0.0, 0.0))
#
# Coordinate system
p.DatumCsysByThreePoints(coordSysType=CARTESIAN, line1=(1.0, 0.0, 0.0), 
line2=(0.0, 1.0, 0.0), name='CART CSYS', origin=(0.0, 0.0, 0.0))
#
# Sets (pre-mesh) and section assignment
p.Set(faces=p.faces.getByBoundingBox(-10,-10,-10,10,10,10), 
name='BODY', referencePoints=(p.referencePoints[2], ))
p.Set(name='RP', referencePoints=(p.referencePoints[2], ))
#
# Create surfaces
p.Surface(name='SURFACE', 
side1Faces=p.faces.getByBoundingBox(-10,-10,-10,10,10,10))
#
# ********************************************************************************
# Mesh
# ********************************************************************************
#
# Crimp tool
p = m.parts['CRIMP TOOL']
p.seedEdgeBySize(constraint=FINER, deviationFactor=0.1, edges=
p.edges.getByBoundingBox(-10,-10,-10,10,10,10), size=0.2)
m.parts['CRIMP TOOL'].generateMesh()
#
p = m.parts['CRIMP TOOL']
p.Set(name='ALL NODES', 
nodes=p.nodes.getByBoundingBox(-10,-10,-10,10,10,10))
#
# ********************************************************************************
# Model generation
# ********************************************************************************
#
time_period = 1
m.StaticStep(initialInc=0.1, maxInc=1, maxNumInc=10000, minInc=1e-5, name='CRIMP-2', 
nlgeom=ON, previous='Initial', timePeriod=time_period)
m.steps['INFLATE'].suppress()
m.steps['RECOIL-2'].suppress()
#
m.setValues(restartJob='RECOIL', restartStep='RECOIL-2')
m.InitialState(createStepName='Initial', endIncrement=STEP_END, endStep=LAST_STEP, 
fileName='RECOIL', instances=(m.rootAssembly.instances['MULTILINK-STENT-1'], ), 
name='Predefined Field-1', updateReferenceConfiguration=ON)
#
# Assembly level set generation
a = m.rootAssembly
i = a.instances['MULTILINK-STENT-1']
#
paramsFile = open('axialedge.txt','r')
edgelabel = [line for line in paramsFile]
edgelabel = edgelabel[0]
edgelabel = eval(edgelabel)
#
p = m.parts['CRIMP TOOL']
a.Instance(dependent=ON, name='CRIMP TOOL-1', part=p)
a.ParallelEdge(fixedAxis=
a.instances['MULTILINK-STENT-1'].edges[edgelabel], flip=ON, movableAxis=
a.instances['CRIMP TOOL-1'].edges[0])
#
a.DatumPointByCoordinate(coords=(0.0, 0.0, -2.0))
a.CoincidentPoint(fixedPoint=a.datums[15], 
movablePoint=a.instances['CRIMP TOOL-1'].referencePoints[2])
a.RadialInstancePattern(axis=(1.0, 0.0, 0.0), 
instanceList=('CRIMP TOOL-1', ), number=8, point=(2.0, 0.0, 0.0), 
totalAngle=360.0)
#
paramsFile = open('centrenodes.txt','r')
nodelabels = [line for line in paramsFile]
nodelabels = nodelabels[0]
nodelabels = eval(nodelabels)
a.SetFromNodeLabels(name='CENTRE NODES ASSY', nodeLabels=(('MULTILINK-STENT-1', 
nodelabels), ))
#
paramsFile = open('innernodes.txt','r')
nodelabels = [line for line in paramsFile]
nodelabels = nodelabels[0]
nodelabels = eval(nodelabels)
a.SetFromNodeLabels(name='INNER NODES ASSY', nodeLabels=(('MULTILINK-STENT-1', 
nodelabels), ))
#
# Assembly level surface generation
paramsFile = open('outersurfaceface.txt','r')
facelabel = [line for line in paramsFile]
facelabel = facelabel[0]
facelabel = eval(facelabel)
outersurfaceassy = i.faces[facelabel].getFacesByFaceAngle(angle=20.0)
a.Surface(name='OUTER ASSY', side1Faces=outersurfaceassy)
#
# Contact
# m.interactions['INFLATE'].suppress()
#
m.SurfaceToSurfaceContactStd(adjustMethod=NONE, 
clearanceRegion=None, createStepName='Initial', datumAxis=None, 
initialClearance=OMIT, interactionProperty='GENERAL', 
master=a.instances['CRIMP TOOL-1'].surfaces['SURFACE'], 
name='CT-1-CONTACT', slave=a.surfaces['OUTER ASSY'], 
sliding=SMALL, thickness=ON)
#
for i in range(2,9,1):
	m.SurfaceToSurfaceContactStd(adjustMethod=NONE, 
	clearanceRegion=None, createStepName='Initial', datumAxis=None, 
	initialClearance=OMIT, interactionProperty='GENERAL', 
	master=a.instances['CRIMP TOOL-1-rad-{}'.format(i)].surfaces['SURFACE'], 
	name='CT-{}-CONTACT'.format(i), slave=a.surfaces['OUTER ASSY'], 
	sliding=SMALL, thickness=ON)
#
# Amplitudes
m.SmoothStepAmplitude(data=((0.0, 0.0), (time_period, 1.0)), 
name='CRIMPING', timeSpan=TOTAL)
#
# Boundary conditions
m.DisplacementBC(amplitude=UNSET, createStepName='CRIMP-2', 
distributionType=UNIFORM, fieldName='', fixed=OFF, 
localCsys=a.datums[1], name='STENT BC', 
region=a.sets['CENTRE NODES ASSY']
, u1=UNSET, u2=0.0, u3=0.0, ur1=UNSET, ur2=UNSET, ur3=UNSET)
#
paramsFile = open('recoil_radius.txt','r')
recoilRadiusAve = [line for line in paramsFile]
recoilRadiusAve = recoilRadiusAve[0]
recoilRadiusAve = eval(recoilRadiusAve)
#
distance = 2.0 - recoilRadiusAve + 0.1 * recoilRadiusAve
#
i = a.instances['CRIMP TOOL-1']
m.DisplacementBC(amplitude='CRIMPING', createStepName=
'CRIMP-2', distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=
i.datums[3], name='DISP 1', 
region=Region(referencePoints=(i.referencePoints[2], )),
u1=0.0, u2=0.0, u3=distance, ur1=0.0, ur2=0.0, ur3=0.0)
#
i = a.instances['CRIMP TOOL-1-rad-2']
m.DisplacementBC(amplitude='CRIMPING', createStepName=
'CRIMP-2', distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=
i.datums[3], name='DISP 2', 
region=Region(referencePoints=(i.referencePoints[2], )),
u1=0.0, u2=0.0, u3=distance, ur1=0.0, ur2=0.0, ur3=0.0)
#
i = a.instances['CRIMP TOOL-1-rad-3']
m.DisplacementBC(amplitude='CRIMPING', createStepName=
'CRIMP-2', distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=
i.datums[3], name='DISP 3', 
region=Region(referencePoints=(i.referencePoints[2], )),
u1=0.0, u2=0.0, u3=distance, ur1=0.0, ur2=0.0, ur3=0.0)
#
i = a.instances['CRIMP TOOL-1-rad-4']
m.DisplacementBC(amplitude='CRIMPING', createStepName=
'CRIMP-2', distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=
i.datums[3], name='DISP 4', 
region=Region(referencePoints=(i.referencePoints[2], )),
u1=0.0, u2=0.0, u3=distance, ur1=0.0, ur2=0.0, ur3=0.0)
#
i = a.instances['CRIMP TOOL-1-rad-5']
m.DisplacementBC(amplitude='CRIMPING', createStepName=
'CRIMP-2', distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=
i.datums[3], name='DISP 5', 
region=Region(referencePoints=(i.referencePoints[2], )),
u1=0.0, u2=0.0, u3=distance, ur1=0.0, ur2=0.0, ur3=0.0)
#
i = a.instances['CRIMP TOOL-1-rad-6']
m.DisplacementBC(amplitude='CRIMPING', createStepName=
'CRIMP-2', distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=
i.datums[3], name='DISP 6', 
region=Region(referencePoints=(i.referencePoints[2], )),
u1=0.0, u2=0.0, u3=distance, ur1=0.0, ur2=0.0, ur3=0.0)
#
i = a.instances['CRIMP TOOL-1-rad-7']
m.DisplacementBC(amplitude='CRIMPING', createStepName=
'CRIMP-2', distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=
i.datums[3], name='DISP 7', 
region=Region(referencePoints=(i.referencePoints[2], )),
u1=0.0, u2=0.0, u3=distance, ur1=0.0, ur2=0.0, ur3=0.0)
#
i = a.instances['CRIMP TOOL-1-rad-8']
m.DisplacementBC(amplitude='CRIMPING', createStepName=
'CRIMP-2', distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=
i.datums[3], name='DISP 8', 
region=Region(referencePoints=(i.referencePoints[2], )),
u1=0.0, u2=0.0, u3=distance, ur1=0.0, ur2=0.0, ur3=0.0)
#
# ********************************************************************************
# Output data
# ********************************************************************************
#
# Job
mdb.Job(activateLoadBalancing=False, atTime=None, contactPrint=OFF, 
description='', echoPrint=OFF, explicitPrecision=SINGLE, historyPrint=OFF, 
memory=90, memoryUnits=PERCENTAGE, model='Model-1', modelPrint=OFF, 
multiprocessingMode=DEFAULT, name='STIFFNESS', nodalOutputPrecision=
SINGLE, numCpus=5, numDomains=5, parallelizationMethodExplicit=DOMAIN, 
queue=None, resultsFormat=ODB, scratch='', type=ANALYSIS, userSubroutine=''
, waitHours=0, waitMinutes=0)
#
# Field output
increments = 10
m.FieldOutputRequest(createStepName='CRIMP-2', name='F-Output-1', 
timeInterval=0.1, timeMarks=ON, 
variables=('S', 'PE', 'PEEQ', 'PEMAG', 'LE', 'U', 'RF', 'CF', 'CSTRESS', 'CDISP', 'COORD'))
#
# History output
m.HistoryOutputRequest(createStepName='CRIMP-2', name='H-Output-1', 
timeInterval=0.1, timeMarks=ON, 
variables=PRESELECT)
#
# Save .cae file for restart analysis
mdb.saveAs(pathName="STIFFNESS")
#
# Generate and submit input file
mdb.jobs['STIFFNESS'].writeInput(consistencyChecking=OFF)
# mdb.jobs['STIFFNESS'].submit(consistencyChecking=OFF)
# #
# # Wait for completion
# mdb.jobs['STIFFNESS'].waitForCompletion()
#
# ********************************************************************************