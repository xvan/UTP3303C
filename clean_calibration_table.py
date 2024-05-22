import pandas as pd

#table = pd.read_csv('owon_calibration1.csv')

# table = pd.read_csv('all_calibration8a16_old.csv')
# ch1 = table.loc[:, ('MULT', 'CH1')].groupby('CH1', as_index=False).mean()
# ch1_monotonic = ch1[ch1['MULT'].diff().fillna(0) >= 0]
# ch1_monotonic.to_csv('CH1_calibration.csv', index=False)
#
# ch2 = table.loc[:, ('MULT', 'CH2')].groupby('CH2', as_index=False).mean()
# ch2_monotonic = ch2[ch2['MULT'].diff().fillna(0) >= 0 ]
# ch2_monotonic.to_csv('CH2_calibration.csv', index=False)
#
# bms_vbat = table.loc[:, ('MULT', 'VBAT')].groupby('VBAT', as_index=False).mean()
# bms_vbat_monotonic = bms_vbat[bms_vbat['MULT'].diff().fillna(0) >= 0 ]
# bms_vbat_monotonic.to_csv('VBAT_calibration.csv', index=False)




# table = pd.read_csv('all_calibration8a16_vpow_old.csv')
#
# bms_vpow = table.loc[:, ('MULT', 'VPOW')].groupby('VPOW', as_index=False).mean()
# bms_vpow_monotonic = bms_vpow[bms_vpow['MULT'].diff().fillna(0) >= 0 ]
# bms_vpow_monotonic.to_csv('VPOW_calibration.csv', index=False)

table = pd.read_csv('all_calibration8a16_curr_plus_old.csv')

bms_curr = table.loc[:, ('MULT', 'IBAT')].groupby('IBAT', as_index=False).mean()
bms_curr_monotonic = bms_curr[bms_curr['MULT'].diff().fillna(0) <= 0 ]
bms_curr_monotonic.to_csv('IBAT_calibration.csv', index=False)
