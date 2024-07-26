import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#allChronicAbsentee is already cleaned
dfAbsRAW = pd.read_csv("allChronicAbsentee.csv")
dfAbsRAW = dfAbsRAW.drop(['District Name', 'ChronicAbsenteeismRate'], axis = 1)
dfAbsRAW = dfAbsRAW.sort_values(by=['Academic Year', 'School Name']).dropna()
#dfAbsRAW

demographicList = [
"RB",
"RI",
"RA",
"RF",
"RH",
"RD",
"RP",
"RT",
"RW",
"GM",
"GF",
"GX",
"SE",
"SD",
"SS",
"SM",
"SF",
"SH",
"GRKN",
"GR13",
"GR46",
"GR78",
"GRK8",
"GR912",
"TA"]

#create a 2d array for storing calculated absentee rates for demographic groups by year
demoYearArray = ([[0 for x in range(25)] for y in range(6)])

yearnum = 0

#getting name of year from df
for year in dfAbsRAW['Academic Year'].unique().tolist():
    absRateDemoList = []
    demonum = 0
    #using demographic symbol in domgraphic list
    for demo in demographicList:
        #refine set to the current demographic
        dfAbsDemo = dfAbsRAW[dfAbsRAW['Reporting Category'] == demo].dropna()
        #refine that to the current year
        dfAbsDemoYear = dfAbsDemo[dfAbsDemo['Academic Year'] == year]
        #sum the eligible students of the set comprised of the demo and the year
        eligibleDemo = dfAbsDemoYear['ChronicAbsenteeismEligibleCumulativeEnrollment'].astype(float).sum()
        #sum the chronically absent students of the set comprised of the demo and the year
        chronicAbsDemo = dfAbsDemoYear['ChronicAbsenteeismCount'].astype(float).sum()
        #create the absentee rate for the demographic for the year
        absRateDemo = chronicAbsDemo/eligibleDemo
    
        #Add it to the list of all the demos for the year
        absRateDemoList.append(absRateDemo)

        #add the demo's absentee rate to the array row for that year
        demoYearArray[yearnum][demonum] = absRateDemo
        demonum += 1
    
        
        print("In", year, "with", chronicAbsDemo, "absent of a possible", eligibleDemo, "students, the chronic absentee rate of", demo, "is: ", absRateDemo)
    
    #print pie chart for ethnicities for that year
    plt.pie(absRateDemoList[0:9], labels = demographicList[0:9], autopct='%1.1f%%', startangle=90)
    titlep = "Chronic Absentee Rates by Ethnicity for " + str(year)
    plt.title(titlep) 
    #plt.show()
    plt.savefig(f'ChronAbsEthni{year}.png')

    #print bar graph for grade groups for that year
    categories = demographicList[18:24]
    values = absRateDemoList[18:24]

    plt.bar(categories, values)
    plt.xlabel('Grade Groups')
    plt.ylabel('Absentee Rate')
    titleb = "Absentee Rates by Grade Group for " + str(year)
    plt.title(titleb)
    #plt.show()
    plt.savefig(f'ChronAbsGrade{year}.png')

    yearnum += 1

#Use the calculated matrix to create more graphs for age groups.
demonum=0
for demo in demographicList:
    print(demo)
    absRates =[]
    yearnum = 0
    
    for year in dfAbsRAW['Academic Year'].unique().tolist():
        
        absRates.append(demoYearArray[yearnum][demonum])
        yearnum += 1
    categories = dfAbsRAW['Academic Year'].unique().tolist()
    values = absRates
    
    plt.bar(categories, values)
    
    plt.xlabel('Years')
    plt.ylabel(f'Absentee Rates for {demo}')
    plt.title(f'Absentee Rates for {demo} over Years')
    plt.savefig(f'Absenteesof{demo}.png')
    
    plt.show()
    

    demonum += 1
