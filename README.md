![alt text][title]

[title]: images/WGTSTitle.png "title"


My best friend when the new season drops.
(a selfish project)

![](https://img.shields.io/badge/Python-3.5-green.svg)

![alt text][screenshot]

[screenshot]: images/crit.png "screenshot"

## What is this?

#### Allow me to set the stage:

**TL;NGR:** It fetches anime you would like and allows you to download them from one app. :unamused:

> time for the next season of anime to drop.

> watching anime is fun, so you intend to pick up a couple of shows

**HOWEVER**
> you don't know whats worth watching....
> you hit up your bois looking for a quick answer and they give you a list of garbage  (because they have :poop: taste)

> now its up to you to go one AniList,  MyAnimeList or whatever and go through each show vetting whether they are worth your immaculate viewing time.

> not only that but maybe you aren't up for the deep Urobuchi-like show that you have to think about. Maybe you just wanna watch cute girls doing cute things. :neckbeard:

> and once you have your list you have to remember. Every. Week. To get on Nyaa, AnimeBytes, irc etc to get the episode to the show you want.

> or maybe you're smart and you set up a feed. regardless it sounds like a lot of work for the average lazy man. And its why **YOU** end up skipping the season or saying "nothing good this season" :grimacing:

**Now WHAT IF:**

> you could just tell a program what you're looking for and it will fetch you shows based on that criteria and allow you to download them all in one app?

## Development

**Make sure you have python 3.5+ and git installed!**

```
$ git clone https://github.com/heroas/WGTS.git

[^7c9a3675]:

$ sh WGTS/build_files/setup_dev.sh

$ source wgts/bin/activate

$ cd WGTS/src

$ python main.py
```

## Build

:small_red_triangle: Inside of WGTS/src/linux_build.spec or window_build.spec

make sure you change <kbd>pathex</kbd> to the path where WGTS is located. :small_red_triangle:

```
$ git clone https://github.com/heroas/WGTS.git

$ sh WGTS/build_files/setup_dev.sh

$ source wgts/bin/activate

$ cd WGTS

$ pyinstaller linux_build.spec / window_build.spec (depending on your system obviously)
```
