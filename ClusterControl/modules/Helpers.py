import elementtree.ElementTree as ET
from PyQt4 import QtCore, QtGui
#import xml.dom.minidom.parseString
from xml.dom.minidom import parseString
CLUSTER_TOKEN = "cluster"
CLUSTER_NODES = "cluster_nodes"
NODE          = "node"

class AppOption:
   """ Encapsulation of command-line options that may be passed to apps. """
   def __init__(self, xmlElt):
      self.label = xmlElt.get("label")
      self.flag  = xmlElt.get("flag")
      self.tip   = xmlElt.get("tooltip")

      enabled = xmlElt.get("enabled")

      if enabled == "" or enabled == None:
         self.enabled = True
      elif enabled == "true" or enabled == "1":
         self.enabled = True
      else:
         self.enabled = False

      selected = xmlElt.get("selected")

      if selected == "" or selected == None:
         self.selected = False
      elif selected == "true" or selected == "1":
         self.selected = True
      else:
         self.selected = False

      print "self.label: ", self.label
      print "self.flag: ", self.flag
      print "self.tip: ", self.tip
      print "self.enabled: ", self.enabled
      print "self.selected: ", self.selected

class AppExclusiveOption:
   def __init__(self, xmlElt):
      self.group_name = xmlElt.get("name")
      self.options = []

      print "AppExclusiveOption name=", self.group_name

      opts = xmlElt.findall("./option")
      for o in opts:
         self.options.append(AppOption(o))

class Application:
   """ Representation of an application that can be launched. """

   def __init__(self, xmlElt):
      self.name = xmlElt.get("name")

      # Could this be any uglier?  I need to learn the Python XML API better...
      self.command = xmlElt.find("./command").text

      help_elts = xmlElt.findall("./helpURL")
      if None != help_elts and len(help_elts) > 0 and help_elts[0].text:
         self.helpURL = help_elts[0].text
      else:
         self.helpURL = None

      tip = self.name  # Fallback in case no tooltip is defined

      tip_elts = xmlElt.findall("./tooltip")
      if None != tip_elts and len(tip_elts) > 0:
         tip = tip_elts[0].text

      self.tip = tip

      self.options = []
      options_elts = xmlElt.findall("./options")
      if None != options_elts and len(tip_elts) > 0:
         option_list = options_elts[0]

         for n in option_list.findall("./option"):
            self.options.append(AppOption(n))
         for n in option_list.findall("./group"):
            self.options.append(AppExclusiveOption(n))
      
      print "App.name", self.name
      print "App.command", self.command
      print "App.helpURL", self.helpURL
      print "App.tip", self.tip

   def getName(self):
      return self.name

   def getCommand(self):
      return self.command

   def getTip(self):
      return self.tip

   def getHelpURL(self):
      return self.helpURL

   def getOptions(self):
      return self.options

class Action:
   """
   Representation of user-defined action buttons displayed in the controls
   panel.
   """
   def __init__(self, xmlElt):
      self.name    = xmlElt.get("name")
      self.command = xmlElt.findall("./command")[0].text

      tip = xmlElt.findall("./tooltip")[0].text

      if tip == "" or tip == None:
         tip = self.name

      self.tip = tip

   def getName(self):
      return self.name

   def getTip(self):
      return self.tip




class ClusterModel(QtCore.QAbstractListModel):
   """Create a new cluster element"""
   def __init__(self, parent=None):
      QtCore.QAbstractListModel.__init__(self, parent)

      self.mElement = ET.Element(CLUSTER_TOKEN)
      self.mNodes = ET.SubElement(self.mElement, CLUSTER_NODES)
      ET.SubElement(self.mNodes, NODE, hostname="slave1")
      ET.SubElement(self.mNodes, NODE, hostname="slave2")

   """Read file from disk."""
   def open(self, file):
      self.mElement = ET.ElementTree().parse(file)
   
   def write(self, fileName="cluster.xml"):
      doc = parseString(ET.tostring(self.mElement))
      out_file = file(fileName,'w')
      out_file.write(doc.toprettyxml())
      print "Test: \n", doc.toprettyxml()

   def data(self, index, role=QtCore.Qt.DisplayRole):
      if not index.isValid():
         return QtCore.QVariant()
        
      if role == QtCore.Qt.DecorationRole:
         return QtCore.QVariant(QtGui.QIcon(":/linux2.png"))
      elif role == QtCore.Qt.DisplayRole:
         return QtCore.QVariant(self.mNodes[index.row()].get("hostname"))
         #return QtCore.QVariant()
       
      return QtCore.QVariant()

   def rowCount(self, parent):
      if parent.isValid():
         return 0
      else:
         return len(self.mNodes)

#cluster = ET.Element(CLUSTER_TOKEN)

#title = ET.SubElement(window, "title", font="large")
#title.text = "A sample text window"

#text = ET.SubElement(window, "text", wrap="word")

#box = ET.SubElement(window, "buttonbox")
#ET.SubElement(box, "button").text = "OK"
#ET.SubElement(box, "button").text = "Cancel"

#cluster = ClusterModel()
#cluster.write()

