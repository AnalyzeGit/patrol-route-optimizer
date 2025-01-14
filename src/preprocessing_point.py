

# Handling
import pandas as pd
import numpy as np




def preprocess_point(df,col):
    
    df[col] = df[col].astype('str')
    
    df[col] = df[col].str.replace('POINT','')
    df[col] = df[col].str.replace('(','')
    df[col] = df[col].str.replace(')','')
    df[col] = df[col].str.strip()

    df['경도'] = df[col].str.split(' ').str[0]
    df['위도'] = df[col].str.split(' ').str[1]
    
    return df

