# -*- coding: utf-8 -*-
# christian@bloglovin
# Provides output decorators for salt-metrics package

# imports #######################################

import json
from   os.path import dirname

# functions #####################################

def decoratate( method, decorator, options ):
  ''' Returns reference to decorator method
  '''
  # TODO: replace with callable class

  def prometheus( self ):
    # exec wrapped method
    method( self )

    # retrieve dump file and convert json to native dict
    # instance
    with open( options.metrics.saved_path, 'r' ) as file:
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
        directory = dirname( options.metrics.saved_path ),
        decorator = decorator
      )
      with open( file, 'w' ) as file:
        file.write("\n".join( dump ))
        
  return locals()[decorator]
