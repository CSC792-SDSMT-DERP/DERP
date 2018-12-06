# Original DERP Language Tutorial: Errata

## Section 1.1
DERP requires at least python 3.5 or higher to run. The tutorial notes that 
DERP is available on all systems that have python3 installed. This is not
entirely true as DERP will fail to run with a python version lower than 3.5.

## Section 3.2
Removing posts from sources is a removed feature. It was initially intended to
allow removing posts labeled as coming from a specific source, however this
was removed due to time constraints.

## Section 4.5
Verified is not an avaliable field to query against in the Reddit module. While
verified posts are a Reddit concept, they are not available as a queryable field
on the post returned by the API.