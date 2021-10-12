import dateparser_en_gb as dp
for line in open( 'tdates.txt' , 'r' , encoding='UTF-8' ).readlines():
    (expected,text) = line.split('|' ) 
    expected = None if expected == 'None' else expected 
    result = dp.find_date( text , dp.all_patterns , echo=True) 
    if result == expected :
        pass
    else :
        print( f'{expected=}    got {result} ' ) 
        print( text )
        print(  '-'* 80 )
