# distrandomiser - Distance, but Randomised (Alpha)
This script takes in the Distance Adventure mode maps, and spits out
a playlist with both the map and ability unlock order randomised -
abilities are even adjusted so that they logically carry over like they
would if the maps were actually played in that order. This can be used
when racing the game, to make it just a little bit more interesting for
those who have played the game to death.

Absolutely nobody asked for this, but guess what? I made it anyway.

As you can probably expect, this is inspired by various game randomisers
such as [ALTTP Randomiser](http://vt.alttp.run). You're probably wondering
why I decided to adapt an action-adventure game mode into a much more
linear game, and I can't actually answer that - I don't know. But it
exists!

This is currently in alpha. Most of the core functionality is there
and works reasonbly well, however it may need tweaking, the code could
be cleaner, and there's obviously more features I want to add. Plus,
Distance itself is currently in beta - this will need to be updated to
support the finished Adventure mode once it is completed, so it doesn't
really make sense to call this a full, stable release until that happens.

As of right now, there's no real options so to speak, besides seed.
I plan to have more options available in the future, as well as the
ability to generate customised games, not just randomised ones.

It shouldn't be possible to get stuck with the current algorithm, but
you may need to use techs like wallshoving (pushing yourself against
walls to leave the track), which may be tricky or unpredictable. Again,
alpha; this is still somewhat experimental. If you do get stuck and
can't progress, make a new issue so I can check that out (or tell you
how to beat it if you just have no idea what to do).

## Differences from the normal game
- Obviously, as mentioned in the first sentence of this readme, the order
  of the maps and the abilities unlocked have been randomised.
- Boost is enabled by default, you do not need to pick it up at an
  ability trigger.
- Wing corruption zones have been removed to allow for more variety.
- All ability tutorial text triggers have been removed, because you
  don't need to learn how to play the game when you're doing randomiser.

## How to Use
First, you need to aquire the randomiser script, and install the
dependencies required to use it:

    $ git clone https://github.com/TntMatthew/distrandomiser.git
    $ pip install distanceutils numpy numpy-quaternion
    
After that, you need to get the .bytes files of the original Adventure
maps. You can do this for most of them by simply opening them in the
editor and saving them as a new file. Don't worry about getting a hold
of Destination Unknown or the Credits level for now - neither are
included at the moment as I can't be bothered to install Spectrum
to get them - and even then, once they are implemented, they may only be
inserted completely unmodified at the end of the playlist, as nobody wants
a long unskippable cutscene in the middle of a run.

Once you have the map files, you can run the randomiser script
with Python.

    $ python distrandomiser.py [dir_of_level_files]

When you run it, you will be asked to input a seed. You can simply just
press enter if you want to use a random seed. The script will then
take in the map files, edit them, then automatically spit them out
into your MyLevels directory with the filenames `randomiser1` through
`randomiser10`. (Don't worry, all mode tags are stripped so they won't
clog up your my levels list ingame.) A playlist file, `randomiser.xml`,
will also be generated and automatically put into the LevelPlaylists
directory. When you want to play your randomised game, go to any Arcade
level select, open the playlist list, and select randomiser.
