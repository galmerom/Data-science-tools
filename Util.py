#####################################################################################################
# This module includes all kind of codes snippets that we use often. 
# The following functions are available:
# 
# File handlings:
#   ReadCsvDirectory2Pandas - used for reading many csv files into one dataframe
#
# Scoring:
#   Scoring - Gets 2 series and return r^2 and RMSE and if asked it also show a chart
#####################################################################################################

#Imports
import os
import pandas as pd
from sklearn.metrics import mean_squared_error , r2_score
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

def ReadCsvDirectory2Pandas(DirectoryPath,**kwargs):
    '''
    Gets a directory path that contains csv files and returns a dataframe that
    contains all the concated data from all the files. At the end of the dataframe it
    adds 2 new columns:
    1. Called "FileName" that includes the name of the original file.
    2. Called "OrigIndex" that include the original index from the original file.
    
    parameters:
    DirectoryPath str. The directory path
    **kwarg dictionary. Contains all  arguments that is needed for pd.read_csv
    
    Example for calling the function:
    argDic={'squeeze':True}
    df = ReadCsvDirectory2Pandas('/gdrive/...",**argDic)

    Returns dataframe
    '''
    if DirectoryPath[-1]!="/":
        DirectoryPath = DirectoryPath+"/"
    First_Flag=True
    for f in os.listdir(DirectoryPath):
        if os.path.isfile(DirectoryPath+f):
            if First_Flag:
                data = pd.read_csv(DirectoryPath + f,**kwargs)
                data['FileName'] = f
                First_Flag=False
            else:
                tmpdata = pd.read_csv(DirectoryPath + f,**kwargs)
                tmpdata['FileName'] = f
                data = pd.concat([data,tmpdata],axis=0,copy=True)
    data = data.reset_index()
    data = data.rename({'index':'OrigIndex'},axis=1)
    return data


def Scoring(y_true,y_pred,colorSer=None,WithChart=False,Figsize=(10,5),ylabel='Predicted values',xlabel='Actual values',Title='Actual ver. predicted'):
    '''
    This fucnction gets 2 series and compare them wirh the following scores: R^2 and RMSE.
    It can also draw a chart if needed.
    input parameters:
    y_true series. The actual values
    y_pred series. The predicted values
    WithChart bool. Show a chart or not
    In case there is a chart, then there are default parameters that can be changed:
    Figsize tuple. chart size
    ylabel string. y axis description
    xlabel string. x axis description
    Title string. Title of chart
    clrTpl tuple. (series,color dictionary) The first elemnent is the series to map. 
                                            The second is a dictionary that maps values (unique values in the series) to colors.
                    
    Returns: tuple. (string that show the results, float.R^2 result,float RMSE result, if colors were used then it returns a dictionary
                    between unique series values and the colors that were picked auto.)
    '''
    r2='{:.3f}'.format(r2_score(y_true, y_pred))
    rmse = '{:.3f}'.format(np.sqrt(mean_squared_error(y_true, y_pred)))
    Diff = y_true-y_pred

    ReturnStr = 'R-squared: '+str(r2)+'   RMSE:'+str(rmse) #+ '     Mean % diff: '+ str('{:.1%}'.format(change.mean()))
    if WithChart:
        MaxValue=max(max(y_true),max(y_pred))
        MinValue=min(min(y_true),min(y_pred))
        MaxValue = MaxValue+0.05*(MaxValue-MinValue)# add a little to the right so the max point will not be on the end of the chart

        plt.figure(figsize=Figsize)
        colorDic = None
        if isinstance(colorSer, pd.Series):
            colorlist = list(colors.ColorConverter.colors.keys())
            colorDic = dict(zip(colorSer.unique(),colorlist[0:len(colorSer.unique())])) # create a dictionary with unique values and colors
            ColorInput = colorSer.map(colorDic)
        else:
            ColorInput = None
            
        plt.scatter(x=y_true,y=y_pred,c=ColorInput ,label = "label_name")
        plt.plot([MinValue, MaxValue], [MinValue, MaxValue], 'k-', color = 'r')

        # for i, txt in enumerate(rngList):
        #     plt.annotate(txt, (TOCPredField.reset_index(drop=True)[i]*1.015, No3PredField.reset_index(drop=True)[i]),fontsize=12)
        # Set x and y axes labels
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)

        plt.xlim(MinValue,MaxValue)
        plt.ylim(MinValue,MaxValue)
        
        plt.title(Title+'\n'+ReturnStr)
        plt.show()
    return ( ReturnStr,float(r2),float(rmse),colorDic)
