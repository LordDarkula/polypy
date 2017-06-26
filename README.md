# polypy
Symbolic manipulation of mathematical expressions

## License
polypy is available under the MIT license. See the LICENSE file for more info. Copyright © 2016 Aubhro Sengupta. 
All rights reserved.

## Introduction
Polypy is a libbrary designed to store mathematical expressions symbolically, 
so they can be stored and evaluated as functions at any time. It is designed to
look and feel like real mathematical notation as much as possible.

## Usage
``` python
from polypy.base import x
```
To create basic functions 
``` python
# Simple linear function
>>> f = 2*x
>>> f(3)
6

# Quadratic function
>>> f = 3*x**2 + 2*x + 3
>>> f(1)
8

```
Simple functions can be chained together to create more complex 
functions.
``` python
# g = 2^2^x
>>> g = 2**2**x
>>> f = x + 3

# h = 2^2^x + 3
>>> h = f(g)
```
