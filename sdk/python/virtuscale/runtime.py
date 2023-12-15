import inspect

from typing import Callable, List
from inspect import Parameter
from virtuscale.decorator.embed_source_decorator import get_function_source_definition, indent

def make_func(parameters: List[Parameter], inner_func: Callable)-> Callable:
    """ make_func create a wrapper for inner_func with parameters as its
    function signature
        And also keep function params into global with _global prefix
    """

    param_str_list = []
    for param in parameters:
        param_str_list.append('{}'.format(str(param)))

    params_in_global = []
    for param in parameters:
        params_in_global.append('global _global_{}'.format(param.name))
        params_in_global.append('_global_{} = {}'.format(param.name, param.name))


    func_str = """def f_make_func({0}):
    ### build up global varialbe for all functional params
{1}
    #######
{2}
    return {3}()
""".format(', '.join(param_str_list),
           indent('\n'.join(params_in_global), 4),
           get_function_source_definition(inner_func, 4),
           inner_func.__name__)

    print('makefunc:')
    print(func_str)
    exec(func_str)
    return locals()['f_make_func']
