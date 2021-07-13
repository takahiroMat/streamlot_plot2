####################################
# 更新：210707
# 動作：python > streamlit
# 課題：> weight_max 
"""    
・plot:fig
・x軸が時間データ非対応？
・weightで、mapの色分け
"""
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd
from PIL import Image
import time
import math


#import plotly.figure_factory as ff

# --------------------------
# 初期設定
f_size = 40
tgt_data = "tmp29_"
path="log_csv/"+tgt_data
st.title(tgt_data)
RANGE_time = 0.4 # plotさせる[s]
range_time = int(RANGE_time * 1000000000 /2)
t_swith=0

#----------------------------

# ----------------------------
# 予定経路(ゴール)座標
#

goal_x_1 = [ 0, -38, -38,   0,   0, -38,   0,   0,  -3,  -3,   0,   0,  -3,  -3,   0,   0,  -3, -3,   0,   0]
goal_y_1 = [ 7,   7,   6,   6,   5,   5,   5,   4,   4,   3,   3,   2,   2,   1,   1,   0,   0, -1,  -1,   7]
#goal_ang_1=[a3,  a3,  a2,   0,  a2,  a3,   0,  a2,  a3,  a2,   0,  a2,  a3,  a2,   0,  a2,  a3, a2,   0,  a3]
    

    
    #initialize goal positions for cleaning area 2
    #goal_x_2 = [-3.5, -46, -46,-3.5,-3.5, -46, -46,-3.5,-3.5, -21, -21,-3.5,-3.5, -21, -21,-3.5,-3.5, -21, -21,-3.5,-3.5, -21, -21,-3.5,-3.5, -46, -46,-3.5,-3.5, -46, -3.5]
goal_x_2 = [-3.5, -44, -44,-3.5,-3.5, -44, -44,-3.5,-3.5, -44, -44,-3.5,-3.5, -44, -44,-3.5,-3.5, -38, -38,-3.5,-3.5, -38, -38,-3.5,-3.5, -38, -38,-3.5,-3.5, -38, -3.5]
goal_y_2 = [  22,  22,  21,  21,  20,  20,  19,  19,  18,  18,  17,  17,  16,  16,  15,  15,  14,  14,  13,  13,  12,  12,  11,  11,  10,  10,   9,   9,   8,   8, 10.5]
#goal_ang_2=[  a3,  a3,  a2,   0,  a2,  a3,  a2,   0,  a2,  a3,  a2,   0,  a2,  a3,  a2,   0,  a2,  a3,  a2,   0,  a2,  a3,  a2,   0,  a2,  a3,  a2,   0,  a2,  a3,   a3]
    
    #initialize goal positions for cleaning area 3
goal_x_3 = [ -30,  -60, -30,   -60,  -30,   -60, -30,   -60,  -30,  -60,  -30,  -30,  -60, -30,   -60,  -30,   -60,  -29,   -60,  -28,   -50,  -27,   -50,  -24,  -50, -21,  -50, -18,  -50, -15,  -50, -12,  -50,   -7,  -50,  -3,   -50,   1,   -46,   5,   -46,   5,   -46,   5,   -46,    5,   -46,   5,   -46,   5,   -46,    3,   -46,  0,  -46,  -3,   -46,  -3]
goal_y_3 = [ 52, 51.5,  51,  50.5,   50,  49.5,   49, 48.5,  48,  47.5,   47,  45, 44.5,  44,  43.5,   43,  42.5,   42,  41.5,   41,  40.5,   40,  39.5,   39, 38.5,  38,  37.5, 37, 36.5,  36, 35.5,  35, 34.5, 34, 33.5,  33,  32.5,  32,  31.5,  31,  30.5,  30,  29.5,  29,  28.5,   28,  27.5,  27,  26.5,  26,  25.5,   25,  24.5, 24, 23.5, 23,  22.5, 22]
    #goal_ang_3=[ 3.14, 3.14,   0,  3.14,    0,  3.14,    0,  3.14,    0,  3.14,    0,   a2,  3.14,    0,  3.14,    0,  3.14,    0,  3.14,    0,  3.14,    0, 3.14,   0,  3.14,  0, 3.14,   0, 3.14,   0, 3.14,   0, 3.14,   0,  3.14,   0,  3.14,   0,  3.14,   0,  3.14,   0,  3.14,    0,  3.14,   0,  3.14,   0,  3.14,    0,  3.14,  0, 3.14,  0,  3.14,  0,  3.14,  0]

    #initialize goal positions for cleaning area 4
goal_x_4 = [-35, -35, -36, -36, -37, -37, -38, -38, -39, -39, -40, -40, -41, -41, -42, -42, -43, -43, -44, -44, -45, -45, -46, -46, -47, -47, -50, -47, -51, -47, -56, -47, -58, -47, -60, -47, -62, -47, -64, -47, -65, -47, -66, -52, -67, -56, -68, -60]
goal_y_4 = [ 72,  78,  72,  79,  71,  81,  71,  83,  70,  85,  70,  89,  70,  90,  72,  90,  76,  90,  80,  90,  82,  90,  82,  90,  82,  90,  89,  89,  88,  88,  87,  87,  86,  86,  85,  85,  84,  84,  83,  83,  82,  82,  81,  81,  80,  80,  79,  79  ]
    #goal_ang_4= [a4,   a4,  a2,  a4,  a2,  a4,  a2,  a4,  a2,  a4,  a2,  a4,  a2,  a4,  a2,  a4,  a2,  a4,  a2,  a4,  a2,  a4,  a2,  a4,  a2,  a4,  a3,   0,  a3,   0,  a3,   0,  a3,   0,  a3,   0,  a3,   0,  a3,   0,  a3,   0,  a3,   0,  a3,   0,  a3,   0] 

    #initialize goal positions for cleaning area 5
goal_x_5 = [-14, -2,  -2, -14, -1, -1, -14,  1,  6, -14, 11, 30, -14, 30, 30, -15, 30, 30, -15, 30, 30, -15,  30, 30,  -6, 30, 30,   4, 30, 30,  14, 30, 29, 24,  29]
goal_y_5 = [ 54, 54,  53,  52, 52, 51,  50, 50, 49,  48, 48, 47,  46, 46, 45, 44,  44, 43, 42,  42, 41,  40,  40, 39,  38, 38, 37,  36, 36, 35,  34, 34, 33,  32, 32]
    #goal_ang_5=[ 0,   0,  a2, 3.1,  0, a2, 3.1,  0, a2, 3.1,  0, a2, 3.1,  0, a2, 3.1,  0, a2, 3.1,  0, a2, 3.1,   0, a2, 3.1,  0, a2, 3.1,  0, a2, 3.1,  0, a2, 3.1,  0]

    #initialize goal positions for cleaning area 6
goal_x_6 = [ 5,  10,    5, 15,  5,  20,  5,  25,  5, 56,  5, 55,  5, 55,  10,  54,  15, 54,   25, 53,   27, 53,   27,   52,   27,   52,  27,   51,   27,   50, 31,  47,  31,   44,  31,   41,    31,    38,    31,   38,   31,   38,    31,   38,    31,   38,    31,   38,   31,    38]
goal_y_6 = [31, 31,  30, 30, 29, 29, 28, 28, 27, 27, 26, 26, 25, 25,  24,  24,  23,  23,  22,  22,   21, 21,  20,  20, 19.5,   19, 18.5,  18, 17.5,   17, 16.5, 16, 15.5,  15, 14.5,  14, 13.5,    13,  12.5,    12, 11.5,   11, 10.5,    10,  9.5,     9,  8.5,     8,  7.5,    7]
    #goal_ang_6=[0, 0, 3.14, 0, 3.14, 0, 3.14, 0, 3.14, 0, 3.14, 0, 3.14,  0, 3.14, 0, 3.14, 0, 3.14, 0, 3.14, 0, 3.14,0, 3.14,    0, 3.14,   0, 3.14,    0, 3.14,  0, 3.14,   0, 3.14,   0, 3.14,    0,  3.14,     0,  3.14,    0, 3.14,    0,  3.14,    0,  3.14,    0,  3.14,    0]


    #initialize goal positions for cleaning area 7
goal_x_7 = [  50,   62,  50.3,  62.3,  50.6,  62.6,   51,   63, 51.3, 63.3 , 51.6, 63.6,   52,    64,  52.3,  64.3,  52.6,  64.6,   53,   65, 53.3, 65.3, 53.6,  65.6,  54,   66, 54.3,  66.3, 54.6,  66.6,   55,   67, 55.3, 67.3, 55.6, 67.6,  56,   68,  56.3,  68.3, 56.6,  68.6,  57,   69, 57.3,  69.3,  57.6,  69.6,   58,   70, 58.3, 70.3, 58.6, 70.6,  59,   71,  59.3, 71.3, 59.6, 71.6,  60,   72, 60.3,  72.3, 60.6, 72.6,   61,   73, 61.3,  73.3, 61.6, 73.6,   62,   74, 62.3,  74.3,  62.6,  74.6,  62,   50]
goal_y_7 = [  52,   48,    53,    49,    54,    50,   55,   51,   56,    52,   57,   53,   58,    54,    59,    55,    60,    56,   61,   57,   62,   58,   63,    59,  64,   60,   65,    61,   66,    62,   67,   63,   68,   64,   69,   65,  70,   66,    71,    67,   72,    68,  73,   69,   74,    70,    75,    71,   76,   72,   77,   73,   78,   74,  79,   75,    80,   76,   81,   77,  82,   78,   83,    79,   84,   80,   85,   81,   86,    82,   87,   83,   88,   84,   89,    85,    90,    86,  48,   52]
    #goal_ang_7=[-0.5, -0.5,   2.6,  -0.5,   2.6,  -0.5,  2.6, -0.5,  2.6,  -0.5,  2.6, -0.5,  2.6,  -0.5,   2.6,  -0.5,   2.6,  -0.5,  2.6, -0.5,  2.6, -0.5,  2.6,  -0.5, 2.6, -0.5,  2.6,  -0.5,  2.6,  -0.5,  2.6, -0.5,  2.6, -0.5,  2.6, -0.5, 2.6, -0.5,   2.6,  -0.5,  2.6,  -0.5, 2.6, -0.5,  2.6,  -0.5,   2.6,  -0.5,  2.6, -0.5,  2.6, -0.5,  2.6, -0.5, 2.6, -0.5,   2.6, -0.5,  2.6, -0.5, 2.6, -0.5,  2.6,  -0.5,  2.6, -0.5,  2.6, -0.5,  2.6,  -0.5,  2.6, -0.5,  2.6, -0.5,  2.6,  -0.5,   2.6,  -0.5, 1.0, -0.5]
    


goal_11=pd.DataFrame(
    [goal_x_1,goal_y_1]
)

goal_12=pd.DataFrame(
    [goal_x_2,goal_y_2]
)
goal_13=pd.DataFrame(
    [goal_x_3,goal_y_3]
)
goal_14=pd.DataFrame(
    [goal_x_4,goal_y_4]
)
goal_15=pd.DataFrame(
    [goal_x_5,goal_y_5]
)
goal_16=pd.DataFrame(
    [goal_x_6,goal_y_6]
)
goal_17=pd.DataFrame(
    [goal_x_7,goal_y_7]
)
#goal_18=pd.DataFrame(
#    [goal_x_8,goal_y_8]
#)
#goal_19=pd.DataFrame(
#    [goal_x_9,goal_y_9]
#)
goal_11=goal_11.T
goal_12=goal_12.T
goal_13=goal_13.T
goal_14=goal_14.T
goal_15=goal_15.T
goal_16=goal_16.T
goal_17=goal_17.T
#goal_18=goal_18.T
#goal_19=goal_19.T
goal_11.columns=['x','y']
goal_12.columns=['x','y']
goal_13.columns=['x','y']
goal_14.columns=['x','y']
goal_15.columns=['x','y']
goal_16.columns=['x','y']
goal_17.columns=['x','y']
#goal_19.columns=['x','y']
#st.write(goal_11)
# ----------------------------




# read ---------------
# position
#tgt_csv0 = path+"amcl.csv"
tgt_csv0 = st.file_uploader("amclファイルアップロード", type='csv')
tmp_df = pd.read_csv(tgt_csv0)
pposition_x = tmp_df["field.pose.pose.position.x"]
pposition_y = tmp_df["field.pose.pose.position.y"]
tmp_ros_time = tmp_df["%time"]
position_time = pd.to_datetime(tmp_ros_time)
position_time = position_time.dt.tz_localize('UTC').dt.tz_convert('Asia/Tokyo')
position_time = position_time.dt.tz_localize(None)

position_x= pd.DataFrame(
    pposition_x
    #index = tmp_ros_time
)
position_y=pd.DataFrame(
    pposition_y
)
position_x.index = position_time
position_x.index=position_x.index.round('100ms')
#position_x=position_x.resample('100ms').apply(list)
position_y.index = position_time
position_y.index=position_y.index.round('100ms')
#position_y=position_y.resample('100ms').apply(list)



#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#
#
position_time_arr = np.array(position_y.index)
#st.slider('time',position_time_arr[0],position_time_arr[len(position_time_arr)-1],position_time_arr[0])


# 距離計算
cal_l = 0
for i in range(len(pposition_x)-1):
    tmp_l = math.sqrt((pposition_x[i+1]-pposition_x[i])**2 + (pposition_y[i+1]-pposition_y[i])**2)
    cal_l = cal_l+tmp_l
   # if i==len(position_x):
#print(cal_l)

cleanzone = cal_l*0.7
#print(cleanzone)

clean_time = position_time[len(position_time)-1]-position_time[0]
#print(clean_time)
#len(position_x)
st.write('mileage[m]           :',cal_l)
st.write('clean area[m^2]      :',cleanzone)
st.write('cleaning time        :',clean_time)

#----------------------
# weight_max

if (t_swith==1):
    #tgt_csv=path+"weight.csv"
    tgt_csv9 = st.file_uploader("weightファイルアップロード", type='csv')
    tmp_weight = pd.read_csv(tgt_csv9)
    weight = tmp_weight["field.data0"]
    tmpweight_time = tmp_weight["%time"]
    tweight_time = pd.to_datetime(tmpweight_time)
    weight_time = tweight_time.dt.tz_localize('UTC').dt.tz_convert('Asia/Tokyo')
    weight_time = weight_time.dt.tz_localize(None)
    df_weight=pd.DataFrame(weight)
    df_weight.index=weight_time
    df_weight.index=df_weight.index.round('100ms')
    #df_weight_re = df_weight.resample('100ms').apply(list)
    st.line_chart(df_weight)


# read ---------------
# cmd_vel
#tgt_csv = path+"cmdvel.csv"
tgt_csv = st.file_uploader("cmd_velファイルアップロード", type='csv')
cmd_vel = pd.read_csv(tgt_csv)

plinear_x = cmd_vel["field.linear.x"]
pangular_z = cmd_vel["field.angular.z"]
tmp_cmd_time = cmd_vel["%time"]
tcmd_time = pd.to_datetime(tmp_cmd_time)
#cmd_time.dt.tz
cmd_time = tcmd_time.dt.tz_localize('UTC').dt.tz_convert('Asia/Tokyo')
#print(cmd_time)
cmd_time = cmd_time.dt.tz_localize(None)
#cmd_time = cmd_time.dt.strftime('%m%d-%H:%M:%S')
#st.write(cmd_time)
#st.write(cmd_time.dt.tz)
#print(cmd_time)

linear_x=pd.DataFrame(
    plinear_x
)
angular_z=pd.DataFrame(
    pangular_z
)
linear_x.index = cmd_time
linear_x.index=linear_x.index.round('100ms')
#linear_x=linear_x.resample('100ms').apply(list)
angular_z.index=cmd_time
angular_z.index=angular_z.index.round('100ms')
#angular_z=angular_z.resample('100ms').apply(list)
tmp_sss=angular_z.resample('100ms').apply(list)
#st.write(tmp_sss)
#st.write(df_weight_re)
# read ---------------
# Mover , Mover status

#tgt_mcsv = path+'M.csv'
tgt_mcsv = st.file_uploader("Mover(M)ファイルアップロード", type='csv')
tgt_scsv = st.file_uploader("Moverstatus(MS)ファイルアップロード", type='csv')
#tgt_scsv = path+'MS.csv'
mover = pd.read_csv(tgt_mcsv)
moverstatus = pd.read_csv(tgt_scsv)
pmover_R = mover["field.data0"]
pmover_L = mover["field.data1"]
tmp_mover_time = mover["%time"]
tmover_time = pd.to_datetime(tmp_mover_time)
mover_time = tmover_time.dt.tz_localize('UTC').dt.tz_convert('Asia/Tokyo')
mover_time = mover_time.dt.tz_localize(None)



tmp_moverstatus_time = moverstatus["%time"]
tmoverstatus_time = pd.to_datetime(tmp_moverstatus_time)
moverstatus_time = tmoverstatus_time.dt.tz_localize('UTC').dt.tz_convert('Asia/Tokyo')
moverstatus_time = moverstatus_time.dt.tz_localize(None)


pmoverstatus_R = moverstatus["field.data0"]
pmoverstatus_L = moverstatus["field.data1"]
pmoverstatus_buttery = moverstatus["field.data2"]
pmoverstatus_flag = moverstatus["field.data3"]


mover_R = pd.DataFrame(pmover_R)
mover_R.index = mover_time
mover_R.index = mover_R.index.round('100ms')
#mover_R=mover_R.resample('100ms').apply(list)

mover_L = pd.DataFrame(pmover_L)
mover_L.index=mover_time
mover_L.index = mover_L.index.round('100ms')
#mover_L=mover_L.resample('100ms').apply(list)


moverstatus_R = pd.DataFrame(pmoverstatus_R)
moverstatus_R.index = moverstatus_time
moverstatus_R.index = moverstatus_R.index.round('100ms')
#moverstatus_R=moverstatus_R.resample('100ms').apply(list)

moverstatus_L = pd.DataFrame(pmoverstatus_L)
moverstatus_L.index=moverstatus_time
moverstatus_L.index = moverstatus_L.index.round('100ms')
#moverstatus_L=moverstatus_L.resample('100ms').apply(list)

moverstatus_buttery = pd.DataFrame(pmoverstatus_buttery)
moverstatus_buttery.index=moverstatus_time
moverstatus_buttery.index = moverstatus_buttery.index.round('100ms')
#moverstatus_buttery=moverstatus_buttery.resample('100ms').apply(list)

moverstatus_flag = pd.DataFrame(pmoverstatus_flag)
moverstatus_flag.index=moverstatus_time
moverstatus_flag.index = moverstatus_flag.index.round('100ms')
#moverstatus_flag=moverstatus_flag.resample('100ms').apply(list)

#tmp_stime=moverstatus_buttery.index
#idx = tmp_stime.index(moverstatus_buttery.index[0])
#st.write(idx)
# read ---------------
# emg_status
#tgt_csv = path+'emgS.csv'
tgt_csv = st.file_uploader("emgSファイルアップロード", type='csv')
emgS = pd.read_csv(tgt_csv)
pemg_status = emgS["field.data"]
tmp_emg_statustime = emgS["%time"]
temg_statustime = pd.to_datetime(tmp_emg_statustime)
emg_statustime = temg_statustime.dt.tz_localize('UTC').dt.tz_convert('Asia/Tokyo')
emg_statustime=emg_statustime.dt.tz_localize(None)

emg_status = pd.DataFrame(pemg_status)
emg_status.index=emg_statustime
emg_status.index=emg_status.index.round('100ms')
#emg_status=emg_status.resample('100ms').apply(list)

# read ---------------
# sequence_status
#tgt_csv = path+'seqS.csv'

tgt_csv = st.file_uploader("seqSファイルアップロード", type='csv')
seqS = pd.read_csv(tgt_csv)
pseq_status = seqS["field.data0"]
tmp_seq_statustime = seqS["%time"]
tseq_statustime = pd.to_datetime(tmp_seq_statustime)
seq_statustime = tseq_statustime.dt.tz_localize('UTC').dt.tz_convert('Asia/Tokyo')
seq_statustime=seq_statustime.dt.tz_localize(None)

seq_status = pd.DataFrame(pseq_status)
seq_status.index=seq_statustime
seq_status.index=seq_status.index.round('100ms')
#seq_status=seq_status.resample('100ms').apply(list)
# read ---------------
# movebase
#tgt_csv = path+'mb.csv'
tgt_csv = st.file_uploader("movebaseファイルアップロード", type='csv')
#movebase = pd.read_csv('rog_csv/210628_1_mb.csv', names = ['%time', 'field.header.seq', 'field.header.stamp', 'field.header.frame_id', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n','o','p'])
#movebase = pd.read_csv('log_csv/210628_1_mb.csv',names = ['%time', 'field.header.seq', 'field.header.stamp', 'field.header.frame_id', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n','o','p'])
movebase = pd.read_csv(tgt_csv,header=None,names = ['%time', 'b', 'c', 'flag', 'e', 'f', 'g', 'h','i'],skiprows=1)
pmovebase_flag = movebase["flag"]
tmp_movebase_time = movebase["%time"]
movebase_time = pd.to_datetime(tmp_movebase_time)
movebase_time = movebase_time.dt.tz_localize('UTC').dt.tz_convert('Asia/Tokyo')
movebase_time=movebase_time.dt.tz_localize(None)
movebase_flag=pd.DataFrame(pmovebase_flag)
movebase_flag.index=movebase_time
movebase_flag.index=movebase_flag.index.round('100ms')
#movebase_flag=movebase_flag.resample('100ms').apply(list)




# --------------------------------------------------------------
# PLOT
# 
# --------------------------------------------------------------
#tmp = st.slider('時間',cmd_time[0],cmd_time[len(cmd_time)-1],cmd_time[0],format="MM/DD/YY-hh:mm:ss")


#-----------------
# position(time)
OFF_x=649
OFF_y=816
OFF_d=7.2
slider = st.slider("指定時間",0,len(position_x)-1)
#slider2 = st.slider("time",)
st.write(position_x.index[slider])
#st.write(position_x)
#st.write(len(position_x))
fig1 = plt.figure(figsize=(8*5, 6*5))
#fig.patch.set_facecolor('white')
ax1 = fig1.add_subplot(1, 1, 1)
map_file = st.file_uploader("マップファイルアップロード", type='png')
im = Image.open(map_file)
ax1.imshow(im, alpha=0.6)
plt.xticks([0, OFF_d*50, OFF_d*100, OFF_d*150], ["0", "50", "100", "150"])
plt.yticks([0, OFF_d*50, OFF_d*100,], ["0", "50", "100"])
#ax1.scatter(position_x*5.5+409,position_y*(-5.5)+505,color="black",s=40)
#ax1.scatter(pposition_x[slider]*5.5+409,pposition_y[slider]*(-5.5)+505,color="red",s=400)

ax1.scatter(position_x*OFF_d+OFF_x,position_y*(-OFF_d)+OFF_y,color="black",s=20)
ax1.scatter(pposition_x[slider]*OFF_d+OFF_x,pposition_y[slider]*(-OFF_d)+OFF_y,color="red",s=400)
plt.plot(goal_11.x*OFF_d+OFF_x,goal_11.y*(-OFF_d)+OFF_y)
plt.plot(goal_12.x*OFF_d+OFF_x,goal_12.y*(-OFF_d)+OFF_y)
plt.plot(goal_13.x*OFF_d+OFF_x,goal_13.y*(-OFF_d)+OFF_y)
plt.plot(goal_14.x*OFF_d+OFF_x,goal_14.y*(-OFF_d)+OFF_y)
plt.plot(goal_15.x*OFF_d+OFF_x,goal_15.y*(-OFF_d)+OFF_y)
plt.plot(goal_16.x*OFF_d+OFF_x,goal_16.y*(-OFF_d)+OFF_y)
plt.plot(goal_17.x*OFF_d+OFF_x,goal_17.y*(-OFF_d)+OFF_y)



#plt.plot(goal_11.x*5.5+409,goal_11.y*(-5.5)+505)
#plt.plot(goal_12.x*5.5+409,goal_12.y*(-5.5)+505)
#plt.plot(goal_13.x*5.5+409,goal_13.y*(-5.5)+505)
#plt.plot(goal_14.x*5.5+409,goal_14.y*(-5.5)+505)
#plt.plot(goal_15.x*5.5+409,goal_15.y*(-5.5)+505)
#plt.plot(goal_16.x*5.5+409,goal_16.y*(-5.5)+505)
#plt.plot(goal_17.x*5.5+409,goal_17.y*(-5.5)+505)
#plt.plot(goal_18.x*5.5+409,goal_18.y*(-5.5)+505)
#plt.plot(goal_19.x*5.5+409,goal_19.y*(-5.5)+505)
#ax2.scatter(11,10,color="red",s=40)
fig1.suptitle("trace")
plt.rcParams["font.size"] = f_size
st.pyplot(fig1)


# --------------------------------------------------------------
# idx find << slider
position_time_arr = np.array(position_y.index)
tgt_time = position_time_arr[slider]


#-----------------
#cmd_vel_plot
#-----------------
fig3 = plt.figure(figsize=(8*4, 6*4))
ax3 = fig3.add_subplot(1, 1, 1)
plt.scatter(cmd_time,linear_x,label="linear_x")
plt.scatter(cmd_time,angular_z,label="zngular_z")
#ax2.scatter(cmd_time)
plt.xlabel("TIME")
plt.ylabel("IN")



chart_data = pd.DataFrame(
    [plinear_x,pangular_z]
)
chart_data = chart_data.T
chart_data.index = cmd_time
chart_data.index = chart_data.index.round('100ms')
#chart_data.resample('100ms').apply(list)
#st.write(chart_data)
#st.line_chart(chart_data)
tmp_time = np.array(chart_data.index)
tgt_idx = np.argwhere((tmp_time <= tgt_time+range_time)&(tmp_time > tgt_time-range_time))
#st.write(tgt_idx)
tgt_idx2=tgt_idx.reshape(len(tgt_idx),)
#st.line_chart(chart_data.iloc[tgt_idx2])
#ax3.scatter(chart_data[tgt_idx2])
#plt.plot(chart_data.iloc[tgt_idx2], linewidth=15,label=['time_x','time_z'])
plt.scatter(chart_data.index[tgt_idx2],chart_data['field.linear.x'].iloc[tgt_idx2],color="red",s=400)
plt.scatter(chart_data.index[tgt_idx2],chart_data['field.angular.z'].iloc[tgt_idx2],color="blue",s=400)
#fig0=plt.plot(chart_data.iloc[tgt_idx2])
#st.pyplot(fig0)
plt.legend()
fig3.suptitle("cmd_vel")
plt.rcParams["font.size"] = f_size
st.pyplot(fig3)

#st.line_chart(chart_data)
#st.line_chart(chart_data.iloc[:,0],chart_data.iloc[:,2])

#---------------------------------------------
fig4 = plt.figure(figsize=(8*4, 6*4))
ax4 = fig4.add_subplot(1, 1, 1)
plt.scatter(mover_time,mover_R,label="mover_R")
plt.scatter(moverstatus_time,moverstatus_R,label="moverstatus_R")


#st.pyplot(fig4)

#chart_mover_R = pd.DataFrame(
#    mover_R,
#    index=mover_time
#)
#chart_moversts_R = pd.DataFrame(
##    moverstatus_R,
#    index=moverstatus_time
#)
#mover_R.index = mover_time
#mover_L.index = mover_time
#moverstatus_L.index=moverstatus_time
#moverstatus_R.index=moverstatus_time



#st.line_chart(mover_R)
#st.line_chart(moverstatus_R)
#st.line_chart(mover_L)
#st.line_chart(moverstatus_L)
tmp_time2 = np.array(mover_R.index)
tgt_idx22 = np.argwhere((tmp_time2 <= tgt_time+range_time)&(tmp_time2 > tgt_time-range_time))
#st.write(tgt_idx)
tgt_idx32=tgt_idx22.reshape(len(tgt_idx22),)
#st.line_chart(mover_R.iloc[tgt_idx32])
#st.line_chart(mover_L.iloc[tgt_idx32])

tmp_time3 = np.array(moverstatus_R.index)
tgt_idx23 = np.argwhere((tmp_time3 <= tgt_time+range_time)&(tmp_time3 > tgt_time-range_time))
tgt_idx33 =tgt_idx23.reshape(len(tgt_idx23),)
#st.line_chart(moverstatus_R.iloc[tgt_idx33])
#st.line_chart(moverstatus_L.iloc[tgt_idx33])
#st.line_chart(moverstatus_buttery.iloc[tgt_idx33])
#st.line_chart(moverstatus_flag.iloc[tgt_idx33])
#plt.plot(mover_R.iloc[tgt_idx32], linewidth=15,label='time_R')
#plt.plot(moverstatus_R.iloc[tgt_idx33], linewidth=15,label='time_statusR')

plt.scatter(mover_R.index[tgt_idx32],mover_R['field.data0'].iloc[tgt_idx32],color="red",s=400)
plt.scatter(moverstatus_R.index[tgt_idx33],moverstatus_R['field.data0'].iloc[tgt_idx33],color="blue",s=400)
plt.legend()
plt.ylabel("IN")
plt.yticks([2000,3000,4000,5000,6000,7000,8000], ["-2000", "-1000", "0","1000","2000","3000","4000"])
#plt.yticks([0, 55.5*5, 55.5*10,], ["0", "50", "100"])
fig4.suptitle("mover_R")
plt.rcParams["font.size"] = f_size
st.pyplot(fig4)


#tmp_time0=np.array(df_weight.index)

#st.line_chart(moverstatus_buttery)
#st.line_chart(moverstatus_flag)

#tmp_time = np.array(mover_R.index)
#tgt_idx = np.argwhere((tmp_time <= tgt_time+range_time)&(tmp_time > tgt_time-range_time))
#st.altair_chart(mover_R[tgt_idx])
#st.altair_chart(mover_L[tgt_idx])

#-----------------
#mover_L_plot
#-----------------

fig5 = plt.figure(figsize=(8*4, 6*4))
ax5 = fig5.add_subplot(1, 1, 1)
plt.scatter(mover_time, mover_L, label="mover_L")
plt.scatter(moverstatus_time, moverstatus_L, label="moverstatus_L")


#plt.plot(mover_L.iloc[tgt_idx32],linewidth=15,label='time_L')
#plt.plot(moverstatus_L.iloc[tgt_idx33],linewidth=15,label='time_statusL')

plt.scatter(mover_L.index[tgt_idx32],mover_L['field.data1'].iloc[tgt_idx32],color="red",s=400)
plt.scatter(moverstatus_L.index[tgt_idx33],moverstatus_L['field.data1'].iloc[tgt_idx33],color="blue",s=400)

plt.legend()
plt.xlabel("TIME")
plt.ylabel("IN")
plt.yticks([2000,3000,4000,5000,6000,7000,8000], ["-2000", "-1000", "0","1000","2000","3000","4000"])
#plt.yticks([0,1000,2000,3000,4000,5000,6000,7000,8000,9000], ["-4000", "-3000", "-2000", "-1000", "0","1000","2000","3000","4000","5000"])
fig5.suptitle("mover_L")
plt.rcParams["font.size"] = f_size
st.pyplot(fig5)


#-----------------
#mover_buttery_plot
#-----------------

fig7 = plt.figure(figsize=(8*4, 6*4))
ax7 = fig7.add_subplot(1, 1, 1)
plt.scatter(moverstatus_time,moverstatus_buttery,label="mover_buttery")

plt.xlabel("TIME")
plt.ylabel("buttery[%]")
plt.yticks([0,50,100,105], ["0", "50", "100", ""])
fig7.suptitle("mover_buttery")
#plt.plot(moverstatus_buttery.iloc[tgt_idx33],linewidth=15,label='slider')
plt.scatter(moverstatus_buttery.index[tgt_idx33],moverstatus_buttery['field.data2'].iloc[tgt_idx33],color="red",s=400)

plt.rcParams["font.size"] = f_size
plt.legend()
st.pyplot(fig7)

#moverstatus_buttery.index = moverstatus_time
#moverstatus_flag.index=moverstatus_time

#-----------------
#moverstatus_flag_plot
#-----------------


fig8 = plt.figure(figsize=(8*4, 6*4))
ax8 = fig8.add_subplot(1, 1, 1)
plt.scatter(moverstatus_time,moverstatus_flag,label="moverstatus_flag")

plt.yticks([0,1], ["normal", "motor_err"])
plt.xlabel("TIME")
plt.ylabel("flag")
fig8.suptitle("moverstatus_flag")
#plt.plot(moverstatus_flag.iloc[tgt_idx33],linewidth=15,label='slider')
plt.scatter(moverstatus_flag.index[tgt_idx33],moverstatus_flag['field.data3'].iloc[tgt_idx33],color="red",s=400)
plt.rcParams["font.size"] = f_size
plt.legend()
st.pyplot(fig8)

#-----------------
#emergency_status_plot
#-----------------

fig9 = plt.figure(figsize=(8*4, 6*4))
plt.scatter(emg_statustime,emg_status,label="emg_status")

plt.xlabel("TIME")
plt.ylabel("emg_status")
#plt.yticks([0,1,2,3], ["normal", "mojiden_err", "zig_err", "emg_STOP"])
plt.yticks([0,1,2,3],["normal","mojiden","zick","emergency_button"])
plt.ylim(-0.2,3.2)
fig9.suptitle("emergency_status")


#emg_status.index=emg_statustime
#st.line_chart(emg_status)
tmp_time4 = np.array(emg_status.index)
tgt_idx24 = np.argwhere((tmp_time4 <= tgt_time+range_time)&(tmp_time4 > tgt_time-range_time))
tgt_idx34 =tgt_idx24.reshape(len(tgt_idx24),)
#plt.plot(emg_status.iloc[tgt_idx34],linewidth=15, label='slider')
plt.scatter(emg_status.index[tgt_idx34],emg_status['field.data'].iloc[tgt_idx34],color="red",s=400)
plt.legend()
plt.rcParams["font.size"] = f_size
st.pyplot(fig9)
#-----------------
#sequence_status_plot
#-----------------
''' sequence_status means:
    data[0] = 10: manual cleaning
    data[0] = 11: cleaning sequence area 1
    data[0] = 12: cleaning sequence area 2
    data[0] = 13: cleaning sequence area 3
    data[0] = 14: cleaning sequence area 4
    data[0] = 15: cleaning sequence area 5
    data[0] = 21: carrying to A
    data[0] = 22: carrying to B
    data[0] = 3:  goal arrived
    data[0] = 33: all goal arrived
    data[0] = 44: emergency stop
    data[0] = 55: bluetooth connection dead
    data[0] = 9:  cancel goal
    data[0] = 50: initial value
    data[0] = 99: goal is not published
'''


fig10 = plt.figure(figsize=(8*6, 6*6))
plt.scatter(seq_statustime,seq_status,label="seq_status")
plt.legend()
plt.xlabel("TIME")
plt.ylabel("seq_status")
plt.yticks([0,3,9,10,11,12,13,14,15,21,22,33,44,50,55,60], ["","goal_arrived", "cancel_goal", "manual cleaning", "area1","area2","area3","area4","area5","carrying toA","carrying toB","all goal arived","emgstop","initial value", "bluetooth connection dead",""])
plt.ylim(0,60)
fig10.suptitle("sequence_status")


#seq_status.index = seq_statustime
#st.line_chart(seq_status)

tmp_time5 = np.array(seq_status.index)
tgt_idx25 = np.argwhere((tmp_time5 <= tgt_time+range_time)&(tmp_time5 > tgt_time-range_time))
tgt_idx35 =tgt_idx25.reshape(len(tgt_idx25),)
#plt.plot(seq_status.iloc[tgt_idx35],linewidth=15,label='slider')
plt.scatter(seq_status.index[tgt_idx35],seq_status['field.data0'].iloc[tgt_idx35],color="red",s=400)
plt.rcParams["font.size"] = f_size
st.pyplot(fig10)
"""

for i in range(len(emg_status)-1):
    if (emg_status[i]==0):
        emg_status[i]="pending"
        
    elif (emg_status[i]==1):
        emg_status[i]="run"
    elif (emg_status[i]==2):
        emg_status[i]="preempted"
    elif (emg_status[i]==3):
        emg_status[i]="goal"
    elif (emg_status[i]==4):
        emg_status[i]="aborted"
    elif (emg_status[i]==5):
        emg_status[i]="rejected"
    elif (emg_status[i]==6):
        emg_status[i]="preempting"
    elif (emg_status[i]==7):
        emg_status[i]="recalling"
    elif (emg_status[i]==8):
        emg_status[i]="recalled"
    elif (emg_status[i]==9):
        emg_status[i]="lost"

"""

#st.line_chart.
#-----------------
#movebase_flag_plot
#-----------------

fig11 = plt.figure(figsize=(8*4, 6*4))
plt.scatter(movebase_time,movebase_flag,label="movebase_flag")
plt.legend()
plt.xlabel("TIME")
plt.ylabel("flag")
plt.yticks([0,1,2,3,4,5,6,7,8,9], ["pending", "run", "preempted", "goal","aborted","rejected","preempting", "recalling", "recalled", "lost"])
fig11.suptitle("movebase_flag")


#movebase_flag.index = movebase_time
#st.line_chart(movebase_flag)

tmp_time6 = np.array(movebase_flag.index)
tgt_idx26 = np.argwhere((tmp_time6 <= tgt_time+range_time)&(tmp_time6 > tgt_time-range_time))
tgt_idx36 =tgt_idx26.reshape(len(tgt_idx26),)
#plt.plot(emg_status.iloc[tgt_idx36],linewidth=15,label='slider')
#plt.scatter(mover_R.index[tgt_idx2],mover_R['field.data.0'].iloc[tgt_idx2],color="red",s=400)
plt.scatter(movebase_flag.index[tgt_idx36],movebase_flag['flag'].iloc[tgt_idx36],color="red",s=400)


plt.legend()
plt.rcParams["font.size"] = f_size
st.pyplot(fig11)
#######################
# test

