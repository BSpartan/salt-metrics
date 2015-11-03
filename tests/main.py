# -*- coding: utf-8 -*-
# christian@bloglovin
# simple set of unit tests

# imports #######################################

import unittest
import saltmetrics
from saltmetrics import collector

# tests #########################################

class MainTest( unittest.TestCase ):
  ''' Provides test cases for overall and expected functionality
  '''
  
  def setUp( self ):
    self.collector = collector({
      '__role': 'master',
      'transport': 'zeromq',
      'sock_dir': '/tmp',
      'metrics': {
        'update_interval': 30,
        'saved_path': '/tmp/salt_metrics.json',
        'persistence': True,
        'decorator': 'prometheus'
      }
    })


  def test_collector( self ):
    self.assertEqual(type(self.collector), saltmetrics.collectors.DecoratedMetricsCollector)
    
  
  
# main ##########################################

if __name__ == '__main__':
    unittest.main()