# Project Plan

DERP development was active from August 27, 2018 to December 07, 2018. DERP was developed following the [Iterative Waterfall](https://www.geeksforgeeks.org/software-engineering-iterative-waterfall-model/) model. As such, a large amount of time was spent developing requirements and specifications (August 27, 2018 - November 04, 2018). These requirements and specifications were set forth in the [White Paper](./White%20Paper.pdf) and [Language Reference](./Language%20Reference.pdf). The [Language Tutorial](./Language%20Tutorial.pdf) also set forth expectations for user interaction. The initial design phase lasted from November 04, 2018 to November 08, 2018. However, certain aspects of DERP were found to be infeasible and needed to be re-specified. These changes to the specifications may be found in the errata pages ([White Paper Errata](./White%20Paper%20Errata.md), [Language Reference Errata](./Language%20Reference%20Errata.md), [Language Tutorial Errata](./Language%20Tutorial%20Errata.md)). Coding took place between November 08, 2018 and December 03, 2018. Additional tests were put in place between December 03, 2018 and December 05, 2018. Finally, documentation was then written to promote maintenance.

## Deliverable Schedule
  - September 21: [White Paper](./White%20Paper.pdf) due
  - October 22: [Language Tutorial](./Language%20Tutorial.pdf) and [Reference](./Language%20Reference.pdf) due
  - November 28: [Presentation](./presentation/Presentation.md) and Demo
  - December 05: Soft due date for project
  - December 13: Hard due date for project


## Project Timeline
  - August 27:
    - Form team of five members
  - August 29:
    - Propose DERP
    - Outline White Paper
  - September 03:
    - Write Test Plan
  - September 09:
    - Begin drafting DERP grammar
    - Set up CI with GitLab and Azure Cloud
  - September 12:
    - Begin writing White Paper
  - September 21:
    - Finish White Paper
  - September 27:
    - Finish rough draft of DERP grammar
  - October 05:
    - Spin up on Python parsing (Lark)
  - October 06:
    - Outline Language Reference
    - Outline Language Tutorial
  - October 15:
    - Begin drafting Language Reference
    - Team size decreased to four members
  - October 18:
    - Begin drafting Language Tutorial
  - October 21:
    - Finish Language Tutorial
    - Finish Language Reference
  - November 04:
    - Begin drafting DERP Architecture
    - Team size decreased to three members
  - November 08:
    - Finish drafting DERP Architecture
    - Draft timeline for code requirements
  - November 11:
    - Break ground on Python code
    - Encode DSL grammar in code
  - November 16:
    - Implement basic language processing
  - November 18:
    - Implement language processing completely
  - November 23:
    - Set up CI with Digital Ocean and GitLab
    - Implement basic backend logic and data structures
  - November 25:
    - Implement Reddit module
    - Implement backend logic and data structures completely
    - Begin enforcing semantic checks
  - November 27:
    - Write DERP presentation and demo script
  - December 03:
    - Outline Final Report
    - Migrate repository to Github
    - Set up CI with TravisCI and Github
    - Finish implementing semantic checks
  - December 04:
    - Ensure Test Plan is enforced
  - December 05:
    - Finish main development cycle on DERP
    - Begin drafting Final Report, Errata
  - December 13:
    - Last possible date to turn in project and report

Acceptance and certification testing? Solves the problems set forth in the White Paper.

## Code and Documentation Storage
Between August 27 and December 03, DERP was version controlled using Git on the SDSM&T MCS GitLab server. However, on December 03, the code was migrated to Github. All commit history was preserved during this transition.

As the team consisted of three members by the time coding began, branching was not enforced; however, feature branches were used for implementation of a number of pieces of the project. Communication sufficed to prevent major merge conflicts and resolve minor ones.

## Acceptance Criteria
As stated in our white paper, our primary goals were:
  - Intuitively querying multiple sources to produce a single stream of data
  - Supporting plugin modules which could be used with the same core language
  - Supporting speech-to-text and text-to-speech with a languge designed to be as close to natural English as possible

Firstly, it is possible to query multiple sources to produce a single stream of data as is required.
This feature is demonstrated in the example below which shows multiple
sources being saved into a reusable selection and then read from. A feature that was under
consideration but was removed was to permit querying against all loaded sources. As a module
may provide an infinite number of sources, this was deemed infeasible.
```
>>> load "reddit"
>>> create a new selection
(selection)>>> add posts from subreddit "nfl" and subreddit "all"
(selection)>>> save as "my news"
(selection)>>> stop
>>> read "my news"
>>>
```

Secondly, the language defines a set of core statements, and allows modules to specify grammar extensions.
This is possible thanks to our module interface definition which specifies the required API for all
extending modules. For example, the Reddit module specifies the keywords "subreddit" and "reddit" for
selecting sources. Additionally, it specifies the fields to expect on Reddit posts, such as the
upvote count and the post's body.

Finally, almost all statements in the language are grammatically correct English
phrases, though some are occasionally somewhat odd sounding when spoken.
The example given above demonstrates a reasonable English phrase for creating a selection,
however the following example is a little rougher:
```
>>> load "reddit"
>>> create a new selection
(selection)>>> add posts from subreddit "nfl" without under 100 upvotes
(selection)>>> save as "my news"
(selection)>>> stop
>>> read "my news"
>>>
```

# DERP Architecture

DERP can be split into three components: the frontend, the core library, and the module system.

## Frontend
The frontend is responsible fetching input from the user and supplying it to the core library. Additionally, the frontend must handle the various [UXActions](../derp/session/UXAction.py) that may be returned. This interaction is driven by the frontend by calling the methods defined in [ISessionController](../derp/session/ISessionController.py).

The READ UXAction returns a [SelectionExecutor](../derp/selections/execution/SelectionExecutor.py) which returns an iterable of [Post](../derp/posts/IPost.py) results via the `results()` method. These posts must then be presented by the frontend. The iterable will end when no more posts are found for a given selection, or the sources for the selection return a large number of sequential posts which do not match the criteria specified.

## Core Library

The core implementation of ISessionController is [SessionController](../derp/session/SessionController.py). The SessionController handles interpreting statements in the DERP language and maintaining the state of the interpreter. The SessionController delegates much of its logic to other classes. These classes include the language focused components such as the [Parser](../derp/language/Parser.py), [Transformer](../derp/language/Transformer.py), [SemanticChecker](../derp/language/SemanticChecker.py), and [Evaluator](../derp/session/Evaluator.py) as well as the [SessionStateController](../derp/session/session_state/SessionStateController.py), [SelectionExecutorFactory](../derp/selections/execution/SelectionExecutorFactory.py), and [ModuleController](../derp/modules/ModuleController.py).

### Converting Lines of Input to ASTs

Lines of input are passed first into the Parser for the appropriate mode. If a syntax error occurs, an exception is raised and returned to the frontend as an ERROR UXAction. After passing through the Parser, the SessionController receives a raw Lark Tree (AST). The SessionController then passes the AST through the Transformer. The Transformer applies various transforms contained in the [Transformer class proper](../derp/language/Transformer.py) and in the [qualifier reduction directory](../derp/language/qualifier_reductions). Once the tree has been shaped, the tree undergoes various semantic checks as applied by the [Semantic Checker](../derp/language/SemanticChecker.py). If a semantic error is detected during either of the previous steps, an exception is raised and handled in the same manner as syntax errors. If the tree is found to be semantically valid, it is passed to the [Evaluator](../derp/session/Evaluator.py) in order to produce a [SessionAction](../derp/session/SessionAction.py) which will be interpreted by the SessionController.

### Converting ASTs to SessionActions
The [Evaluator](../derp/session/Evaluator.py) uses a Lark Visitor to search for certain types of nodes inside the AST. When a node is found that would imply a certain action should be taken, the evaluator constructs a [SessionAction](../derp/session/SessionAction.py) with the action to take and the data needed to carry out the action.

### Interpreting Criteria and Selection Lines
As lines of selections and criteria are processed by
the Evaluator, APPEND_TO_BUFFER SessionActions are created.
The SessionController then appends the line of text and the processed AST to the active [Buffer](../derp/session/session_state/IBuffer.py) via the [SessionStateController](../derp/session/session_state/SessionStateController.py). The buffer may be a [CriteriaBuffer or SelectionBuffer](../derp/session/session_state/Buffer.py) depending on the active mode. The buffers progressively append the lines and ASTs to internal data structures. The lines are simply stored in lists, and the ASTs are appended to [Criteria](../derp/criteria/Criteria.py) objects and [Selection](../derp/selections/Selection.py) objects respectively. During an append step, the appended AST is converted into its backend representation.  

Criteria statement ASTs are split into their actions (ADD or REMOVE) and their qualifier subtrees. The qualifier subtrees are then converted into [QualifierTrees](../derp/qualifiers/QualifierTree.py). This conversion happens via the static `convert(root_qualifier)` function in the [LarkQualifierConverter](../derp/qualifiers/Converter.py).
The new QualifierTree may then be appended to the criteria by joining the existing QualifierTree for the criteria wih the new one using various ParentNodes. For ADD statements, the two trees are joined with an OR node. For REMOVE statements, the new tree is added to a NOT node and an AND node is used to join the previous tree with the new NOT node.

Selections statement ASTs undergo a similar transformation. The action (ADD or REMOVE) and qualifier subtree are parsed out for each line; however, the specified sources are additionally extracted. Each selection maintains a dictionary consisting of (Source AST, QualifierTree) pairs. In the case of ADD statements, the newly converted QualifierTree is then merged with the existing QualifierTree for each of the sources specified. For REMOVE statements, the new QualifierTree is merged with all of the existing QualifierTrees. If one of the sources specified is another selection rather than a module defined source AST, a few extra steps must be taken. All of the (Source AST, QualifierTree) pairs defined in the nested selection are merged with the QualifierTree specified by the AST to be appended. Then, each of the newly qualified (Source AST, QualifierTree) pairs are merged with the existing (Source AST, QualifierTree) pairs in the selection being appended to.

Semantic errors may be thrown during the append process. For example, if a user tries to issue a REMOVE statement in Selection Mode before any ADD statements have been issued, a semantic error will be thrown.

### Executing a Selection

As discussed above, a selection is simply a dictionary of (Source AST, QualifierTree) pairs. When a selection is to be executed, it is passed through the [SelectionExecutorFactory](../derp/selections/execution/SelectionExecutorFactory.py). The SelectionExecutorFactory then loops over the (Source AST, QualifierTree) pairs, dispatches the queries to the  [ModuleController](../derp/modules/ModuleController.py), filters the returned results using [PostIteratorFilters](../derp/selections/execution/PostIteratorFilter.py), and recombines the filtered results into one stream using a [PostIteratorMuxer](../derp/selections/execution/PostIteratorMuxer.py). The result stream is finally wrapped in a [SelectionExecutor](../derp/selections/execution/SelectionExecutor.py) and returned to the frontend in a READ UXAction.

### Saving Selections and Criteria
The SessionController expects an [IFileManager](../derp/session/session_state/IFileManager.py) to be passed into its constructor which will be used for saving selections and criteria. It simply expects to be able to save, recall, and delete lists of strings by name. This allows the persistence layer to be adapted across many implementations. The [default implementation](../derp/session/session_state/FileManager.py) stores the data in directories in the current working directory. However, a [mock implementation](../derp/session/session_state/tests/MockFileManager.py) is used for testing which simply uses Python dictionaries. One could imagine that if DERP was used to write an interpreter for a voice assistant, the data could be stored in cloud services such as [Firebase](https://firebase.google.com/products/database).

## Module System
The DERP interpreter has a built in system for loading and unloading language modules; this system closely parallels the expectations laid out in the DERP Language Reference. For now, all modules are registered from known locations on startup, so adding a new module would require modifying the program entrypoint [derp.py](../derp.py). In the future, the interpreter will search some known directory for submodules and attempt to discover and load them.

The modules themselves provide the following functionalities through the [IModule](../derp/modules/IModule.py) interface:

 * Obtain the name of the module
 * Obtain the Grammar for sources of the module
 * Obtain the definition of Posts generated by this module. This definition includes the names and types of fields exposed by the posts.
 * Obtain an iterator from the module, given the AST for its source and the Qualifier Tree for the query

When building a post iterator, modules are encouraged to use the Qualifier Tree given to filter the posts returned; however, this is not a requirement. Posts will be filtered by the interpreter after they are returned.

For a full description of the Module API, see the [Module API page](./Module%20API.md). For information about built in modules, see the [Built in Modules page](./Built%20In%20Modules.md). Below are descriptions of the main considerations when implementing a Module.

### Source Grammars
The grammars returned by a module have the following restrictions:
 * Every rule or token in the Grammar must begin with the module name. They may optionally be prepended by the Lark modifiers '?', '_', and '!'
 * One of the rules or tokens in the grammar MUST be '[module name]_source'. This is the implicit entry point for the grammar
    * This rule must not have any productions containing '->' (the Lark alias indicator)
    * This rule may begin with '!', but it may not begin with '?' or '_'
 * The Grammar object must not have an explicit start symbol

These rules are required to ensure that the grammars from modules can be merged into the DERP grammar without conflicts.

When a module source is matched in the AST, the node for '[module name]_source' will be the root of the tree passed to the module to obtain a Post Iterator.

### Posts
Posts are a collection of key-value pairs with pre-defined types for the value associated with each key. They should follow the [IPost](../derp/posts/IPost.py) interface and be able to provide their own definition as well as the name of the module that they were generated by. Posts are allowed (but not required) to perform lazy operations and acquire data from the internet only when the data is required for a specific field. If a post is queried for data it does not contain, it should return `None` (The Python `NoneType`).

Posts should expose an `about` function, which is a topical check defined by the module. A simple example of the topical check is `topic in [post title] or topic in [post body]`

Posts should also implement the Python builtin `__str__` function. This is used to convert the entire post to text which can be displayed to the user.

### Post Iterators
Post Iterators must follow the Python iterator specification, and each element returned should follow the `IPost` interface mentioned above.

# Dropped and Re-specified Features
## Saving Results
Saving results is no longer supported. It was intended that results could be saved for later.

## Module Field Grammars
Modules are no longer allowed to define grammar for the fields its posts expose; they may only define grammar for sources.

## Criteria Builder Mode
The Critera Builder Mode section states that, 'While selections
must reference a loaded news source, criteria do not have the same constraint.' Rather than not having the constraint, Criteria actually have a different constraint - They
CANNOT include a specific news source.

## Knowledge Modules
This feature was dropped entirely. Additional information about the intended feature is available in the [White Paper](./White%20Paper.pdf).

## Persistance of Selections and Criteria
Criteria and Selections were previously composed by value, however this behavior has been inverted. DERP is now defined such that composed selections and criteria ARE references, rather than copied data. This behaves similar to standard C macro expansions. It is implementation-defined whether or not saved selections and criteria are persistent across interpreter sessions.

## 'like'
The 'like' qualification has been removed from the language. Additional information about the intended feature is available in the [White Paper](./White%20Paper.pdf).

## 'Are' and 'Are Not'
The phrases 'are' and 'are not' have been removed. Only 'which are' and 'which are not' are included in the language. While
this was intended to make it easier to express joined qualifiers, requiring the 'which' made it easier to separate
qualifiers.

## 'Over', 'Under', 'Exactly', and 'Roughly'
The phrases 'over', 'under', 'exactly', and 'roughly' have been removed. Only 'with over', 'with under', 'with exactly', and 'with roughly' are supported
as key phrases. Additionally, any one of them can be used with the word 'without' in place of 'with' to negate the effect.
While this was intended to make it easier to express joined qualifiers, requiring the 'with' made it easier to separate
qualifiers.

## Removing Posts by Source
Removing posts from sources is a removed feature. It was initially intended to
allow removing posts labeled as coming from a specific source, however this
was removed due to time constraints.

# Development Environment and Run-Time System

DERP depends on python 3.5 and above, but is not otherwise limited
as to the platforms it can be run on. The interpreter serves as the development
environment for the language, and the default implementation provides text
output to the terminal. The following packages are required to run the interpreter:

  - lark-parser 0.6.5
  - newspaper3k 0.2.8
  - praw 6.0.0
  - pytest 4.0.1

all of which can be obtained with the command `pip3 install -r ./requirements.txt`, where `requirements.txt` is the file provided in the repository root.

Additional requirements can be added to the requirements.txt file
by creating a new virtual-environment, installing the requirements, and then using the command `pip3 freeze > ./requirements.txt`.

# Continuous Integration

The initial continuous integration solution for the repository consisted of a GitLab runner hosted on a Windows Server 2019 Datacenter VM on Azure. The runner communicated with the GitLab server by means of the school's VPN. This solution lasted for roughly a
month before the subscription's free credit ran out and another solution became necessary.

At this point the runner was moved to a Digital Ocean Ubuntu 18.04 droplet which was similarly configured to run through
the school's VPN. This solution was in place until the repository migrated to GitHub, at which point using the runner
would have required workarounds to mirror the repository on GitLab that were not ideal.

After deciding that the GitLab runner was no longer the ideal solution, Travis CI was introduced as a replacement. This
is the currently used solution on the GitHub repository. The Travis CI server status can be viewed [here](https://travis-ci.org/CSC792-SDSMT-DERP/DERP)

# Testing Plan and Scripts

The plan for testing and verification of this project is a three-pronged approach:

  1. Follow good coding practices, and utilize the EAFP principle
  2. Use assertions to guarantee the code is not in invalid states
  3. Provide test harnesses to verify things other than individual implementation details (Interface behaviors, monkey tests, etc.)

This approach was chosen mainly due to the arguments presented in [this article](http://pythontesting.net/strategy/why-most-unit-testing-is-waste/). The most important argument being that the project had a rapid development timeline and that interfaces would be changing rapidly. If the project were unit tested at a low level or following full TDD, this would have resulted to a large, difficult to change, mass of tests hindering development of the actual project.

## Coding Practices, EAFP, and Assertions

 The specific practices that emphasize was put on are as follows:
 * Use accurate and descriptive names for functions and variables
 * Keep function definitions (and preferably also class definitions) short. If the definition of a function is too long, split it into multiple functions.
 * Use assertions liberally. The goal being that if execution reaches any unexpected, invalid state, it should crash, not continue as if nothing were wrong.

These practices were chosen specifically to foster code readability, so that when exceptions are thrown by the interpreter, they occur in reasonable locations (because of assertions), and it is easy to read the
code to verify what is or should be happening.

The EAFP approach (Easier to Ask Forgiveness than Permission) reinforces these behaviors by requiring that developers be mindful of what operations may throw exceptions, and by preventing the project from functioning in the case that exceptions are not properly minded.

## Test Scripts

All this is not to say there are no automated tests in the project, just that they do not (for the most part) get down to the level of individual function testing. There are essentially three types of tests defined in the DERP project:
 * Class tests
 * Interface tests
 * System tests and Monkey tests

Interface tests are defined for the major interfaces in the interpreter which are used to inject dependencies into other objects. A prime example of this is the [IModule](../derp/modules/IModule.py) interface, which is used by language modules and has a set of tests which can be used to check that a module conforms to the API.

There few class-level tests, used to verify that individual class functions exhibit the desired behaviors. These are used mainly to test security features, such as in the [FileManager](../derp/session/session_state/FileManager.py) implementation.

Finally, the majority of the tests in the project are system integration or monkey tests. These tests instantiate a DERP Session, which is the entry point to the DERP library, and execute language statements against it.
Using the powerful Pytest library, the system integration tests verify that, aside from arbitrary capitalization, almost every single variation of DERP statements is properly handled, by the DERP library.

There are three sets of monkey tests which, by default, run 1000 cases each. These tests generate random sequences of text and pass them to the DERP Session, in an attempt to crash it or cause it to hang. The first group of tests passes purely random strings, the second passes random sequences of DERP keywords, and the third passes random sequences of DERP statements (full lines of DERP code).

## Usage of Testing Scripts

It is the responsibility of the developers to ensure the code they add to the project works correctly, whether it be through test scripts or manual testing. The system integration and interface tests are provided as an avenue towards this goal, but there is no strict requirement that they be passing at all times. This decision was made due to the small size of the development team and the rapid pace of development.

Once continuous integration was working correctly, tests were run through that on every pushed commit to the repository, so developers could have constant visibility as to the state of the project.

Tests are built using the Pytest library, and can be executed by running `python3 -m pytest` from the root of the project. This command will find and execute all tests in the project. Tests are defined in files named beginning with `test_` or ending with `_test.py`. These files are in `tests` subfolders throughout the project.

Since there are a plethora of tests defined, Pytest marks are utilized so that developers can easily run subsets of the tests.

 * `slow` - This mark indicates that the test takes a long time to run and developers may not want to wait for it during rapid iteration
 * `monkey` - This mark indicates that the test is a monkey test
 * `plugins` - This mark indicates that the test is used to verify plugins function correctly.

For example, a developer who is doing rapid iteration may want to run tests with `python3 -m pytest -m "not slow"` to exclude long-running tests. For more information about Pytest, see the [Pytest reference pages](https://docs.pytest.org/en/latest/index.html).

Furthermore, the marks `sequential` and `parallel` are defined for tests that must be run sequentially and tests that can be run in parallel, respectively. If developers have a Pytest plugin to run tests in parallel, such as `pytest-xdist`, they can use the `parallel` mark to only execute tests that are safe to run in parallel. (i.e. `python3 -m pytest -m parallel -n 10`)

### Pytest Fixtures
A number of the test files end with `_tests.py`. These files are not auto-discovered by Pytest, and if they were, they would not execute. These files contain Interface tests, which require a Pytest fixture to be defined. To run these tests on an implementation of a specific interface, import everything in the `_tests.py` file and define the Pytest fixture to return the implementation needed. See the [Reddit Module Tests](../modules/reddit/tests/test_reddit.py) for an example of using Pytest fixtures in this way.

# Conclusions
The DERP project presented a significant challenge; however, that challenge was conquered. DERP fulfills all of the goals set out when it was first imagined. Unfortunately, some compromises had to be made. The biggest was the use of quotation marks around strings. Unfortunately, the team could not find a clear way to implement bare strings in the context of the DERP grammar. This is the single largest hurdle to deploying DERP on a voice enabled device. Perhaps natural language processing offers a way forward.

The loss of team members meant the team had to move faster than it would have liked. Certain software design quality standards were not upheld as a result. While, today, DERP has a swath of integration, interface, and monkey tests, the verification of code was mostly done by hand during development. Additionally, large sections of code made their way into DERP, only to be reviewed at a much later date. Thankfully, skilled hands, rigid interfaces, and copious assertions provided a path forward in spite of these shortcomings.

The core development happened over the course of roughly two weeks. Due to the scope of the project, an immense amount of time was spent on the required documentation. Perhaps the team could have been a bit briefer when writing the documentation, saving time for more critical processes. Perhaps the team should have scoped less work from the start. Nonetheless, the project was finished within the provided time constraints.

Future developers may extend DERP using the built in module system. DERP may be readily adapted to fetch data from RSS feeds, news sites, forums, and much more. A future extension that would expand this horizon even further would be an extension of the "posts" keyword. One could imagine that DERP modules could define what type of data they return ("posts", "files", "people", etc.). Then modules that return the same type of data could be freely mixed with one and another. This would allow DERP to fetch data from nearly any source.

All in all, designing, building, and testing the DERP project provided a valuable software engineering experience.
