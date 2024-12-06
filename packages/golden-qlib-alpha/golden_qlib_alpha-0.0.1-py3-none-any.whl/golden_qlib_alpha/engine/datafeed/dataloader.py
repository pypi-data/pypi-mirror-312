# encoding:utf8
import pandas as pd

from engine.datafeed.expr.expr_mgr import ExprMgr
from engine.datafeed.datafeed_hdf5 import Hdf5DataFeed


class Dataloader:
    def __init__(self):
        self.expr = ExprMgr()
        self.feed = Hdf5DataFeed()

    def load_one_df(self, codes,start,end ,names, fields):
        dfs = self.load_dfs(codes,start,end, names, fields)
        all = pd.concat(dfs)
        all.sort_index(ascending=True, inplace=True)
        all.dropna(inplace=True)
        return all

    def load_dfs(self, codes,start,end ,names, fields):
        dfs = []
        for code in codes:
            # 直接在内存里加上字段，方便复用
            df = self.feed.get_df(code,start,end)
            for name, field in zip(names, fields):
                exp = self.expr.get_expression(field)
                # 这里可能返回多个序列
                se = exp.load(code,start,end)
                if type(se) is pd.Series:
                    df[name] = se
                if type(se) is tuple:
                    for i in range(len(se)):
                        df[name + '_' + se[i].name] = se[i]
            df['code'] = code
            dfs.append(df)

        return dfs


if __name__ == '__main__':
    names = []
    fields = []

    '''
    
    fields += ["$close/Ref($close,20)-1"]
    names += ['mom_20']

    fields += ["$mom_20>0.08"]
    names += ['buy_signal']

    fields += ["$mom_20<0"]
    names += ['sell_signal']

    fields += ["$close"]
    names += ['close']
    '''

    #fields += ['BBands($close)']
    #names += ['BBands']



    fields += ["RSRS($high,$low,18)"]
    names += ['RSRS']

    fields += ['Norm($RSRS_beta,600)']
    names += ['Norm_beta']

    #fields += ['OBV($close,$volume)']
    #names += ['obv']


    fields += ['Slope($close,20)']
    names += ['mom_slope']

    fields += ['KF($mom_slope)']
    names += ['kf_mom_slope']

    fields += ["Ref($close,-1)/$close - 1"]
    names += ['label']

    all = Dataloader().load_one_df(['000300.SH'], names, fields)
    print(all)
    #all['obv'].plot()
    #import matplotlib.pyplot as plt
    #plt.show()
