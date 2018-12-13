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
import shutil
from mpi4py import MPI
import shutil
from array import array
import numpy as np

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

def randomFloatStr(start, end):
  return str(random.uniform(start, end))

def randomIntStr(start, end):
  return str(random.randint(start, end))

def getChemotaxisLambda():
  MAX_CHEMOTAXIS_LAMBDA = 20
  return randomIntStr(0, MAX_CHEMOTAXIS_LAMBDA)

def getCellContact():
  MIN = -10
  MAX = 30
  return randomIntStr(MIN, MAX)

def getMediumCellContact():
  MIN = 0
  MAX = 30
  return randomIntStr(MIN, MAX)

def addChemotaxis(CompuCell3DElmnt, config):
  PluginElmnt_4=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"Chemotaxis"})
  # Select chemical field?
  ChemicalFieldElmnt=PluginElmnt_4.ElementCC3D("ChemicalField",{"Name":"FDS","Source":"DiffusionSolverFE"})
    
  # Define chemotaxis for cell type
  # TODO: iterate over cell types
  addedChemo = False
  for cell in range(1, config["numCellTypes"] + 1):
    if random.choice([True, False]):
      addedChemo = True
      ChemicalFieldElmnt.ElementCC3D("ChemotaxisByType",{"Lambda":getChemotaxisLambda(),"Type":str(cell)})
    elif cell == config["numCellTypes"] and addedChemo == False:
      # Always add chemotaxis for at least one cell type
      ChemicalFieldElmnt.ElementCC3D("ChemotaxisByType",{"Lambda":getChemotaxisLambda(),"Type":"1"})

    
  # Define chemical field
  SteppableElmnt=CompuCell3DElmnt.ElementCC3D("Steppable",{"Type":"DiffusionSolverFE"})
  DiffusionFieldElmnt=SteppableElmnt.ElementCC3D("DiffusionField",{"Name":"FDS"})
  DiffusionDataElmnt=DiffusionFieldElmnt.ElementCC3D("DiffusionData")
  DiffusionDataElmnt.ElementCC3D("FieldName",{},"FDS")
  DiffusionDataElmnt.ElementCC3D("GlobalDiffusionConstant",{},randomFloatStr(0, 1.0))
  DiffusionDataElmnt.ElementCC3D("GlobalDecayConstant",{},randomFloatStr(0, 1.0))
  
  secretionDataElement = DiffusionFieldElmnt.ElementCC3D("SecretionData")
  addedSecretion = False
  for cell in range(1, config["numCellTypes"] + 1):
    if random.choice([True, False]):
      addedSecretion = True
      secretionDataElement.ElementCC3D("Secretion", {"Type":str(cell)}, randomFloatStr(0.0, 100))
    elif cell == config["numCellTypes"] and addedSecretion == False:
      # Always add secretion for at least one cell type
      secretionDataElement.ElementCC3D("Secretion", {"Type":"1"}, randomFloatStr(0.0, 100))

  #BoundaryConditionsElmnt=DiffusionFieldElmnt.ElementCC3D("BoundaryConditions")
  #PlaneElmnt=BoundaryConditionsElmnt.ElementCC3D("Plane",{"Axis":"X"})
  #PlaneElmnt.ElementCC3D("ConstantValue",{"PlanePosition":"Min","Value":"10.0"})
  #PlaneElmnt.ElementCC3D("ConstantValue",{"PlanePosition":"Max","Value":"5.0"})
  #PlaneElmnt_1=BoundaryConditionsElmnt.ElementCC3D("Plane",{"Axis":"Y"})
  #PlaneElmnt_1.ElementCC3D("ConstantDerivative",{"PlanePosition":"Min","Value":"10.0"})
  #PlaneElmnt_1.ElementCC3D("ConstantDerivative",{"PlanePosition":"Max","Value":"5.0"})

def updateSecretion(newNode):
  diffusionSolver = newNode.getFirstElement("Steppable", CC3DXML.MapStrStr({"Type": "DiffusionSolverFE"}))
  diffusionField = diffusionSolver.getFirstElement("DiffusionField")
  secretionData = diffusionField.getFirstElement("SecretionData")
  secretionData.getFirstElement("Secretion").updateElementValue(randomFloatStr(0.0, 100.0))

def updateChemotaxisLambda(newNode):
  chemotaxis = newNode.getFirstElement("Plugin", CC3DXML.MapStrStr({"Name": "Chemotaxis"}))
  chemicalField = chemotaxis.getFirstElement("ChemicalField")
  chemicalField.getFirstElement("ChemotaxisByType").updateElementAttributes(CC3DXML.MapStrStr({"Lambda": getChemotaxisLambda()}))
  
def updateChemicalFieldConstants(newNode):
  diffusionSolver = newNode.getFirstElement("Steppable", CC3DXML.MapStrStr({"Type": "DiffusionSolverFE"}))
  diffusionField = diffusionSolver.getFirstElement("DiffusionField")
  diffusionData = diffusionField.getFirstElement("DiffusionData")
  
  if random.choice([True, False]):
    diffusionData.getFirstElement("GlobalDiffusionConstant").updateElementValue(randomFloatStr(0, 1.0))
  else:
    diffusionData.getFirstElement("GlobalDecayConstant").updateElementValue(randomFloatStr(0, 1.0))

def configureSimulation(config, path):
  CompuCell3DElmnt=ElementCC3D("CompuCell3D",{"Revision":"20150808","Version":"3.7.4"})
  PottsElmnt=CompuCell3DElmnt.ElementCC3D("Potts")
  PottsElmnt.ElementCC3D("Dimensions",{"x":str(config["simulationSize"]),"y":str(config["simulationSize"]),"z":"1"})
  PottsElmnt.ElementCC3D("Steps",{},"1010")
  PottsElmnt.ElementCC3D("Temperature",{},"10.0")
  PottsElmnt.ElementCC3D("NeighborOrder",{},"2")
  PottsElmnt.ElementCC3D("RandomSeed",{},str(random.randint(1, 999999)))
  SettingsPlugin=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"PlayerSettings"})
  SettingsPlugin.ElementCC3D("VisualControl",{"ScreenshotFrequency":"1000"})
  PluginElmnt=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"CellType"})
  PluginElmnt.ElementCC3D("CellType",{"TypeId":"0","TypeName":"Medium"})
    
  # Define cell types
  # TODO use variable ratio of cell types
  for cell in range(1, config["numCellTypes"] + 1):
      PluginElmnt.ElementCC3D("CellType",{"TypeId":str(cell),"TypeName":str(cell)})
    
  PluginElmnt_1=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"Volume"})
    
  # Define volume for cell types
  for cell in range(1, config["numCellTypes"] + 1):
    volume = random.randint(20, 30)
    lambdaVolume = volume / 2#randomIntStr(0, 100)
    PluginElmnt_1.ElementCC3D("VolumeEnergyParameters",{"CellType":str(cell),"LambdaVolume": str(lambdaVolume), "TargetVolume": str(volume)})
    
    
  # Define surface for cell types
  PluginElmnt_2=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"Surface"})
  for cell in range(1, config["numCellTypes"] + 1):
      PluginElmnt_2.ElementCC3D("SurfaceEnergyParameters",{"CellType":str(cell),"LambdaSurface":"2.0","TargetSurface":"25"})
    
  #CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"CenterOfMass"})
  PluginElmnt_3=CompuCell3DElmnt.ElementCC3D("Plugin",{"Name":"Contact"})
  PluginElmnt_3.ElementCC3D("Energy",{"Type1":"Medium","Type2":"Medium"},"0.0")
    
  # Define contact for cell types
  for cell in range(1, config["numCellTypes"] + 1):
      PluginElmnt_3.ElementCC3D("Energy",{"Type1":"Medium","Type2":str(cell)}, getMediumCellContact())
      for cell2 in range(cell, config["numCellTypes"] + 1):
          PluginElmnt_3.ElementCC3D("Energy",{"Type1":str(cell),"Type2":str(cell2)}, getCellContact())
  PluginElmnt_3.ElementCC3D("NeighborOrder",{},"2")
    
  #if random.choice([True, False]):
  addChemotaxis(CompuCell3DElmnt, config)

  # Define initialization parameters
  SteppableElmnt_1=CompuCell3DElmnt.ElementCC3D("Steppable",{"Type":"RandomFieldInitializer"})
  SteppableElmnt_1.ElementCC3D("offset",{"x":"10","y":"10","z":"0"})
  SteppableElmnt_1.ElementCC3D("growthsteps",{},"10")
  SteppableElmnt_1.ElementCC3D("order",{},"2")
  SteppableElmnt_1.ElementCC3D("types",{},",".join(str(i) for i in range(1, config["numCellTypes"] + 1)))
  SteppableElmnt_1.ElementCC3D("ncells",{},str(config["ncells"]))
  SteppableElmnt_1.ElementCC3D("seed",{},randomIntStr(1, 999999))
  #SteppableElmnt_1=CompuCell3DElmnt.ElementCC3D("Steppable",{"Type":"UniformInitializer"})
  #RegionElmnt=SteppableElmnt_1.ElementCC3D("Region")
  #RegionElmnt.ElementCC3D("BoxMin",{"x":"10","y":"10","z":"0"})
  #RegionElmnt.ElementCC3D("BoxMax",{"x":str(simulationSize - 10),"y":str(simulationSize - 10),"z":"1"})
  #RegionElmnt.ElementCC3D("Gap",{},"5")
  #RegionElmnt.ElementCC3D("Width",{},str(width))
  #RegionElmnt.ElementCC3D("Types",{},",".join(str(i) for i in range(1, config["numCellTypes"] + 1)))
 
  # TRICKY: need to saveXML from here. For some reason saving after returning results in a blank file.
  CompuCell3DElmnt.CC3DXMLElement.saveXML(path + "/simulation.xml")

  return CompuCell3DElmnt

def updateContact(newNode):
  max = 30
  print("x")  
  contact = newNode.getFirstElement("Plugin", CC3DXML.MapStrStr({"Name": "Contact"}))
  print("x")  
  # Allow updating contact energy between any two cell types except for Medium-Medium
  node = contact.getFirstElement("Energy")
  if node.getAttribute("Type1") == "Medium":
    newContact = getMediumCellContact()
  else:
    newContact = getCellContact()


#def updateSurface(newNode):
#  cellType = random.randint(1, numCellTypes)
#  surface = newNode.getFirstElement("Plugin", CC3DXML.MapStrStr({"Name":"Surface"}))
#  surfaceParams = surface.getFirstElement("SurfaceEnergyParameters", CC3DXML.MapStrStr({"CellType": str(cellType)}))
#  surfaceParams.updateElementAttributes(CC3DXML.MapStrStr({ "TargetSurface": randomIntStr(12, 25) }))

def newSeed(node, path):
  converter = Xml2Obj()
  newNode = converter.ParseString(node)
  newNode.getFirstElement("Potts").getFirstElement("RandomSeed").updateElementValue(str(random.randint(1, 999999)))
  initializer = newNode.getFirstElement("Steppable", CC3DXML.MapStrStr({"Type": "RandomFieldInitializer" }))
  initializer.getFirstElement("seed").updateElementValue(randomIntStr(1, 999999))
  
  # TRICKY: need to saveXML from here. For some reason saving after returning results in a blank file.
  newNode.saveXML(path + "/simulation.xml")
  return newNode

def writeSimulationFile(node, path):
  converter = Xml2Obj()
  newNode = converter.ParseString(node)
  newNode.saveXML(path + "/simulation.xml")

def randomWalk(node, path):
  print("a")
  converter = Xml2Obj()
  print("a")
  newNode = converter.ParseString(node)

  print("a")
  if (newNode.getFirstElement("Plugin", CC3DXML.MapStrStr({"Name": "Chemotaxis"})) != None):
    choice = random.randint(1, 4)
    if choice == 1:
      updateContact(newNode)
    elif choice == 2:
      updateChemotaxisLambda(newNode)
    elif choice == 3:
      updateChemicalFieldConstants(newNode)
    elif choice == 4:
      updateSecretion(newNode)
  else:
    updateContact(newNode)
  
  print("e")
  # TRICKY: need to saveXML from here. For some reason saving after returning results in a blank file.
  newNode.saveXML(path + "/simulation.xml")

  return newNode.getCC3DXMLElementString()
  
# Get the most recent PNG file
def getFiles(outputPath):
  #all_subdirs = [os.path.join(path, d) for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
  #latest_subdir = max(all_subdirs, key=os.path.getmtime)
  #files = glob.glob(latest_subdir + "/*.png")
  files = glob.glob(outputPath + "/*.png")
  return files

# http://stackoverflow.com/questions/1359383/python-run-a-process-and-kill-it-if-it-doesnt-end-within-one-hour
def wait_timeout(proc, seconds):
  """Wait for a process to finish, or raise exception after timeout"""
  start = time.time()
  end = start + seconds
  interval = min(seconds / 1000.0, .25)

  while True:
    result = proc.poll()
    if result is not None:
      return result
    if time.time() >= end:
      raise RuntimeError("Process timed out")
    time.sleep(interval)

def invokeCommand(command):
  proc = subprocess.Popen(command)
  try:
    # TRICKY: The CC3D simulator occasionally freezes when starting. If the simulation hasn't finished
    # in 5 minutes then terminate it and start over.
    wait_timeout(proc, 300)
  except RuntimeError:
    invokeCommand(command)

def testNode(node, outputPath, simulationPath, iter):
    newSeed(node, simulationPath)
    savePath = outputPath + "/" + str(iter) + "-" + str(rank)
    command = environ["PREFIX_CC3D"] + "/compucell3d.bat --exitWhenDone -i " + simulationPath + "/simulation.cc3d -o " + savePath
    invokeCommand(command)
    imageFile = max(getFiles(savePath), key=os.path.getmtime)
    return imageFile
    #return max(getFiles(savePath), key=os.path.getmtime))
#  return (setComplexity.setComplexity(files, path), files[0])

def writeBest(path, node, value, bestPng):
  bestFile = open(path + "/Best.txt", "a+")
  bestFile.write("%s\n" % value)
  bestFile.close()
  xmlFile = open(path + "/Best.xml", "w+")
  xmlFile.write(node)
  xmlFile.close()
  shutil.copyfile(bestPng, path + "/Best.png")
  
def writeComplexity(path, value):
  bestFile = open(path + "/Complexity.txt", "a+")
  bestFile.write("%s\n" % value)
  bestFile.close()

def getNewConfig():
  return {
    "simulationSize": 125,
    "numCellTypes": random.randint(1, 2),
    "ncells": 100
  }

def run(path):
  import time
  outputPath = path + "/Output/" + str(int(time.time()))
  basePath = path + "/Simulation"
  simulationPath = path + "/Simulation" + str(rank)
  if not os.path.exists(simulationPath):
    shutil.copytree(basePath, simulationPath)

  iteration = 0
  currentNode = []
  if rank == 0:
    if not os.path.exists(outputPath):
      os.makedirs(outputPath)

    config = getNewConfig()
    element = configureSimulation(config, simulationPath)
    currentNode = element.CC3DXMLElement.getCC3DXMLElementString()

  currentNode = comm.bcast(currentNode, root = 0)
  writeSimulationFile(currentNode, simulationPath)
  sys.stdout.flush()
  outFile = testNode(currentNode, outputPath, simulationPath, iteration)
  files = comm.gather(outFile, root = 0)
  sys.stdout.flush()
  
  currentComplexity = 0
  imageFile = ""
  if rank == 0:
    currentComplexity, imageFile = (setComplexity.setComplexity(files, path), files[0])
    writeBest(outputPath, currentNode, currentComplexity, imageFile)
    writeComplexity(outputPath, currentComplexity)

  sys.stdout.flush()
  bestCount = 1 # number of iterations that best has not improved

  while bestCount < 20:
    iteration += 1
    sys.stdout.flush()

    sys.stdout.flush()
    newNode = ""
    if rank == 0:
      newNode = randomWalk(currentNode, simulationPath)

    sys.stdout.flush()
    currentNode = comm.bcast(newNode, root = 0)
    sys.stdout.flush()
    writeSimulationFile(currentNode, simulationPath)
    sys.stdout.flush()
    outFile = testNode(currentNode, outputPath, simulationPath, iteration)
    sys.stdout.flush()
    files = comm.gather(outFile, root = 0)
    sys.stdout.flush()

    if rank == 0:
      newComplexity, imageFile = (setComplexity.setComplexity(files, path), files[0])
      writeComplexity(outputPath, newComplexity)
      if (newComplexity > currentComplexity):
        writeBest(outputPath, newNode, newComplexity, imageFile)
        bestCount = 0
        currentNode = newNode
        currentComplexity = newComplexity
      bestCount += 1
    bestCount = comm.bcast(bestCount, root = 0)

  return currentNode

if __name__ == "__main__":
  path = sys.argv[1]
  #while True:
  run(path)
