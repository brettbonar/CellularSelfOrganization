from __future__ import division
import sys
from os import environ
from os import getcwd
import string

sys.path.append(environ["PYTHON_MODULE_PATH"])
sys.path.append(environ["SWIG_LIB_INSTALL_DIR"])

import subprocess
import os
import glob
import random
random.seed()
from PIL import Image
import CompuCellSetup
from XMLUtils import *
import CC3DXML
from CC3DXML import *
  
import copy
import setComplexity
import time

path = "C:/Dev/CS6600/Project/Test/Output/"
#path = "C:/Users/Brett/CC3DWorkspace"
simulationSize = 100
numCellTypes = random.randint(1, 2)
ncells = 100#random.randint(100,200)

def randomFloatStr(start, end):
  return str(random.uniform(start, end))

def randomIntStr(start, end):
  return str(random.randint(start, end))

def configureSimulation(first, second):    
  CompuCell3DElmnt=ElementCC3D("CompuCell3D",{"Revision":"20150808","Version":"3.7.4"})
  PottsElmnt=CompuCell3DElmnt.ElementCC3D("Potts")
  PottsElmnt.ElementCC3D("Dimensions",{"x":str(simulationSize),"y":str(simulationSize),"z":"1"})
  PottsElmnt.ElementCC3D("Steps",{},"1010")
  PottsElmnt.ElementCC3D("Temperature",{},"10.0")
  PottsElmnt.ElementCC3D("NeighborOrder",{},"2")
  PottsElmnt.ElementCC3D("RandomSeed",{},str(random.randint(1, 999999)))
  SettingsPlugin=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"PlayerSettings"})
  SettingsPlugin.ElementCC3D("VisualControl",{"ScreenshotFrequency":"1000"})
    
  # Define cell types
  PluginElmnt=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"CellType"})
  PluginElmnt.ElementCC3D("CellType",{"TypeId":"0","TypeName":"Medium"})
  PluginElmnt.ElementCC3D("CellType",{"TypeId":"1","TypeName":"1"})
  PluginElmnt.ElementCC3D("CellType",{"TypeId":"2","TypeName":"2"})
    
    
  #surface
  PluginElmnt_2=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"Surface"})
  PluginElmnt_2.ElementCC3D("SurfaceEnergyParameters",{"CellType":"1","LambdaSurface":"2.0","TargetSurface":"25"})
  PluginElmnt_2.ElementCC3D("SurfaceEnergyParameters",{"CellType":"2","LambdaSurface":"2.0","TargetSurface":"25"})
    

  # Define volume for cell types
  PluginElmnt_1=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"Volume"})
  PluginElmnt_1.ElementCC3D("VolumeEnergyParameters",{"CellType":"1","LambdaVolume": "2", "TargetVolume": "25"})
  PluginElmnt_1.ElementCC3D("VolumeEnergyParameters",{"CellType":"2","LambdaVolume": "2", "TargetVolume": "25"})
    
  #CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"CenterOfMass"})
  PluginElmnt_3=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"Contact"})
  PluginElmnt_3.ElementCC3D("Energy",{"Type1":"Medium","Type2":"Medium"},"0.0")
    
  # Define contact for cell types
  PluginElmnt_3.ElementCC3D("Energy",{"Type1":"Medium","Type2":"1"}, "16")
  PluginElmnt_3.ElementCC3D("Energy",{"Type1":"1","Type2":"2"}, "10")
  PluginElmnt_3.ElementCC3D("Energy",{"Type1":"1","Type2":"1"}, str(first))
  PluginElmnt_3.ElementCC3D("Energy",{"Type1":"2","Type2":"2"}, str(second))
  PluginElmnt_3.ElementCC3D("NeighborOrder",{},"2")

  # Define initialization parameters
  #SteppableElmnt_1=CompuCell3DElmnt.ElementCC3D("Steppable",{"Type":"RandomFieldInitializer"})
  #SteppableElmnt_1.ElementCC3D("offset",{"x":"10","y":"10","z":"0"})
  #SteppableElmnt_1.ElementCC3D("growthsteps",{},"10")
  #SteppableElmnt_1.ElementCC3D("order",{},"2")
  #SteppableElmnt_1.ElementCC3D("types",{},"1,2")
  #SteppableElmnt_1.ElementCC3D("ncells",{},str(ncells))
  #SteppableElmnt_1.ElementCC3D("seed",{},randomIntStr(1, 999999))
  SteppableElmnt_1=CompuCell3DElmnt.ElementCC3D("Steppable",{"Type":"UniformInitializer"})
  RegionElmnt=SteppableElmnt_1.ElementCC3D("Region")
  RegionElmnt.ElementCC3D("BoxMin",{"x":"10","y":"10","z":"0"})
  RegionElmnt.ElementCC3D("BoxMax",{"x":str(simulationSize - 10),"y":str(simulationSize - 10),"z":"1"})
  RegionElmnt.ElementCC3D("Gap",{},"0")
  RegionElmnt.ElementCC3D("Width",{},"5")
  RegionElmnt.ElementCC3D("Types",{},"1,2")
  RegionElmnt.ElementCC3D("seed",{},randomIntStr(1, 999999))
  RegionElmnt.ElementCC3D("RandomSeed",{},randomIntStr(1, 999999))
 
  CompuCell3DElmnt.CC3DXMLElement.saveXML("C:/Dev/CS6600/Project/Test/Simulation/NewSimulation.xml")
  return CompuCell3DElmnt

def configureSimulationDiffusion(first, second):    
  CompuCell3DElmnt=ElementCC3D("CompuCell3D",{"Revision":"20150808","Version":"3.7.4"})
  PottsElmnt=CompuCell3DElmnt.ElementCC3D("Potts")
  PottsElmnt.ElementCC3D("Dimensions",{"x":str(simulationSize),"y":str(simulationSize),"z":"1"})
  PottsElmnt.ElementCC3D("Steps",{},"1010")
  PottsElmnt.ElementCC3D("Temperature",{},"10.0")
  PottsElmnt.ElementCC3D("NeighborOrder",{},"2")
  PottsElmnt.ElementCC3D("RandomSeed",{},str(random.randint(1, 999999)))
  SettingsPlugin=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"PlayerSettings"})
  SettingsPlugin.ElementCC3D("VisualControl",{"ScreenshotFrequency":"1000"})
    
  # Define cell types
  PluginElmnt=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"CellType"})
  PluginElmnt.ElementCC3D("CellType",{"TypeId":"0","TypeName":"Medium"})
  PluginElmnt.ElementCC3D("CellType",{"TypeId":"1","TypeName":"1"})
    
  #surface
  PluginElmnt_2=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"Surface"})
  PluginElmnt_2.ElementCC3D("SurfaceEnergyParameters",{"CellType":"1","LambdaSurface":"2.0","TargetSurface":"50"})

  # Define volume for cell types
  PluginElmnt_1=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"Volume"})
  PluginElmnt_1.ElementCC3D("VolumeEnergyParameters",{"CellType":"1","LambdaVolume": "20", "TargetVolume": "25"})
    
    
  # Define contact for cell types
  PluginElmnt_3=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"Contact"})
  PluginElmnt_3.ElementCC3D("Energy",{"Type1":"Medium","Type2":"Medium"},"0.0")
  PluginElmnt_3.ElementCC3D("Energy",{"Type1":"Medium","Type2":"1"}, "16")
  PluginElmnt_3.ElementCC3D("Energy",{"Type1":"1","Type2":"1"}, "2")
  PluginElmnt_3.ElementCC3D("NeighborOrder",{},"2")
    
  # Select chemical field?
    
  # Define chemotaxis for cell type
  PluginElmnt_4=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"Chemotaxis"})
  ChemicalFieldElmnt=PluginElmnt_4.ElementCC3D("ChemicalField",{"Name":"FDS","Source":"DiffusionSolverFE"})
  ChemicalFieldElmnt.ElementCC3D("ChemotaxisByType",{"Lambda":"2","Type":"1"})
    
  # Define chemical field?
  SteppableElmnt=CompuCell3DElmnt.ElementCC3D("Steppable",{"Type":"DiffusionSolverFE"})
  DiffusionFieldElmnt=SteppableElmnt.ElementCC3D("DiffusionField",{"Name":"FDS"})
  DiffusionDataElmnt=DiffusionFieldElmnt.ElementCC3D("DiffusionData")
  DiffusionDataElmnt.ElementCC3D("FieldName",{},"FDS")
  DiffusionDataElmnt.ElementCC3D("GlobalDiffusionConstant",{},str(first / 10))
  DiffusionDataElmnt.ElementCC3D("GlobalDecayConstant",{},str(second / 10))
  
  secretionDataElement = DiffusionFieldElmnt.ElementCC3D("SecretionData")
  secretionDataElement.ElementCC3D("Secretion", {"Type":"1"}, "20")

  # Define initialization parameters
  SteppableElmnt_1=CompuCell3DElmnt.ElementCC3D("Steppable",{"Type":"RandomFieldInitializer"})
  SteppableElmnt_1.ElementCC3D("offset",{"x":"10","y":"10","z":"0"})
  SteppableElmnt_1.ElementCC3D("growthsteps",{},"10")
  SteppableElmnt_1.ElementCC3D("order",{},"2")
  SteppableElmnt_1.ElementCC3D("types",{},"1")
  SteppableElmnt_1.ElementCC3D("ncells",{},str(ncells))
  SteppableElmnt_1.ElementCC3D("seed",{},randomIntStr(1, 999999))
  #SteppableElmnt_1=CompuCell3DElmnt.ElementCC3D("Steppable",{"Type":"UniformInitializer"})
  #RegionElmnt=SteppableElmnt_1.ElementCC3D("Region")
  #RegionElmnt.ElementCC3D("BoxMin",{"x":"10","y":"10","z":"0"})
  #RegionElmnt.ElementCC3D("BoxMax",{"x":str(simulationSize - 10),"y":str(simulationSize - 10),"z":"1"})
  #RegionElmnt.ElementCC3D("Gap",{},"0")
  #RegionElmnt.ElementCC3D("Width",{},"5")
  #RegionElmnt.ElementCC3D("Types",{},"1,2")
  #RegionElmnt.ElementCC3D("seed",{},randomIntStr(1, 999999))
  #RegionElmnt.ElementCC3D("RandomSeed",{},randomIntStr(1, 999999))
 
  CompuCell3DElmnt.CC3DXMLElement.saveXML("C:/Dev/CS6600/Project/Test/Simulation/NewSimulation.xml")
  return CompuCell3DElmnt

def newSeed(node):
  converter = Xml2Obj()
  newNode = converter.ParseString(node)
  newNode.getFirstElement("Potts").getFirstElement("RandomSeed").updateElementValue(str(random.randint(1, 999999)))
  initializer = newNode.getFirstElement("Steppable", CC3DXML.MapStrStr({"Type": "UniformInitializer"}))
  region = initializer.getFirstElement("Region")
  region.getFirstElement("seed").updateElementValue(randomIntStr(1, 999999))
  region.getFirstElement("RandomSeed").updateElementValue(randomIntStr(1, 999999))
  #initializer = newNode.getFirstElement("Steppable", CC3DXML.MapStrStr({"Type": "RandomFieldInitializer" }))
  #initializer.getFirstElement("seed").updateElementValue(randomIntStr(1, 999999))

  newNode.saveXML("C:/Dev/CS6600/Project/Test/Simulation/NewSimulation.xml")

def getFiles():
  all_subdirs = [os.path.join(path, d) for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
  latest_subdir = max(all_subdirs, key=os.path.getmtime)
  files = glob.glob(latest_subdir + "/*.png")
  return files

def testNode(node, path, first, second):
  numIterations = 4
  files = []
  for i in range(numIterations):
    newSeed(node)
    outputPath = path + "/" + str(first) + "-" + str(second) + "_" + str(i)
    command = "C:/CompuCell3D/compucell3d.bat --exitWhenDone -i C:/Dev/CS6600/Project/Test/Test.cc3d -o " + outputPath
    subprocess.call(command)
    print(command)
    files.append(max(getFiles(), key=os.path.getmtime))
  return setComplexity.setComplexity(files, path)

  
def writeComplexity(path, value, first, second):
  bestFile = open(path + "/Complexity.txt", "a+")
  bestFile.write("%s, %s-%s\n" % (value, first, second))
  bestFile.close()

def run():
  import time
  global path
  path = "C:/Dev/CS6600/Project/Test/Output/CellSortTest2"
  if not os.path.exists(path):
    os.makedirs(path)

  outputFile = open(path + "/Complexity.txt", "w+")

  for a in range(9):
    for b in range(a, 9):
      first = a * 2
      second = b * 2
      element = configureSimulation(first, second)
      currentNode = element.CC3DXMLElement.getCC3DXMLElementString()
      currentComplexity = testNode(currentNode, path, first, second)
      outputFile.write(str(currentComplexity) + ",")
    outputFile.write("\n")

#def run():
#  import time
#  global path
#  path = "C:/Dev/CS6600/Project/Test/Output/DiffusionTest"
#  if not os.path.exists(path):
#    os.makedirs(path)

#  for a in range(11):
#    for b in range(11):
#      element = configureSimulationDiffusion(a, b)
#      currentNode = element.CC3DXMLElement.getCC3DXMLElementString()
#      currentComplexity = testNode(currentNode, path, a, b)
#      writeComplexity(path, currentComplexity, a, b)

run()
