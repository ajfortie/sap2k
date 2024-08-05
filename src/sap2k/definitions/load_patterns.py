"""
The purpose of this module is to define load patters for the SAP Model
"""
from typing import Union

def Add(lp_name:str, my_type: Union[str,int]=1,self_wt_mult:float=1)->int:

    #Validate inputs
    assert isinstance(lp_name,str)
    assert isinstance(my_type,Union[str,int])
    assert isinstance(self_wt_mult,float)

    ret = 