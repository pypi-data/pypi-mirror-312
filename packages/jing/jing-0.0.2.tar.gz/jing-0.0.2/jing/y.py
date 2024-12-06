#!/usr/bin/env python
# -*- encoding: utf8 -*-

import data_center
import reference

import pandas as pd

import warnings
warnings.filterwarnings("ignore")

pd.set_option('display.max_columns', None)

class Y:
    def __init__(self, _market="us", _date="", _code="") -> None:
        self.market = _market
        self.date = _date
        self.code = _code

        self.dataCenter = data_center.DataCenter(self.market)
        self.df = self.dataCenter.one('IONQ', self.date) 
        self.ref = reference.Reference(self.df)

if __name__=="__main__":
    y = Y("us", _date="2024-09-27", _code='IONQ')
    ref = y.ref
    print(ref.date(0), ref.ma20(0), ref.ma50(0), ref.ma200(0), ref.vma50(0), ref.macd(0), ref.diff(0), ref.dea(0))

