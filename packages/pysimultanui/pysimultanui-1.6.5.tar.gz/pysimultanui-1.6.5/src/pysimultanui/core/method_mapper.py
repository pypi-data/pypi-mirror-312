import inspect
import logging
import asyncio
import traceback
import sys
from typing import Any, Optional, Union, Dict, List

from nicegui import ui, run, app, events
from .tools import ConfirmationDialog

from PySimultan2.simultan_object import SimultanObject
from ..views.argument_dialog import ArgumentDialog


logger = logging.getLogger('pysimultanui')


class UnknownClass(object):
    def __init__(self, *args, **kwargs):
        self.cls_name: type = kwargs.get('cls_name', 'Unknown class')
        self.cls: type = kwargs.get('cls', None)
        self.mapper = kwargs.get('mapper', None)


class UnmappedMethod(object):

    def __init__(self,
                 name: str = 'Unnamed method',
                 io_bound: bool = False,
                 description: str = '',
                 method: callable = None,
                 add_data_model_to_kwargs: bool = False,
                 add_user_to_kwargs: bool = False,
                 icon: str = 'play_circle',
                 color: str = 'green-5',
                 *args,
                 **kwargs):
        self.name: str = name
        self.description: str = description
        self.method = method
        self.args: list[Any] = kwargs.get('args', [])  # list with description of the arguments
        self.kwargs: dict[str:Any] = kwargs.get('kwargs', dict())  # dict with description of the keyword arguments

        self.add_data_model_to_kwargs = add_data_model_to_kwargs
        self.add_user_to_kwargs = add_user_to_kwargs
        self.io_bound = io_bound

        self.icon = icon
        self.color = color

    @property
    def user(self):
        from .. import user_manager
        return user_manager[app.storage.user['username']]

    @property
    def logger(self):
        return self.user.logger

    @property
    def data_model(self):
        return self.user.data_model

    def ui_content(self):
        with ui.item().classes('w-full h-full'):
            with ui.item_section():
                ui.label(self.name)
            with ui.item_section():
                ui.button(on_click=self.run, icon='play_circle').classes('q-ml-auto')

    async def run(self, *args, **kwargs):

        # res = await get_arguments(self)
        res = await ArgumentDialog(method=self)

        if res is None or res['ok'] is False:
            logger.info(f'User canceled running method {self.name}')
            return

        self.logger.info(f'Running global method {self.name}')

        if self.data_model is None:
            self.logger.error('No project loaded!')
            ui.notify('No project loaded!', type='negative')
            return

        n = ui.notification(timeout=None)
        n.spinner = True
        n.message = f'Running method {self.name}'

        if self.add_data_model_to_kwargs:
            kwargs['data_model'] = self.data_model
        if self.add_user_to_kwargs:
            kwargs['user'] = self.user

        try:
            if inspect.iscoroutinefunction(self.method):
                if self.io_bound:
                    await run.io_bound(self.method, *args, *self.args, **kwargs, **self.kwargs, **res['args'])
                else:
                    await self.method(*args, *self.args, **kwargs, **self.kwargs, **res['args'])
            else:
                if self.io_bound:
                    await run.io_bound(self.method, *args, *self.args, **kwargs, **self.kwargs, **res['args'])
                else:
                    self.method(*args, *self.args, **kwargs, **self.kwargs, **res['args'])
            n.type = 'positive'
            n.message = f'Successfully ran method {self.name}!'
            n.spinner = False
            await asyncio.sleep(1)
            n.dismiss()
            self.logger.info(f'Method {self.name} ran successfully!')
        except Exception as e:
            self.logger.error(f'Error running global method {self.name}:\n{e}'
                              f'{traceback.print_exception(*sys.exc_info())}')
            n.message = f'Error running method {self.name}: {e}'
            n.spinner = False
            await asyncio.sleep(2)
            n.dismiss()


class MappedMethod(object):

    def __init__(self,
                 method: callable,
                 cls,
                 name: str = None,
                 args: Optional[Union[list, tuple]] = None,
                 kwargs: Optional[Dict[str, Any]] = None,
                 add_data_model_to_kwargs: bool = False,
                 add_user_to_kwargs: bool = False,
                 io_bound: bool = False,
                 description: str = '',
                 icon: str = 'play_circle',
                 color: str = 'green-5',
                 *s_args,
                 **s_kwargs):
        self.name: str = name if name is not None else 'Unnamed method'
        self.description: str = description
        self.method = method
        self.cls: type = cls
        self.args: list[str] = args if args is not None else []  # list with description of the arguments
        self.kwargs: dict[
                     str:str] = kwargs if kwargs is not None else {}  # dict with description of the keyword arguments
        self.add_data_model_to_kwargs = add_data_model_to_kwargs
        self.add_user_to_kwargs = add_user_to_kwargs
        self.io_bound = io_bound

        self.icon = icon
        self.color = color

    @property
    def user(self):
        from .. import user_manager
        return user_manager[app.storage.user['username']]

    @property
    def data_model(self):
        return self.user.data_model

    @property
    def logger(self):
        return self.user.logger

    def ui_content(self):
        with ui.item():
            with ui.item_section():
                ui.label(self.name)
            with ui.item_section():
                ui.button(on_click=self.run, icon='play_circle').classes('q-ml-auto')

    async def run(self,
                  *args,
                  **kwargs):

        selected_instances: list[SimultanObject] = kwargs.get('selected_instances', None)
        kwargs.pop('selected_instances', None)

        self.logger.info(f'Running method {self.name} of {self.cls.__name__}')

        if selected_instances is None:
            self.logger.error('No instances selected!')
            ui.notify('No instances selected!')
            await asyncio.sleep(1)
            return


        if not all((hasattr(instance, self.method.__name__) for instance in selected_instances)):
            wrong_names = r' \n'.join([str((instance.name, str(instance.id))) for instance in selected_instances
                                       if not hasattr(instance, self.method.__name__)])
            self.logger.error(f'Not all selected instances have a method {self.method.__name__} implemented!:'
                              f"{wrong_names}")

        # if not all(instance._taxonomy == self.cls._taxonomy for instance in selected_instances) \
        #         or not all(isinstance(instance, self.cls) for instance in selected_instances):
        #     wrong_names = r' \n'.join([str((instance.name, str(instance.id))) for instance in selected_instances])
        #     self.logger.error(f'Not all selected instances are of the type {self.cls.__name__}!:'
        #                       f"{wrong_names}")

            ui.notify(f'Not all selected instances are of the type {self.cls.__name__}!:'
                      f"{wrong_names}",
                      type='negative',
                      close_button=True,
                      multi_line=True)
            await asyncio.sleep(1)
            return

        from .. import user_manager

        if user_manager[app.storage.user['username']].data_model is None:
            ui.notify('No project loaded!', type='negative')
            self.logger.error('No project loaded!')
            return

        if not selected_instances:
            ui.notify('No instances selected!')
            return

        def additional_content_fcn():
            ui.label('Selected instances:')
            for instance in selected_instances:
                with ui.row():
                    ui.label(f'{instance.name} ({instance.id})')

        if self.add_data_model_to_kwargs:
            kwargs['data_model'] = self.data_model
        if self.add_user_to_kwargs:
            kwargs['user'] = self.user

        result = await ConfirmationDialog(f'Are you sure you want to run {self.name}?',
                                          'Yes',
                                          'No',
                                          additional_content_fcn=additional_content_fcn)

        if result=='No':
            return

        parameters = dict(inspect.signature(self.method).parameters)
        if set(parameters.keys()) - {'args', 'kwargs', 'self'}:
            res = await ArgumentDialog(method=self)
            # res = await get_arguments(self)
        else:
            res = {'ok': True, 'args': {}}

        self.logger.info(f'User confirmed running method {self.name} of {self.cls.__name__}')

        if result == 'Yes':
            n = ui.notification(timeout=None)
            n.spinner = True
            n.message = f'Running method {self.name} of {self.cls.__name__}'
            logger.info(f'Running method {self.name} of {self.cls.__name__}')
            await asyncio.sleep(0.01)
            for instance in selected_instances:
                logger.info(f'Running method {self.name} on {instance.name} {instance.id}')

                method = getattr(instance, self.method.__name__)

                if inspect.iscoroutinefunction(method):
                    try:
                        if self.io_bound:
                            await run.io_bound(method,
                                               *args,
                                               *self.args,
                                               **kwargs,
                                               **self.kwargs,
                                               **res['args'])
                        else:
                            await method(*args,
                                         *self.args,
                                         **kwargs,
                                         **self.kwargs,
                                         **res['args'])
                    except Exception as e:
                        err = '\n'.join(traceback.format_exception(*sys.exc_info()))

                        self.logger.error(f'Error running method {self.name} on {instance.name}: {e}'
                                          f'{err}')
                        ui.notify(f'Error running method {self.name} on {instance.name}: {e}', type='negative')
                        continue

                else:
                    try:
                        if self.io_bound:
                            await run.io_bound(method,
                                               *args,
                                               *self.args,
                                               **kwargs,
                                               **self.kwargs,
                                               **res['args'])
                        else:
                            method(*args,
                                   *self.args,
                                   **kwargs,
                                   **self.kwargs,
                                   **res['args'])

                    # self.method(instance, *self.args, **self.kwargs)
                    except Exception as e:
                        err = '\n'.join(traceback.format_exception(*sys.exc_info()))

                        self.logger.error(f'Error running method {self.name} on {instance.name}: {e}'
                                          f'{err}')
                        ui.notify(f'Error running method {self.name} on {instance.name}: {e}', type='negative')
                        continue

                # getattr(instance, self.name)(*self.args, **self.kwargs)
                # self.method(instance, *self.args, **self.kwargs)
            self.logger.info(f'Method {self.name} run on {len(selected_instances)} instances!')
            n.type = 'positive'
            n.message = f'Method {self.name} run on {len(selected_instances)} instances!'
            n.spinner = False
            await asyncio.sleep(1)
            # self.method(*args, **kwargs)
            n.dismiss()


class MappedMethods(object):

    def __init__(self, *args, **kwargs):
        self.mapped_methods: dict[type: List[MappedMethod]] = {}

    def __getitem__(self, item: type) -> tuple[MappedMethod]:
        return self.mapped_methods.__getitem__(item)

    def __setitem__(self,
                    key: type,
                    value: MappedMethod) -> None:
        self.mapped_methods.__setitem__(key, value)

    def __delitem__(self, key: type) -> None:
        self.mapped_methods.__delitem__(key)

    def __iter__(self):
        return self.mapped_methods.__iter__()

    def __len__(self):
        return self.mapped_methods.__len__()

    def __contains__(self, item: type) -> bool:
        return self.mapped_methods.__contains__(item)

    def __repr__(self):
        return self.mapped_methods.__repr__()

    def get(self, key: type, default=None) -> MappedMethod:
        return self.mapped_methods.get(key, default)

    def items(self):
        return self.mapped_methods.items()

    def keys(self):
        return self.mapped_methods.keys()

    def values(self):
        return self.mapped_methods.values()

    def update(self, other: Union[dict, 'MappedMethods']) -> None:
        if isinstance(other, MappedMethods):
            self.mapped_methods.update(other.mapped_methods)
        else:
            self.mapped_methods.update(other)

    def copy(self) -> 'MappedMethods':
        new_mm = MappedMethods()
        new_mm.mapped_methods = self.mapped_methods.copy()
        return new_mm

    def get_inherited_mapped_methods(self, cls: type) -> list[MappedMethod]:

        mapped_methods = set()

        def get_mapped_methods(cls):
            if cls in (SimultanObject, object, UnknownClass):
                return

            if not SimultanObject in cls.__bases__:
                mapped_cls = next((key for key in self.mapped_methods.keys() if key.__name__ == cls.__name__), None)
                mapped_methods.update(self.mapped_methods.get(mapped_cls, []))
            else:
                mapped_methods.update(self.mapped_methods.get(cls, []))

            if hasattr(cls, '__bases__'):
                for base in cls.__bases__:
                    get_mapped_methods(base)

        get_mapped_methods(cls)

        return mapped_methods



class MethodMapper(object):

    mappers = {}

    def __init__(self, *args, **kwargs):

        self._mapped_methods: MappedMethod = MappedMethods()
        self.unmapped_methods: dict[str: UnmappedMethod] = {}
        self.mapper = kwargs.get('mapper', None)
        self.card = None

        self.global_methods_table = None
        self.mapped_methods_table = None

        self.cls_select = None

    @property
    def mapped_methods(self):
        if self._mapped_methods is None:
            self._mapped_methods = MappedMethods()
        return self._mapped_methods

    @mapped_methods.setter
    def mapped_methods(self, value):
        self._mapped_methods = MappedMethods()
        self._mapped_methods.update(value)

    @property
    def selected_cls(self):
        return next((cls for cls in self.mapped_methods.keys()
                     if not isinstance(cls, UnknownClass)
                     and cls.__name__ == self.cls_select.value), None)

    @property
    def user(self):
        from .. import user_manager
        return user_manager[app.storage.user['username']]

    def register_method(self,
                        method: callable,
                        name: str = 'unnamed_method',
                        description: str = '',
                        args: Optional[Union[list, tuple]] = (),
                        kwargs: Optional[Dict[str, Any]]=None,
                        cls: type = None,
                        add_data_model_to_kwargs: bool =False,
                        add_user_to_kwargs: bool = False,
                        io_bound=False,
                        icon: str = 'play_circle',
                        color: str = 'green-5',
                        *s_args,
                        **s_kwargs) -> None:

        """
        Register a method with the method mapper. The method will be displayed in the UI and can be run from there.

        Typing hints for the method will be used to generate the input fields for the arguments of the method. Currently
        only int, float, str, bool and instances of registered classes are supported. If the method has a parameter of
        a class which is not registered, a select field with all instances of the class will be displayed.

        :param method: The method to register which will be called when the method is run.
        :param name: The name of the method which will be displayed in the UI.
        :param description: A description of the method which will be displayed in the UI.
        :param args: A list of the arguments which will be passed to the called method.
        :param kwargs: A dict of the keyword arguments which will be passed to the called method.
        :param cls: The class of the method. If None, the method will be registered as a global method.
        :param add_data_model_to_kwargs: If True, the data model will be added as a kwargs when the method is called.
        :param add_user_to_kwargs: If True, the user will be added to the kwargs of the method.
        :param io_bound: If True, the method will be run in an io_bound context.
        :param s_args: List of additional arguments to the registration.
        :param s_kwargs: Dict of additional keyword arguments to the registration.
        :return: None
        """

        if kwargs is None:
            kwargs = {}
        if cls is None:
            self.unmapped_methods[name] = UnmappedMethod(name=name,
                                                         method=method,
                                                         args=args,
                                                         description=description,
                                                         add_data_model_to_kwargs=add_data_model_to_kwargs,
                                                         add_user_to_kwargs=add_user_to_kwargs,
                                                         io_bound=io_bound,
                                                         icon=icon,
                                                         color=color,
                                                         kwargs=kwargs,
                                                         *s_args,
                                                         **s_kwargs)

            return

        if cls not in self.mapped_methods:
            self.mapped_methods[cls] = []
        self.mapped_methods[cls].append(MappedMethod(cls=cls,
                                                     name=name,
                                                     method=method,
                                                     args=args,
                                                     description=description,
                                                     kwargs=kwargs,
                                                     add_data_model_to_kwargs=add_data_model_to_kwargs,
                                                     add_user_to_kwargs=add_user_to_kwargs,
                                                     io_bound=io_bound,
                                                     icon=icon,
                                                     color=color,
                                                     *s_args,
                                                     **s_kwargs),
                                        )

    @ui.refreshable
    def ui_content(self):

        with ui.expansion(icon='play_circle',
                          text='Methods').classes('w-full'):
            with ui.expansion(icon='public',
                              text='Global Methods').classes('w-full') as self.card:
                columns = [{'name': 'id', 'label': '#', 'field': 'id', 'sortable': True},
                           {'name': 'name', 'label': 'Name', 'field': 'name', 'sortable': True},
                           {'name': 'actions', 'label': 'Actions', 'field': 'actions', 'sortable': False}]

                rows = [{'id': i, 'name': method.name} for i, method in enumerate(self.unmapped_methods.values())]

                self.global_methods_table = ui.table(columns=columns,
                                                     rows=rows,
                                                     pagination={'rowsPerPage': 5, 'sortBy': 'id', 'page': 1},
                                                     row_key='id').classes('w-full h-full bordered')

                self.global_methods_table.add_slot('body-cell-actions', r'''
                                                        <q-td key="actions" :props="props">
                                                            <q-btn size="sm" color="blue" round dense
                                                                @click="$parent.$emit('run_global_method', props)"
                                                                icon="play_circle" />
                                                        </q-td>
                                                    ''')
                self.global_methods_table.on('run_global_method', self.run_global_method)

                self.resolve_classes()

            with ui.expansion(icon='public',
                              text='Mapped Methods').classes('w-full'):
                options = [cls.__name__ for cls in self.mapped_methods.keys()
                           if not isinstance(cls, UnknownClass)]
                self.cls_select = ui.select(label='Select class',
                                            options=options,
                                            value=options[0] if options else None,
                                            on_change=self.ui_method_select_content.refresh)
                self.cls_select.classes('w-full')
                self.ui_method_select_content()

    async def run_method(self,
                         e: events.GenericEventArguments,
                         cls: type = None,
                         selected_instances: Optional[list[SimultanObject]] = None):
        if cls is None:
            cls = self.selected_cls
            if selected_instances is None:
                selected_instances = await self.user.grid_view.selected_instances
        await self.mapped_methods[cls][int(e.args['key'])].run(selected_instances=selected_instances)

    @ui.refreshable
    def ui_method_select_content(self):

        columns = [{'name': 'id', 'label': 'ID', 'field': 'id', 'sortable': True},
                   {'name': 'name', 'label': 'Name', 'field': 'name', 'sortable': True}]

        if self.selected_cls is None:
            rows = []
        else:
            rows = [{'id': i,
                     'name': method.name}
                    for i, method in enumerate(self.mapped_methods[self.selected_cls])]

        methods_table = ui.table(columns=columns,
                                 rows=rows,
                                 row_key='id').classes('w-full bordered')

        methods_table.add_slot('body', r'''
                                    <q-tr :props="props">
                                        <q-td v-for="col in props.cols" :key="col.name" :props="props">
                                            {{ col.value }}
                                        </q-td>
                                        <q-td auto-width>
                                            <q-btn size="sm" color="blue" round dense
                                                   @click="$parent.$emit('run_method', props)"
                                                   icon="play_circle" />
                                        </q-td>
                                    </q-tr>
                                ''')

        methods_table.on('run_method', self.run_method)

    async def run_global_method(self, e: events.GenericEventArguments):

        method = self.unmapped_methods[e.args['row']['name']]
        await method.run()

    def resolve_classes(self):

        mapped_methods = self.mapped_methods.copy()

        for cls, methods in self.mapped_methods.items():
            if isinstance(cls, UnknownClass):
                for method in methods:
                    new_cls = self.mapper.mapped_classes.get(method.method.__qualname__.split('.')[-2], None)
                    if new_cls is None:
                        continue
                    method.cls = new_cls
                    if new_cls not in mapped_methods:
                        mapped_methods[new_cls] = []
                    mapped_methods[new_cls].append(method)
                    mapped_methods[cls].remove(method)

        self.mapped_methods = mapped_methods


    def copy(self):
        new_method_mapper = MethodMapper()
        new_method_mapper.mapped_methods = self.mapped_methods
        new_method_mapper.unmapped_methods = self.unmapped_methods
        new_method_mapper.mapper = self.mapper
        return new_method_mapper

    def __add__(self, other: 'MethodMapper') -> 'MethodMapper':
        new_method_mapper = self.copy()
        new_method_mapper.mapped_methods.update(other.mapped_methods)
        new_method_mapper.unmapped_methods.update(other.unmapped_methods)
        return new_method_mapper


method_mapper = MethodMapper()


def mapped_method(name=None,
                  description: str ='',
                  add_data_model_to_kwargs: bool = False,
                  add_user_to_kwargs: bool = False,
                  io_bound: bool = False,
                  *args,
                  **kwargs):
    dat_dict = {}
    dat_dict['name'] = name
    dat_dict['description'] = description
    dat_dict['add_data_model_to_kwargs'] = add_data_model_to_kwargs
    dat_dict['add_user_to_kwargs'] = add_user_to_kwargs
    dat_dict['io_bound'] = io_bound

    def wrapper(func):
        # vars(sys.modules[func.__module__])[func.__qualname__.split('.')
        method_mapper.register_method(method=func,
                                      name=dat_dict['name'],
                                      description=dat_dict['description'],
                                      add_data_model_to_kwargs=dat_dict['add_data_model_to_kwargs'],
                                      add_user_to_kwargs=dat_dict['add_user_to_kwargs'],
                                      io_bound=dat_dict['io_bound'],
                                      args=args,
                                      kwargs=kwargs,
                                      cls=UnknownClass(cls_name=func.__qualname__))
        return func

    return wrapper
