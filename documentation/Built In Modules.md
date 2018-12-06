# Built-In Modules
At present there are two built-in modules that are registered on startup, the MockModule used for
testing and the Reddit module which is the primary module for the language.

## Reddit Module
The Reddit module permits querying for posts from reddit and filtering them based on the criteria specified.

### Name
The Reddit module is identified by the name "reddit" and may be loaded with the expression
`load "reddit"`.

### Post Definition
The following field names and types are defined for posts returned by the Reddit module
  - "nsfw": FieldType.BOOLEAN,
  - "author": FieldType.STRING,
  - "title": FieldType.STRING,
  - "upvotes": FieldType.NUMBER,
  - "date": FieldType.DATE,
  - "body": FieldType.STRING

### Pre-Filtering
As the Reddit API provides limited searching capabilities, some results can be pre-filtered before
leaving the server. In cases where this is possible the Reddit search API is invoked with the
appropriate values extracted from the qualifier tree, otherwise the posts are returned as-is from
the Reddit API's 'hot' endpoint while specifying the appropriate subreddit if applicable.

## Mock Module
The Mock module contains a list of generated MockPost objects that are queried against.

### Name
The Mock module is identified by the name "MockModule" and may be loaded with the expression
`load "mockmodule"`.

### Post Definition
The following field names and types are defined for posts returned by the Reddit module
  - "title": FieldType.STRING,
  - "points": FieldType.NUMBER,
  - "verified": FieldType.BOOLEAN,
  - "post date": FieldType.DATE

### Pre-Filtering
The Mock module doesn't perform any pre-filtering on the posts before returning an iterator.
