import sys,os,re,json
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.ai.AIQASchema import AIQASchema

class DouBaoQASchema(AIQASchema):

  def create_url_atom(self):
    self.url_atom = self.atom_factory.createURL('QA page url','https://www.doubao.com/chat/')

  def create_question_atom(self):
    atoms = [
      # value placeholder 2: material_body_text
      #self.atom_factory.createClickable('swich','div[data-testid="create_conversation_button"]'),
      self.atom_factory.createInput('input','textarea.semi-input-textarea','${question}'),
    ]

    self.question_atom = self.atom_factory.createArray('question',atoms)

  def create_submit_atom(self):
    atoms = [
      # value placeholder 2: material_body_text
      self.atom_factory.createClickable('submit','#flow-end-msg-send'),
    ]

    self.submit_atom = self.atom_factory.createArray('submit',atoms)

  def create_answer_atom(self):
    '''
    Fetch the title and content as a text block
    The line will be split by \n\n
    This seletor suport left and right receive message
    '''
    title_selectors = [
      'div[class^=right-side] .flow-markdown-body h1',
      'div[data-testid="receive_message"] .message-content h1',
    ]
    content_selectors = [
      'div[class^=right-side] .flow-markdown-body',
      'div[data-testid="receive_message"] .message-content',
    ]
    para_field_atoms = [
      # main selector
      self.atom_factory.createText('title',','.join(title_selectors)),
      self.atom_factory.createText('content',','.join(content_selectors))
    ]
    self.answer_atom = self.atom_factory.createArray('title and content',para_field_atoms) 

