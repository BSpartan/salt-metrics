# -*- coding: utf-8 -*-
# christian@bloglovin
# Provides output decorators for salt-metrics package

# imports #######################################

import json
from   os.path import dirname

# functions #####################################

class Decorate( object ):
  ''' Returns reference to decorator method
  '''
  def __init__( self, method, decorator, options ):
    self.method    = method
    self.decorator = decorator
    self.options   = options

  def __call__( self ):

    def prometheus( self ):
      # exec wrapped method
      self.method( self )

      # retrieve dump file and convert json to native dict
      # instance
      with open( self.options.metrics.saved_path, 'r' ) as file:
        data      = json.loads( file.read() ) 
        dump      = [ ]  
        arguments = { }

        # pass through dict object and retrieve all values 
        # top level scalar values
        for key, value in data:
          if not isinstance( value, dict ):
            arguments.append('{key}="{value}"'.format(
              key   = key,
              value = value 
            ))

        arguments = '{{args}}'.format(args = ','.join( arguments ))

        # pass through data again and "flatten" out all dict
        # structures so we can easily dump into exposition 
        # format
        # NOTE: see ./examples/prometheus-exposition
        for type, arbitrary in data:
          if isinstance( arbitrary, dict ):
            for property, number in arbitrary:
              dump.append('salt_{type}_{property}={arguments} {number}'.format(
                type      = type,
                property  = property,
                arguments = arguments,
                number    = number
              ))

        # finally, lets write dump to file
        file = '{directory}/salt_metrics.{decorator}'.format(
          directory = dirname( self.options.metrics.saved_path ),
          decorator = self.decorator
        )
        with open( file, 'w' ) as file:
          file.write("\n".join( dump ))

    return locals()[self.decorator]
