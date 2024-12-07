import inspect
from functools import partial
from typing import get_type_hints, get_origin, Annotated, get_args, Union


def kaya_io():
    def wrapper(cls):
        annotations = get_type_hints(cls, include_extras=True)

        # Build the __init__ signature and method body
        parameter_lines = []
        body_lines = []
        for field_name, field_type in annotations.items():
            # Skip non-Annotated fields
            if get_origin(field_type) is not Annotated:
                continue

            if field_name in ["_errors", "_results"]:
                continue

            # Extract the base type from Annotated
            base_type = get_args(field_type)[0]

            # Create the property getter
            getter_func = partial(create_getter, field_name=field_name)
            getter = getter_func()
            setattr(cls, field_name.lstrip('_'), getter)

            # Create the setter if MinLen is present
            setter_func = partial(create_setter, field_name=field_name)
            setter = setter_func()
            setattr(cls, f'set_{field_name.lstrip("_")}', setter)

            # Add to the parameters list
            optional_type = Union[base_type, None]  # Optional[type]
            param = inspect.Parameter(
                field_name.strip("_"),  # Remove leading underscore for the argument
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                default=None,
                annotation=optional_type,
            )

            # Add to the method body
            body_lines.append(
                f"if {field_name.strip('_')} is not None: self.set_{field_name.strip('_')}({field_name.strip('_')})"
            )

            # Build the parameter string for the method
            parameter_lines.append(
                f"{param.name}: {base_type.__name__} | None = None"
            )

        # Combine everything into a valid function string
        init_code = f"""def __init__(self, {', '.join(parameter_lines)}):\n\tsuper(type(self), self).__init__()\n\t{'\n\t'.join(body_lines)}
        """
        # Create a local namespace to define the method
        namespace = {}
        exec(init_code, globals(), namespace)

        # Attach the dynamically created `__init__` method to the class
        setattr(cls, "__init__", namespace["__init__"])

        return cls
    return wrapper


def create_setter(field_name):
    def setter(self, values):
        setattr(self, field_name, values)

    return setter


def create_getter(field_name):
    @property
    def getter(self):
        return getattr(self, field_name)

    return getter
