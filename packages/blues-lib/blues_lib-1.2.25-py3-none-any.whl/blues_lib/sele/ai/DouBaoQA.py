import sys,os,re,json
from .AIQA import AIQA
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from model.models.DouBaoModelFactory import DouBaoModelFactory
from sele.loginer.doubao.DouBaoLoginerFactory import DouBaoLoginerFactory   
from util.BluesConsole import BluesConsole

class DouBaoQA(AIQA):
  
  def __init__(self,question='',rule=None):
    self.rule = rule
    # { AIQASchema }
    material = {'question':question}
    model = DouBaoModelFactory().create_qa(material)
    # { Loginer } set loginer for relogin
    loginer = DouBaoLoginerFactory().create_mac()

    super().__init__(model['schema'],loginer)

  def extract(self,ai_entity):
    '''
    Template method: extract title and para list from the text square
    Parameters:
      ai_entity {dict} : such as {'title':'text','content':'xxx\n\nxxx\n\nxxx'}
    Returns:
      {dict} : {'title':'xxx','paras':'json of text list'}
    '''
    title = ai_entity['title'] # don't use now
    content = ai_entity['content']
    return self.__get_field_dict(content)

  def __get_field_dict(self,content):
    '''
    Returns {json} : json of str list
    '''
    if not content:
      return None

    # remov all " for convert to json
    paras = content.replace('"',"'").split('\n\n')
    # first line is the title
    title_para = paras.pop(0)
    if not paras:
      return None
    
    title = self.__get_title(title_para)
    title_length = self.rule.get('title_length')
    if title_length and title_length<len(title):
      BluesConsole.error('Title too long (max:%s)' % str(title_length))
      return None

    return {
      'paras':json.dumps(paras,ensure_ascii=False),
      'title':title
    }

  def __get_title(self,title):
    # pattern 1 : 标题：《xxx》
    matcheds_01 = re.findall(r'《(.+)》',title)
    # pattern 2: 标题: xxx
    matcheds_02 = re.findall(r'标题\s*[:：]?\s*(.+)',title)
    # If have no title, don't use the ai result
    if matcheds_01:
      return matcheds_01[0]
    if matcheds_02:
      return matcheds_02[0]

    return title
