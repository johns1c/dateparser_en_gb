# parses dates from strings using regular expressions.  Unlike some other
# extract routines it will pick out dates from longer text strings
# returning a string in form yyyy-mm-dd or yyyy-mm.
#   
# you can parse for a given format or supply a list to try them one by one 
# it only parses english month names and abbreviations and the list given
# has uk day month ordering.  
#
# the aim is to be simple and operate in a py2exe enviroment 
#  the yyyy pattern used to accept two, three or four digits - now it is only 4 
#
__title__  = 'dateparser_en_gb'
__author__ = 'Chris Johnson'

import re
import datetime    
all_patterns = [
        'dd/mm/yyyy' , 
        'dd-mm-yyyy' , 'yyyy-mm-dd' , 
        'dd Month yyyy',   'dd Month, yyyy',    'dd Month, yyyy'  ,   
        'ddth Month yyyy', 'ddth Month, yyyy' , 'ddth Month,yyyy' , 
        'Month dd yyyy',   'Month dd, yyyy',      'Month dd,yyyy' ,   
        'Month ddth yyyy', 'Month ddth, yyyy' , 'Month ddth,yyyy' , 
        'dd Mon yyyy',   'dd Mon, yyyy',            'dd Mon,yyyy' ,   
        'ddth Mon yyyy', 'ddth Mon, yyyy' ,       'ddth Mon,yyyy' , 
        'Mon dd yyyy',   'Mon dd, yyyy', 'Mon dd,yyyy'  ,   
        'Mon ddth yyyy', 'Mon ddth, yyyy' , 'Mon ddth,yyyy' , 
        'dd MONTH yyyy',   'dd MONTH, yyyy',    'dd MONTH, yyyy'  ,   
        'ddth MONTH yyyy', 'ddth MONTH, yyyy' , 'ddth MONTH,yyyy' , 
        'MONTH dd yyyy',   'MONTH dd, yyyy', 'MONTH dd, yyyy'  ,   
        'MONTH ddth yyyy', 'MONTH ddth, yyyy' , 'MONTH ddth,yyyy' , 
        'dd MON yyyy',   'dd MON, yyyy',    'dd MON, yyyy'  ,   
        'ddth MON yyyy', 'ddth MON, yyyy' , 'ddth MON,yyyy' , 
        'MON dd yyyy',   'MON dd, yyyy', 'MON dd, yyyy'  ,   
        'MON ddth yyyy', 'MON ddth, yyyy' , 'MON ddth,yyyy' , 
         'dd Month', 'ddth Month',  'dth Month' ,
         'dd Mon', 'ddth Mon',  'dth Mon' ,
         'dd MONTH', 'ddth MONTH',  'dth MONTH' ,
         'dd MON', 'ddth MON',  'dth MON' ,
        'Month yyyy' , 'Mon yyyy' , 'Monthyyyy' , 
        'MONTH yyyy' , 'MON yyyy' ,
        'Month ddth' , 'Mon ddth' , 'MONTH ddth' , 'MON ddth' ,
        'Month dd' , 'Mon dd' , 'MONTH dd' , 'MON dd' ,
        'mm/yyyy' ,
        'yyyy-mm' ,
        'Mon' , 'MON' ,
        'Month', 'MONTH' ]

def find_date( source,  stuff , echo=False) :
        """ finds a date with a given format or a list of formats
            the date pattern has 
            dd one or two digit day
            ddth    1st 2nd 3rd.. 
            Month   January February ...
            Mon     Jan Feb Mar ...
            MON     JAN FEB MAR
            MONTH   JANUARY ...
            mm      month number 01..12
            yy      two digit year            
            yyyy    four digit date
            /       slash as separator  
            -       hyphen as separator
            space   white space as separator
            """
        currentDateTime = datetime.datetime.now()   
            
        if isinstance( stuff , list ) :
            for pat in stuff :
                a_date  = find_date( source , pat ) 
                if a_date is not None  :
                    if echo:
                        print( f"pattern used {pat} " ) 
                    return a_date
            return None                     
                             
        def find(  source , stuff ) :
            """ regex search forward through source  
            """
            pattern_test = re.compile( stuff ) 
            match = pattern_test.search ( source )     
            return match

        
        MonthString = 'January|February|March|April|May|June|July' \
        '|August|September|October|November|December'
        
        MonthStrings = MonthString.split('|' ) 
        MonthUppers  = [ M.upper() for M in MonthStrings ] 
        MonStrings   = [ M[:3] for M in MonthStrings ]
        MonUppers   =  [ M.upper() for M in MonStrings ] 
        
        MonString = '|'.join(MonStrings)  
        
        MonBoth      = f'(?P<m>{MonthString}|{MonString})' 
        MonStr       = f'(?P<m>{MonString})' 
        MonBothUpper = f'(?P<m>{MonthString.upper()}|{MonString.upper()})' 
        MonUpper     = f'(?P<m>{MonString.upper()})' 

        dd = r'(?P<d>\d+)' 
        dd_at_start = r'\b' + dd 
        ddth = '(?P<d>1st|2nd|3rd|21st|22nd|23rd|31st|\dth|\d\dth|)'
        mm = '(?P<m>01|02|03|04|05|06|07|08|09|10|11|12|1|2|3|4|5|6|7|8|9)'
        yy = r'(?P<y>\d\d)'
        yyyy = r'(?P<y>\d{4})'
        
        blank = r'\s'
        comma = ','
        escaped_comma = r'\,'    
        
        pattern = '\\b' + stuff
        pattern = pattern.replace( comma , escaped_comma )  
        
        pattern = pattern.replace( 'ddth' , ddth ) 
        pattern = pattern.replace( 'dd' , dd ) 
        
        pattern = pattern.replace( 'mm' , mm ) 
        pattern = pattern.replace( 'Month' , MonBoth ) 
        pattern = pattern.replace( 'Mon'   , MonStr ) 
        pattern = pattern.replace( 'MONTH' , MonBothUpper ) 
        pattern = pattern.replace( 'MON'   , MonUpper ) 

        pattern = pattern.replace( 'yyyy' , yyyy ) 
        pattern = pattern.replace( 'yy' , yy ) 
        
        pattern = pattern.replace( ' ' , blank )
        pattern = pattern.replace( ' ' , blank )
        pattern = pattern.replace( ' ' , blank )
        pattern = pattern.replace( ' ' , blank )
        #print( f"Date Pattern >>>>>>>{pattern}<<<<<<" ) 
        
        match = find(source , pattern ) 
        if  match:
            #print( self.last_match.groups() ) 
            day = 0
            try:
                day = match.group('d') 
                day = day.replace( 'st' , '' )
                day = day.replace( 'nd' , '' )
                day = day.replace( 'rd' , '' )
                day = day.replace( 'th' , '' )
                
                day = int(day) 
            except  IndexError : 
                day = 0 
            except  AttributeError :            
                print( f'Attribute error on day in date {day=} day pattern = {dd} ' ) 
                print( match.groups() ) 
                print( f"Date Regex >>>>>>>{pattern}<<<<<<" ) 
            except ValueError :
                print( f'Attribute error on day in date {day=} day pattern = {dd} ' ) 
                print( match.groups() ) 
                print( f"Date Regex >>>>>>>{pattern}<<<<<<" ) 
                day = 0 
                
            try:
                mon = match.group('m' )
            except  IndexError :
                print( f'Month component not found - Supplied pattern ={stuff}' ) 
                print( match.groups() ) 
                mon = '00' 
                           
            if mon.isnumeric() :
                mon = int(mon)
            elif mon in  MonthStrings :
                mon = MonthStrings.index( mon) +1 
            elif mon in  MonStrings :
                mon = MonStrings.index( mon ) +1 
            elif mon in  MonthUppers :
                mon = MonthUppers.index( mon ) +1 
            elif mon in  MonUppers :
                mon = MonUppers.index( mon ) +1 
            else:
                pass
                
            try:
                year = match.group('y' ) 
            except:
                year = str(currentDateTime.year)
            
            if year.isnumeric() :
                year = int(year)  
                if year  < 50 :
                    year = year + 2000
                    
                           
            if day is not None and (day > 0):
                datestr = '{:04}-{:02}-{:02}'.format( year , mon , day ) 
            else :
                datestr = '{:04}-{:02}'.format( year , mon) 
                
            return datestr   
            
            
        else:
            failed_date_pattern = pattern
            return None 
 
if __name__ == '__main__' :
       import sys
       if len( sys.argv ) > 1 :
           input = sys.argv[1] 
       else :
           input = 'dates.txt'
       for date_text in open( input , 'r' , encoding='UTF-8' , errors='x'  ).readlines():
            print( find_date( date_text , all_patterns, echo=True ),'<====',date_text ,  )
  
