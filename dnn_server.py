import os
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import Normalizer, MinMaxScaler
from sklearn.pipeline import Pipeline
import random as rn

RANDOM_SEED = 42
rn.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
tf.random.set_seed(RANDOM_SEED)
# TODO data processing
## find customer

def change_feature(df):
    df.columns = map(str.lower, df.columns)
    df = df.replace(to_replace="A", value=3)
    df = df.replace(to_replace="H", value=0)
    df = df.replace(to_replace="O", value=1)
    df = df.replace(to_replace="R", value=2)

    df = df.drop('1', axis=1)
    df = df.drop('2', axis=1)
    df = df.drop('5', axis=1)
    df = df.drop('9', axis=1)
    df = df.drop('c0', axis=1)
    df = df.drop('c1', axis=1)
    df = df.drop('c2', axis=1)
    df = df.drop('c3', axis=1)
    df = df.drop('c4', axis=1)
    df = df.drop('c5', axis=1)
    df = df.drop('avg_amount', axis=1)
    df = df.drop('current_amount', axis=1)
    return df


def normalize(df, data):
    df = df.drop(['cust_no'], axis=1)
    non_breach = df[df.label == 0]
    non_breach = non_breach.sample(frac=1).reset_index(drop=True)
    X_train = non_breach.iloc[:int(3053 * 0.8)].drop('label', axis=1)
    X_train, _ = train_test_split(X_train, test_size=0.2, random_state=42)
    pipeline = Pipeline([('normalizer', Normalizer()), ('scaler', MinMaxScaler())])
    pipeline.fit(X_train)
    data = pipeline.transform(data)
    return data



def find_cust(df,cust):
    c_df = df.loc[df[1] == cust].reset_index(drop=True)
    return c_df

# TODO: after prediction
def mad_score(point):
    ad = np.abs(point - 0.6745)
    return 0.6745 * ad




def dnn_server(cust_no, company, c_stock, t_type):
    # TODO: load dataset
    df = pd.read_csv('data.csv', index_col=[0])
    df = change_feature(df)
    df['avg_stock'] = np.log10(df.avg_stock + 0.00001)
    df['current_stock'] = np.log10(df.current_stock + 0.00001)
    df.fillna(0, inplace=True)
    # TODO: load model
    input_dim = 14
    autoencoder = tf.keras.models.Sequential([

        # deconstruct / encode
        tf.keras.layers.Dense(input_dim, activation='elu', input_shape=(input_dim,)),
        tf.keras.layers.Dense(128, activation='elu'),
        tf.keras.layers.Dense(64, activation='elu'),
        tf.keras.layers.Dense(32, activation='elu'),
        tf.keras.layers.Dense(16, activation='elu'),
        tf.keras.layers.Dense(8, activation='elu'),
        # reconstruction / decode
        tf.keras.layers.Dense(16, activation='elu'),
        tf.keras.layers.Dense(32, activation='elu'),
        tf.keras.layers.Dense(64, activation='elu'),
        tf.keras.layers.Dense(128, activation='elu'),
        tf.keras.layers.Dense(input_dim, activation='elu')

    ])
    # autoencoder.summary()
    autoencoder.load_weights('autoencoder.h5')

    # TODO: company type dict
    company_data = pd.read_csv('company_data.csv', index_col=0)
    com_dict = dict(company_data.values)
    # print(com_dict)
    # TODO: input
    # cust_no = '0x78D069BCC23EAD3DF21154E5C04838C7F942ACD422BBD1D902A0065A68B90238'
    # company = '0x456FEE4ACB733FD682DEDE7D1EF34F61'
    # c_stock = 10000  # how much stock
    # t_type = 0  # transaction type

    # TODO: update data to predict
    cust_df = df.loc[df['cust_no'] == cust_no].reset_index(drop=True)
    cust_df = cust_df.drop(['cust_no'], axis=1)
    cust_df = cust_df.drop(['label'], axis=1)
    cust_df.trans_type[0] = t_type
    if company in com_dict:
        cust_df.company_type[0] = com_dict[company]
    else:
        cust_df.company_type[0] = 6
    cust_df.current_stock[0] = np.log10(float(c_stock) + 0.00001)

    # TODO: prediction
    data = cust_df
    data = normalize(df, data)

    re_data = autoencoder.predict(data)
    mse = np.mean(np.power(data - re_data, 2), axis=1)
    # mse = mad_score(mse)
    threshold = 0.0003
    y_pred = 1 if mse > threshold else 0
    return y_pred


if __name__ == '__main__':
    response = dnn_server('0x2919A6CC3E1DC3432BB3F60F4D88EF98930829740F52A3C34B03CAA4ABF1E2F4','0x5E8EDFFA3C25E6FB6E21701CBDCC0ABF','1150','0')

    response1 = dnn_server('0xCFEAD510FA89A8C96F85B748FAA9C815F9E2F5D3D3FE51DB48174EACCA042026','0x0D146D60FF69F2BD8B3367E1574A8A5D', '1000', '0')
    print(response)
    print(response1)