from __future__ import annotations
import sys
import logging
import traceback
from nicegui import ui
from copy import copy
import typing
from typing import Callable, Union, _GenericAlias, TYPE_CHECKING, Optional, Any, GenericAlias
from PySimultan2 import PythonMapper
from functools import partial
import inspect
from enum import EnumType
from PySimultan2.simultan_object import SimultanObject


logger = logging.getLogger('pysimultan_ui')


def create_backward_fcn(cls: type):

    class BackwardFcn(object):
        def __init__(self, *args, **kwargs):
            self.cls = kwargs.get('cls', cls)

        def __call__(self, x):
            if x is None:
                return None
            return next((instance for instance in self.cls.cls_instances
                         if f'{instance.name}_{instance.id}' == x),
                        None)

    backward_fcn = BackwardFcn(cls=cls)

    return lambda x: backward_fcn(x)


if TYPE_CHECKING:
    from ..core.method_mapper import UnmappedMethod, MappedMethod


class ArgumentDialog(ui.dialog):

    def __init__(self,
                 name: str = None,
                 description: str = None,
                 mapper: PythonMapper = None,
                 fnc: Callable = None,
                 method: Union['UnmappedMethod', 'MappedMethod'] = None,
                 options: Optional[dict[Any, Any]] = None,
                 additional_parameters: Optional[dict[Any, inspect.Parameter]] = None,
                 **kwargs):

        """

        :param name:
        :param description:
        :param mapper:
        :param fnc:
        :param method:
        :param options: Example: {'arg1': {'default': 1,
                                           'options': [1, 5, 7]},
                                  'arg2': {'default': 'test'},
                                           'options': ['opt1', 'opt2', 'opt3']
                                           }
                                  'arg2': {'default': 'test'},
                                           'classes': [type1, type2, type3]
                                           }
                                  }
        :param kwargs:
        """

        if options is None:
            options = {}

        if name is None:
            name = method.name

        if description is None:
            description = method.description

        if mapper is None:
            mapper: PythonMapper = method.user.mapper

        if fnc is None:
            fnc = method.method

        super().__init__(value=True)
        self.props("fullWidth fullHeight")

        self.fcn_args = {}
        parameters = dict(inspect.signature(fnc).parameters)

        if additional_parameters is not None:
            parameters.update(additional_parameters)

        with self, ui.card().classes('w-full h-full'):
            ui.label(f'Edit method arguments for {name}').classes('text-h5')

            ui.label(description).classes('text-caption')

            with ui.row():
                ui.button('OK', on_click=lambda e: self.submit({'ok': True, 'args': copy(self.fcn_args)}))
                ui.button('Cancel', on_click=lambda e: self.submit({'ok': False}))

            with ui.list().classes('w-full border-top border-bottom'):

                for key, parameter in parameters.items():
                    if key in ('args', 'kwargs', 'self'):
                        continue

                    try:

                        cls = None

                        with ui.item():
                            with ui.item_section():
                                ui.label(key)
                            with ui.item_section():
                                if hasattr(parameter.annotation, '__name__'):
                                    ui.label(str(parameter.annotation.__name__))
                                else:
                                    ui.label(str(parameter.annotation))
                            with ui.item_section():
                                if parameter.annotation is int:
                                    IntegerInput(key=key,
                                                 parameter=parameter,
                                                 options=options.get(key, {}),
                                                 fcn_args=self.fcn_args,
                                                 mapper=mapper).ui_content()
                                    continue
                                elif parameter.annotation is float:
                                    FloatInput(key=key,
                                               parameter=parameter,
                                               options=options.get(key, {}),
                                               fcn_args=self.fcn_args,
                                               mapper=mapper).ui_content()
                                    continue

                                elif isinstance(parameter.annotation, EnumType):
                                    EnumInput(key=key,
                                               parameter=parameter,
                                               options=options.get(key, {}),
                                               fcn_args=self.fcn_args,
                                               mapper=mapper).ui_content()
                                    continue
                                elif parameter.annotation is bool:
                                    BooleanInput(key=key,
                                                 parameter=parameter,
                                                 options=options.get(key, {}),
                                                 fcn_args=self.fcn_args,
                                                 mapper=mapper).ui_content()
                                    continue
                                elif parameter.annotation is str:
                                    StringInput(key=key,
                                                parameter=parameter,
                                                options=options.get(key, {}),
                                                fcn_args=self.fcn_args,
                                                mapper=mapper).ui_content()
                                    continue
                                elif parameter.annotation is list or parameter.annotation is typing.List:
                                    ComponentListInput(key=key,
                                                       parameter=parameter,
                                                       options=options.get(key, {}),
                                                       fcn_args=self.fcn_args,
                                                       mapper=mapper).ui_content()
                                    continue
                                elif parameter.annotation is dict or parameter.annotation is typing.Dict:
                                    ComponentDictInput(key=key,
                                                       parameter=parameter,
                                                       options=options.get(key, {}),
                                                       fcn_args=self.fcn_args,
                                                       mapper=mapper).ui_content()
                                    continue
                                elif parameter.annotation in mapper.registered_classes.keys():
                                    ComponentInput(key=key,
                                                   parameter=parameter,
                                                   options=options.get(key, {}),
                                                   fcn_args=self.fcn_args,
                                                   cls=mapper.get_mapped_class(parameter.annotation),
                                                   mapper=mapper).ui_content()
                                    continue
                                elif parameter.annotation in mapper.registered_classes.values():
                                    taxonomy = next((key for key, cls in mapper.registered_classes.items() if
                                                     cls == parameter.annotation), None)
                                    try:
                                        ComponentInput(key=key,
                                                       parameter=parameter,
                                                       options=options.get(key, {}),
                                                       fcn_args=self.fcn_args,
                                                       cls=mapper.get_mapped_class(taxonomy),
                                                       mapper=mapper).ui_content()
                                    except Exception as e:
                                        print(f'Error displaying edges: {e}\n')
                                        print('\n'.join(traceback.format_exception(*sys.exc_info())))

                                        logger.error(f'Error displaying edges: {e}\n'
                                                     f'{traceback.format_exception(*sys.exc_info())}')
                                        raise e
                                elif isinstance(parameter.annotation, _GenericAlias) or isinstance(parameter.annotation, GenericAlias):
                                    if parameter.annotation.__origin__ is list or parameter.annotation.__origin__ is typing.List:
                                        ComponentListInput(key=key,
                                                           parameter=parameter,
                                                           options=options.get(key, {}),
                                                           fcn_args=self.fcn_args,
                                                           mapper=mapper).ui_content()
                                        continue
                                    elif parameter.annotation.__origin__ is dict or parameter.annotation.__origin__ is typing.Dict:
                                        ComponentDictInput(key=key,
                                                           parameter=parameter,
                                                           options=options.get(key, {}),
                                                           fcn_args=self.fcn_args,
                                                           mapper=mapper).ui_content()
                                if hasattr(parameter.annotation, '__bases__'):
                                    if SimultanObject in parameter.annotation.__bases__:
                                        ComponentInput(key=key,
                                                       parameter=parameter,
                                                       options=options.get(key, {}),
                                                       fcn_args=self.fcn_args,
                                                       cls=mapper.mapped_classes.get(parameter.annotation._taxonomy, None),
                                                       mapper=mapper).ui_content()
                                else:
                                    ComponentInput(key=key,
                                                   parameter=parameter,
                                                   options=options.get(key, {}),
                                                   fcn_args=self.fcn_args,
                                                   cls=None,
                                                   mapper=mapper).ui_content()
                    except Exception as e:
                        print(f'Error displaying edges: {e}\n')
                        print(traceback.format_exception(*sys.exc_info()))

                        logger.error(f'Error displaying edges: {e}\n'
                                     f'{traceback.format_exception(*sys.exc_info())}')
                        raise e


class ParameterInput:

    def __init__(self,
                 key: str,
                 fcn_args: Union[dict[str, Any], Any],  # function arguments to be passed to the function
                 mapper: Optional[PythonMapper] = None,
                 parameter: Optional[inspect.Parameter] = None,  # parameter to be passed to the function
                 options: Optional[dict[str, Any]] = None,  # options for the input field
                 *args,
                 **kwargs):

        self.key = key
        self.parameter = parameter
        self.options = options if options is not None else {}
        self.fcn_args = fcn_args
        self.mapper = mapper
        self.args = args
        self.kwargs = kwargs

        if self.options and self.options.get('default', None) is not None:
            self.fcn_args[self.key] = self.options['default']
        else:
            if self.parameter is not None:
                self.fcn_args[self.key] = self.parameter.default if self.parameter.default != inspect._empty else None

    def ui_content(self):
        pass


class BooleanInput(ParameterInput):

    def ui_content(self):
        ui.checkbox(text=self.key).bind_value(self.fcn_args,
                                              self.key)


class IntegerInput(ParameterInput):

    def ui_content(self):
        ui.input(label=self.key,
                 validation=self.validate).bind_value(self.fcn_args,
                                                      self.key,
                                                      forward=lambda x: int(x) if x is not None else None,
                                                      backward=lambda x: str(x) if x is not None else None,
                                                      )
    @staticmethod
    def validate(x):
        try:
            int(x)
        except Exception as e:
            return 'Not an integer'


class FloatInput(ParameterInput):

    def ui_content(self):
        ui.input(label=self.key,
                 validation=self.validate).bind_value(self.fcn_args,
                                                      self.key,
                                                      forward=lambda x: float(x) if x is not None else None,
                                                      backward=lambda x: str(x) if x is not None else None,
                                                      )

    @staticmethod
    def validate(x):
        try:
            float(x)
        except ValueError:
            return 'Not a float'


class StringInput(ParameterInput):

    def ui_content(self):
        ui.input(label=self.key).bind_value(self.fcn_args,
                                            self.key)


class EnumInput(ParameterInput):

    @property
    def value_options(self):
        return {x.value: x.name for x in [*self.parameter.annotation]}

    @property
    def default_value(self):
        self.fcn_args[self.key] = self.parameter.default.name if self.parameter.default != inspect._empty else None
        return self.fcn_args[self.key]

    def ui_content(self):
        self.fcn_args[self.key] = self.parameter.default.name if self.parameter.default != inspect._empty else None

        ui.select(label=self.key,
                  options=self.value_options,
                  value=self.default_value,
                  with_input=False).bind_value(self.fcn_args,
                                               self.key,
                                               forward=lambda x: self.parameter.annotation[x],
                                               backward=lambda x: x.value if x is not None else None,
                                               )


class ComponentInput(ParameterInput):

    def __init__(self,
                 key: str,
                 fcn_args: Union[dict[str, Any], Any],  # function arguments to be passed to the function
                 mapper: Optional[PythonMapper] = None,
                 parameter: Optional[inspect.Parameter] = None,  # parameter to be passed to the function
                 options: Optional[dict[str, Any]] = None,  # options for the input field
                 cls: type(SimultanObject) = None,
                 *args,
                 **kwargs):
        super().__init__(key=key,
                         parameter=parameter,
                         options=options,
                         fcn_args=fcn_args,
                         mapper=mapper,
                         *args,
                         **kwargs)
        self.cls: SimultanObject = cls
        self._value_options = None

    @property
    def value_options(self):
        if self._value_options is None:
            try:
                options = {}
                if self.options:
                    if 'options' in self.options.keys():
                        for option in self.options.get('options', []):
                            options[f'{option.name}_{option.id}'] = option

                    elif 'classes' in self.options.keys():
                        for cls in self.options.get('classes', []):
                            try:
                                if cls in self.mapper.registered_classes.values():
                                    mapped_cls = self.mapper.get_mapped_class_for_python_type(cls)
                                else:
                                    mapped_cls = cls
                                for instance in mapped_cls.cls_instances:
                                    options[f'{instance.name}_{instance.id}'] = instance
                            except Exception as e:
                                continue
                else:
                    if self.cls is not None:
                        classes = [self.cls]
                    else:
                        classes = self.mapper.mapped_classes.values()

                    for mapped_cls in classes:
                        for instance in mapped_cls.cls_instances:
                            options[f'{instance.name}_{instance.id}'] = instance
                self._value_options = options
            except Exception as e:
                print(traceback.format_exception(*sys.exc_info()))
                raise e
        return self._value_options

    def ui_content(self):
        ui.select(label=f'{self.key} ({self.cls._taxonomy if self.cls is not None else "Any"})',
                  options=list(self.value_options.keys()),
                  value=f'{self.parameter.default.name}_{self.parameter.default.id}' if self.parameter.default is not None else None,
                  with_input=True).bind_value(self.fcn_args,
                                              self.key,
                                              backward=self.backward_fcn,
                                              forward=self.forward_fcn
                                              )

    @staticmethod
    def backward_fcn(x: Optional[SimultanObject]):
        return f'{x.name}_{x.id}' if x is not None else ''

    def forward_fcn(self, x: Optional[str]):
        if x in (None, 'None', ''):
            return None
        return self.value_options[x]


class ComponentListInput(ComponentInput):

    def __init__(self, *args, **kwargs):
        super().__init__(cls=kwargs.get('mapper').get_mapped_class('ComponentList'),
                         *args,
                         **kwargs)


class ComponentDictInput(ComponentInput):

    def __init__(self, *args, **kwargs):
        super().__init__(cls=kwargs.get('mapper').get_mapped_class('ComponentDict'),
                         *args,
                         **kwargs)
