import pandas as pd
import numpy as np

dct_ = [{"Gender": "Male", "HeightCm": 171, "WeightKg": 96 },
{ "Gender": "Male", "HeightCm": 161, "WeightKg": 85 },
{ "Gender": "Male", "HeightCm": 180, "WeightKg": 77 },
{ "Gender": "Female", "HeightCm": 166, "WeightKg": 62},
{"Gender": "Female", "HeightCm": 150, "WeightKg": 70},
{"Gender": "Female", "HeightCm": 167, "WeightKg": 82}]

## Define UDF to calculate the category and Risk
def calculations(bmi):
    #cal_ = "None|None"
    if   bmi <= 18.4:
        cal_ = "Underweight|Malnutrition risk"
    elif bmi >= 18.5 and bmi <= 24.9:
        cal_ = "Normal weight|Low risk"
    elif bmi >= 25 and bmi <= 29.9:
        cal_ = "Overweight|Enhanced risk"
    elif bmi >= 30 and bmi <= 34.9:
        cal_ = "Moderately obese|Medium risk"
    elif bmi >= 35 and bmi <= 39.9:
        cal_ = "Severely obese|High risk"
    elif bmi >=40:
        cal_ = "Very severely obese|Very high risk"
    return cal_

def cal_bmi(WeightKg,HeightCm ):
    bmi = WeightKg/((HeightCm/100)**2)
    bmi = round(bmi, 2)
    return bmi

## Test cases
def test_cal(bmi):  
    if bmi==40:
        assert calculations(bmi)== "Very severely obese|Very high risk", "check calculations UDF, incorrect values"
    

def fun(dct_):

    ## read source
    print("Hello There, reading Source ..")
    src_df = pd.DataFrame(list(dct_))
    
    ## Divide by 0 exception + round to 2 decimal places
    df_bmi = src_df.assign(bmi = lambda rec: round( rec['WeightKg']/((rec['HeightCm']/100)**2).replace(np.inf, 0), 2))
   
    ## Apply UDF to calculate the category and Risk into single field
    df_bmi['calculations'] = df_bmi['bmi'].apply(calculations) 
    
    ## Derive BMI Category & Health risk from calculated field
    df_bmi[['BMI Category', 'Health risk']] = df_bmi['calculations'].str.split('|', 1, expand=True)
    
    ## Drop intermediatory field 
    df_bmi = df_bmi.drop('calculations', 1)


    ## Count Number of Overweight People 
    cnts = df_bmi[df_bmi['BMI Category'] == 'Overweight' ].shape[0]
    print("###### ------ ------- #####")
    print("Number of Overweight People =", cnts)

    ## Final Table
    print("###### Final table #####\n")
    #print('\n',df_bmi)
    print(df_bmi.to_dict('records'))

if __name__ == "__main__":
    
    test_cal(40)
    print("Test case passed !!")
    fun(dct_)
    
#### Or Python Approach:

# tgt_dict=[]
# rec={}
# dct_
# # Or using Python 
# for rec in dct_:
#     rec['bmi'] = round( rec['WeightKg']/((rec['HeightCm']/100)**2), 2)  
#     rec['calculations'] = calculations(rec['bmi']) 
#     rec['BMI Category'], rec['Health risk'] = rec['calculations'].split('|')[0], rec['calculations'].split('|')[1]
#     del rec['calculations']
#     tgt_dict.append(rec)
# print(tgt_dict)
# cnts =0
# for t in tgt_dict:
#     if t['BMI Category']=='Overweight':
#         cnts +=1
# print("Number of Overweight People =", cnts)