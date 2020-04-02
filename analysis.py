import os
import datetime
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from fbprophet import Prophet
from fbprophet.diagnostics import cross_validation, performance_metrics
from fbprophet.plot import plot_cross_validation_metric


def analysis(filename, images_dir, max_val, min_val, future_val):

    # 画像スタイル
    sns.set(style="darkgrid")

    # 1,2列のみ読み込み
    df = pd.read_csv(filename, usecols=[0, 1], encoding="cp932")

    # カラム名取得
    clm_name_date = df.columns[0]
    clm_name_data = df.columns[1]

    # カラム名変更
    df.rename(columns={clm_name_date: 'ds', clm_name_data: 'y'}, inplace=True)

    df['cap'] = max_val
    df['floor'] = min_val

    # モデル作成
    model = Prophet(growth='logistic')
    model.fit(df)

    # 未来予測
    future_df = model.make_future_dataframe(future_val)
    future_df['cap'] = max_val
    future_df['floor'] = min_val

    # 結果を格納
    forecast_df = model.predict(future_df)

    # 凡例
    header = [clm_name_date, clm_name_data, 'lower', 'upper']

    # データフレームからリストに変換
    datas = {}

    tmp = forecast_df['ds'].astype(str)
    datas['ds'] = tmp.values.tolist()

    tmp = df['y']
    datas['y'] = tmp.values.tolist()

    for i in 'yhat_lower', 'yhat_upper':
        tmp = forecast_df[i]
        datas[i] = tmp.values.tolist()

    # 値を返す
    return header, datas
