# -*- coding: utf-8 -*-
"""

Phased_Kit_Maker_V5.py creates phased paternal and maternal files.

Phased files are in Ancestry format.

Ancestry, FTDNA and 23andme DNA files supported.

The default designation of phased no calls is an 'X'.

This version generates Evil Twin files in addition to maternal and paternal 
phased kits.

The files generated are of one these types:
    
Namemp.txt - Paternal phased file with mother as reference.
Namepp.txt - Paternal phased file with father as reference.
Namepm.txt - Maternal phased file with father as reference.
Namemm.txt - Maternal phased file with mother as reference.
Nameetp.txt - Paternal evil twin file with father as reference.
Nameetm.txt - Maternal evil twin file with mother as reference.

@author: mickjolley (mickj1948@gmail.com) © 2026 
"""
import os
import pandas as pd
import numpy as np
import sys

from PKMconfig_V5 import *

def conditions_opp(df1,df2,df3,df4):
    if df1 == df2:
        return df1
    elif df1 != df2 and df3 == df4 and df1 == df3:
        return df2
    elif df1 != df2 and df3 == df4 and df2 == df3:
        return df1
    else:
        return NO_CALLS
    
def conditions_same(df1,df2,df3,df4):
    if df1 == df2:
        return df1
    elif df1 != df2 and df3 == df4 and df1 == df3:
        return df1
    elif df1 != df2 and df3 == df4 and df2 == df3:
        return df2
    else:
        return NO_CALLS
    
def conditions_et(df1,df2,df3,df4):
    if df3 == df4:
        return df3
    elif df1 == df2 and df1 == df3 and df1 != df4:
        return df4
    elif df1 == df2 and df1 == df4 and df1 != df3:
        return df3
    else:
        return NO_CALLS    
    
def load_DNA_file(ind):
    # Load DNA file.
    file_names = os.listdir(DNA_FOLDER)
    
    for filname in file_names:
        if ind + "_raw_dna.txt" in filname:

            this_file = os.path.join(DNA_FOLDER, filname)

            if 'Ancestry' in filname:
                df = pd.read_csv(this_file, 
                    sep='\t',
                    skip_blank_lines=True,
                    comment='#',
                    header=0,
                    dtype = {0:str},
                    names=['rsid', 
                       'chromosome',
                       'position',
                       f"{ind}-allele1",
                       f"{ind}-allele2"])
                
            else:
                df = pd.read_csv(this_file, 
                        sep='\t',
                        skip_blank_lines=True,
                        comment='#',
                        header=0,
                        low_memory = False,
                        names=['rsid', 'chromosome', 'position', f"{ind}_allele_pair"])
                
                df[f"{ind}-allele1"] = df[f"{ind}_allele_pair"].str[0]
                df[f"{ind}-allele2"] = df[f"{ind}_allele_pair"].str[1]
                df.drop([f"{ind}_allele_pair"], axis=1, inplace=True)
                df.replace('X', '23', inplace = True)
                df.replace('XY', '23', inplace = True)
                df= df.drop(df[df["chromosome"] == "Y"].index)
                df= df.drop(df[df["chromosome"] == "MT"].index)
                df= df.astype({'chromosome': 'int64'})
                    
            df[ind + '-allele1'] = df[ind + '-allele1'].astype('string')
            df[ind + '-allele2'] = df[ind + '-allele2'].astype('string')
            
            df = df[df[ind + '-allele1'].eq('A') | df[ind + '-allele2'].eq('A') |
            df[ind + '-allele1'].eq('T') | df[ind + '-allele2'].eq('T') |
            df[ind + '-allele1'].eq('C') | df[ind + '-allele2'].eq('C') |
            df[ind + '-allele1'].eq('G') | df[ind + '-allele2'].eq('G')]
    
            df = df.reset_index(drop = True)
            
    try:
        return df
    except:
        print('\nFile does not exist. Check spelling of name.')
        sys.exit()    

if __name__ == '__main__':
    
    # End with forward slash.
    DNA_FOLDER = os.path.normpath(DNA_FOLDER) + '/'
    
    # Suffix to file name.
    if RELATIONSHIP == 'Father':
        if MODE == 'Opposite':
            fnme = 'pm'
        elif MODE == 'Same':
            fnme = 'pp'
        elif MODE == 'ET':
            fnme = 'etp'
        else:
            print('\nMode not correctly selected! Please reenter.')
            sys,exit()
            
    if RELATIONSHIP == 'Mother':
        if MODE == 'Opposite':
            fnme = 'mp'
        elif MODE == 'Same':
            fnme = 'mm'
        elif MODE == 'ET':
            fnme = 'etm'
        else:
            print('\nMode not correctly selected! Please reenter.')
            sys.exit()
            
    print('\nPlease wait while files are loaded...')        
            
    # Load parent file.
    dpar = load_DNA_file(PARENT)
                
    # Load sib file.
    for indname in SIB_NAMES:
        df = load_DNA_file(indname)
        
    
        # Merge PARENT and sib file.
        dfm = pd.merge(dpar, df, on = ('rsid', 'chromosome', 'position'))
        dfm = dfm[dfm['chromosome'] < 24]
        dfm.reset_index(drop = True, inplace = True)
        
        dfm.loc[pd.isna(dfm[indname + '-allele2']), indname + '-allele2'] = dfm[indname + '-allele1']
    
        # Find phased PARENT allele.
        if MODE == 'Opposite':
            dfm['allele1'] = np.vectorize(conditions_opp)(dfm[indname + '-allele1'],
                      dfm[indname + '-allele2'], dfm[PARENT + '-allele1'],
                      dfm[PARENT + '-allele2'])
        elif MODE == 'Same':
            dfm['allele1'] = np.vectorize(conditions_same)(dfm[indname + '-allele1'],
                      dfm[indname + '-allele2'], dfm[PARENT + '-allele1'],
                      dfm[PARENT + '-allele2'])
        else:    
            dfm['allele1'] = np.vectorize(conditions_et)(dfm[indname + '-allele1'],
                      dfm[indname + '-allele2'], dfm[PARENT + '-allele1'],
                      dfm[PARENT + '-allele2'])
            
        dfm = dfm.drop([PARENT + '-allele1', PARENT + '-allele2',indname + '-allele1', 
                        indname + '-allele2'], axis = 1)    
            
        dfm['allele2'] = dfm['allele1']
        
        save_file = DNA_FOLDER + "Ancestry_" + indname + fnme + "_raw_dna.txt"
     
        # Delete file if it exists.
        if os.path.exists(save_file):
            os.remove(save_file)
            
        dfm.to_csv(save_file, sep = '\t', index = False)    
        
        print(f'\nFile Ancestry_{indname}{fnme}_raw_dna.txt written.')
        
    print('\nFinished')
