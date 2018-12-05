# Dictation Evaluation Reddit Parser [![Build Status](https://travis-ci.org/CSC792-SDSMT-DERP/DERP.svg?branch=master)](https://travis-ci.org/CSC792-SDSMT-DERP/DERP)

## What is DERP?
DERP is a query language for aggregating data from various sources. It was developed as a requriement for CSC 792, Compilers in Fall of 2018 at the South Dakota School of Mines & Technology. While it was designed with a focus on Reddit and includes a plugin for querying Reddit, it allows for language modification through plugins which can be used to get data from any location. The code in this project is an implementation of a DERP interpreter, and this project's wiki serves as a manual for the language itself.

## Getting Started
The DERP interpreter is built to run in Python 3.5+. 

The following Python packages are required to run the project and its tests:
 * lark-parser 0.6.5
 * newspaper3k 0.2.8
 * praw 6.0.0
 * prawcore 1.0.0
 * pytest 4.0.1

A `requirements.txt` file is included with the project which can be used to install dependencies using `pip3 -r requirements.txt` 

Once the project has been cloned and requirements installed, execute the application with
`python3 ./derp.py` from the root of the project. This will open the DERP Interpreter, which presents a prompt that looks much like a standard Python interpreter prompt (`>>>`).

To execute a file of DERP code, simply redirect the file into the DERP interpreter: `python3 ./derp.py < my_file`
 
## Example Code
DERP has three modes of execution. Interpreters begin in Main Mode, and switch modes at `create` and `stop` statements. The simplest DERP code which will do anything significant will simply acquire some posts from a source and start displaying them on screen.

```
load "reddit"

create a new selection
add posts from reddit
read
```

After executing the above code, the REPL will pause, and a post presentation frontend will take over the terminal. This frontend will present the data returned by the query until the user enters `stop` or there is no more data left.

Let's look at a more complicated example. The following DERP code will build a query to search a few subreddits for posts that are about Elon Musk, but not about the Tesla company.

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

Note that if you save this to a file and pipe it into the DERP interpreter, it will display a single post and then exit because the end of the file was found. To display additional posts, just add empty lines to the end of the file. 

One of the features of this implementation of the DERP interpreter is persistent storage of all critera and selections ever created. If you would like to read the posts one at a time, start the DERP interpreter and enter the following lines:

```
load "reddit"
read "Tech News about Elon Musk"
```

This will load up the Reddit module, and then execute the selection statements that were saved by the interpreter previously. 

## DERP Plugins
TODO: Link the following into WIKI
 * Module API
 * Built-in Modules


## Original Project Documentation
TODO: Link the following into WIKI
 * White Paper
 * Language Tutorial
 * Language Reference
 * Errata
 * Final Report
