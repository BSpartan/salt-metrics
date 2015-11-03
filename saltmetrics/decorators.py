# -*- coding: utf-8 -*-
# christian@bloglovin
# Provides output decorators for salt-metrics package

# imports #######################################

import json
from   os.path import dirname
from   .       import log

# functions #####################################

class Decorate( object ):
  ''' Returns reference to decorator method
  '''
  def __init__( self, method, decorator, options ):
    self.method    = method
    self.decorator = decorator
    self.options   = options

  def __call__( self ):
    # exec wrapped method, which should be BaseMetrics#save_metrics
    self.method()

    # finally call type specific method
    getattr( self, self.decorator )()


  def prometheus( self ):
    # retrieve dump file and convert json to native dict
    # instance
    saved_path = self.options['metrics']['saved_path']

    with open( saved_path, 'r' ) as file:
      data      = json.loads( file.read() ) 
      dump      = [ ]  
      arguments = [ ]

      # pass through dict object and retrieve all values 
      # top level scalar values
      for key, value in data.iteritems():
        if not isinstance( value, dict ):
          arguments.append('{key}="{value}"'.format(
            key   = key,
            value = value 
          ))

      arguments = '{' + (','.join( arguments )) + '}'

      # pass through data again and "flatten" out all dict
      # structures so we can easily dump into exposition 
      # format
      # NOTE: see ./examples/prometheus-exposition
      for type, arbitrary in data.iteritems():
        if isinstance( arbitrary, dict ):
          for property, number in arbitrary.iteritems():
            dump.append('salt_{type}_{property}{arguments} {number}'.format(
              type      = type,
              property  = property,
              arguments = arguments,
              number    = number
            ))

      # finally, lets write dump to file
      file = '{directory}/salt_metrics.{decorator}'.format(
        directory = dirname( saved_path ),
        decorator = self.decorator
      )
      with open( file, 'w' ) as file:
        file.write("\n".join( dump )) 
