import pandas as pd

table = pd.read_csv('owon_calibration1.csv')
ch1 = table.loc[:, ('MULT', 'CH1')].groupby('CH1', as_index=False).mean()
ch1_monotonic = ch1[ch1['MULT'].diff().fillna(0) >= 0]
ch1_monotonic.to_csv('CH1_calibration.csv', index=False)

ch2 = table.loc[:, ('MULT', 'CH2')].groupby('CH2', as_index=False).mean()
ch2_monotonic = ch2[ch2['MULT'].diff().fillna(0) >= 0 ]
ch2_monotonic.to_csv('CH2_calibration.csv', index=False)

