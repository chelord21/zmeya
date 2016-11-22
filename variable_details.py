# TODO: Agregar dirección de memoria cuando sea prudente, valor, etc..
class VariableDetails:
  'Class holding details of any variable declared'
  def __init__(self, vtype, vmemory):
    self.vtype = vtype
    self.vmemory = vmemory
    self.isArray = False
