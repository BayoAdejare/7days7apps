
from copy import deepcopy
import django.newforms as forms
from django.utils.datastructures import SortedDict

from django.newforms.fields import Field
from django.newforms.widgets import TextInput, Textarea

#Dyna forms
class DynaDeclarativeFieldsMetaclass(forms.forms.DeclarativeFieldsMetaclass):
    """
    Metaclass that converts Field attributes to a dictionary called
    'base_fields', taking into account parent class 'base_fields' as well.
    """
    def __new__(cls, name, bases, attrs):
        #fields = [(field_name, attrs.pop(field_name)) for field_name, obj in attrs.items() if isinstance(obj, Field)]
        fields = []
        for field_name, obj in attrs.items():
            if isinstance(obj, Field):
                fields.append((field_name, attrs.pop(field_name)))
            elif isinstance(obj, list):
                obj = attrs.pop(field_name)
                for i in xrange(len(obj)):
                    fields.append((field_name+"_"+str(i + 1), obj[i]))
        fields.sort(lambda x, y: cmp(x[1].creation_counter, y[1].creation_counter))

        # If this class is subclassing another Form, add that Form's fields.
        # Note that we loop over the bases in *reverse*. This is necessary in
        # order to preserve the correct order of fields.
        for base in bases[::-1]:
            if hasattr(base, 'base_fields'):
                fields = base.base_fields.items() + fields

        attrs['base_fields'] = SortedDict(fields)
        return type.__new__(cls, name, bases, attrs)
    
class DynaForm(forms.Form):
    __metaclass__ = DynaDeclarativeFieldsMetaclass