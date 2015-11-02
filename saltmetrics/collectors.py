# -*- coding: utf-8 -*-
# christian@bloglovin
# Provides output decorators for salt-metrics package

# imports #######################################

from decorators import Decorate
from . import MetricsCollector

# classes #######################################

class DecoratedMetricsCollector( MetricsCollector ):
    """
    Metrics collector that allows runtime decorator declarations
    """
    def __init__(self, opts=None):
      super(DecoratedMetricsCollector, self).__init__( opts )
        
      # get decorator and/or raise exception if not found
      decorator = opts.metrics.decorator
      
      if not decorator:
        raise Exception(
          'You must pass a decorator to metrics configuration!'
        )

      # now apply decorator to BaseMetrics#save_metrics methods
      self._collector.save_metrics = Decorate( 
        self._collector.save_metrics, decorator, opts
      )
