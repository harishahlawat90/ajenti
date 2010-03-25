import random
import xml.dom.minidom as dom


class Element(dom.Element):
    """ Generate XML element

    @tag - element name
    *args - any number of dictionaries {'attribute':'value'}
    **kwargs - any number of keyword arguments attribute="value"
    """
    visible = True
    def __init__(self, tag, *args, **kwargs):
        dom.Element.__init__(self, tag)
        self.id = str(random.randint(1,9000*9000))
        self._init(*args, **kwargs)

    def _init(self, *args, **kwargs):
        for attr in kwargs:
            self.setAttribute(attr, str(kwargs[attr]))
        for attrs in args:
            if isinstance(attrs, dict):
                # Append attributes in dicts
                for attr in attrs:
                    self.setAttribute(attr, str(attrs[attr]))
            elif isinstance(attrs, dom.Element):
                # Append childs
                self.appendChild(attrs)

    def __getitem__(self, key):
        return self.getAttribute(key)

    def __setitem__(self, key, value):
        self.setAttribute(key, str(value))


class Html(object):
    """ Automatically generate XML tag by calling name

    >>> from ajenti.ui.html import Html
    >>> h = Html()
    >>> h.meta(encoding='ru').toxml()
    '<meta encoding="ru"/>'
    >>>
    """
    def __getattr__(self, name):
        return lambda *args, **kwargs: Element(name, *args, **kwargs)

    def gen(self, name, *args, **kwargs):
        return Element(name, *args, **kwargs)


class UI(object):
    class __metaclass__(type):
        def __getattr__(cls, name):
            return lambda *args, **kwargs: Element(name.lower(), *args, **kwargs)


class Text(Element):
    """ FIXME: xml.dom.minidom does not provide plain text element """
    def __init__(self, text):
        Element.__init__(self, 'span', {'py:content':"'%s'"%text, 'py:strip':""})


class Category(Element):
    def __init__(self, *args, **kwargs):
        Element.__init__(self, 'category', *args, **kwargs)


class VContainer(Element):
    """ Container class
    To maintain same syntax with XML Templates - we should use vnode()
    """
    def __init__(self, *args):
        Element.__init__(self, 'vcontainer')
        self.elements = []
        for e in args:
            if isinstance(e, dom.Element):
                self.vnode(e)

    def vnode(self, e):
        self.appendChild(Html().vnode(e))


class HContainer(Element):
    """ Container class
    To maintain same syntax with XML Templates - we should use hnode()
    """
    def __init__(self, *args):
        Element.__init__(self, 'hcontainer')
        self.elements = []
        for e in args:
            if isinstance(e, dom.Element):
                self.hnode(e)

    def hnode(self, e):
        self.appendChild(Html().hnode(e))

class DialogBox(Element):
    def __init__(self, title='Dialog', *args, **kw):
        Element.__init__(self, 'dialogbox', title=title, *args, **kw)
 
class Select(Element):
    def __init__(self, *args, **kw):
        Element.__init__(self, 'select', *args, **kw)

class Option(Element):
    def __init__(self, text='option', *args, **kw):
        Element.__init__(self, 'option', *args, **kw)
        self.appendChild(Text(text))

