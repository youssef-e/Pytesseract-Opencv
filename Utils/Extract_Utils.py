



def fields_extract(extracted_lines):
    fname="-1"
    birthday = "-1"
    name = "-1"
    nationality = "-1"
    gender = "-1"
    id_nbr = "-1"
    mrz1 = "-1"
    mrz2 = "-1"
    for i, extracted_line in enumerate(extracted_lines):
        line = extracted_line
        if ((" Nom" in line ) or (" Mom" in line) or (" nom" in line) or (" Non " in line) or (" non" in line)):
            name=clean_name(line) if not is_found(name) else name
      
        elif (("Pren" in line) or ("preno" in line) or ("Prenom" in line) or ("Pre" in line)):
            fname = first_name_extract(line) if not is_found(fname) else fname
            name=clean_name(extracted_lines[i-1]) if not is_found(name) else name
            try:
                line=extracted_lines[i+1]
            except IndexError:
                birthday ="-1"
                gender = "-1"
            else:
                birthday = birthday_extract(line) if not is_found(birthday) else birthday
                gender = gender_extract(line) if not is_found(gender) else gender
            
        elif (("ationale" in line.lower()) or ("carte" in line.lower()) or (" identite" in line.lower())):
            id_nbr =id_extract(line) if not is_found(name) else name
            try:
                line=extracted_lines[i+1]
            except IndexError:
                name ="-1"
            else:
                name = clean_name(line) if not is_found(name) else name
        elif ("Natio" in line or "alite" in line or " ation" in line or "onatite" in line):
            nationality = nationality_extract(line) if not is_found(nationality) else nationality
        else:
            line=clean_alphanum(line).upper()
            if("<<" in line and ("IDFRA" in line or "IOFRA" in line or "DFRA" in line or "OFRA" in line)):
                mrz1 = mrz1_extract(line) if not is_found(mrz1) else mrz1
                try:
                    line=extracted_lines[i+1]
                except IndexError:
                    mrz2 ="-1"
                    print("mrz2 not found")
                else:
                    mrz2 = mrz2_extract(line) if not is_found(mrz2) else mrz2
    result = {
    "name" : name,
    "fname" : fname,
    "id_nbr" : id_nbr,
    "nationality" : nationality,
    "gender" : gender,
    "birthday" : birthday,
    "mrz1" : mrz1,
    "mrz2" : mrz2
    }

    for i,(k,v) in enumerate(result.items()):
        result[k]="-1" if v == "" else result[k]
    return result


def clean_name(line):
    name ="-1"
    cleanedLine=line
    for c in line:
        if ((c<'a'or c>'z') and (c<'A'or c>'Z') and (c != '-') and(c !=" ") and(c!= ":")):
            cleanedLine=cleanedLine.replace(c,"")
    words = cleanedLine.split(":")[len(cleanedLine.split(":"))-1].split(" ")
    k=1
    while(k<=len(words)-1):
        if(len(words[len(words)-k])>2):
            name=words[len(words)-k]
            break
        k = k + 1
    return name

def is_found(string):
    if("-1" in string):
        return False
    return True


#look for the first name(s) in the extracted lines using key words to locate it/them; it returns a str containing the first names separated with spaces
def first_name_extract(line):
    name="-1"
    if ("Pren" in line or "preno" in line or "Prenom" in line or "Pre" in line):
        name = line.split(":")[len(line.split(":"))-1]
    names= name.split(" ")
    fname= ""
    l = len(names)
    j = 0
    while(j<l):
        word=names[j]
        #cleaning unnecessary words and spaces from the line
        if("Pren" in word or "preno" in word or "Prenom" in word or "Pre" in word):
            names[j]=""
        if(names[j]==""):
            names.pop(j)
            j=j-1
            l=l-1
        else:
            if ("-1" not in names[j]):
                #clean the unnecessary caracters from the extracted name(s)
                for i in range(len(names[j])):
                    if ((names[j][i]<'a'or names[j][i]>'z') and (names[j][i]<'A'or names[j][i]>'Z') and (names[j][i] != '-')):
                        word=word.replace(names[j][i],"")
                if word != "":
                    fname = fname + word + " "
            else:
                fname = "-1"
        j=j+1
    if fname =="":
        fname = "-1"
    if (fname !="-1"):
        if(fname[0]==" "):    
            fname=fname.replace(fname[0],"")
        l=len(fname)
        i=l-1
        while(i<l):
            if((fname[i]<'a' or fname[i]>'z') and (fname[i]<'A' or fname[i]>'Z')):
                fname=fname[:i]
                l=len(fname)
                i=l-1
            else:
                break
    return fname

#look for the id in the extracted lines using key words to locate it; it returns a str
def id_extract(line):
    id_nbr="-1"
    if ("ationale" in line.lower() or "carte" in line.lower() or " identite" in line.lower()):
        id_nbrs = line.split(" ")
        for value in id_nbrs:
            notFound = True
            for c in value:
                if notFound :
                    if(c>='0' and c<='9'):
                        id_nbr=value
                        notFound = False                   
                        break
                    else:
                        break

    return id_nbr

#look for the nationality in the extracted lines using key words to locate it; it returns a str
def nationality_extract(line):
    nationality="-1"
    if ("Natio" in line or "alite" in line or " ation" in line or "onatite" in line):
        nationality = line.split(" ")[len(line.split(" "))-1]
    return nationality

#look for the birthday in the extracted lines using key words to locate it; it returns a str
def birthday_extract(extracted_line):
    result="-1"
    line = extracted_line
    #since the line containing the birthday tend to not be read correctly
    #it first look for the line containing the first name, then try
    #to locate the birthday in the line below it
    line = clean_alphanum(line, " ")
    words = line.split(" ")
    clean_line=[]
    for value in words:
        if value !="":
            clean_line.append(value)
    #it then can extract the date
    try:
        result = clean_line[len(clean_line)-3]+" "+clean_line[len(clean_line)-2]+" "+clean_line[len(clean_line)-1]
    except IndexError:
        result="-1"
    else:
        for c in result:
            if((c <'0' or c>'9') and (c!=" ")):
                result=result.replace(c,"")
        if len(result)!= 10:
            result ="-1"
    #however if the image is too small, they may not be any lines below the firstname, it then sends an error       
    return result

#look for the gender in the extracted lines using key words to locate it; it returns a str
def gender_extract(extracted_line):
    gender = "-1"    
    line = extracted_line
    #since the line containing the gender tend to not be read correctly
    #it first look for the line containing the first name, then try
    #to locate the gender in the line below it
    words = line.replace("."," ").split(" ")
    for word in words:
        if(word == "M" or word =="F"):
            gender = word
            break
    return gender    

def clean_alphanum(line,replacement = ""):
    word = line
    result =""
    for c in line:
        if ((c<'a'or c>'z') and (c<'A'or c>'Z') and (c != '<') and (c <'0' or c >'9')):
            word=word.replace(c,replacement)
    result = result + word
    return result

#look for the mrz in the extracted lines using key words to locate it; it returns a list of str
def mrz1_extract(extracted_line):
    mrz="-1"
    line = extracted_line.upper()
    if("<<" in line and ("IDFRA" in line or "IOFRA" in line or "DFRA" in line or "OFRA" in line)):
        mrz=line
    result=""
    if ("-1" not in mrz):
        #clean the unnecessary caracters from the extracted str
        result = clean_alphanum(mrz)
    else:
        result = "-1"
    return result

def mrz2_extract(extracted_line):
    line = extracted_line.upper()
    word = clean_alphanum(line)
    result = ""
    if ("-1" not in word):
        #clean the unnecessary caracters from the extracted str
        result = clean_alphanum(word)
    else:
        result = "-1"
    return result

def mean_length(words):
    mean_lengths=[]
    max_occur=0
    mean_length=0
    for word in words:
        if word != "-1":
            mean_lengths.append(len(word))
    for length in mean_lengths:
        if(max_occur<mean_lengths.count(length)):
            max_occur=mean_lengths.count(length)
            mean_length = length
        if(isinstance(mean_length,str)):
            mean_length = 0
    return mean_length 

def mean_length_mrz(words):
    mean_lengths=[]
    max_occur=0
    mean_length=0
    for word in words:
        if word != "-1":
            mean_lengths.append(len(word))
    for length in mean_lengths:
        if(length == 36):
            return  length
        if(max_occur<mean_lengths.count(length)):
            max_occur=mean_lengths.count(length)
            mean_length = length
        if(isinstance(mean_length,str)):
            mean_length = 0
    return mean_length  

def mean_word(words):
    mean_len = mean_length(words)
    final_word = ""
    for i in range(mean_len):
        chars={}        
        for j,word in enumerate(words):
            if len(word) == mean_len:
                if word[i] in chars:
                    if(len(words)>11 and (j == 12 or j == 14)):
                        chars[word[i]] =chars[word[i]] + 4
                    elif(len(words)>11 and j == 11 ):
                        chars[word[i]] =chars[word[i]] + 2
                    elif(len(words)>10 and j<=9):
                        chars[word[i]] =chars[word[i]] + 0.10
                    else:
                        chars[word[i]] =chars[word[i]] + 0.5
                else:
                    if(len(words)>11 and (j==12 or j == 14)):
                        chars[word[i]] = 4
                    elif(len(words)>11 and j == 11 ):
                        chars[word[i]] = 2
                    elif(len(words)>10 and j <=9 ):
                        chars[word[i]] = 0.10
                    else:
                        chars[word[i]] = 0.5
        max_val=-1
        key=""
        for c in chars:
            if chars[c]>=max_val:
                max_val=chars[c]
                key = c
        final_word = final_word + key 
    return final_word

def mean_mrz(words):
    mean_len = mean_length_mrz(words)
    final_word = ""
    for i in range(mean_len):
        chars={}        
        for j, word in enumerate(words):
            if len(word) == mean_len:
                if word[i] in chars:
                    if(len(words)>19 and (j == 18)):
                        chars[word[i]] =chars[word[i]] + 3
                    elif(len(words)>10 and j<=9):
                        chars[word[i]] =chars[word[i]] + 0.10
                    else:
                        chars[word[i]] = chars[word[i]] + 0.5
                else:
                    if(len(words)>19 and (j == 18)):
                        chars[word[i]] = 3
                    elif(len(words)>10 and j<=9):
                        chars[word[i]] = 0.10
                    else:
                        chars[word[i]] = 0.5
        print(chars)
        max_val=-1
        key=""
        for c in chars:
            if c == "<" or c=="(" or c == "[" or c == "{":
                key = "<"
                break
            elif ((c == "S" or c == "C") and ( i-1 >= 0 and len(final_word) !=0) and (final_word[i-1] == "<")):
                key = "<"
                break
            elif chars[c]>=max_val:
                max_val=chars[c]
                key = c
        final_word = final_word + key
    return final_word
