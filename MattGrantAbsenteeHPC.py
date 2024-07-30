import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os


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
slurmnum = os.getenv('SLURM_ARRAY_TASK_ID')

yearnum = slurmnum - 1

#getting name of year from df
for year in dfAbsRAW['Academic Year'].unique().tolist():
    #absRateDemoList = []
    demonum = 0
    #using demographic symbol in domgraphic list
    for demo in demographicList:
        #refine set to the current demographic
		dfAbsSlurmYEAR = pd.read_csv(f"Sample{slurmnum}.csv")
        dfAbsDemo = dfAbsSlurmYEAR[dfAbsSlurmYEAR['Reporting Category'] == demo].dropna()
       
        #sum the eligible students of the set comprised of the demo and the year
        eligibleDemo = dfAbsDemo['ChronicAbsenteeismEligibleCumulativeEnrollment'].astype(float).sum()
        #sum the chronically absent students of the set comprised of the demo and the year
        chronicAbsDemo = dfAbsDemo['ChronicAbsenteeismCount'].astype(float).sum()
        #create the absentee rate for the demographic for the year
        absRateDemo = chronicAbsDemo/eligibleDemo
    
        #Add it to the list of all the demos for the year
        absRateDemoList.append(absRateDemo)

        #add the demo's absentee rate to the array row for that year
        #demoYearArray[yearnum][demonum] = absRateDemo
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

    #yearnum += 1

