## Instructions

### File Names
Templates are text files which can hold any name.  We recommend using the format of: `STATECODE_TYPECODE_TABLECODE.txt`

e.g. AL_cafr_statewidenetassets.txt


### File Contents
Templates contain instructions for converting a section of specific categories of PDF file into structured data.

A template is defined in terms of:

1. type_code - this string is appended to the output file.
2. format - this string exists for potential extensibility, since the system may eventually allow for alternative target taxonomies or export structures.
3. file_pattern - a regular expression applied to filenames to determine which files the template should be applied to.
4. anchor - a base 64 encoded version of the literal string to indicate where in the file the template is applied to.
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

- concept (required) - a string representing the type of item being categoried, mapped to a valid xbrl concept in our government-centric extended version of gaap.
- dimensions - a dictionary where keys are dimensions and values are the appropriate dimension value.

{ "concept": "cashAndEquivalents", dimensions": { "category": Governmental Activities", "section": "Asset" }}

## Examples
### Example 1: Alabama CAFR Statewide Net Assets
{
	"type_code": "statewide-net-assets",

	"file_pattern": "/AL\_cafr\_[\d+]/",
	"anchor": "ASSETS
   Cash and Cash Equivalents
   Investments
   Internal Balances
   Due from Primary Government
   Due from Component Units
   Investment Sales Receivable
   Accounts Receivable
   Due from Other Governments
   Taxes Receivable
   Interest and Dividends Receivable
   Mortgages, Notes, and Loans Receivable
   Securities Lending Collateral
   Inventory
   Restricted Assets
   Other Assets
   Capital Assets, Net of Accumulated Depreciation
   Capital Assets Not Depreciated
   Deferred Outflows
      TOTAL ASSETS
     
LIABILITIES
   Warrants Payable
   Investment Purchases Payable
   Salaries Payable
   Due to Primary Government
   Due to Component Units
   Accounts Payable
   Interest Payable
   Tax Refunds Payable
   Due to Other Governments
   Securities Lending Obligation
   Unearned Revenue
   Amounts Held in Custody for Others
   Noncurrent Liabilities:
      Due Within One Year
      Due In More Than One Year
      TOTAL LIABILITIES
     
NET ASSETS
   Invested in Capital Assets, Net of Related Debt
   Restricted for:
      Permanent - Expendable
      Permanent - Non-expendable
      Forever Wild Stewardship Account
      Alabama Trust Capital
      Local Government
      Education
      Natural Resources and Recreation
      Social Services
      Protection of Persons and Property
      Transportation
      General Government
      Debt Service
      Capital Projects
      Other Purposes
   Unrestricted
      TOTAL NET ASSETS
     

Governmental

Activities

Business-type

Activities

$          ",
	"template": []
}