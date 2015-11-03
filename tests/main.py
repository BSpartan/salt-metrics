# -*- coding: utf-8 -*-
# christian@bloglovin
# simple set of unit tests

# imports #######################################

import unittest
import saltmetrics
from saltmetrics import collector
from saltmetrics import log
from threading import Thread
from time import sleep
from functools import wraps
from multiprocessing import Process


# tests #########################################

class MainTest( unittest.TestCase ):
  ''' Provides test cases for overall and expected functionality
  '''
  UPDATE_INTERVAL = 5

  def setUp( self ):
    log.info( 'MainTest#setUp: start' )    

    # NOTE: I don't understand what weird pythonic bullshit
    # neccessitates this, but it is needed for using timeout
    # decorator 
    self.__name__ = 'MainTest'

    # setup collector instance with enough options to be
    # able to successfully instantiate
    try:
      self.collector

    except:
      log.info( 'MainTest#setup: exception' )
      self.collector = collector({
        '__role': 'master',
        'transport': 'zeromq',
        'sock_dir': '/tmp',
        'pki_dir': '/etc/salt/pki',
        'metrics': {
          'update_interval': self.UPDATE_INTERVAL,
          'saved_path': '/tmp/salt_metrics.json',
          'persistence': True,
          'decorator': 'prometheus'
        }
      })

  def __timeout(seconds=15, error_message="Timeout"):
    def decorator(func):
      def wrapper(*args, **kwargs):
        process = Process(None, func, None, args, kwargs)
        process.start()
        process.join(seconds)
        if process.is_alive():
          process.terminate()
          raise Exception(error_message)

      return wraps(func)(wrapper)
    return decorator 

  @__timeout
  def test_collector( self ):
    '''Ensure collector is correct instance type
    '''
    log.info( 'MainTest#test_collector: start' )
    self.assertEqual(
      type(self.collector), saltmetrics.collectors.DecoratedMetricsCollector
    )
  
  def test_run( self ):
    log.info( 'MainTest#test_run: start' )    
    self.collector.run()

# main ##########################################

if __name__ == '__main__':
    unittest.main()
