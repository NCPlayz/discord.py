.. currentmodule:: discord

.. _ext_commands_help:

The Help Command
===================

Using The Help Command
-------------------------

By default, there is a help command made for you. What it
does is walk through your commands, and formats it like
``<Command Name> Description``. This is then sorted out
by indents to signify a different cog. By default, your
commands will be in ``No Category``, which is always at the
bottom of the commands list.

Here is a simple example of the default behaviour:

::

    An example bot to showcase the discord.ext.commands extension
    module.

    There are a number of utility commands being showcased here.

    MyCoolCog:
    cool   Says if a user is cool.
    No Category:
      add    Adds two numbers together.
      choose Chooses between multiple choices.
      help   Shows this message
      joined Says when a member joined.
      repeat Repeats a message multiple times.
      roll   Rolls a dice in NdN format.

    Type !help command for more info on a command.
    You can also type !help category for more info on a category.

You may want to send help if the user doesn't use a command
correctly. Here is an example of how to do this:

.. code-block:: python3
    :caption: sos.py
    :emphasize-lines: 8, 10, 18
<<<<<<< HEAD

    from discord.ext import commands

=======

    from discord.ext import commands

>>>>>>> Rewrite the help command prose page (I)
    bot = commands.Bot(command_prefix='!', description="Nothing to worry about here.")

    @bot.command()
    async def sos(ctx, what: str=None):
        """Send Help!"""
        if not what:
            return await ctx.send_help(sos)
        await ctx.send('Sending help for {0}!'.format(what))
        await ctx.send_help(what)

    class MyCoolCog(commands.Cog):
        """It's OK, we saved the damsel."""

        @commands.command()
        async def damsel(self, ctx):
            """There's a damsel in distress!"""
            await ctx.send_help(ctx.bot.get_cog('MyCoolCog'))

    bot.add_cog(MyCoolCog())

:meth:`~.commands.Context.send_help` allows you to specify a
:class:`~.commands.Command`, :class:`~commands.Cog`, or even
a regular string.

Let's take a look at this code step by step:

#. In the command ``sos``, there is a parameter of type ``str`` called ``what``.
    - If that parameter is not passed, it will send help for the ``sos`` :meth:`~.commands.Command` instance.
    - If the parameter is passed, it will send help for the string, which is used to look
      through cog names and commands.
        - Doing ``!sos damsel`` would try to find the command or cog named ``damsel``, and
          send the help for it.

#. In the cog ``MyCoolCog``, there is a docstring provided for help commands.

#. In the command ``damsel``, it will send help for the cog called ``MyCoolCog``, found via :meth:`~.commands.Bot.get_cog`.
    - This would send the docstring of ``MyCoolCog``, and its commands.

    ::

        It's OK, we saved the damsel.

        Commands:
          damsel There's a damsel in distress!

        Type !help command for more info on a command.
        You can also type !help category for more info on a category.

Replacing The Help Command
-----------------------------

If you don't like the default help command, you can replace
the normal help command by setting :attr:`~commands.Bot.help_command`
to a subclass of :class:`~.commands.HelpCommand`.

Here is an example of an alternative help command you can set,
:class:`~.commands.MinimalHelpCommand`

.. code-block:: python3
    :caption: mini_help_bot.py
    :emphasize-lines: 5

    from discord.ext import commands

    description = """Hey! I am your local test bot."""
    bot = commands.Bot(command_prefix='!', description=description,
                       help_command=commands.MinimalHelpCommand())

By default, the help command appears in ``No Category``, which can
seem like a bit of a nuisance when categorising commands. One way
of doing this is by setting the :attr:`~.commands.DefaultHelpCommand.no_category`,
an attribute also found on :attr:`~.commands.MinimalHelpCommand`.

.. code-block:: python3
    :emphasize-lines: 4

    from discord.ext import commands

    bot = commands.Bot(command_prefix='!', description="There is no saviour.",
                       help_command=commands.DefaultHelpCommand(no_category='Help Me!'))

You can also set the :class:`~commands.Cog` of a help command,
simply by setting :attr:`~commands.HelpCommand.cog`. However,
if you plan on having the ability to reload or disable extensions
containing cogs, just setting it isn't wise idea.

To counter this, you could set the new help command to default,
 during the teardown of an extension.

.. code-block:: python3
    :emphasize-lines: 22, 23

    from discord.ext import commands


    class Help(commands.Cog):
        """This isn't the right place for help."""

        @commands.command()
        async def sos(self, ctx, what: str = None):
            """Send Help!"""
            if not what:
                return await ctx.send_help(self.sos)
            await ctx.send('Sending help for {0}!'.format(what))
            await ctx.send_help(what)


    def setup(bot):
        bot.add_cog(Help())
        bot.help_command = commands.DefaultHelpCommand(no_category='Help.')
        bot.help_command.cog = bot.get_cog('Help')


    def teardown(bot):
        bot.help_command = commands.DefaultHelpCommand()

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

    description = """rooEZ"""
    bot = commands.Bot(command_prefix='!', description=description, help_command=MyHelp())

Writing A Help Command
-------------------------

