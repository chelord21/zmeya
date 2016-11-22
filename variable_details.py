# TODO: Agregar dirección de memoria cuando sea prudente, valor, etc..
class VariableDetails:
  'Class holding details of any variable declared'
  def __init__(self, vtype, vmemory):
    self.vtype = vtype
    self.vmemory = vmemory
    self.isArray = False
    self.arrayDetails = None

  def __init__(self, vtype, vmemory, ad):
    self.vtype = vtype
    self.vmemory = vmemory
    self.arrayDetails = ad
    if ad.details:
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
    def __init__(self):
        self.details = []

    def add_details(self, details):
        self.details.append(details)

    def get_dimension(self, x):
        return self.details[x]

    def first(self):
        return self.details[0]

    def erase(self):
        self.details = []
