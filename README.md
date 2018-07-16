# Discord-Bot
This is a general purpose Discord Bot made for music functionality and miscellaneous fun.

### Getting Started
First, you should install the requirements:

```
pip install -r requirements.txt
```

Additionally, if you want to use the Youtube feature, you'll need to install ffmpeg and add it to
your environment variables.

In secret.py, set the `SECRET_KEY` variable equal to the bot account's token (don't commit after
you've edited it).


### Debug Mode
You should use `debug_out()` instead of `print` statements for debugging.

When running main.py from the terminal, you can specify debug-mode:

```
python main.py debug
```

In debug-mode, `debug_out` statements are printed and the debug bot specified in secret.py is used
instead of the public bot.