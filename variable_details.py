# TODO: Agregar dirección de memoria cuando sea prudente, valor, etc..
class VariableDetails:
  'Class holding details of any variable declared'
  #def __init__(self, vtype, vmemory):
  #  self.vtype = vtype
  #  self.vmemory = vmemory
  #  self.isArray = False
  #  self.arrayDetails = None

  def __init__(self, vtype, vmemory, ad=None):
    self.vtype = vtype
    self.vmemory = vmemory
    self.arrayDetails = ArrayDetails(ad)
    if ad and ad.details :
        self.isArray = True
    else:
        self.isArray = False

  def set_arrayDetails(self, arrayDetails):
      self.isArray = True
      self.arrayDetails = arrayDetails

class Details:
    '''Class that stores the information of array'''
    def __init__(self, size):
        self.size = size
        self.m = 0

    def set_m(self, r):
        self.m = r

class ArrayDetails:
    '''Class that holds the Details information'''
    def __init__(self, ad=None):
        if ad:
            self.details = ad.details
            self.totalSize = ad.totalSize
        else:
            self.details = []
            self.totalSize = 0

    def add_details(self, details):
        self.details.append(details)
        self.totalSize += 1

    def get_dimension(self, x):
        return self.details[x]

    def first(self):
        return self.details[0]

    def erase(self):
        self.details = []
        self.totalSize = 0

    def print(self):
        for det in self.details:
            print("::", det.size, ":", det.m)

