
1) Delete SchoolsList.xlsx, school_details.xlsx, school_codes.xlsx from this folder.
2) Go to: http://det.wa.edu.au/schoolinformation/detcms/navigation/school-lists/ and download the xlsx version of the alphabetic list. Save the file in this folder as SchoolList.xlsx
3) Open PULL_SCHOOL_CODES.xlsx. Click the developer tab -> MACROS -> PullSchoolCodes*. You will be prompted to enter the line of the first school (integer), then the line of the last school (integer), 
   then the coloumn of the Codes (character). After Running there schould be a school_codes.xlsx file in this folder.

--------------------------------------------------------------------------------------------------------------------------------------------------------

	*IF THE DEVELOPER TAB IS NOT VISIBLE:

	1) Right click the ribbon (ie insert or page layout)
	2) click "customize the ribbon"
	3) in the main tabs check the developer box
	4) click ok

--------------------------------------------------------------------------------------------------------------------------------------------------------

4) Open the Command Prompt (Type "cmd" into the bottom left search bar on the desktop to find it)
5) Copy this: cd C:\Users\Eoghan\Desktop\Programs\schoolDataScrape
6) Right click on the command prompt window and press enter
7) Copy this: py schoolDataScrape.py
8) Right click on the command prompt window and press enter

This will take about 2.5 hours to run and afterwards you should have a school_details.xlsx file. DO NOT open this file while untill the program has finished.

9) Open school_details_formatted.xslx click the data tab and click refresh. When prompted just click OK

