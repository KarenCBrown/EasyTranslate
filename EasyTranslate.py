import re


numsOnly = re.compile("^\d[.\\\/,]?\d*$")
numsTest = re.compile("[.\s]*([.\/\d]+)(?:\s|\Z)")
tvarNum = 0

def identify_numbers(line):
    alphaOnly = line.isalpha()

    if alphaOnly:
        return (line)
    elif numsOnly.match(line):
        out = "{{formatnum:" + line + "}}"
        return(out)
    else:
        match = numsTest.findall(line)
        if match:
            out = "{{formatnum:"+match[0]+"}}"
            out2 = line.replace(match[0],out)
            return out2
        else:
            return (line)

def identify_links(line):
    global tvarNum                                  #enable local manipulation of global variable
    hasWikilinks = re.compile("[\b\s]*\[\[.+\]\]")  #find double brackets
    haslinks = hasWikilinks.findall(line)           #search for all instances where a string has double brackets on each end
    if haslinks:                                    #if we found something...
        print(haslinks[0])
        openbrackets = haslinks[0].rfind("[")       #search for the rightmost instance of "[" (i.e. second one)
        tvarname = "[[<tvar|"+str(tvarNum)+">"      #construct tvar label
        replaceme = haslinks[0].replace("[[", tvarname) #replace "[[" with version with tvar label
        print(replaceme)
        tvarNum =  tvarNum + 1                      #increment tvar so the next use has a distinct name
        closebrackets = haslinks[0].rfind("]")      #search for rightmost close bracket
        replaceyou = replaceme.replace("]]", "</>]]")   #take previously-replaced string and replace other end of brackets
        print(replaceyou)


def tag_line(line):
    nums = identify_numbers(line)
    out = "<translate>"+nums+"</translate>"
    return out

with open('myFileName.txt', 'r') as workingFile:
    for line in workingFile:
        cleaner = line.rstrip().lstrip()
        result = tag_line(cleaner)
        identify_links(cleaner)
        #print(result)