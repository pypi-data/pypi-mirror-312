import functools
from typing import Type
from pathlib import Path
from dektools.str import tab_str
from .template import TemplateWide
from .collection import Collection, DictCollection, NamedListCollection
from .part import Repr, ReprTuple, Cache


class Generator:
    TEMPLATE_DIR = None

    template_name = None
    template_cls = TemplateWide
    template_ext = '.tpl'

    Repr = Repr
    ReprTuple = ReprTuple

    env_default = {}

    def __init__(self, instance, kwargs=None):
        self.instance = instance
        self.parent = None
        self.kwargs = kwargs or {}
        self.cache = Cache(self)

    def render(self):
        raise NotImplementedError

    def render_tpl(self, tpl, variables=None):
        return self.template_cls(self.normalize_variables(
            {**(self.variables if variables is None else variables), **self.kwargs}), self.env_default).render_string(
            str(Path(self.template_path) / (tpl + self.template_ext)))

    def normalize_variables(self, variables):
        return variables

    @property
    @functools.lru_cache(None)
    def template_path(self):
        return str(Path(self.TEMPLATE_DIR) / self.template_name) if self.template_name else str(self.TEMPLATE_DIR)

    @property
    @functools.lru_cache(None)
    def variables(self):
        return self.collect_data('variables', DictCollection)

    def get_variables(self, *args, **kwargs):
        return {
            **{k: self.variables[k] for k in args},
            **{k: self.variables[v] for k, v in kwargs.items()}
        }

    def collect_data(self, entry, collection: Type[Collection]):
        result = collection(entry)
        pre_collect = f'pre_collect_{entry}'
        post_collect = f"post_collect_{entry}"
        if hasattr(self, pre_collect):
            result.set_data(getattr(self, pre_collect)(result.get_data()))
        prefix = f'{entry}_'
        for x in dir(self):
            if x.startswith(prefix):
                name = x[len(prefix):]
                v = getattr(self, x)
                result.append(name, self.cache[x]() if callable(v) else v)
        if hasattr(self, post_collect):
            result.set_data(getattr(self, post_collect)(result.get_data()))
        return result.get_data()

    @staticmethod
    def tab_str(s, n, p=4, sl=False):  # s: list or str
        return tab_str(s, n, p, sl)

    @property
    @functools.lru_cache(None)
    def children(self):
        return self.collect_data('children', NamedListCollection)

    @property
    @functools.lru_cache(None)
    def parent_root(self):
        cursor = self.parent
        while cursor:
            if cursor.parent:
                cursor = cursor.parent
            else:
                return cursor
        return cursor

    def post_collect_children(self, children):
        for lst in children.values():
            for child in lst:
                child.parent = self
        return children

    def post_collect_variables(self, variables):
        children_data = {}
        all_filter_children = getattr(self, f'all_filter_children', lambda k, x, y: x)
        for key, array in self.children.items():
            r = self.tab_str([node.render() for node in array], 0)
            filter_children = getattr(self, f'filter_children_{key}', None)
            if filter_children:
                children_data[key] = filter_children(r, array)
            else:
                children_data[key] = all_filter_children(key, r, array)
        return {
            **variables,
            **children_data,
        }


class GeneratorTpl(Generator):
    template_tpl = 'main'

    def render(self):
        return '' if self.template_tpl is None else self.render_tpl(self.template_tpl)


class GeneratorFiles(Generator):
    def __init__(self, target_dir, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_dir = str(target_dir)

    def check(self):
        return self.instance is not None

    def action(self):
        if self.check():
            self.render()
            self.on_rendered()

    def on_rendered(self):
        pass

    def render(self):
        self.template_cls(
            self.normalize_variables({**self.variables, **self.kwargs}),
            env=self.env_default,
            multi=self.multi
        ).render_dir(self.target_dir, self.template_path)
        for generator_cls, ins_list in self.sibling.items():
            for ins in ins_list:
                generator_cls(self.target_dir, ins).action()

    @property
    @functools.lru_cache(None)
    def multi(self):
        return self.collect_data('multi', NamedListCollection)

    @property
    @functools.lru_cache(None)
    def sibling(self):
        return self.collect_data('sibling', DictCollection)
