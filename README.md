## Motivation

## About
This is a python script to get all accepted submissions after a given time and date of a given contest on vjudge.net and make those submissions shareable after some cleaning and sorting and then generate a file contains those shareable links as json format.

## Installation
* Install python3
* Download this repo
* Set config.json file
* Open the terminal where the repo's directory is the current working directory
* run `index.py` file by the following command `python3 index.py`
* DONE :)

## About config.json file
* You can get `contestId` from the url. for example if `https://vjudge.net/contest/123456` is the contest link then `123456` is the contestId
* `dateAndTime`
  * If you want only submissions after specific date and time, set`dateAndTime` property. Otherwise leave it as empty string
  * If it is given, it must be in this format `%Y-%m-%d %H:%M` like this `2022-11-18 14:55`
* To get `Jax.Q` cookie 
  * Open vjudge.net on your browser
  * Login if you are not logged in.
  * Open dev tool and type `document.cookie` in the console 
  * `Jax.Q` would be something like this `username|GO0BOBZXFGHQ3QYJKP54IVP18CVUMS`
* If `generatedFileName` is not given, the generated file name will be in the following format `username_contestId_randomNumber.txt`

## About the generated file
* All submissions grouped by problem number
* All submissions of the same problem number group by language
* All submissions of the same language sorted by submission time (newest first)

## Contribution
Here is some ideas for contributing
- The output file is json format, do you have a better format that you think it would be nicer ?

- Instead of generating txt file, generate pdf. It would be nicer and shorter as you can make problem links as clickable hyperlink

- Build error handlers as script assumes data is correct and everything goes as expected.

- Refactor the code to be more maintainable, extendable and reusable. this would be highly appreciated.