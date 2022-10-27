[![Bankers logo](https://i.imgur.com/aVEdIp2.png)](https://github.com/EarthToAccess/bankers.py)

---

# Welcome to Bankers.py!

Bankers is a card game made by Earth while brainstorming stupidity (until otherwise found). Bankers<b><i>.py</i></b> is a text-based version of this card game coded in Python 3, because Earth had nothing better to do on a Sunday night.

This README will introduce to you the proper setup for the Python file, as well as provide a how-to guide on playing the game! There is also a how-to-play tutorial in the game proper, if you really need it.

---

# Disclaimer

**Bankers.py currently only works under Linux and Windows systems.** Other systems are intended to be programmed for, but lack of resources to do so prevents that. Please ensure you're running on one of these two operating systems ***before*** you use Bankers.py.

# Getting started

Installing and setting up Bankers.py is fairly straightforward! Most of the game's internals are built-in, but there are a few things that get created on first load (or if the files aren't found);

1) The game will initially ask to set up its folders and files for easy configuration, as well as providing savedata. You can choose to ignore this, but will lose access to achievements and saving.
    - On Windows, this will save to your `AppData\Roaming` folder under "Bankers.py".
    - On Linux, this will save to a "Bankers.py" folder in your Home directory.
2) The game will then, within its own directory, create an achievements file. It may also create a save file if you choose to save your game's progress.

Otherwise, the actual install and running is easy; ensure you have Python installed on a Windows machine -- at least 3.8.10 -- and you're on your way!

# Playing the game

## How to play Bankers

Bankers, in this iteration, is a solo game of you versus the House. You'll start with $1000, and you will bet on exactly how likely it is you'll match your card to the House before it matches to you.

You'll be prompted to make your bet of up to 3/4ths your current wallet (e.g. if you have $1000, you can only bet as high at $750). Once you've done that, you'll be given two cards out of a standard 52-card deck. Then, the House will reveal its card. Choose a card from your hand; if it matches the card the House revealed, you've won! Collect your bet doubled. 

If it doesn't, the House will reveal another card. If the House matches the card you played, you lose your bet! If it doesn't, play continues as it did prior.

## Configuring Bankers.py

Configuration can be done from the Main Menu before loading in the game. Currently, you can manage the following;

1) Change the number of cards you can hold in your hand from 2 to 5,
2) Change the number of cards the House can hold in its hand from 1 to 3,
3) Change the type of Wallet you have from the Standard simple $1000 number to Denominations of 1, 5, 25, 125, and 625, or to Endless for no worries (but also no achievements).

# Contributing

It's recommended you [open an issue](https://github.com/EarthToAccess/bankers.py/issues), as problems may be fixed, features may be planned, and so on and so forth behind the scenes. Opening an issue also makes issues, features, and so on easier to track. Pull requests will be ignored; if you open an issue and your bug gets fixed/feature gets added, you'll be added to the game's credits on exit.

# Changelog

The changelog here has some special denotations for its additions/removals/and so on. Additions will be marked with "+"; removals, "-"; notes, "~"; changes/fixes, ">".

## Latest - Beta v1.1

\+ Added proper support for Endless Mode via special blurbs and proper dialog! No more asking for bets, just get straight into the game!  
\> Fixed an issue with the Configuration menu where changing Wallet Type wouldn't actually return up a level like it should've. Now, changing your Wallet Type will bring you back to the Configuration menu properly.  

## Previous

### Beta v1.0

\+ THE GAME. The game is now playable in full! [Open an issue](https://github.com/EarthToAccess/bankers.py/issues) if you find any bugs!  
~ And on that note; there's a known bug involving betting all-in and letting your wallet hit 0 off a bet. A workaround is being found; for now, make sure when you make a bet that you don't bet your total wallet amount.  
~ Also, saving/loading is NOT implemented properly yet. You'll get screamed at that things are disabled. Working on it.

### Alpha v0.2

\+ Proper menu structures! We now have "working" menus, stylized and all! Not that the game is functioning yet but it's the thought that counts I guess
