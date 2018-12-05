# Dictation Evaluation Reddit Parser [![Build Status](https://travis-ci.org/CSC792-SDSMT-DERP/DERP.svg?branch=master)](https://travis-ci.org/CSC792-SDSMT-DERP/DERP)

## What is DERP?
DERP is a query language for aggregating data from various sources. It was developed as a requirement for CSC 792, Compilers, in the Fall of 2018 at the South Dakota School of Mines & Technology.

DERP was designed with a focus on querying Reddit and includes a module for doing so. Other sources may be integrated with DERP using additionl plug-in modules which modify the core language.

This repository contains the core DERP library as well as a simple console frontend for interacting with the library.

### Documentation
Documentation covering the DERP library, language, frontend, and module system can be found in the [documentation subdirectory](./documentation).

- Original Project Documentation
  - [White Paper](./documentation/White%20Paper.pdf) ([Errata](./documentation/White%20Paper%20Errata.md))
  - [Language Tutorial](./documentation/Language%20Tutorial.pdf) ([Errata](./documentation/Language%20Tutorial%20Errata.md))
  - [Language Reference](./documentation/Language%20Reference.pdf) ([Errata](./documentation/Language%20Reference%20Errata.md))
  - [Final Report](./documentation/Final%20Report.md)
- DERP Modules
  - [Module API](./documentation/Module%20API.md)
  - [Built In Modules](./documentation/Built%20In%20Modules.md)

## Getting Started
The DERP interpreter is built to run in Python 3.5+.

The following Python packages are required to run the project and its tests:
 * lark-parser 0.6.5
 * newspaper3k 0.2.8
 * praw 6.0.0
 * prawcore 1.0.0
 * pytest 4.0.1

Once the project has been cloned, these dependencies may be installed automatically by simply running `pip3 -r ./requirements.txt`.

Once the dependencies have been installed, start the application by running
`python3 ./derp.py` **from the root of the project**. This will open the DERP Interpreter, which presents a prompt that looks much like a standard Python interpreter prompt (`>>>`).

To execute a file of DERP code, simply redirect the file into the DERP interpreter: `python3 ./derp.py < my_file`.

To run all of the available tests, run `python3 -m pytest` from the root of the project.

## Example Code
DERP has three modes of execution: Main Mode, Selection Mode, and Criteria Mode.

DERP interpreters begin in Main Mode, and switch modes using `create` and `stop` statements.

The simplest DERP program consists of acquiring posts from a source and presenting them to the user (as in the example below).

```
load "reddit"

create a new selection
add posts from reddit
read
```

After executing the above code, the interpreter will pause, and execution will transfer to the post presentation frontend. In the reference implementation, the frontend will present the data returned by the query until the user enters `stop` or there is no more data left.

The next example builds a query to search multiple subreddits for posts that pertain to Elon Musk, but not the Tesla company.

```
load "reddit"

create a new criteria
add posts with "Musk" in the title
remove posts with "Tesla" in the title or with "Tesla" in the body
save as "News on Elon Musk"
exit

create a new selection
add posts from subreddit "technology" or subreddit "futurology" or subreddit "space"
remove posts with under 1000 upvotes
save as "Tech News"
exit

create a new selection
add posts from "Tech News" matching
"News on Elon Musk"
save as "Tech News about Elon Musk"
stop

read "Tech News about Elon Musk"
```

Selections and criteria that have been saved persist across multiple runs of the program. In the future, we may fetch an updated listing of posts using the following code.

```
load "reddit"
read "Tech News about Elon Musk"
```
