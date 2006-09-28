import os,sys
pj = os.path.join

sys.path.append( pj(os.path.dirname(__file__), "..",".."))

import unittest
import util.mixins

class MySingletonA(util.mixins.Singleton):
   def __init__(self):
      self.val = "A"   
   def returnA(self):
      return "A"

class MySingletonB(util.mixins.Singleton):
   def __init__(self):
      self.val = "B"   
   def returnB(self):
      return "B"


class MyBorgA(util.mixins.Borg):
   def __init__(self):
      self.val = "A"   
   def returnA(self):
      return "A"

class MyBorgB(util.mixins.Borg):
   def __init__(self):
      self.val = "B"   
   def returnB(self):
      return "B"


class testMixins(unittest.TestCase):
   
   def setUp(self):
      pass

   def tearDown(self):
      pass
   
   def testSingleton(self):
      a1 = MySingletonA()
      a2 = MySingletonA()
      
      self.assert_(a1 == a2)
      
      self.assert_(a1.val == "A")
      a2.val = "A2"
      self.assert_(a1.val == "A2")
      self.assert_(a1.returnA() == "A")

      b1 = MySingletonB()
      b2 = MySingletonB()
      
      self.assert_(a1.val == "A2")
      self.assert_(b1.val == "B")
      self.assert_(b1.returnB() == "B")
      self.assert_(b1 == b2)

   def testBorg(self):
      a1 = MyBorgA()
      a2 = MyBorgA()
      
      self.assert_(a1 != a2)
      
      self.assert_(a1.val == "A")
      a2.val = "A2"
      self.assert_(a1.val == "A2")
      self.assert_(a1.returnA() == "A")

      b1 = MyBorgB()
      b2 = MyBorgB()
      
      self.assertEqual(a1.val, "A2")
      self.assertEqual(b1.val, "B")
      self.assert_(b1.returnB() == "B")
      self.assert_(b1 != b2)

if __name__ == '__main__':
   unittest.main()

