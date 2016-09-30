Fracture (Fork)
=============

![img](/img/img1.png?raw=true "image")

Generative algorithm that makes fracture-like patterns from pre-distributed
randomized seeds.

## Prerequisites

In order for this code to run you must first download and install
repositories:

*    `iutils`: http://github.com/inconvergent/iutils
*    `fn`: http://github.com/inconvergent/fn-python3 (only used to generate
     file names, can be removed in `main.py`.)

## Other Dependencies

The code also depends on:

*    `numpy`
*    `scipy`
*    `python-cairo` (do not install with pip, this generally does not
     work)
*    `pygobject3`
*    `GTK+3`

-----------
http://inconvergent.net

## Fork description

This fork has been developed by Javier Salazar Loyola
([@feandir](https://twitter.com/feandir)), in order to add a front-end
to the algorithm, via a GUI with GTK3 for Python.

## TODO

*    There are some more parameters which can be configured.
*    Fix layout of the screen (too wide for the canvas)
*    Figure out if there is a way to change the size of the Cairo
     canvas on the fly, in order to change the size of the picture.
*    Define if it can be changed the save file format.
