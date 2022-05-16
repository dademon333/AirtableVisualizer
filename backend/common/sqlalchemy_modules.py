import enum

from sqlalchemy.orm.collections import InstrumentedList

from common.db import Base


def convert_instance_to_dict(element_instance: Base):
    """Converts sqlalchemy's instance to dict."""
    result = dict(element_instance.__dict__)
    del result['_sa_instance_state']
    # list() to avoid RuntimeError: dictionary changed size during iteration
    for key, value in list(result.items()):
        if issubclass(value.__class__, enum.Enum):
            result[key] = value.value
        if type(value) is InstrumentedList or issubclass(value.__class__, Base):  # remove relationship's elements
            del result[key]

    return result
