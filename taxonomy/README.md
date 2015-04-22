A Brief Overview of CAFR Taxonomies
===================================

Currently we have a taxonomy only for the "Statement of Activities"
table, for only a few states.  So the cafr-* files in this directory
just define that taxonomy directly.  As we add more tables, we'll
probably break their taxonomy definitions out into separate files
(with names based on the table names), and then cafr-* will just be
high-level master files that include the table-specific files.

However, for now we're not doing that extra level of abstraction.
Here's what's in the files currently:

* `cafr-2015-04-20.xsd`:

  This is the "base taxonomy schema" (in XBRL-speak).

  Note that it is an XBRL best-practice to put dates in the definition
  file name, as a kind of versioning scheme.

  Think of lines 32-38 as representing column headers in a CAFR
  Statement of Activities.  Think of lines 40-91 as the row labels.
  Put them together and now you have an actual table, and the number
  of "facts" is going to be equal to the product of rows * columns.

  "Dimensions" are what allow us to *not* have to list out every one
  of those 9 * 51 == 459 concepts individually; dimensions allow
  expressive compression while still effectively specifying all the
  exact slots we need.

  For example, we *could* have had a concept for

    Business Type Activities, General Revenues, Miscellaneous

  and we *could* have had that as a totally separate concept from 

    Governmental Activities, General Revenues, Miscellaneous

  But, instead we have "Business Type Activities" and "Governmental
  Activities" as "dimensions", and we have "General Revenues,
  Miscellaneous" as a "concept".  IOW, if you look at an individual
  fact, what various pieces of information are the components of that
  fact.  Think of "dimensions" are all the structural components
  leading down the leaf node of "General Revenues, Miscellaneous".
  Or think of dimensions as things you can pivot on.

  Starting on line 40 are elements that reflect types of information
  in the Statement of Activities tables (right now, specifically for
  NY and ID).  <element id="cafr_statementOfActivities"
  name="statementOfActivities" xbrli:periodType="instant"
  type="xbrli:stringItemType" substitutionGroup="xbrli:item"
  abstract="true" nillable="true"/>

  In other words, if you look at the Statement of Activities in a
  particular CAFR, these are the different rows.

  BUT, in an actual CAFR, those rows have hierarchy to them, and that
  hierarchy is not reflected in this base taxonomy schema.  For
  hierarchy, you need a "link base".  IOW, lines 40-91 specific XBRL
  objects (concepts) but nothing more.  They're given names and ids,
  but not labels, nor relationships to each other, nor presentation
  information about what order they should be presented in, nor rules
  about calculations (e.g., do certain tax elements need to be summed
  together to make a total that matches some other row somewhere? etc).

  All of these things are defined in "link bases".  XBRL has a couple
  of different types of link bases, which in this file are defined on
  line 13-15 (search for "linkbase").  The 'xlink:href' attributes
  always refer to another file name that's here; the 'xlink:role'
  attributes determine what type of link base this is.

  So the next three files are... you guessed it... link bases!

* `cafr-label.xml`:

  This is where labels are defined.  It could sure use more documentation.

* `cafr-presentation.xml`:

  This is where the hierarchy is defined.  It could sure use more
  documentation too.

* `cafr-definition.xml`:

  This is about "dimensions".  Think of them as the column headers of
  the Statement of Activities table.  And some more documentation here
  would be nice, wouldn't it?
