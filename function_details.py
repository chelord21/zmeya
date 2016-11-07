class FunctionDetails:
  '''Class holding details of any function declared. Function's id expected
     to be held in function dictionary.
     Expect both params_types and params be arrays and match in size'''
  def __init__(self, ftype, params_types, params_names)
    self.ftype = ftype
    self.params_types = params_types
    self.params_names = params_names