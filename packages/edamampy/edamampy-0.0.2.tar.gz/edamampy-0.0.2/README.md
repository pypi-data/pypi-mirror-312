# edamampy

This project is a library which wraps the Edamam Rest API and provides validation.

## Caution
!!! This is the very first version of this package. There is until now only the code in here for the recipe search api.
In the future I plan on extending the SDK or maybe just leave it at the one api provided by Edamam. !!!
Under active development and breaking changes WILL most likely happen.

## Overview
This project was created by me to make interacting with the Edamam Recipe Search Rest API easier. I wanted to build an app which is
using Edamams vast DB, but the API was cumbersome to work with. Hence, I developed this little library.
It has everything you need to make validated requests to the Recipe Search API provided by Edamam. 
So that in valid queries don't even reach the API don't hit your API quota and make your life easier.
Validation also makes error handling much easier.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation
To install this project, run the following command:
```bash
pip install edamampy
```

# Usage
```
from edamampy import EdamamAPIHandler
from edamampy import ApiSettings

settings = ApiSettings()

handler = EdamamAPIHandler(settings)

for recipes in handler:
    print(recipes.model_dump())

```
Each for loop iteration is one part of the paiginated api response.

# Contribution
If you find anything wrong with the package open up an issue on Github: https://github.com/ma-a-sc/edamampy/issues

# License

MIT License

Copyright (c) 2024 Mark Scharmann

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.