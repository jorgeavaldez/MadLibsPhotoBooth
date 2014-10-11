import string

#Change path to wherever it is locally
namesFile = open(r"D:\Github\Fall2014IDE\Fall2014IDE\Fall2014IDE\NameStripper\talknames.txt", "r", errors="ignore")

for line in namesFile:
    formattedLine = ""
    cleanLine = True

    for char in line:
        if char not in string.printable:
            cleanLine = False
            break

        elif char is ':':
            formattedLine = ""
        
        else:
            formattedLine += char    
            
    if cleanLine and formattedLine != "":
        print(formattedLine)

    formattedLine = ""
