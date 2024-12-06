# irctk-bot

Bot framework for irctk. irctk-bot can be installed from PyPI.

Usage:

```shell
$ irctk-bot -h irc.example.com -m irctk_bot.modules.ping
```

Where module is the Python module name to any modules you wish to load, you may
provide `-m` multiple times.

Alternatively, you may use a config file, see `example.toml`.

```
$ irctk-bot -c example.toml
```

## Writing a module

Expose an instance of the `Module` class as a global `module` property to a
Python module. Use the `Module.command` decorator to register commands.

```python
from irctk_bot import Context, Module

module = Module()

@module.command()
def ping(context: Context, name: Optional[str] = None) -> None:
    if name:
        return context.reply(f'pong {name}')
    context.reply('pong')
```
