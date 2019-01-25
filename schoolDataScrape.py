import requests
import time
from bs4 import BeautifulSoup
from csv import writer,reader

def removeJunkFromString( string ):
    
    #find first non empty or new line char
    first_char = 0
    for c in string:
        if c != " " and c != "\n":
            break
        else:
            first_char = first_char + 1

    #build new string with | in single spaces
    new_string = ""
    for x in range(first_char, len(string)):
        if string[x] == " ":
            if string[x + 1] != " ":
                new_string += '|'
            else:
                break
        elif string[x] == "\n":
            break
        else:
            new_string += string[x] 

    #remove all spaces and new line characters and then replace | with a space
    new_string = new_string.replace(" ", "")
    new_string = new_string.replace("\n", "")
    new_string = new_string.replace("|", " ")
    
    return new_string
#---------Open school_codes.csv and read all entries into an array---------
with open('school_codes.csv', newline='') as csvfile:
    schools = list(reader(csvfile))[0]

#----------Open CSV file and write top row----------
with open('school_details.csv', 'w') as csv_file:
    csv_writer = writer(csv_file)
    headers = ['School','Code','Principal', 'Vice / Deputy / Associate Principals', 'Manager Corporate Services','Phone','Address','Email','Website','Education Region','Local Government Area',\
               'State Electorate','Commonwealth Electorate','Independent Public School','School year from','School year to','Principal Level','Classification Group','Broad Classification',\
               'PPR','Y01','Y02','Y03','Y04','Y05','Y06','Y07','Y08','Y09','Y10','Y11','Y12','PrimaryTotal','SecondaryTotal','Total']
    csv_writer.writerow(headers)

#----------For each school code in school_codes.csv----------
for x in range(0,len(schools)):
    print(schools[x])

    #--------Administration Page--------------------------------------------------------------------------------------------------------------------
    time.sleep(4)
    url = 'https://www.det.wa.edu.au/schoolsonline/generaladmin.do?schoolID=' + schools[x] + '&pageID=GI01'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    School = removeJunkFromString(soup.find(class_='schoolNameHeading').contents[0])
    emptyNameCheck = '(' + schools[x] + ')'

    if School == emptyNameCheck: #If The School Name is Empty (ie just the code) there will be no Data and this school can be skipped
        continue

    #----------Reset Variables----------
    Code,Principal,VDA,MCS,EducationRegion,LGA,StateElectorate,CommonwealthElectorate,IPS,SchoolYearFrom,SchoolYearTo,PrincipalLevel,\
    ClassificationGroup,BroadClassification,Phone,Address,Email,Website,PPR,Y01,Y02,Y03,Y04,Y05,Y06,Y07,Y08,Y09,Y10,Y11,Y12,PrimaryTotal,SecondaryTotal,Total =\
    "","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""

    #----------Begin Table Processing----------
    adminTables = soup.find_all(class_='tableDataText') #Return Array with the 2 tables of interest on Administration Page
    
    #--------Right Table--------
    rightTable = adminTables[1].contents[1] #The Right of the 2 tables (School Details)

    CodeFind = rightTable.find(string="School Code:")
    EducationRegionFind = rightTable.find(string="Education Region:")
    LGAFind = rightTable.find(string="Local Government Area:")
    StateElectorateFind = rightTable.find(string="State Electorate:")
    CommonwealthElectorateFind = rightTable.find(string="Commonwealth Electorate:")
    IPSFind = rightTable.find(string="Independent Public School:")
    SchoolYearFromFind = rightTable.find(string="School year from:")
    SchoolYearToFind = rightTable.find(string="School year to:")
    PrincipalLevelFind = rightTable.find(string="Principal Level:")
    ClassificationGroupFind = rightTable.find(string="Classification Group:")
    BroadClassificationFind = rightTable.find(string="Broad Classification:")

    if CodeFind is not None:
        Code = removeJunkFromString(CodeFind.parent.parent.contents[5].text)
    if EducationRegionFind is not None:
        EducationRegion = removeJunkFromString(EducationRegionFind.parent.parent.contents[5].text)
    if LGAFind is not None:
        LGA = removeJunkFromString(LGAFind.parent.parent.contents[5].text)
    if StateElectorateFind is not None:
        StateElectorate =removeJunkFromString( StateElectorateFind.parent.parent.contents[5].text)
    if CommonwealthElectorateFind is not None:
        CommonwealthElectorate = removeJunkFromString(CommonwealthElectorateFind.parent.parent.contents[5].text)
    if IPSFind is not None:
        IPS = removeJunkFromString(IPSFind.parent.parent.contents[5].text)
    if SchoolYearFromFind is not None:
        SchoolYearFrom = removeJunkFromString(SchoolYearFromFind.parent.parent.contents[5].text)
    if SchoolYearToFind is not None:
        SchoolYearTo = removeJunkFromString(SchoolYearToFind.parent.parent.contents[5].text)
    if PrincipalLevelFind is not None:
        PrincipalLevel = removeJunkFromString(PrincipalLevelFind.parent.parent.contents[5].text)
    if ClassificationGroupFind is not None:
        ClassificationGroup = removeJunkFromString(ClassificationGroupFind.parent.parent.contents[5].text)
    if BroadClassificationFind is not None:
        BroadClassification = removeJunkFromString(BroadClassificationFind.parent.parent.contents[5].text)

    #----------Left Table----------
    #This is tricky and looks strange because of the cases where there is multiple entries (mainly in VDA) seperate by spaces and newline characters.
    #This will concatinate multiple names together with a '/' character in between

    leftTable = adminTables[0].contents #The Left of the 2 tables (School Management)
    LeftTableNoJunk = []

    for v in range(0, len(leftTable)): #add non "<br/>","\n" elements from array to the new array
        if str(leftTable[v]) != "<br/>" and str(leftTable[v]) != "\n":
            LeftTableNoJunk.append(removeJunkFromString(str(leftTable[v])))

    DATAswitch = 0

    for v in range(1, len(LeftTableNoJunk)):
        if LeftTableNoJunk[v] == '<span class="blueText">Vice / Deputy / Associate Principals</span>':
            DATAswitch = 1
        elif LeftTableNoJunk[v] == '<span class="blueText">Manager Corporate Services</span>':
            DATAswitch = 2
        else:
            if DATAswitch == 0:
                if len(Principal) > 0:
                    Principal += "/"
                Principal += LeftTableNoJunk[v]
            elif DATAswitch == 1:
                if len(VDA) > 0:
                    VDA += "/"
                VDA += LeftTableNoJunk[v]
            elif DATAswitch == 2:
                if len(MCS) > 0:
                    MCS += "/"
                MCS += LeftTableNoJunk[v]

    #----------Contact Details Page-----------------------------------------------------------------------------------------------------
    time.sleep(4)
    url = 'https://www.det.wa.edu.au/schoolsonline/contact.do?schoolID=' + schools[x] + '&pageID=CI01'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    contactTable = soup.find(class_='tableDataFixedWidth')

    EmailFind = contactTable.find(string="Email - Official School Email ")
    WebsiteFind = contactTable.find(string="Website ")
    PhoneFind = contactTable.find(string="Phone")
    AddressFind = contactTable.find(string="Physical Address:")

    if EmailFind is not None:
        Email = EmailFind.parent.parent.find("a").contents[0]
    if WebsiteFind is not None:
        Website = WebsiteFind.parent.parent.find("a").contents[0]
    if PhoneFind is not None:
        Phone = PhoneFind.parent.parent.contents[5].text
    if AddressFind is not None:
        AddressSplit = AddressFind.parent.parent.contents[5].contents
        Address = AddressSplit[0] + ' ' + AddressSplit[2] + ' ' + AddressSplit[4]

    #----------Current Student Page---------------------------------------------------------------------------------------------------
    time.sleep(4)
    url = 'https://www.det.wa.edu.au/schoolsonline/student_current.do?schoolID=' + schools[x] + '&pageID=SP01'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    #--------Primary Years Table----------------------------
    PrimaryTable = soup.find(id='studNrsPrim')
    if PrimaryTable is not None:

        PrimaryTableTopRow = PrimaryTable.find_all('tr')[0].contents
        PrimaryTableBottomRow = PrimaryTable.find_all('tr')[1].contents

        PPRFind = PrimaryTable.find(string="PPR")
        Y01Find = PrimaryTable.find(string="Y01")
        Y02Find = PrimaryTable.find(string="Y02")
        Y03Find = PrimaryTable.find(string="Y03")
        Y04Find = PrimaryTable.find(string="Y04")
        Y05Find = PrimaryTable.find(string="Y05")
        Y06Find = PrimaryTable.find(string="Y06")
        PrimaryTotalFind = PrimaryTable.find(string="Total")

        if PPRFind is not None: 
            PPRindex = PrimaryTableTopRow.index(PPRFind.parent)
            PPR = PrimaryTableBottomRow[PPRindex].text
        if Y01Find is not None: 
            Y01index = PrimaryTableTopRow.index(Y01Find.parent)
            Y01 = PrimaryTableBottomRow[Y01index].text
        if Y02Find is not None: 
            Y02index = PrimaryTableTopRow.index(Y02Find.parent)
            Y02 = PrimaryTableBottomRow[Y02index].text
        if Y03Find is not None: 
            Y03index = PrimaryTableTopRow.index(Y03Find.parent)
            Y03 = PrimaryTableBottomRow[Y03index].text
        if Y04Find is not None: 
            Y04index = PrimaryTableTopRow.index(Y04Find.parent)
            Y04 = PrimaryTableBottomRow[Y04index].text
        if Y05Find is not None: 
            Y05index = PrimaryTableTopRow.index(Y05Find.parent)
            Y05 = PrimaryTableBottomRow[Y05index].text
        if Y06Find is not None: 
            Y06index = PrimaryTableTopRow.index(Y06Find.parent)
            Y06 = PrimaryTableBottomRow[Y06index].text
        if PrimaryTotalFind is not None: 
            PrimaryTotalindex = PrimaryTableTopRow.index(PrimaryTotalFind.parent)
            PrimaryTotal = PrimaryTableBottomRow[PrimaryTotalindex].text

    #--------Secondary Years Table----------------------------
    SecondaryTable = soup.find(id='studNrsSec')
    if SecondaryTable is not None:

        SecondaryTableTopRow = SecondaryTable.find_all('tr')[0].contents
        SecondaryTableBottomRow = SecondaryTable.find_all('tr')[1].contents

        Y07Find = SecondaryTable.find(string="Y07")
        Y08Find = SecondaryTable.find(string="Y08")
        Y09Find = SecondaryTable.find(string="Y09")
        Y10Find = SecondaryTable.find(string="T10")
        Y11Find = SecondaryTable.find(string="Y11")
        Y12Find = SecondaryTable.find(string="Y12")
        SecondaryTotalFind = SecondaryTable.find(string="Total")

        if Y07Find is not None: 
            Y07index = SecondaryTableTopRow.index(Y07Find.parent)
            Y07 = SecondaryTableBottomRow[Y07index].text
        if Y08Find is not None: 
            Y08index = SecondaryTableTopRow.index(Y08Find.parent)
            Y08 = SecondaryTableBottomRow[Y08index].text
        if Y09Find is not None: 
            Y09index = SecondaryTableTopRow.index(Y09Find.parent)
            Y09 = SecondaryTableBottomRow[Y09index].text
        if Y10Find is not None: 
            Y10index = SecondaryTableTopRow.index(Y10Find.parent)
            Y10 = SecondaryTableBottomRow[Y10index].text
        if Y11Find is not None: 
            Y11index = SecondaryTableTopRow.index(Y11Find.parent)
            Y11 = SecondaryTableBottomRow[Y11index].text
        if Y12Find is not None: 
            Y12index = SecondaryTableTopRow.index(Y12Find.parent)
            Y12 = SecondaryTableBottomRow[Y12index].text
        if SecondaryTotalFind is not None: 
            SecondaryTotalindex = SecondaryTableTopRow.index(SecondaryTotalFind.parent)
            SecondaryTotal = SecondaryTableBottomRow[SecondaryTotalindex].text
    
    Total = PrimaryTotal + SecondaryTotal

    with open('school_details.csv', 'a') as csv_file:
        csv_writer = writer(csv_file)
        csv_writer.writerow([School ,Code ,Principal, VDA, MCS,Phone,Address,Email,Website,EducationRegion,LGA,StateElectorate,CommonwealthElectorate,IPS,\
        SchoolYearFrom,SchoolYearTo,PrincipalLevel,ClassificationGroup,BroadClassification,PPR,Y01,Y02,Y03,Y04,Y05,Y06,Y07,Y08,Y09,Y10,Y11,Y12,PrimaryTotal,SecondaryTotal,Total])