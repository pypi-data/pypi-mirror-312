import sys,os,re,json
from .Material import Material

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from pool.BluesMaterialIO import BluesMaterialIO

class DBMaterial(Material):
  '''
  The material from db
  '''
  # override
  def first(self,query_condition):
    query_condition['count'] = 1
    rows = self.get(query_condition) 
    return rows[0] if rows else None

  # override
  def get(self,query_condition):
    mode = query_condition.get('mode')
    count = query_condition.get('count')
    rows = None

    if mode == 'latest':
      rows = self.__latest(count)
      self.__format(rows) 

    return rows

  def __latest(self,count=1):
    response = BluesMaterialIO.latest(count)
    return response.get('data')

  def __format(self,rows):
    '''
    Set the foramt entity dict, extract the json fields to object
    Returns 
      {list<dict>}
    '''
    for material in rows:
      texts = json.loads(material.get('material_body_text'))
      images = json.loads(material.get('material_body_image'))
      body = json.loads(material.get('material_body'))
      
      # convert the json to object
      material['material_body_text']=texts
      material['material_body_image']=images
      material['material_body']=body

