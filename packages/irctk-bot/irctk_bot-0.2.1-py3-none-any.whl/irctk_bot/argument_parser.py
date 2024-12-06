from inspect import Parameter, signature
from typing import Any, Dict, List, Optional, Tuple, Union

from irctk.client import Client
from irctk.message import Message
from irctk_bot.context import Context
from irctk_bot.controller import Controller


class ArgumentBuilder:
    def __init__(self):
        self.args = []
        self.kwargs = {}

    def add(self, value: Any, parameter: Parameter) -> None:
        if parameter.kind == Parameter.KEYWORD_ONLY:
            self.kwargs[parameter.name] = value
        elif parameter.kind == Parameter.POSITIONAL_OR_KEYWORD:
            self.args.append(value)

    def build(self) -> Tuple[List[str], Dict[str, Any]]:
        return (self.args, self.kwargs)


class ArgumentParser:
    def __init__(self, func):
        self.func = func
        self.supported_types = (
            str,
            int,
            Context,
            Any,
            Parameter.empty,
            Controller,
            Client,
            Message,
        )

    def validate(self):
        for value in signature(self.func).parameters.values():
            if value.kind == Parameter.POSITIONAL_OR_KEYWORD:
                if (
                    self.unwrap_type_optional(value.annotation)
                    not in self.supported_types
                ):
                    raise TypeError(f'unsupported type {value.annotation}')

            elif value.kind == Parameter.VAR_POSITIONAL:
                pass

            else:
                raise TypeError(f'unsupported argument kind {value.kind}')

    def unwrap_type_optional(self, annotation):
        if '__origin__' not in annotation.__dict__:
            return annotation

        if '__args__' not in annotation.__dict__:
            return annotation

        if annotation.__dict__['__origin__'] != Union:
            return annotation

        args = list(annotation.__dict__['__args__'])
        args.remove(None.__class__)
        if len(args) == 1:
            return args[0]
        return annotation

    def parse(
        self, text: str, dependencies: Optional[Dict[Any, Any]] = None
    ) -> Tuple[List[str], Dict[str, Any]]:
        builder = ArgumentBuilder()

        for parameter in signature(self.func).parameters.values():
            human_name = parameter.name.replace('_', ' ')

            if parameter.kind == Parameter.POSITIONAL_OR_KEYWORD:
                if dependencies and parameter.annotation in dependencies:
                    builder.add(dependencies[parameter.annotation], parameter)

                elif len(text):
                    value, _, text = text.partition(' ')

                    annotation = self.unwrap_type_optional(parameter.annotation)

                    if parameter.annotation == Parameter.empty:
                        builder.add(value, parameter)
                    elif parameter.annotation == Any:
                        builder.add(value, parameter)
                    elif annotation == str:
                        builder.add(value, parameter)
                    elif annotation == int:
                        try:
                            integer_value = int(value)
                        except ValueError:
                            raise ValueError(
                                human_name, 'argument is not a valid number'
                            )
                        builder.add(integer_value, parameter)
                    else:
                        raise TypeError(f'unsupported type {parameter.annotation}')
                elif parameter.default == Parameter.empty and not len(text):
                    raise ValueError(human_name, 'missing argument')

            elif parameter.kind == Parameter.VAR_POSITIONAL:
                builder.args += text.split()
                text = ''

            else:
                raise TypeError(f'unsupported argument kind {parameter.kind}')

        if len(text):
            raise ValueError(f'unexpected arguments {text}')

        return builder.build()
