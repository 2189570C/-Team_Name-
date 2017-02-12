#test = 'P<GBRSCHNUR<<DANIEL<MARC<<<<<<<<<<<<<<<<<<<<' + '3046530706GBR7710104M1509223<<<<<<<<<<<<<<04'

def parsePassport(code):
    line1 = code[5:44].split('<<')
    line2 = code[44:]
    
    # names
    surname = line1[0].lower().capitalize()
    forename  = line1[1].split('<')[0].lower().capitalize()
    passportNo = line2[:9]

    # date of birth
    DoB = line2[13:19]
    DoB = DoB[4:] + '/' + DoB[2:4] + '/' + DoB[:2]

    exp = line2[21:27]
    exp = exp[4:] + '/' + exp[2:4] + '/' + exp[:2]

    # gender
    gender = line2[20:21]

    return forename, surname, passportNo, DoB, gender, exp
    #return forename, surname, passportNo, DoB, gender
