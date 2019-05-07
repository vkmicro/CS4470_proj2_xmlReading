# Author: Vasiliy Ulin
# Semester: Fall 2019
# Course: CS 4470 Health Data Analytics
# Project 2

'''
from xml.dom import minidom
doc = minidom.parse("220-01.xml")

for TEXT in doc.getElementsByTagName("TEXT"):
    print (TEXT.toxml())
'''

import os
from xml.etree import ElementTree as ET
from xml.dom import minidom
import xmltodict
import pickle
from numpy import loadtxt


# global vars and arrays
file_content = []
all_files_content = []
file_contents_tree_text = []
file_contents_tree_tags = []
xml_files_list = []
medication_types = [] # contains ACTUAL types of medications
doc_file_contents = []

#Very important array
arr_of_contents = []

def main():
    # to change path of files, simply replace the string after r with desired folder dir
        # i.e. r"yourPathHere"
        # then append it to the dir_par_arr so the forloop can run through all the new directories
    dir_path_arr = []
    directory_path = r"C:\Users\vkmicro\Dropbox\University Sem 7\Health Data analytics\Proj 2\!i2b2 CORRECTED data\i2b2TrainingData-ForStudents\training-RiskFactors-Gold-Set1"
    directory_path2 = r"C:\Users\vkmicro\Dropbox\University Sem 7\Health Data analytics\Proj 2\!i2b2 CORRECTED data\i2b2TrainingData-ForStudents\training-RiskFactors-Gold-Set2"
    dir_path_arr.append(directory_path)
    dir_path_arr.append(directory_path2)
    directory_path3 = r"C:\Users\vkmicro\Dropbox\University Sem 7\Health Data analytics\Proj 2\!i2b2 CORRECTED data\i2b2TrainingData-ForStudents\i2b2-rf-110-03-abbrev-marked.txt"
    #directory_path3 = r"C:\Users\vkmicro\Dropbox\University Sem 7\Health Data analytics\Proj 2\!i2b2 CORRECTED data\i2b2TrainingData-ForStudents\_i2b2-rf-110-03-abbrev-marked - Copy.txt"

    for dir in dir_path_arr: # this for loop runs through all the directories paths
        for filename in os.listdir(dir):
            if not filename.endswith('.xml'):
                continue
            elif filename.startswith('._'):  # skip the weird fking files which contain nothing that seem to be
                # macOS leftovers or something....
                continue
            file = os.path.join(dir, filename)  # each individual file in the folder and it's directory path
            # print(file)
            xml_files_list.append(file)

            with open(file) as fd:
                doc_contents = xmltodict.parse(fd.read())
                doc_file_contents.append(doc_contents)

    # call function create list of meds
    createListOfMeds(file_contents_tree_text, file_contents_tree_tags, xml_files_list, doc_file_contents)
    createMedicationTypeDict(doc_file_contents)

    #the abbrev file thing
    abbrev_file_cont = []
    abbrev_things = []
    with open (r"C:\Users\vkmicro\Dropbox\University Sem 7\Health Data analytics\Proj 2\!i2b2 CORRECTED data\i2b2TrainingData-ForStudents\i2b2-rf-110-03-abbrev-marked.txt", encoding = "utf8") as file:
        doc_contents = xmltodict.parse(file.read())
        abbrev_file_cont.append(doc_contents)

    #loads fine
    #print(abbrev_file_cont)
    print()
    print()
    for line in abbrev_file_cont:
        for key, value in line.items():
            #print(key)
            #print(value)
            for kkey, vvalue in value.items():
                #print(kkey) # text , tags the usual stuff
                #print(vvalue)
                #abbrev_things.append(vvalue.strip().split()) # strip and split
                try:
                    abbrev_things.append(vvalue.strip()) # strip and split
                except:
                    #print("something is bitching, fuck it")
                    continue
                #for item in vvalue:
                #    print(item)

    ###############
    abbrev_dict = {}
    i = 0
    tempArr = []
    resArr = [[]]
    for item in abbrev_things:
        tempArr.append(item.strip().split())

    #print(len(tempArr))
    #print(tempArr[0])
    i = 0
    for i in range(len(tempArr[0])):
        if("(" in tempArr[0][i] or "((" in tempArr[0][i]):
            #print()
            #print(tempArr[0][i-1])
            #print(":")
            #print(tempArr[0][i])
            abbrev_dict.update({tempArr[0][i-1]: None})
            temp = tempArr[0][i-1]

            temppArr = []

            while not(")" in tempArr[0][i] or "))" in tempArr[0][i]):
                temppArr.append(tempArr[0][i])  # creates a temp arr of all the words in the brackets
                i += 1
            temppArr.append(tempArr[0][i])

            abbrev_dict[temp] = temppArr    # adds those words as VALUE to the previously mentioned key which is the abbreviation

    #print(abbrev_dict)
    pickle.dump(abbrev_dict, open("abbreviations.p","wb"))
    temp = pickle.load(open("abbreviations.p","rb"))

    print(temp)

def createListOfMeds(file_contents_tree_text, file_contents_tree_tags, xml_files_list, doc_file_contents):
    #print("looking for meds")
    meds = {}
    for line in doc_file_contents:  # for all the conents of file
        #print("--entire thing--")
        #print(line)
        for key, value in line.items(): # each line is a dictionary (the whole xml file)
            #print("--key")
            #print(key)
            #print("--value")
            #print(value)
            for kkey, vvalue in value.items():   # each value is a dictionary of its own
                #print("--for word in value print word")
                # print(key)
                #print(vvalue)
                helpTrav(vvalue)    # appends all vvalues (ALL the text from the doc to an array)
                    #traverse the values inside the values
        break # run loop once for testing purposes

    tempArr = []
    i = 0
    # this would be used to mine through and find all the thingies thingies... the medications and their abbreviations
    # for i in range(len(arr_of_contents)):
    #   # i+=1
    #    #if (arr_of_contents[i] == any medication or med-abbreviation in library of all medications)
    #        while(arr_of_contents[i] != "Allergies"):
    #            print(arr_of_contents[i])
    #            i += 1



def helpTrav(value):
    if isinstance(value, str):
       # arr_of_contents.append(value.split(r'\n'))
        #arr_of_contents.append(value)
        #print(value)
        for line in value.split():
            #line.strip()
            #line.replace(r'\n', '')
        #for line in value:

            #print(line)
            arr_of_contents.append(line.strip())
            #arr_of_contents.append(line)
        #arr_of_contents.append(value)
    elif isinstance(value, list):
        for subelement in value:
            helpTrav(subelement)
    elif isinstance(value, dict):
        for subelement in value.values():
            helpTrav(subelement)
    # print(len(doc_file_contents))
    #print(meds)

def createMedicationTypeDict(doc_file_contents):
    print(len(doc_file_contents))
    tags_contents = []
    #medication_types = []
    for line in doc_file_contents:  # for all the conents of file
            # the whole file contents is the line,
            # line is a dictionary of dictionaries
        # print("--entire thing--")
        # print(line)
        for key, value in line.items():  # each line is a dictionary (the whole xml file)
                # accessing every line in the dictionary that is the file contents
            # print("--key")
            # print(key)
            # print("--value")
            # print(value)
            for kkey, vvalue in value.items():  # each value is a dictionary of its own
                # this dictionary (values dictionary) contains the KEY (root) , VALUE (<TEXT> or <TAGS> we need TAGS)
                # print(kkey) # see for yourself
                # print (vvalue)
                if(kkey == "TAGS"):
                    # print(kkey)
                    # print(vvalue)
                    tags_contents.append(vvalue)

    for item in tags_contents:
        # print(item)
        for key, value in item.items(): # items is a dictionary containing key,value. Where key is the  <MEDICATION,  <HYPERLIPEDIA, etc etc)
            # print(key) #see for yourself
            if(key == "MEDICATION"):  # key is tags (i.e. <MEDICATION , looking for the MEDICATION tag
                # print(key)
                # print(value)
                try:
                    #TODO: FIX THIS ERROR / BUG IF IT"S OF IMPORTANCE WHICH I DON"T THINK IT IS!!!
                        # the error happens in the for line in value. The FIRST for loop after try- except
                    for line in value:  # the whole  <MEDICATION id="DOC3" time="after DCT" type1="metformin" type2=""/> is a LINE in this case, which is a dictionary
                        # print(line)
                        # print(value[i])
                        for kkey, vvalue in line.items():  # line is a dictionary so we look for the key, value in this case we're looking for '@type1'
                        # for kkey, vvalue in line.items():  # line is a dictionary so we look for the key, value in this case we're looking for '@type1'
                            # print(kkey)
                            if(kkey == "@type1"): # found the @type1 which is the MEDICATION TYPE
                                # print(kkey)
                                    # kkey = @type1
                                # print(vvalue)
                                    # the TYPE of medicine
                                if vvalue not in (vvalue for vvalue in medication_types):
                                        # this just simply gets rid of any repetitions
                                        # so that we don't have the same medical abbreviation repeating multiple times
                                    medication_types.append(vvalue)
                                #    medications_abbreviations.append(vvalue)
                                    # vvalue = the TYPE of medication
                            # end if
                        # end for
                    # end for
                except:
                    continue
                    # print("something screwed up. It's like going out or bounds or something, "
                    #      "but it shouldn't be important")
            # end if
        # end for
        # break  # this makes the loop execute once for testing purposes
    # end for
####################################################
    # print contents of the medicine abbreviations list
    print("All of the medication types from the 2 gold sets: ")
    print(medication_types)
    # for item in medication_types:
    #    print(item)

    print("amount of medication types = " + str(len(medication_types)))

#end createMedicationTypeDict



if __name__ == "__main__":
    main()