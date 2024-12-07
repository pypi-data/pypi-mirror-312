import sys,os,re
from .BluesCookie import BluesCookie    
from .BluesStandardChrome import BluesStandardChrome   

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from util.BluesConsole import BluesConsole   
from util.BluesPowerShell import BluesPowerShell    
from util.BluesType import BluesType    
from util.BluesFiler import BluesFiler    
from sele.loginer.Loginer import Loginer    

class BluesLoginChrome(BluesStandardChrome,BluesCookie):
  '''
  This class is used exclusively to open pages that can only be accessed after login
  There are three ways to complete automatic login:
    1. Login by a cookie string
    2. Login by a cookie file path
    3. Login by the BluesLoginer class
  '''
  
  # Maximum relogin times
  max_relogin_time = 1

  def __init__(self,loginer):
    '''
    Parameter:
      url {str} : the url will be opened
      loginer_or_cookie {Loginer|str} : 
        - when as str: it is the cookie string or local cookie file, don't support relogin
        - when as Loginer : it supports to relogin
      anchor {str} : the login page's element css selector
        some site will don't redirect, need this CS to ensure is login succesfully
    '''
    super().__init__()
    
    # {LoginerSchema} : three kinds of mode, use schema
    self.loginer = loginer

    # {int} : relogin time
    self.relogin_time = 0

    # login
    self.__login()
    
  def __login(self):
    # read cookie need get the domain from the url
    self.open(self.loginer.log_in)

    # read the cookie
    cookie = self.read_cookies()
    if cookie and self.__login_with_cookie(cookie):
      BluesConsole.success('Success to login by the cookie')
      return 

    BluesConsole.info('Fail to login by the cookie, relogin...')
    self.__relogin()

  def __login_with_cookie(self,cookie):
    # add cookie to the browser
    self.interactor.cookie.set(cookie) 
    # Must open the logged in page ,Otherwise, you cannot tell if you have logged in
    self.open(self.loginer.logged_in)

    # Check if login successfully
    return self.__is_logged_in()

  def __is_logged_in(self):
    '''
    Current open a logged in page
    @return:
      {bool} : If you are not logged in, you are redirected to the login page
    '''
    if self.loginer.log_in_element:
      return not self.waiter.querier.query(self.loginer.log_in_element,timeout=5)
    else:
      return not self.waiter.ec.url_changes(self.loginer.logged_in,5)
  
  def __relogin(self):
    if self.relogin_time>=self.max_relogin_time:
      BluesConsole.error('Login failed, the maximum number of relogins has been reached.')
      return

    self.relogin_time+=1
    
    # Relogin and save the new cookies to the local file
    BluesConsole.info('Relogin using the %s' % type(self.loginer).__name__)
    self.loginer.login()

    # Reopen the page using the new cookies
    self.__login()

