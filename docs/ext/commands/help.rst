.. currentmodule:: discord

.. _ext_commands_help:

Help Commands
=================

The simplicity of :class:`~.commands.HelpCommand` allows you to customise
your experience very easily.

Sending Help
---------------

You may want to send help if the user doesn't use your command
correctly. Here is an example of what you can do:

.. code-block:: python3
    :caption: sos.py
    :emphasize-lines: 8, 10

    from discord.ext import commands 

    @commands.command()
    async def sos(ctx, what: str=None):
        """Send Help!"""
        if not what:
            return await ctx.send_help('sos')
        await ctx.send('Sending help for {0}!'.format(what))
        await ctx.send_help(what)

    def setup(bot):
        bot.add_command(sos)

Custom HelpCommand
---------------------

If you don't like the default help command, you can try out
:class:`~.commands.MinimalHelpCommand`, or even make your own
by subclassing it.

Both of these methods follow this simple method:

Providing a form of :class:`~.commands.HelpCommand` as the
`help_command` kwarg for :class:`~.commands.Bot`.

.. code-block:: python3
    :caption: mini_help_bot.py
    :emphasize-lines: 5

    from discord.ext import commands

    description = '''Hey! I am your local test bot.'''
    bot = commands.Bot(command_prefix='!', description=description,
                       help_command=commands.MinimalHelpCommand())

Subclassing it is as easy as pie, you can modify any exposed parts
of the system and it should work fine.

Here is an example of what you are able to do by subclassing
:class:`~.commands.MinimalHelpCommand`:

.. code-block:: python3
    :caption: roo_ez.py

    from discord.ext import commands

    class MyHelp(commands.MinimalHelpCommand):
        def __init__(self):
            super().__init__(no_category='Misc')

        def add_bot_commands_formatting(self, commands, heading):
            if commands:
                joined = ', '.join('`{0}`'.format(c.name) for c in commands)
                self.paginator.add_line('Category: [__**%s**__]' % heading)
                self.paginator.add_line(joined)

    description = '''rooEZ'''
    bot = commands.Bot(command_prefix='!', description=description, help_command=MyHelp())
