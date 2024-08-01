import io

import pandas as pd
import decimal
import numpy as np
def find_decimals(value):
    return (abs(decimal.Decimal(str(value)).as_tuple().exponent))

#table = pd.read_csv('owon_calibration1.csv')

# table = pd.read_csv('all_calibration8a16_old.csv')
# ch1 = table.loc[:, ('MULT', 'CH1')].groupby('CH1', as_index=False).mean()
# ch1_monotonic = ch1[ch1['MULT'].diff().fillna(0) >= 0]
# ch1_monotonic.to_csv('CH1_calibration.csv', index=False)
#
# ch2 = table.loc[:, ('MULT', 'CH2')].groupby('CH2', as_index=False).mean()
# ch2_monotonic = ch2[ch2['MULT'].diff().fillna(0) >= 0 ]
# ch2_monotonic.to_csv('CH2_calibration.csv', index=False)



def clean_data(dataframe, real_value_key, adc_value_key, csv_filename, step=10, decimals=-1):
    monotonic = force_monotonic(dataframe, real_value_key, adc_value_key)
    save_calibration(monotonic, csv_filename)
    xspaced = force_xspaced(monotonic, decimals, step)
    save_header(xspaced, step, csv_filename)
def force_monotonic(dataframe, real_value_key, adc_value_key):
    data = dataframe.loc[:, (real_value_key, adc_value_key)].groupby(adc_value_key, as_index=False).mean()
    data_monotonic = data[data[real_value_key].diff().fillna(0) >= 0]
    return data_monotonic

def save_calibration(dataframe, filename):
    dataframe.to_csv('%s.csv' % filename, index=False)

def force_xspaced(data_monotonic, decimals, step):
    data_np = data_monotonic.to_numpy()
    x_base = round(data_np[0, 0], decimals)
    x_max = round(data_np[-1, 0], decimals)
    x_values = np.arange(x_base, x_max + step / 2, step)
    y_values = np.interp(x_values, data_np[:, 0], data_np[:, 1])
    data_xspaced = pd.DataFrame(np.vstack([x_values, y_values]).T, columns=data_monotonic.columns)
    return data_xspaced
    #data_xspaced.to_csv('%s' % csv_filename, index=False)

def save_header(dataframe_xspaced: pd.DataFrame, step: float, filename: str):
    with open("%s.h" % filename, 'w') as fo:

        y_data = dataframe_xspaced.iloc[:,1]
        sf = io.StringIO()
        y_data.T.to_csv(sf, header=False, index=False)
        sf.seek(0)
        body=",\n".join(" "*8 + line.strip() for line in sf)

        # typedef struct
        # {
        #   uint32_t nValues;           /**< nValues */
        #   float32_t x1;               /**< x1 */
        #   float32_t xSpacing;         /**< xSpacing */
        #   float32_t *pYData;          /**< pointer to the table of Y values */
        # } arm_linear_interp_instance_f32;

        header_tag = "__%s_H" % filename.upper()
        fo.write("#ifndef %s\n" % header_tag)
        fo.write("#define %s\n" % header_tag)
        fo.write("#include \"arm_math.h\"\n")
        fo.write('const arm_linear_interp_instance_f32 %s = {\n' % filename)
        fo.write('    %d, // nValues\n' % len(y_data))
        fo.write('    %f, // x1\n' % dataframe_xspaced.iloc[0,0])
        fo.write('    %f, // xSpacing\n' % step)
        fo.write('    (float32_t []){ //pYData\n')
        fo.write(body + '\n')
        fo.write('    }\n')
        fo.write('};\n')
        fo.write("#endif /* %s */" % header_tag)



# table = pd.read_csv('slave_raw_bms_cal_ch1fix2.2.csv')
# clean_data(table, 'v_meas_ch2', 'slA_ch1', 'SLVA_CH1_calibration')
# clean_data(table, 'v_meas_ch2', 'slB_ch1', 'SLVB_CH1_calibration')
#
#
# lo = pd.read_csv('slave_raw_bms_cal_ch2fix2.2.csv')
# hi = pd.read_csv('slave_raw_bms_cal_ch2fix3.7.csv')
# table = pd.concat([lo, hi],ignore_index=True)
#
# clean_data(table, 'v_meas_ch2', 'slA_ch2', 'SLVA_CH2_calibration')
# clean_data(table, 'v_meas_ch2', 'slB_ch2', 'SLVB_CH2_calibration')

charge = pd.read_csv('raw_bms_charge_cal.csv').iloc[1:, :][::-1]
charge["i_meas"] = -1* charge["i_meas"]
discharge = pd.read_csv('raw_bms_discharge_cal.csv')
discharge["i_meas"] = -1* discharge["i_meas"]
table = pd.concat([charge, discharge], ignore_index=True)
current_table = table
clean_data(table, 'i_meas', 'v_current', 'MST_CURR_calibration', step=1, decimals=0)

table = pd.read_csv('raw_bms_cal.csv')
clean_data(table, 'MULT', 'VBAT', 'MST_vbat_calibration')
clean_data(table, 'MULT', 'VPOW', 'MST_vpow_calibration')