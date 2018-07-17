# Discord-Bot
This is a general purpose Discord Bot made for music functionality and miscellaneous fun.

### Getting Started

##### Requirements
First, you should install the requirements:

```
pip install -r requirements.txt
```

Additionally, if you want to use the voice feature, you'll need to install ffmpeg and add it to
your environment variables. Instructions on how to do that can be found here:

http://adaptivesamples.com/how-to-install-ffmpeg-on-windows/

##### Installation

Either clone the project or download the .zip file. In secret.py, set the `SECRET_KEY` variable 
equal to the bot account's token (don't push secret.py after you've edited it).

You can run the bot with:

```
python main.py
```


### Debug Mode
You should use `debug_out()` instead of `print` statements for debugging.

When running main.py from the terminal, you can specify debug-mode:

```
python main.py debug
```

In debug-mode, `debug_out` statements are printed and the debug bot specified in secret.py is used
instead of the public bot.