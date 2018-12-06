# Original DERP Language Reference: Errata
A number of the original grammar rules have been since modified, removed, or split into multiple rules. Unless necessary for clarity, this 
document will not list the previous version of the grammar. It will prefer to list just the section number for the grammar which changed and then
the new version of the grammar. A full definition of the current grammar, which is used in the parser implementation, can be found in the [grammar definition](../derp/language/GrammarDefinitions.py) file.
Note that the actual set of rules defined in the parser is not required to match the rules defined in the reference manual exactly; it is just required to be
functionally equivalent.

## Section 2
Modules are no longer allowed to define grammar for the fields its posts expose; they may only define grammar for sources.

## Section 3.1
It should be noted that while the language will ignore whitespace in most contexts, it may be required in some cases to prevent ambiguity when
parsing. This is implementation-defined and dependent upon the parser implementation.

## Section 3.3
<i>`digit`</i> is removed. <i>`number`</i> becomes

<pre>
<i>number</i><b>: -?[0-9]+</b>
</pre>

## Section 4.1
Saving results is no longer supported

## Section 5
Posts are no longer required to have a text body; however, it is anticipated that in most implementations, the body text of the post will
be included as a field of the Post.

## Section 5.2
Modules are not allowed to directly define new grammar for <i>`field`</i>, rather modules may define specific named fields that their posts expose, and those
names should be added to the grammar by the interpreter.

## Section 5.4
Additionally, selections must begin with an `add` statement.

## Section 6.1.1
<pre>
<i>load_expression</i> <b>:</b> load <i>string</i>
</pre>

Module names are matched case-insensitively, and must be unique. Therefore, loading modules named "Reddit" and "ReDdIt" at the same time cannot
be done.

## Section 6.1.3
<i>`save_expresssion`</i>, rather than <i>`create_expression`</i> is used to save criteria and selections.

## Section 6.1.4
The DERP language does not specify exactly what method is used to retrieve and display posts to the user. Interpreter writers may define this 
process as only returning the first 10 items, or something similar; however, the original intent of the read statement is that it should trigger 
continuous posts until no more can be found or the user requests to stop the query.

## Section 6.2.4
<pre>
<i>date</i> <b>:</b> <b>(</b><i>month day</i><b>?</b>,<b>?)?</b><i>year</i>
<i>year</i> <b>:</b> <i>number</i>
 <i>day</i> <b>:</b> <i>number</i>
</pre>

It is now a semantic error to enter an invalid date, rather than a parse error. Additionally, it is a semantic error
to do an exact date check without specifying day, month, and year.

## Section 6.2.8
<i>above_expression</i> and <i>below_expression</i> should be named <i>above_expr</i> and <i>below_expr</i> respectively
to keep with internal naming conventions.

## Section 6.2.10
<i>qualifier</i> <b>:</b> not<b>?</b> matching <i>string</i>

Criteria may not be matched such that they create a circular dependency.

## Section 6.3
In Selection mode, <i>`selector`</i> has been split. Sources may also be previously-defined selections,
and remove expressions may no longer remove posts based on their source origin. The first rule of <i>remove_expression</i>
still stands though - <i>remove_expression</i> is not valid until at least one <i>add_expression</i> is part of the selection.

<pre>
   <i>add_expression</i> <b>:</b> add posts <i>add_selector</i>
<i>remove_expression</i> <b>:</b> add posts <i>remove_selector</i>

   <i>add_selector</i> <b>:</b> from <i>source</i> qualifier_or?
<i>remove_selector</i> <b>:</b> qualifier_or

<i>source</i> <b>:</b> <i>source</i> <b>(</b>and<b>|</b>or<b>)</b> <i>source</i>
       <b>|</b> <i>string</i>
</pre>

Sources may not be specified such that they create a circular dependency.
