## Instructions

### File Names
Templates are .txt files which can hold any name.  We recommend using the format of: `STATECODE_TYPECODE_TABLECODE.txt`

e.g. AL_cafr_statewidenetassets.txt


### File Contents
Templates contain instructions for converting a section of specific categories of PDF file into structured data.

A template is defined in terms of:

1. type_code - this string is appended to the output file.
2. format - this string exists for potential extensibility, since the system may eventually allow for alternative target taxonomies or export structures.
3. file_pattern - a regular expression applied to filenames to determine which files the template should be applied to.
4. anchor - a regular expression used to identify where in the file the template should be applied.
5. template - this list of line mappings contains one item per line break in the template.  An empty object indicates that the line should be skipped.  Otherwise, the line is processed according to the mapping instructions (see below for details on mapping instruction format).  Note, this system makes the assumption that each line will contain a single value to be mapped.

```
{
	"type_code": "",
	"format": "",
	"file_pattern": "",
	"anchor": "",
	"template": []
}
```

### Line Mappings

A line mapping is an object which describes how to route a specific line.  The structure of a line mapping will depend on the selected export format.

#### Export Format: xbrl:gaap-gbrl

Line mappings intended for the xbrl:gaap-gbrl format can contain the following fields:

- xbrl_concept (required) - a string representing the type of item being categoried, mapped to a valid xbrl concept in our government-centric extended version of gaap.
- xbrl_dimensions - a dictionary where keys are dimensions and values are the appropriate dimension value.