# Original DERP Whitepaper: Errata

## Section 2.2
Section 2.2 states that DERP would be very easy to adapt to a speech-to-text and text-to-speech interface for a voice platform. In the end, there are a number of
significant hurdles that would have to be overcome to do this. The first issue is that DERP does not support bare words as identifiers, that is, identifiers must be quoted.
Building a speech-to-text platform that would properly quote identifiers is a difficult task, and left as an open problem for anyone trying to build such a platform. An alternate solution
would be to modify the DERP language definition to allow for bare words as identifiers. The second main issue arising with a voice implementation would be that of error output. Consistently 
presenting syntax issues to the user through a speech interface is no easy task, and also left as an open problem.

## Section 2.3
Section 2.3 could give readers the impression that queries implicitly use all loaded sources. That is not the case; rather, each query specifies
one or more individual sources that should be used.

## Section 3.1.1
Section 3.1.1 states that 'the interpreter will retrieve only enough information to identify an article’s
defining information for the user.' The final implementation of this ended up being dependent upon language plugins. It is possible for a language plugins
to provide posts which lazily acquire information from sites; however, that is not a strict requirement (or guarantee) of DERP.

## Section 3.1.2: Criteria Builder Mode
The Critera Builder Mode section states that, 'While selections
must reference a loaded news source, criteria do not have the same constraint.' Rather than not having the constraint, Criteria actually have a different constraint - They 
CANNOT include a specific news source.

## Section 3.1.3: News Source Modules
The Reddit module does not define the keyword 'posts.' It does define the parse rules 'reddit' and 'subreddit "[subreddit name]"' as ways
to specify news sources.

## Section 3.1.3: Knowledge Modules
This feature was dropped entirely

## Section 4
Section 4 introduces the term 'DERP-QL' for the DERP Query Language. This term is not actually used outside the whitepaper document. In its place, the nomenclature of
DERP Query Language or DERP Language is used.

## Section 4.4
This section ended up being flipped entirely on its head. DERP is now defined such that composed selections and criteria ARE references, rather than
copied data. This behaves similar to standard C macro expansions. Additionally, it states that memory management is automatic and handled by Python. It is not 
a requirement that DERP interpreters be implemented in Python; however, they should automatically handle memory. It is implementation-defined whether or not
saved selections and criteria are persistent across interpreter sessions.

## Section 4.5.1
The 'like' qualification has been removed from the language.

## Section 4.5.3
The phrases 'are' and 'are not' have been removed. Only 'which are' and 'which are not' are included in the language.

## Section 4.5.4
The phrases 'over', 'under', 'exactly', and 'roughly' have been removed. Only 'with over', 'with under', 'with exactly', and 'with roughly' are supported
as key phrases. Additionally, any one of them can be used with the word 'without' in place of 'with' to negate the effect.
