__path__ = __import__('pkgutil').extend_path(__path__, __name__)

__version__ = '0.0.1'

import sys
import warnings

TYPE_CHECK = True

import os

## compile-time only dependencies
#if os.environ.get('_KFP_RUNTIME', 'false') != 'true':
#    # make `from kfp import components` and `from kfp import dsl` valid;
#    # related to namespace packaging issue
#    from kfp import components  # noqa: keep unused import
#    from kfp import dsl  # noqa: keep unused import
#    from kfp.client import Client  # noqa: keep unused import
