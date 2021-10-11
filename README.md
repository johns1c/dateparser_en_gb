# dateparser_en_gb

Extracts dates from strings using regular expressions.  Unlike some other routines it will pick out dates from longer text strings returning a string
in the form yyyy-mm-dd or yyyy-mm.

The aim was to be simple, operate in a Python 3.8 and py2exe enviroment and to provide a return value that can be inserted in to a sqlite database.

It can look for a given format or go through a list of formats trying them one by one.  The package includes a list of formats that covers most english dates.  

## Limitations

Dates only and no times or time zone handling.

It only handles english month names and three character abbreviations and the list given has UK day month ordering (although it could be easily changed to support US month day).

Potential for result not to be a real date.

## Installation

pip install dateparser_en_gb

## Usage 

import dateparser_en_gb
format = 'dd mon yyyy' 
a_date =  ( long_text , format )
a_date =  ( long_text , format_list )

Format elements - see code for definitive list and meaning.  Also formats may include regex 

* dd - a one or two digit day of month
* ddth - 1st, 2nd etc
* mm - a one or two digit month of year
* yyyy - a four digit year
* month - one of January, February, March etc
* mon - one of Jan, Feb, Mar ...


## Future Enhancements

The aim was to keep it simple and I  but possible enhancements are

* make it a class
* check that we return valid dates e.g. Not 2021-02-30 or  2021-30-05.
* return the position of the found date within the input string to allow for incremental parsing.
* provide more control of defaults such a preferring a result before or after a given reference date.
* allow missing components to be explicitly returned - perhaps using the ISO rules
* return a datetime object rather than a string.

all of these will complicate the routine and there are already packages like scrapinghub's dateparser which provide a lot of facilities but have a few issues as a result.





