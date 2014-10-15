Fall2014IDE
===========

Code for the Fall 2014 IG IDE with TEDxSMU.

Runs a photobooth with 4 Raspberry Pi's, asking users
to take a picture with a whiteboard that contains a word
with a certain part of speech. It'll then crop and insert
their word and face within the correct part of a TED Talk
title that has been given in the past.

camerabooth.py runs the photo booth on Raspberry Pis with the
camera module. It takes pictures and saves them to a directory
with a naming schema that the server watches. The schema is based
on the Raspberry Pi's "index", or the integer identifier you give
it.

PictureManipulation.py runs on the "server" computer, and watches 4
drive paths, updating to see the most recent files, and seeing if they
match the schema it expects. When it gets one picture from each Pi, it'll
generate the Mad Libs title picture and display it for 2 mins and 30 secs
before it listens and generates the next one if the files exist.

Both modules require PyGame.

This repository contains Visual Studio 2013 project and solution files.
It also contains tools I wrote to make this easier, and tools I meant to 
implement but left for later. I'll probably migrate those to a new repository 
later on.

Written in Python, in case you couldn't tell originally.
