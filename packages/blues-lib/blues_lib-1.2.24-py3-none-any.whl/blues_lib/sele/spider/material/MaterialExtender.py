import sys,os,re,json 
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.spider.deco.MaterialDeco import MaterialDeco
from sele.spider.crawler.CrawlerHandler import CrawlerHandler
from util.BluesURL import BluesURL 

class MaterialExtender(CrawlerHandler):
  '''
  Extend the required fields by existed fields
  '''
  kind = 'handler'

  @MaterialDeco()
  def resolve(self,request):
    if not request or not request.get('material'):
      return
    
    self.__extend(request)

  def __extend(self,request):
    material = request.get('material')
    body_dict = self.__get_body_dict(material['material_body'])

    # append extend fields
    material['material_type'] = 'article'
    material['material_recommend_pub_channel'] = 'events'
    material['material_body_text'] = json.dumps(body_dict['text'],ensure_ascii=False)
    material['material_body_image'] = json.dumps(body_dict['image'],ensure_ascii=False)

    # convert the dict to json
    material['material_body'] = json.dumps(material['material_body'],ensure_ascii=False)

  def __get_body_dict(self,paras):
    body_dict = {
      'text':[],
      'image':[],
    }
    for para in paras:
      body_dict[para['type']].append(para['value'])
    
    # set the max image count
    #max_image_size = self.schema.image_size_atom.get_value()
    max_image_size = 9
    body_dict['image'] = body_dict['image'][:max_image_size]
    return body_dict




