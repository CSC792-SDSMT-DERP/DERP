# Project Plan

DERP development was active from August 27, 2018 to December TODO:XX, 2018. DERP was developed following the [Iterative Waterfall](https://www.geeksforgeeks.org/software-engineering-iterative-waterfall-model/) model. As such, a large amount of time was spent developing requirements and specifications (August 27, 2018 - November 04, 2018). These requirements and specifications are set forth in the [White Paper](./White%20Paper.pdf) and [Language Reference](./Language%20Reference.pdf). The [Language Tutorial](./Language%20Tutorial.pdf) also set forth expectations for user interaction. The initial design phase lasted from November 04, 2018 to November 08, 2018. However, certain aspects of DERP were found to be infeasible and needed to be re-specified. These changes to the specifications may be found in the errata pages ([White Paper Errata](./White%20Paper%20Errata.md), [Language Reference Errata](./Language%20Reference%20Errata.md), [Language Tutorial Errata](./Language%20Tutorial%20Errata.md)). Coding took place between November 08, 2018 and December 03, 2018. Additional tests were put in place between December 03, 2018 and December TODO:XX, 2018. Additional documentation was then written to promote maintenance.  

## Timeline
  - August 27: Form team of five members
  - August 29:
    - Propose DERP
    - Outline White Paper
  - September 03: Write Test Plan
  - September 09:
    - Begin drafting DERP grammar
    - Set up CI with GitLab and Azure Cloud
  - September 12: Begin writing White Paper
  - September 21: Finish White Paper
  - September 27: Finish rough draft of DERP grammar
  - October 05: Spin up on Python parsing (Lark)
  - October 06:
    - Outline Language Reference
    - Outline Language Tutorial
  - October 15:
    - Begin drafting Language Reference
    - Team size decreased to four members
  - October 18: Begin drafting Language Tutorial
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
  - November 16: Implement basic language processing
  - November 18: Implement language processing completely
  - November 23:
    - Set up CI with Digital Ocean and GitLab
    - Implement basic backend logic and data structures
  - November 25:
    - Implement Reddit module
    - Implement backend logic and data structures completely
    - Begin enforcing semantic checks
  - November 27: Write DERP presentation and demo script
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


Are you doing to do some form of Agile software development? No. Iterative waterfall.

When will you have requirements created? Requirements were created before any coding happened.

Deliverable schedule:
  - September 21: White Paper due
  - October 22: Language Tutorial and Reference due
  - November 28: Presentation and Demo
  - December 05: Soft due date for project
  - December 13: Hard due date for project

Acceptance and certification testing? Solves the problems set forth in the White Paper.

How are you maintaining code and document revisions?
- Drive + GitLab
- Drive + Github (Overleaf) + GitLab
- Drive + GitLab
- Drive + Github

Language Evolution Document [Shortcomings/ Stuff in Errata]
  Was the design such that additional features and capabilities could be added or did you require significant redesign / rethinking?
  Translator / Compiler Architecture [Design doc in prose]
  This architecture should match the implementation evident in the Code Listing
Development Environment and Run-Time System [trivial/ slides]
  Are there OS restrictions?
  Special hardware required?
  Have you created a runtime system or are you leveraging existing libraries?
  Do you need a special editor or IDE to write programs in your language?
  Unique input or display devices?
Test Plan and Scripts [cut & paste from old doc and updated news]
  What sort of testing is done?
  When is it done?
  Who is responsible for doing the testing?
  Is development tied to testing/certification?
  For example, is there a requirement that all tests run before feature branches can be merged into a development branch?
  Are you running with multiple development branches?
  Integration branch?
  What are the requirements in terms of testing, code review, etc. before something goes into the master or release branch?
Conclusions
  What did you learn?
  What would you do differently?
  Did you successfully scope the project in terms of the amount of work that could be reasonably done by the team in the time alloted?
  Is the design such that future work could be integrated?
  Had you more time/resources/team members, what could have been added to the language? [natural english]
