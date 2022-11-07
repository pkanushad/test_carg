from tkinter import *
import tkinter.ttk as ttk
global futures
import sqlite3
import pandas as pd
import numpy as np
import sys
import os
from PIL import Image, ImageFont
import PIL
from PIL import ImageTk
from PIL import Image
import calendar
from datetime import timedelta 
from functools import reduce
from tkinter import messagebox
from datetime import datetime
from datetime import date


#*********************root***************************************************************************#
root = Tk()
root.title("Physical Blotter")
f=font=('Times', 12)
f1=font=('Times', 5)
root.config(bg='white')
# root.geometry("2000x2050")
root.geometry("1540x800+0+0")


#*********************db connection***************************************************************************#
my_conn = sqlite3.connect('trading_derivative_db.db')
cursor = my_conn.cursor()


#***********DATE**********************#
today = date.today()
current_date=StringVar()
today=today.strftime("%d-%b-%y")
date_variable=today
current_date.set(date_variable)

#*****************Trader*******************************************************************************************#
   
Trader=()
cursor.execute("SELECT * FROM TRADE")
Trader_select = cursor.fetchall()
for x in Trader_select:
    Trader+=tuple(x)

    
    
    
#*********Book*********************     
book=()
cursor.execute("SELECT * FROM BOOK")
book_select = cursor.fetchall()
for x in book_select:
    book+=tuple(x)
    
counter_party_val=()
cursor.execute("SELECT * FROM COUNTER_PARTY")
counter_party_select = cursor.fetchall()
for x in counter_party_select:
    counter_party_val+=tuple(x)



#*********strategy*********************     
strategy=()
cursor.execute("SELECT * FROM STRATEGY")        
strat_select = cursor.fetchall()
for x in strat_select:
    strategy+=tuple(x)
    print(strategy)
    
#*********derivative********************* 


derivative_var=StringVar()
derivative=('Physical')
derivative_var.set(derivative)

pricing=()
swaps_contract=()
cursor.execute("SELECT Contract FROM SWAPS_CONTRACT")
swaps_select = cursor.fetchall()
for x in swaps_select:
    swaps_contract+=tuple(x)
        


futures_contract=()
cursor.execute("SELECT Futures_contract FROM FUTURES_CONTRACT")
futures_select = cursor.fetchall()
for x in futures_select:
    futures_contract+=tuple(x)
pricing=futures_contract+swaps_contract
print(pricing)


product=()
cursor.execute("SELECT Product FROM PHYSICAL_PRODUCT")
product_select = cursor.fetchall()
for x in product_select:
    product+=tuple(x)

pricing_term_value=()
cursor.execute("SELECT Pricing_Term FROM PRICING_TERM")
pricing_term_select = cursor.fetchall()
for x in pricing_term_select:
    pricing_term_value+=tuple(x)


holiday_set=()
holiday_data = pd.read_sql('SELECT * FROM HOLIDAY_SETTINGS', my_conn)
holiday_set=holiday_data['Holiday_type'].unique().tolist()
holiday_set.append('No Holiday')
# holiday_select = cursor.fetchall()
# for x in holiday_data['Holiday_type']:
#     holiday_set+=tuple(x)

Tank_Ports=()
cursor.execute("SELECT DISTINCT  Port FROM TANK_CAPACITY")
Ports_select = cursor.fetchall()
for x in Ports_select:
    Tank_Ports+=tuple(x)

Ports=()
cursor.execute("SELECT DISTINCT  Port FROM PORT")
Ports_select = cursor.fetchall()
for x in Ports_select:
    Ports+=tuple(x)


physical_purchase_data = pd.read_sql_query('SELECT * FROM PHYSICAL_BLOTTER ' , my_conn)

physical_purchase_data['Shore_Received'] = pd.to_numeric(physical_purchase_data['Shore_Received'])

physical_purchase_data_values=physical_purchase_data.loc[physical_purchase_data['Shore_Received']>0.0]

physical_purchase_contract_value=physical_purchase_data_values['PRICING_CONTRACT'].unique().tolist()


#background image
img =Image.open('position_img.png')
resize_image = img.resize((2000, 2000))
bg = ImageTk.PhotoImage(resize_image)




#************************frames**********************************************************************************#
f1=Frame(root, bg="#646464", width=2000, height=2000)
label1 = Label(f1,image=bg)
label1.image = bg
f1_left_frame = Frame(f1, bd=1, relief=SOLID, padx=1, pady=1,background="white")
# f1_right_frame = Frame(f1, bd=1, relief=SOLID, padx=10, pady=30)



f2=Frame(root, bg="#646464", width=2000, height=2000)
label2 = Label(f2,image=bg)
label2.image = bg

f2_frame=Frame(f2, bd=1, relief=SOLID, padx=10, pady=10)
f2_right=Frame(f2, bd=1, relief=SOLID, padx=10, pady=1)


f3=Frame(root, bg="#646464", width=2000, height=2000)
label3 = Label(f3,image=bg)
label3.image = bg

f4=Frame(root, bg="#646464", width=2000, height=2000)
label4 = Label(f4,image=bg)
label4.image = bg

f5=Frame(root, bg="#646464", width=2000, height=2000)
label5 = Label(f5,image=bg)
label5.image = bg


def bill_shore_raise_frame(frame):
    frame.tkraise()

def refresh():
    root.destroy()
    os.system('python Physical__blotters.py')
    


def raise_frame(frame):
    frame.tkraise()
    physical_data = pd.read_sql('SELECT * FROM PHYSICAL_BLOTTER', my_conn)
#     physical_data= physical_data[physical_data['DATE']== date_variable]
    physical_data=physical_data.drop(['kgal','kl','kcbm'], axis=1)
    print('+++',physical_data)


    my_conn.commit()

    df_rows = physical_data.to_numpy().tolist() 

    for item in physical_tree.get_children():
        physical_tree.delete(item)


    for index in range(len(df_rows)):
        if index %2==0:
            physical_tree.insert("",'end',values=df_rows[index],tags=('even'))
        else:
            physical_tree.insert("",'end',values=df_rows[index],tags=('odd'))
            
    today_btn.config(background= 'slategray', foreground= 'white')
    yest_btn.config(bg='#388087', foreground= "white")
    month_btn.config(background= '#388087', foreground= 'white')
    six_month_btn.config(background= '#388087', foreground= 'white')
    year_btn.config(background= '#388087', foreground= 'white')
    show_all_btn.config(background= '#388087', foreground= 'white')

def homeCallBack():
    root.destroy()
    os.system('python index_page.py')
    
    
    
def load_data(name):
    import datetime
    print(name)
    today = date.today()
    print(today)
    curr_month=today.month
    curr_year=today.year
    offset = max(1, (today.weekday() + 6) % 7 - 3)
    timedelta = datetime.timedelta(offset)
    most_recent = today - timedelta
    yesterday=most_recent.strftime("%d-%b-%y")
    print(yesterday)

    my_conn = sqlite3.connect('trading_derivative_db.db')
    cursor = my_conn.cursor()
    load_data = pd.read_sql('SELECT * FROM PHYSICAL_BLOTTER', my_conn)
    load_data=physical_data.drop(['kgal','kl','kcbm'], axis=1)


    if name =='Today':

        today_data= load_data[load_data['DATE']== date_variable]
        df_rows = today_data.to_numpy().tolist()
        
        today_btn.config(background= 'slategray', foreground= 'white')
        yest_btn.config(bg='#388087', foreground= "white")
        month_btn.config(background= '#388087', foreground= 'white')
        six_month_btn.config(background= '#388087', foreground= 'white')
        year_btn.config(background= '#388087', foreground= 'white')
        show_all_btn.config(background= '#388087', foreground= 'white')
        
        

        

    if name=='Yesterday':
        yesterday_data= load_data[load_data['DATE']== yesterday]
        df_rows = yesterday_data.to_numpy().tolist() 
        
        yest_btn.config(bg='slategray', foreground= "white")
        today_btn.config(background= '#388087', foreground= 'white')
        month_btn.config(background= '#388087', foreground= 'white')
        six_month_btn.config(background= '#388087', foreground= 'white')
        year_btn.config(background= '#388087', foreground= 'white')
        show_all_btn.config(background= '#388087', foreground= 'white')
  
        print(df_rows)
    if name=='Month':
        load_data['Month'] = pd.DatetimeIndex(load_data['DATE']).month
        load_data['Year'] = pd.DatetimeIndex(load_data['DATE']).year

        month_data= load_data[(load_data['Month']== curr_month) & (load_data['Year']== curr_year)]
        df_rows =  month_data.to_numpy().tolist() 
        
        month_btn.config(background= 'slategray', foreground= 'white')
        today_btn.config(background= '#388087', foreground= 'white')
        yest_btn.config(bg='#388087', foreground= "white")
        six_month_btn.config(background= '#388087', foreground= 'white')
        year_btn.config(background= '#388087', foreground= 'white')
        show_all_btn.config(background= '#388087', foreground= 'white')

        
        
    if name=='Year':
        load_data['Year'] = pd.DatetimeIndex(load_data['DATE']).year

        year_data=load_data[(load_data['Year']== curr_year)]
        df_rows =  year_data.to_numpy().tolist() 
        
        year_btn.config(background= 'slategray', foreground= 'white')
        month_btn.config(background= '#388087', foreground= 'white')
        today_btn.config(background= '#388087', foreground= 'white')
        yest_btn.config(bg='#388087', foreground= "white")
        six_month_btn.config(background= '#388087', foreground= 'white')
        show_all_btn.config(background= '#388087', foreground= 'white')

        
    if name=='Show All':
        df_rows =  load_data.to_numpy().tolist() 
        
        show_all_btn.config(background= 'slategray', foreground= 'white')

        year_btn.config(background= '#388087', foreground= 'white')
        month_btn.config(background= '#388087', foreground= 'white')
        today_btn.config(background= '#388087', foreground= 'white')
        yest_btn.config(bg='#388087', foreground= "white")
        six_month_btn.config(background= '#388087', foreground= 'white')
        
        
        
    for item in physical_tree.get_children():
        physical_tree.delete(item)


    for index in range(len(df_rows)):
        if index %2==0:
            physical_tree.insert("",'end',values=df_rows[index],tags=('even'))
        else:
            physical_tree.insert("",'end',values=df_rows[index],tags=('odd'))



def source_tank_qty_check(source_ld_df,m3_list_st,MT_list_st):
    
    if len(source_ld_df)>0:
        
        for index, row in source_ld_df.iterrows():

            if row['Source_Unit']=='m³':
                
                m3_list_st.append(row['Source_cargo_LD_QTY'])
                
                if float(row['Dest_Tank_Density']) < 1:
                    
                    con_m3_to_mt=float(row['Source_cargo_LD_QTY'])* float(row['Dest_Tank_Density'])
                    MT_list_st.append(con_m3_to_mt)
                
                else:
                    con_m3_to_mt=float(row['Source_cargo_LD_QTY'])* (float(row['Dest_Tank_Density'])/1000)
                    MT_list_st.append(con_m3_to_mt)
                    
            
            elif row['Source_Unit']=='MT':
                
                MT_list_st.append(row['Source_cargo_LD_QTY'])
                
                if float(row['Dest_Tank_Density']) < 1:
                    
                    con_MT_to_m3=float(row['Source_cargo_LD_QTY'])/float(row['Dest_Tank_Density'])
                    m3_list_st.append(con_MT_to_m3)
                    
                else:
                    
                    con_MT_to_m3=float(row['Source_cargo_LD_QTY'])/(float(row['Dest_Tank_Density'])/1000)
                    m3_list_st.append(con_MT_to_m3)
                    
            
            print('source mt list',MT_list_st)
            print('source m3 list',m3_list_st)
            sum_m3_list=sum(m3_list_st)
            sum_MT_list=sum(MT_list_st)
            print('source')
            print('m3 list',sum_m3_list,'mt list',sum_MT_list)
            
    else:
        sum_m3_list=0
        sum_MT_list=0

    return sum_m3_list,sum_MT_list
        
def dest_tank_qty_check(dest_ld_df,m3_list_dt,MT_list_dt):
       
    if len(dest_ld_df)>0:

        for index, row in dest_ld_df.iterrows():
            
            if row['Dest_Unit']=='m³':
                
                m3_list_dt.append(row['Dest_Cargo_LD_Qty'] )
                
                if float(row['Dest_Tank_Density']) < 1:
                    
                    con_m3_to_mt=float(row['Dest_Cargo_LD_Qty'])* float(row['Dest_Tank_Density'])
                    MT_list_dt.append(con_m3_to_mt)
                
                else:
                    con_m3_to_mt=float(row['Dest_Cargo_LD_Qty'])* (float(row['Dest_Tank_Density'])/1000)
                    MT_list_dt.append(con_m3_to_mt)
                    
            
            elif row['Dest_Unit']=='MT':
                
                MT_list_dt.append(row['Dest_Cargo_LD_Qty'])
                
                if float(row['Dest_Tank_Density']) < 1:
                    
                    con_MT_to_m3=float(row['Dest_Cargo_LD_Qty'])/float(row['Dest_Tank_Density'])
                    m3_list_dt.append(con_MT_to_m3)
                    
                else:
                    
                    con_MT_to_m3=float(row['Dest_Cargo_LD_Qty'])/(float(row['Dest_Tank_Density'])/1000)
                    m3_list_dt.append(con_MT_to_m3)
                    
            
            print('dest mt list',MT_list_dt)
            print('dest m3 list',m3_list_dt)
            
            sum_m3_list_dt=sum(m3_list_dt)
            sum_MT_list_dt=sum(MT_list_dt)
            print('destination')
          
            print(sum_m3_list_dt,sum_MT_list_dt)
            
    else:
        sum_m3_list_dt=0
        sum_MT_list_dt=0

    return sum_m3_list_dt,sum_MT_list_dt
        






def tank_update(shore_port_value,shore_terminal_value,bill_tank_name_value,shore_product_value):
    
    m3_list_st=[]
    MT_list_st=[]
    
    m3_list_dt=[]
    MT_list_dt=[]
 
    
    if bill_shore_mode_entry.get().strip()=='Tank':
        print(shore_port_value,shore_terminal_value,bill_tank_name_value,shore_product_value)
    
        dest_tank_physical_df= pd.read_sql_query('SELECT * FROM PHYSICAL_BLOTTER WHERE Port = (?) AND Terminal=(?) AND Tank_Number=(?)' , my_conn,params=(shore_port_value,shore_terminal_value,bill_tank_name_value,))
        print('=====',dest_tank_physical_df)
        
        dest_phys_total_vol=dest_tank_physical_df['Shore_Received'].unique().tolist()
        print(dest_phys_total_vol)
        dest_phys_total_vol = [float(x) for x in dest_phys_total_vol]
        
#         dest_phys_total_vol=''. join(map(str,dest_phys_total_vol))
#         dest_phys_total_vol=float(dest_phys_total_vol)
        dest_phys_total_vol=sum(dest_phys_total_vol)
        
        print('dest_phys_total_vol',dest_phys_total_vol,type(dest_phys_total_vol))
        
        
        dest_phys_density=dest_tank_physical_df['Density'].unique().tolist()
        dest_phys_density=dest_phys_density[0]
        density_entry=dest_phys_density

        
        dest_phys_unit=dest_tank_physical_df['UNIT'].unique().tolist()
        dest_phys_unit=''. join(map(str, dest_phys_unit[0]))
        print(dest_phys_unit)
        


        

        
        try:
            if float(density_entry)>1:
                density_value=float(density_entry)/1000
            else:
                density_value=float(density_entry)
        
                print(density_value)
        except:
                messagebox.showerror("error",'Enter numeric value fo Density') 
        
        if (dest_phys_unit=='MT'):
#             print(dest_phys_unit)
            MT_val=float(dest_phys_total_vol)
            m3_val=float(dest_phys_total_vol)/float(density_value)
            

            
        elif (dest_phys_unit=='m³'):
            m3_val=float(dest_phys_total_vol)
            MT_val=float(dest_phys_total_vol)* float(density_value)
        print('m3_val',m3_val,'MT_val',MT_val)
            
            
        
        cursor.execute("SELECT * FROM TANK_CAPACITY WHERE Port = ? AND Terminal=? AND Tank_Num=?", (shore_port_value,shore_terminal_value,bill_tank_name_value))
        dest_tank_details = cursor.fetchall()

        for dest_tank_details_row in dest_tank_details:
            dest_safe_fill_val_check=dest_tank_details_row[5]
            dest_current_qty_check=dest_tank_details_row[9]
            dest_rem_space_check=dest_tank_details_row[10]
        print('dest_safe_fill_val_check',dest_safe_fill_val_check)
        print('dest_current_qty_check',dest_current_qty_check)
        print('dest_rem_space_check',dest_rem_space_check)
            
        source_ld_df = pd.read_sql_query('SELECT * FROM INVENTORY_TRANSFER WHERE   Source_Port=(?)AND Source_Terminal=(?) AND Source_Name=(?) ' , my_conn,params=(shore_port_value,shore_terminal_value,bill_tank_name_value)) 
        dest_ld_df  =  pd.read_sql_query('SELECT * FROM INVENTORY_TRANSFER WHERE    Dest_Port=(?) AND Dest_Terminal=(?)   AND Dest_Tank_Num=(?) ' , my_conn,params=(shore_port_value,shore_terminal_value,bill_tank_name_value)) 
        
        ss=source_tank_qty_check(source_ld_df,m3_list_st,MT_list_st)
        dd=dest_tank_qty_check(dest_ld_df,m3_list_dt,MT_list_dt)

        
        if ([(len(source_ld_df)>0) or (len(dest_ld_df)>0)]):
        
            print('ss[1])',float(ss[1]),'dd[1]',float(dd[1]))
            print('+++++')
            print(float(ss[0]),float(dd[0]))
            print('m3_val',m3_val,'MT_val',MT_val)
            print(MT_val)
            current_MT_qty=float(ss[1])+float(dd[1])+float(MT_val)
            current_MT_qty=round(current_MT_qty,4)
            current_m3_qty=float(ss[0])+float(dd[0])+float(m3_val)
            current_m3_qty=round(current_m3_qty,4)
            current_tank_rem_space=float(dest_safe_fill_val_check) - float(current_m3_qty)
            current_tank_rem_space=round(current_tank_rem_space,4)
            
        else:
            
            current_MT_qty=float(MT_val)
            current_MT_qty=round(current_MT_qty,4)
            current_m3_qty=float(m3_val)
            current_m3_qty=round(current_m3_qty,4)
            current_tank_rem_space=float(dest_safe_fill_val_check) - float(current_m3_qty)
            current_tank_rem_space=round(current_tank_rem_space,4)
            

            
            

        
        print(current_MT_qty) 
        print(current_m3_qty)
        print(current_tank_rem_space)
        print(shore_port_value,shore_terminal_value,bill_tank_name_value,shore_product_value)
        print(type(current_m3_qty),type(current_tank_rem_space),type(current_MT_qty))
        
        if current_MT_qty==0.0:
            shore_product_value='EMPTY'
        cursor.execute('UPDATE TANK_CAPACITY SET Qty_Add_Discharge_m³ =? ,Remaining_Space_m³=?,Current_Quantity_MT=?,Product=? WHERE Port = ? AND Terminal=? AND Tank_Num=?',(current_m3_qty,current_tank_rem_space,current_MT_qty,shore_product_value,shore_port_value,shore_terminal_value,bill_tank_name_value))
        my_conn.commit()
        TEST = pd.read_sql_query('SELECT * FROM TANK_CAPACITY WHERE   Port = ? AND Terminal=? AND Tank_Num=?' , my_conn,params=(shore_port_value,shore_terminal_value,bill_tank_name_value)) 
  
        print(TEST )
    
            
                   
    
    
    
def raise_hist(frame):
    frame.tkraise()
    
    history_frame = Frame(f3, bd=1, relief=SOLID, padx=10, pady=10,width=1500, height=800)
    history_tree = ttk.Treeview(history_frame, show="headings",selectmode='browse',style="mystyle.Treeview",height=30)
    history_tree.tag_configure('odd', background='#FFEFD5')
    history_tree.tag_configure('even', background='white')

    history_tree.grid(row=1, columnspan=1)

#     for item in history_tree.get_children():
#         history_tree.delete(item)

    
    history_data = pd.read_sql('SELECT * FROM PHYSICAL_BLOTTER', my_conn)
    my_conn.commit()
    
 
    history_data=history_data[['DATE', 'TRADER', 'COUNTER_PARTY', 'BOOK', 'STRATEGY', 'DERIVATIVE','PRODUCT', 'PRICING_CONTRACT', 'kbbl', 'kMT', 'PRICING_METHOD','PREMIUM_DISCOUNT', 'PRICING_TERM', 'BL_DATE', 'START_DATE', 'END_DATE','HOLIDAY', 'UNIT', 'TOTAL_DAYS', 'PRICED_DAYS', 'UNPRICED_DAYS','TOTAL_VOLUME', 'PRICED_VOLUME', 'UNPRICED_VOLUME', 'POSITION','PRICED_PRICE', 'UNPRICED_PRICE', 'CONV_kbbl_MT', 'CONV_MT_kbbl',"Container",'Port','Terminal','Vessel_Name','Tank_Number','External_Terminal','NOTES','Shore_Received','Difference']]
    # history_data.columns = ['Date','Clearer','Trader','Book', 'Strategy', 'Derivative','Volume','Contract' ,'Start_Date' ,'End_Date','Price' , 'Holiday','Type','Efs_code','Broker','Notes','Total Days','Total Priced Days','Total Unpriced_Days','Total Priced Volume','Total Unpriced Volume','Total Volume','Clearer Rate','Exchange Rate' ,'Broker Rate']
    
    history_data.columns = ['Date', 'Trader', 'Counter Party', 'Book', 'Strategy', 'Derivative', 'Product', 'Pricing Contract', 'kbbl', 'kMT', 'Pricing Method', 'Premium_Discount', 'Pricing Term', 'Bl_Date', 'Start Date', 'End Date', 'Holiday', 'Unit', 'Total Days', 'Priced Days', 'Unpriced Days', 'Total Volume', 'Priced Volume', 'Unpriced Volume', 'Position', 'Priced Price', 'Unpriced Price', 'CONV_kbbl_MT', 'CONV_MT_kbbl', "Container",'Port','Terminal','Vessel_Name','Tank_Number','External_Terminal','Notes','Shore_Received','Difference']

    cols = list(history_data.columns)
    print(cols)
    history_tree["columns"] = cols
    history_tree["show"] = "headings" 


    for i in cols:
        history_tree.column(i, width = 48,minwidth = 120)

        history_tree.column(i, anchor="center")
        history_tree.heading(i, text=i, anchor='center')

    df_rows = history_data.to_numpy().tolist() 
    
    for index in range(len(df_rows)):
        if index %2==0:
            history_tree.insert("",'end',values=df_rows[index],tags=('even'))
        else:
            history_tree.insert("",'end',values=df_rows[index],tags=('odd'))

        # # ----vertical scrollbar------------
    vbar = ttk.Scrollbar(history_frame, orient=VERTICAL, command=history_tree.yview)
    history_tree.configure(yscrollcommand=vbar.set)
    #tree.grid(row=0, column=0, sticky=NSEW)
    vbar.grid(row=1, column=1, sticky=NS)

    # # ----horizontal scrollbar----------
    hbar = ttk.Scrollbar(history_frame, orient=HORIZONTAL, command=history_tree.xview)
    history_tree.configure(xscrollcommand=hbar.set)
    hbar.grid(row=2, column=0, sticky=EW)
    history_frame.place(x=20, y=75)
    
def raise_frame_position(frame):
    frame.tkraise()
    for item in position_tree.get_children():
        position_tree.delete(item)

    data_position = pd.read_sql('SELECT * FROM PHYSICAL_BLOTTER', my_conn)
    print(data_position)
    #     data_position['VOLUME'] = data_position['VOLUME'].astype(int)
    # print(data_position)
    products=data_position['PRODUCT'].unique()
    print(products)

    data_position.DATE = pd.to_datetime(data_position.DATE)
    data_position.END_DATE = pd.to_datetime(data_position.END_DATE)
    data_position.set_index('END_DATE', inplace=True)

    df_names=[]
    product=[]
    for i in range(len(products)):
        print(products[i])
        product.append(products[i])
        df_position_product='data_position'+str(products[i])
        df_position_product=data_position.loc[data_position['PRODUCT']==products[i]]
        print(df_position_product)

        resampled='monthly_resampled_'+str(products[i])
        resampled = (df_position_product.resample('M').sum()).reset_index().round(3)

        resampled.rename(columns = {'PRICED_VOLUME':products[i]}, inplace = True)
        df_names.append(resampled)
        df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['END_DATE'],how='outer'), df_names)
    data = pd.DataFrame()
    data['END_DATE']=df_merged['END_DATE']
    for i in product:
        data[[i]]=df_merged[[i]]
    # print("++",data)
    data.END_DATE = pd.to_datetime(data['END_DATE'].dt.date)
    data['date_col'] = data['END_DATE'].dt.date
    data['date_col']=pd.to_datetime(data['date_col'])
    data=data.set_index('date_col')
    data = data.sort_values(by =['date_col'])
    data.END_DATE=data.END_DATE.dt.strftime('01-%b-%y').str.upper()
    data.replace([0, 0.0,np.nan],'-', inplace=True)
    data['END_DATE']=pd.to_datetime(data['END_DATE'])
    data.set_index(['END_DATE'], inplace=True)


    df_list=[]
    grouped = data.groupby([data.index.year])
    for index,df in grouped:
        colums=df.columns.tolist()
        status_list=[]
        status='all_null'
        index_list=[]
        for i in range(len(df)) :
            condition_list=[]
            for index, value in enumerate(colums):  
                var=df.iloc[i, index]=='-'
                condition_list.append(var)

            v=(all(condition_list))
            status_list.append(str(all(condition_list)))
        df['flag']=status_list

        index_list=[]
        update_df=pd.DataFrame()
        flag='not_started'
        for i, row in df.iterrows():
            if flag=='not_started':
                index=i
                if row['flag']=='True':
                    flag='not_started'
                    index_list.append(index)
                else:
                    flag='started'
                    continue

        df = df.drop(index=index_list) 
        df = df.reset_index()
        if not df.empty:
            df_list.append(df)
    data = pd.concat(df_list)
    
    print(data)



    data.drop('flag', inplace=True, axis=1)
    data.rename(columns={'END_DATE': 'Date'}, inplace=True)

    data.Date = pd.to_datetime(data['Date'].dt.date)
    data.Date=data.Date.dt.strftime('01-%b-%y').str.upper()
        
    tot_data = data.copy()
    tot_data.drop('Date', inplace=True, axis=1) 
    
    tot_data=tot_data.replace(to_replace ="-",value =0.0)
    print("replaced",tot_data)
    sum_product_position=tot_data.sum(axis = 0)
    print("sum",sum_product_position)
    name_df = sum_product_position.to_frame(name='Total')
    name_df.index.name = 'Products'
    
    df_total=name_df
    df_total=name_df.transpose()
    
    df_total.reset_index(inplace=True)
    df_total.rename(columns = {'index':'Products'}, inplace = True)
    print(df_total)
    
    list_row=df_total.iloc[0].tolist()
    data_new = data.copy()                                  # Create copy of DataFrame
    data_new.loc[-1] = list_row   
    data_new.index=data_new.index+1   # Append list at the bottom
    data_new = data_new.sort_index().reset_index(drop = True)  # Reorder DataFrame
    cols_new=list(data_new.columns)
    print(data_new)
    
    position_tree["columns"] = cols_new
    for i in cols_new:
        position_tree.column(i,width =50,minwidth=60)
    #         minwidth = 250
        position_tree.column(i, anchor="center")
        position_tree.heading(i, text=i, anchor='center')

    df_rows_position_total = data_new.to_numpy().tolist() 

    for index in range(len(df_rows_position_total)):
        if index==0:
            position_tree.insert("",'end',values=df_rows_position_total[index],tags=('first'))

        elif index %2==0:
            position_tree.insert("",'end',values=df_rows_position_total[index],tags=('even'))
        else:
            position_tree.insert("",'end',values=df_rows_position_total[index],tags=('odd'))

    




    
    
def kbbl_event_tab(e):
    global text_value,fg
    text_value=''
    fg='grey'
    Volume_value=kbbl_entry.get()
    
    if not Volume_value:
        text_value=''
        fg='grey'
        buy_sell=Label(f1_left_frame, text='          ', font=f,bg="White",fg = 'grey').grid(row=6, column=1, sticky=W, pady=4,padx=30)

    elif len(Volume_value) != 0 and float(Volume_value) >0 :
        text_value='Buy'
        fg='blue'
    else:
        if len(Volume_value) != 0 and float(Volume_value) <0:
            text_value='Sell'
            fg='red'
    buy_sell=Label(f1_left_frame, text=text_value, font=f,bg="White",fg = fg).grid(row=6, column=1, sticky=W, pady=4,padx=30)
    print(text_value)
#     except:
#         messagebox.showerror("error",'Enter integer for volume')
#         kbbl_entry.delete(0,END)


def kbbl_event(e):
    global text_value,fg
    text_value=''
    fg='grey'
    Volume_value=kbbl_entry.get()
#     try:
    if not kbbl_entry.get():
        text_value=''
        fg='grey'
        buy_sell=Label(f1_left_frame, text='          ', font=f,bg="White",fg = 'grey').grid(row=6, column=1, sticky=W, pady=4,padx=30)

    elif len(Volume_value) != 0 and float(Volume_value) >0 :
        text_value='Buy'
        fg='blue'
    else:
        if len(Volume_value) != 0 and float(Volume_value) <0:
            text_value='Sell'
            fg='red'
    buy_sell=Label(f1_left_frame, text=text_value, font=f,bg="White",fg = fg).grid(row=6, column=1, sticky=W, pady=4,padx=30)
    print(text_value)
#     except:
#         messagebox.showerror("error",'Enter integer for volume')
#         kbbl_entry.delete(0,END)
        
def kMT_event_tab(e):
    global text_value,fg
    text_value=''
    fg='grey'
    Volume_value=kMT_entry.get()
#     try:
    if not kMT_entry.get():
        text_value=''
        fg='grey'
        buy_sell=Label(f1_left_frame, text='               ', font=f,bg="White",fg = 'grey').grid(row=6, column=1, sticky=W, pady=4,padx=30)

    elif len(Volume_value) != 0 and float(Volume_value) >0 :
        text_value='Buy'
        fg='blue'
    else:
        if len(Volume_value) != 0 and float(Volume_value) <0:
            text_value='Sell'
            fg='red'
    buy_sell=Label(f1_left_frame, text=text_value, font=f,bg="White",fg = fg).grid(row=6, column=1, sticky=W, pady=4,padx=30)
    print(text_value)
#     except:
#         messagebox.showerror("error",'Enter integer for volume')
#         kMT_entry.delete(0,END)


# def kMT_event(e):
#     global text_value,fg
#     text_value=''
#     fg='grey'
#     Volume_value=kMT_entry.get()
#     try:
#         if not kMT_entry.get():
#             text_value=''
#             fg='grey'
#             buy_sell=Label(f1_left_frame, text='              ', font=f,bg="White",fg = 'grey').grid(row=6, column=1, sticky=W, pady=4,padx=30)

#         elif len(Volume_value) != 0 and int(Volume_value) >0 :
#             text_value='Buy'
#             fg='blue'
#         else:
#             if len(Volume_value) != 0 and int(Volume_value) <0:
#                 text_value='Sell'
#                 fg='red'
#         buy_sell=Label(f1_left_frame, text=text_value, font=f,bg="White",fg = fg).grid(row=6, column=1, sticky=W, pady=4,padx=30)
#         print(text_value)
#     except:
#         messagebox.showerror("error",'Enter integer for volume')
#         kMT_entry.get().delete(0,END)


def end_date_event_tab(e):
    
    date_value=date_variable

    start_date_value=Start_date.get()
    end_date_value=End_date.get()
    holiday_value=Holiday_entry.get()
    
    try:
        day='01'
        slash = '/'
        hyphen='-'

        try:
            len_start_mon=len(Start_date.get())
            x=6/(len_start_mon)
            start_date_entry=Start_date.get()    

        except Exception as exception:
            print('Enter Start_date') 
            raise ("error in Start_date")


        if slash in start_date_entry:
            reg=slash
        else:
            if hyphen in start_date_entry:
                reg=hyphen
        print(reg)

        if (len(start_date_entry)>6):
            start_date_value=Start_date.get()

        elif (len(start_date_entry)<=6):
            start_counter = start_date_entry.count(reg)
            print("6")
            if start_counter==2:
                print("2")
                try:
                    formats_date_6 = ['%d-%m-%y','%d/%m/%y']
                    for date_format in formats_date_6:
                        start_date_entry=Start_date.get()
                        start_date_formatted = datetime.strptime(start_date_entry, date_format)
                        start_date_value=start_date_formatted.strftime(date_format)
                        print("2",start_date_entry)
                except ValueError as e:
                    pass

            elif start_counter==1:
                start_date_entry=Start_date.get()
                start_date_value=day+reg+start_date_entry
                print("else",start_date_value)

        if Start_date.get()!='':
            formats_date = ['%d-%m-%y','%d/%m/%y','%d-%b-%y','%d/%b/%y']
            for date_format in formats_date:
                try:
                    start_date_formatted = datetime.strptime(start_date_value, date_format)
                    start_date_value=start_date_formatted.strftime('%d-%b-%y').upper()
                    print(start_date_value)

                    break
                except ValueError as e:
                    pass
        elif Start_date.get()=='':
            print('Enter start date')
    except Exception as exception:
        print('Check start date format') 
        raise ("error in start date")
        
    try:
        end_day='01'
        end_slash = '/'
        end_hyphen='-'

        try:
            len_end_mon=len(End_date.get())
            y=6/(len_end_mon)
            end_date_entry=End_date.get()  

        except :
            print('Enter End_date') 
            raise ("error in End_date")

        if end_slash in end_date_entry:
            reg=end_slash
        else:
            if end_hyphen in end_date_entry:
                reg=end_hyphen
        print(reg)

        if (len(end_date_entry)>6):
            end_date_value=End_date.get()
            print(end_date_value)

        elif (len(end_date_entry)<=6):
            end_counter = end_date_entry.count(reg)
            print("6")
            if end_counter==2:
                print("2")
                try:
                    formats_date_end = ['%d-%m-%y','%d/%m/%y']
                    for date_format_end in formats_date_end:
                        end_date_entry=End_date.get()
                        end_date_formatted = datetime.strptime(end_date_entry, date_format_end)
                        end_date_value=end_date_formatted.strftime(date_format_end)
                        print("2",end_date_entry)
                except ValueError as e:
                    pass

            elif end_counter==1:
                end_date_entry=End_date.get()
                end_date_value=end_day+reg+end_date_entry
                print("else",end_date_value)

        if End_date.get()!='':
            formats_date_end = ['%d-%m-%y','%d/%m/%y','%d-%b-%y','%d/%b/%y']
            for date_format_end in formats_date_end:
                try:
                    end_date_formatted = datetime.strptime(end_date_value, date_format_end)
                    end_date_value=end_date_formatted.strftime('%d-%b-%y').upper()
                    print(end_date_value)
                    break
                except ValueError as e:
                    pass
        elif End_date.get()=='':
            print('Enter End date')
            
    except Exception as exception:
        print('Check end date format') 
        raise ("error in end date")
    
    try:
        if Start_date.get()!='' and End_date.get()!='':
            today=datetime.strptime(date_value, "%d-%b-%y")
            start_date_value=datetime.strptime(start_date_value, "%d-%b-%y")
            end_date_value=datetime.strptime(end_date_value, "%d-%b-%y")

            print(start_date_value)
            print(end_date_value)
    
    except Exception as exception:
#         raise ("error in start date")
        print('Check date format') 
        raise ("error in date")
    
    if start_date_value<=end_date_value:
        
        
        business_days = len(pd.bdate_range(start_date_value,end_date_value))
        print("Total business days in range : " + str(business_days))
    else:
        print('end_date should be greater than start date') 
        
    swaps_data = pd.read_sql('SELECT * FROM HOLIDAY_SETTINGS', my_conn)
    my_conn.commit()
    swaps_data.Date=pd.to_datetime(swaps_data.Date)
    holiday_search=swaps_data[(swaps_data["Date"] >= start_date_value) & (swaps_data["Date"] <= end_date_value) & (swaps_data['Holiday_type'] == holiday_value)]


    holidays=len(holiday_search)
    print("Holidays in between start and end",holidays)
    total_swap_days=business_days-holidays
    print("total swaps days",total_swap_days)
    
    if not End_date.get():
        no_days=Label(f1_left_frame, text='                     ', font=f,bg="White",fg = 'grey').grid(row=18, column=1, sticky=W, pady=4,padx=30)

    elif End_date.get() != '' and Start_date.get()!='' :
        no_days=Label(f1_left_frame, text=str(total_swap_days)+"    ", font=f,fg = 'blue').grid(row=18, column=1, sticky=W, pady=4,padx=30)






def discharged_difference(e):
    try:
        bill_shore_difference_entry.delete(0,END)

        billed_qty_eve=bill_shore_billed_qty_entry.get().strip()
        print('+====',billed_qty_eve)
        billed_qty_eve_val=float(billed_qty_eve)

        discharged_qty_eve=bill_shore_discharge_entry.get().strip()
        print(discharged_qty_eve)
        discharged_qty_eve_val=float(discharged_qty_eve)



        gain_loss_eve=abs(float(discharged_qty_eve_val))-abs(float(billed_qty_eve_val))

        bill_shore_difference_entry.insert(0,gain_loss_eve)
    except:
        print('spaces')
    



def physical_blotter_selectItem(e):
    
    Trader.set('Select')
    Counter_party.set('Select')
    book_entry.set('Select')
    strat_entry.set('Select')
    derivative_var.set('Physical')
    Product_entry.set('Select')
    Pricing_contract_entry.set('Select')
    
    kbbl_entry.delete(0,END)
    kMT_entry.delete(0,END)
    pricing_method_entry.set('Select')
    premium_discount.delete(0,END)
    pricing_term_entry.set('Select')
    bl_date.delete(0,END)
    Start_date.delete(0,END)
    End_date.delete(0,END)
    Holiday_entry.set('Select')
    
    Container_entry.set('Select')
    Port_entry.set('Select')
    Terminal_entry.set('Select')
    
    Container_Vessel.delete(0,END)
    Container_Tank.set('Select')
    Container_Truck.delete(0,END)
    nominated_qty.delete(0,END)
    density.delete(0,END)
    
    
    
    Notes.delete(0,END)
    selected = physical_tree.focus()
     # Grab record values
    values = physical_tree.item(selected, 'values')
    print("selected poisined",values)
    
    Trader.set(values[1]) 
    Counter_party.set(values[2])
    book_entry.set(values[3])
    strat_entry.set(values[4])
    derivative_var.set(values[5])
    Product_entry.set(values[6])
    Pricing_contract_entry.set(values[7])
    kbbl_entry.insert(0,values[8])
    kMT_entry.insert(0,values[9])
    
    pricing_method_entry.set(values[10])
    premium_discount.insert(0,values[11])
    pricing_term_entry.set(values[12])
    bl_date.insert(0,values[13])
    Start_date.insert(0,values[14])
    End_date.insert(0,values[15])
    Holiday_entry.set(values[16])
    physical_unit_entry.set(values[17])
    Container_entry.set(values[29])
    Port_entry.set(values[30])
    Terminal_entry.set(values[31])
    Container_Vessel.insert(0,values[32])
    Container_Tank.set(values[33])
    Container_Truck.insert(0,values[34])

    
    
    Notes.insert(0,values[35])
    nominated_qty.insert(0,values[38])
    density.insert(0,values[39])


def clear():

        
    cursor.execute("SELECT Default_trader FROM Default_values")
    trader_fetch=cursor.fetchall()
    for dflt_trader in trader_fetch:
        Trader.set(dflt_trader[0])
    Trader.config(width=15, font=('Times', 12))
    Counter_party.set('Select')

    cursor.execute("SELECT Default_book FROM Default_values")
    book_fetch=cursor.fetchall()
    for dflt_book in book_fetch:
        book_entry.set(dflt_book[0])
    book_entry.config(width=15, font=('Times', 12))
    strat_entry.set('Select')
    derivative_var.set('Physical')
    Product_entry.set('Select')
    Pricing_contract_entry.set('Select')
    kbbl_entry.delete(0,END)
    kMT_entry.delete(0,END)
    pricing_method_entry.set('Select')
    premium_discount.delete(0,END)
    pricing_term_entry.set('Select')
    bl_date.delete(0,END)
    Start_date.delete(0,END)
    End_date.delete(0,END)
    Holiday_entry.set('Select')
    Container_entry.set('Select')
    Port_entry.set('Select')
    Terminal_entry.set('Select')
    physical_unit_entry.set('Select')
    Container_Vessel.delete(0,END)
    Container_Tank.set('Select')
    Container_Truck.delete(0,END)
    
    Notes.delete(0,END)
    no_days=Label(f1_left_frame, text='                     ', font=f,bg="White",fg = 'grey').grid(row=18, column=1, sticky=W, pady=4,padx=30)
    buy_sell=Label(f1_left_frame, text='          ', font=f,bg="White",fg = 'grey').grid(row=6, column=1, sticky=W, pady=4,padx=30)
    nominated_qty.delete(0,END)
    density.delete(0,END)

 


        
def physical_add():
    
    date_value=date_variable
    trader_value=Trader.get()
    Counter_party_value=Counter_party.get()
    book_value=book_entry.get()
    strategy_value=strat_entry.get()
    derivative_value=derivative_var.get()
    product_value=Product_entry.get()
    Pricing_contract_value=Pricing_contract_entry.get()
    kbbl_value=kbbl_entry.get()
    kMT_value=kMT_entry.get()
    pricing_method_value=pricing_method_entry.get()
#     premium_discount_value=premium_discount.get()
    pricing_term_value=pricing_term_entry.get()
    bl_date_value=bl_date.get()
    start_date_value=Start_date.get()
    end_date_value=End_date.get()
    holiday_value=Holiday_entry.get()
    Container_value=Container_entry.get()
    
    Port_entry_value=Port_entry.get()
    Terminal_entry_value=Terminal_entry.get()
    
    Vessel_name_value=Container_Vessel.get()
    Tank_number_value=Container_Tank.get()
    Truck_plate_value=Container_Truck.get()
    print(Vessel_name_value,Tank_number_value,Truck_plate_value)


    
    
    notes_value=Notes.get()
    
    nominated_qty_value=nominated_qty.get()
    try:
        density_value=density.get()
        density_value=float(density_value)
    except:    
        messagebox.showerror("error",'Enter Numeric Value for Density')
        raise
    
    
    
    
    
    
    
    if kbbl_entry.get()!='' and kMT_entry.get()!='':
        try:
            kbbl_inp=float(kbbl_entry.get())
            kmt_inp=float(kMT_entry.get())
            if (kbbl_inp>0 and kmt_inp>0) or (kbbl_inp<0 and kmt_inp<0):

                conv_kbbl__MT=float(kbbl_entry.get())/float(kMT_entry.get())
                conv_kbbl__MT=round(conv_kbbl__MT,2)

                conv_MT__kbbl=float(kMT_entry.get())/float(kbbl_entry.get())
                conv_MT__kbbl=round(conv_MT__kbbl,2)

                Volume_value=kbbl_entry.get()
            else:
                messagebox.showerror("error",'Kbbl , kMT signs need to be same')
        except Exception as exception:
            messagebox.showerror("error",'Enter numeric for kbbl and KMT') 
            raise ("error in kbbl and KMT")
    
    elif kbbl_entry.get()!='' and kMT_entry.get()=='':
        try:
            kbbl_inp=float(kbbl_entry.get())

        
            conv_kbbl__MT=kbbl_entry.get()
            conv_MT__kbbl=''
            Volume_value=kbbl_entry.get()
            
        except Exception as exception:
            
            messagebox.showerror("error",'Enter Numeric value for kbbl') 
            raise ("error in kbbl")
 
    elif kbbl_entry.get()=='' and kMT_entry.get()!='':
        try:
            kmt_inp=float(kMT_entry.get())

            conv_kbbl__MT=''
            conv_MT__kbbl=kMT_entry.get()
            Volume_value=kMT_entry.get()
        except Exception as exception:
            messagebox.showerror("error",'Enter Numeric value for kbbl') 
            raise ("error in kbbl")

        
    elif kbbl_entry.get()=='' and kMT_entry.get()=='':
        messagebox.showerror("error",'Enter the volume in kbbl or KMT')
    print(Volume_value)
        
    try:
        bl_day='01'
        bl_slash = '/'
        bl_hyphen='-'
        if bl_date.get()!= '':
            
            bl_date_entry=bl_date.get()


            if bl_slash in bl_date_entry:
                bl_reg=bl_slash
            else:
                if bl_hyphen in bl_date_entry:
                    bl_reg=bl_hyphen
            print(bl_reg)

            if (len(bl_date_entry)>6):
                bl_date_value=bl_date.get()

            elif (len(bl_date_entry)<=6):
                bl_counter = bl_date_entry.count(bl_reg)
                print("6")
                if bl_counter==2:
                    print("2")
                    try:
                        bl_bl_date_formats_dates_6 = ['%d-%m-%y','%d/%m/%y']
                        for bl_date_format in bl_bl_date_formats_dates_6:
                            bl_date_entry=bl_date.get()
                            bl_date_formatted = datetime.strptime(bl_date_entry, bl_date_format)
                            bl_date_value=bl_date_formatted.strftime(bl_date_format)
                            print("2",bl_date_entry)
                    except ValueError as e:
#                         pass
                        print(e)

                elif bl_counter==1:
                    bl_date_entry=bl_date.get()
                    bl_date_value=bl_day+bl_reg+bl_date_entry
                    print("else",bl_date_value)


        if bl_date.get()!='':
            bl_date_formats_dates = ['%d-%m-%y','%d/%m/%y','%d-%b-%y','%d/%b/%y']
            for bl_date_format in bl_date_formats_dates:
                    try:
                        bl_date_formatted = datetime.strptime(bl_date_value, bl_date_format)
                        bl_date_value=bl_date_formatted.strftime('%d-%b-%y')
                        print("error check",bl_date_value)

                        break
                    except ValueError as e:
                        pass
            bl_date_error_check=datetime.strptime(bl_date_value, '%d-%b-%y')
            print(bl_date_error_check)
    except Exception as exception:
        messagebox.showerror("error",'Check bl date format') 
        raise ("error in bl date")
        
        
    try:
        day='01'
        slash = '/'
        hyphen='-'

        try:
            len_start_mon=len(Start_date.get())
            x=6/(len_start_mon)
            start_date_entry=Start_date.get()    

        except Exception as exception:
            messagebox.showerror("error",'Enter Start_date') 
            raise ("error in Start_date")


        if slash in start_date_entry:
            reg=slash
        else:
            if hyphen in start_date_entry:
                reg=hyphen
        print(reg)

        if (len(start_date_entry)>6):
            start_date_value=Start_date.get()

        elif (len(start_date_entry)<=6):
            start_counter = start_date_entry.count(reg)
            print("6")
            if start_counter==2:
                print("2")
                try:
                    formats_date_6 = ['%d-%m-%y','%d/%m/%y']
                    for date_format in formats_date_6:
                        start_date_entry=Start_date.get()
                        start_date_formatted = datetime.strptime(start_date_entry, date_format)
                        start_date_value=start_date_formatted.strftime(date_format)
                        print("2",start_date_entry)
                except ValueError as e:
                    pass

            elif start_counter==1:
                start_date_entry=Start_date.get()
                start_date_value=day+reg+start_date_entry
                print("else",start_date_value)

        if Start_date.get()!='':
            formats_date = ['%d-%m-%y','%d/%m/%y','%d-%b-%y','%d/%b/%y']
            for date_format in formats_date:
                try:
                    start_date_formatted = datetime.strptime(start_date_value, date_format)
                    start_date_value=start_date_formatted.strftime('%d-%b-%y').upper()
                    print(start_date_value)

                    break
                except ValueError as e:
                    pass
        elif Start_date.get()=='':
            messagebox.showerror("error",'Enter start date')
    except Exception as exception:
        messagebox.showerror("error",'Check start date format') 
        raise ("error in start date")
        
    try:
        end_day='01'
        end_slash = '/'
        end_hyphen='-'

        try:
            len_end_mon=len(End_date.get())
            y=6/(len_end_mon)
            end_date_entry=End_date.get()  

        except :
            messagebox.showerror("error",'Enter End_date') 
            raise ("error in End_date")

        if end_slash in end_date_entry:
            reg=end_slash
        else:
            if end_hyphen in end_date_entry:
                reg=end_hyphen
        print(reg)

        if (len(end_date_entry)>6):
            end_date_value=End_date.get()
            print(end_date_value)

        elif (len(end_date_entry)<=6):
            end_counter = end_date_entry.count(reg)
            print("6")
            if end_counter==2:
                print("2")
                try:
                    formats_date_end = ['%d-%m-%y','%d/%m/%y']
                    for date_format_end in formats_date_end:
                        end_date_entry=End_date.get()
                        end_date_formatted = datetime.strptime(end_date_entry, date_format_end)
                        end_date_value=end_date_formatted.strftime(date_format_end)
                        print("2",end_date_entry)
                except ValueError as e:
                    pass

            elif end_counter==1:
                end_date_entry=End_date.get()
                end_date_value=end_day+reg+end_date_entry
                print("else",end_date_value)

        if End_date.get()!='':
            formats_date_end = ['%d-%m-%y','%d/%m/%y','%d-%b-%y','%d/%b/%y']
            for date_format_end in formats_date_end:
                try:
                    end_date_formatted = datetime.strptime(end_date_value, date_format_end)
                    end_date_value=end_date_formatted.strftime('%d-%b-%y').upper()
                    print(end_date_value)
                    break
                except ValueError as e:
                    pass
        elif End_date.get()=='':
            messagebox.showerror("error",'Enter End date')
            
    except Exception as exception:
        messagebox.showerror("error",'Check end date format') 
        raise ("error in end date")
    
    try:
        if Start_date.get()!='' and End_date.get()!='':
            today=datetime.strptime(date_value, "%d-%b-%y")
            start_date_value=datetime.strptime(start_date_value, "%d-%b-%y")
            end_date_value=datetime.strptime(end_date_value, "%d-%b-%y")

            print(start_date_value)
            print(end_date_value)
    
    except Exception as exception:
#         raise ("error in start date")
        messagebox.showerror("error",'Check date format') 
        raise ("error in date")
    
    if start_date_value<=end_date_value:
        
        
        business_days = len(pd.bdate_range(start_date_value,end_date_value))
        print("Total business days in range : " + str(business_days))
    else:
        messagebox.showerror("error",'end_date should be greater than start date') 
        
    swaps_data = pd.read_sql('SELECT * FROM HOLIDAY_SETTINGS', my_conn)
    my_conn.commit()
    swaps_data.Date=pd.to_datetime(swaps_data.Date)
    holiday_search=swaps_data[(swaps_data["Date"] >= start_date_value) & (swaps_data["Date"] <= end_date_value) & (swaps_data['Holiday_type'] == holiday_value)]


    holidays=len(holiday_search)
    print("Holidays in between start and end",holidays)
    total_swap_days=business_days-holidays
    print("total swaps days",total_swap_days)
    

    
    end_date_value=end_date_value
    start_date_value=start_date_value
    print(start_date_value)
    print(end_date_value)
    print(today)

    
    
    if today <=start_date_value:
        print("first")

        unpriced_days=total_swap_days
        priced_days=0
        print(unpriced_days)
#         print(priced_days)
    
    elif (today > start_date_value) and (today<=end_date_value):
        
        business_days = len(pd.bdate_range(today,end_date_value))
        print("second")
        holiday_search=swaps_data[(swaps_data["Date"] >= today) & (swaps_data["Date"] <= end_date_value) &(swaps_data['Holiday_type'] == holiday_value)]
        holidays_from_tday=len(holiday_search)
        print("business_days",business_days)
        print("holidays_from_tday",holidays_from_tday)
        unpriced_days=business_days-holidays_from_tday
        priced_days=int(total_swap_days)-unpriced_days
        print(unpriced_days)
        print(priced_days)

    elif today > end_date_value:
        unpriced_days=0
        priced_days=int(total_swap_days)
   
        
    if pricing_method_entry.get()=="Fixed":
        if start_date_value==end_date_value:
            priced_volume=Volume_value
            un_priced_volume=0
            premium_discount_value=premium_discount.get()
            t_prx=Volume_value
            position_value=priced_volume
            priced_price=premium_discount_value
            unpriced_price='-'
        else:
            messagebox.showerror("error",'Start and End Date should be same for fixed')
            raise
            
        
    elif pricing_method_entry.get()=="Float":
        premium_discount_value=premium_discount.get()
        print("premium_discount_value",premium_discount_value)
        print("priced_days",priced_days)
        print("unpriced_days",unpriced_days)
        print("total_swap_days",total_swap_days)
        print("Volume_value",Volume_value)
        try:
            priced_vol=(float(Volume_value)/float(total_swap_days))*priced_days
        except ZeroDivisionError:
            messagebox.showerror("error",'end_date should be greater than start date')
            
        priced_volume=round(priced_vol,2)
        
        un_priced_volume=(float(Volume_value)/float(total_swap_days))*unpriced_days
        un_priced_volume=round(un_priced_volume,2)
        print(priced_volume)
        print(un_priced_volume)
        t_prx=Volume_value
#         t_prx=round(t_prx,2)
        print("total_volume",t_prx)
        position_value=priced_volume
        priced_price=premium_discount_value
        unpriced_price='-'
        
        
    physical_unit=physical_unit_entry.get()
    print('+++++++++++++++++++++++++++++++++++++++++')
    
    swaps_contract_fee=pd.read_sql_query('SELECT * FROM SWAPS_CONTRACT WHERE Contract = ?', my_conn, params=(Pricing_contract_entry.get(), ))                              
    if len(swaps_contract_fee)==0:
        messagebox.showerror("error",'Enter Screen and Block fee for the Contract in Admin Side')
        raise
    else:

        
        swaps_screen_fee_val=swaps_contract_fee['Screen_Fee']
        swaps_block_fee_val=swaps_contract_fee['Block_Fee']
        swaps_ticks_val=swaps_contract_fee['Tick']
        
        swaps_ticks_val=swaps_ticks_val.tolist()
        float_lst = list(np.float_(swaps_ticks_val))
        swaps_ticks_val=round(sum(float_lst),3)
        print(swaps_ticks_val)

    

    
    price_data_db_checking = pd.read_sql('SELECT * FROM Swaps_cargo_prices', my_conn)
    price_data_db_checking.columns = price_data_db_checking.columns.str.strip()
    price_data_db_checking['DATE'] = pd.to_datetime(price_data_db_checking['DATE'], format='%d/%m/%Y')

    contract_value_key=Pricing_contract_value.strip()
    

    start_date_value_date=start_date_value.date()
    end_date_value_date=end_date_value.date()
    start_date_value_str = start_date_value_date.strftime("%Y-%m-%d")
    end_date_value_str=end_date_value_date.strftime("%Y-%m-%d")

    date_list_pricing=[]

    for i in price_data_db_checking['DATE']:
        i = i.strftime("%Y-%m-%d")
        date_list_pricing.append(str(i))


    price_data_db_checking_list=price_data_db_checking.columns.tolist()
    
    if pricing_method_entry.get()=="Float":
        if contract_value_key in price_data_db_checking_list:

            print(start_date_value_date)
            print(date_list_pricing)

            if (priced_days!=0):

                if (unpriced_days==0):
                    print('End date  exist')

                    print(start_date_value)
                    print(end_date_value)

                    mask = (price_data_db_checking['DATE'] >= start_date_value) & (price_data_db_checking['DATE'] <=end_date_value)
                    df2 = price_data_db_checking.loc[mask]

                    pricing_list=df2[contract_value_key].tolist()
                    print(pricing_list)

                    Priced_days_price_avg = round(np.nanmean(pricing_list),3)


                    Today_mask=price_data_db_checking.loc[price_data_db_checking['DATE'] == end_date_value]
                    MTM_Price=Today_mask[contract_value_key].tolist()
                    MTM_Price=list(np.float_(MTM_Price))
                    MTM_Price_value=sum(MTM_Price)


                    priced_price= Priced_days_price_avg
                    unpriced_price=0.0


                    avrg_price=int(priced_days)*float(Priced_days_price_avg)
                    avrg_price=avrg_price/int(total_swap_days)


                    PNL=float(MTM_Price_value)-float(avrg_price)
                    print(PNL,'PNL')



                    PNL=float(PNL)*float(Volume_value)*float(swaps_ticks_val)
                    PnL=round(PNL,3)
                    print(PnL,'PNL')


                else:



                    price_data_db_checking=price_data_db_checking.drop_duplicates()

                    mask = (price_data_db_checking['DATE'] >= start_date_value) & (price_data_db_checking['DATE'] <= end_date_value)
                    df2 = price_data_db_checking.loc[mask]


                    last_day_price = df2[contract_value_key].iat[-1]
                    last_date = df2['DATE'].iat[-1]
                    last_date=last_date.date()
                    end_date_value=end_date_value.date()


                    next_day = last_date + timedelta(days = 1) 


                    rem_business_days = np.busday_count(last_date, end_date_value)
                    print(rem_business_days,'rem_business_days')



                    forward_data=int(rem_business_days)*float(last_day_price)
                    print(forward_data,'forward_data')

                    price_value_list=df2[contract_value_key].tolist()
                    print(price_value_list,'price_value_list')

                    avg_priced = np.nanmean(price_value_list)
                    avg_priced_value=avg_priced*priced_days

                    print(avg_priced_value,'avg_priced_value')
                    print(avg_priced_value)

                    Average_Price = (avg_priced_value + forward_data)/total_swap_days
                    print(Average_Price,'Average_Price')
                    print(total_swap_days)


                    total_price_diff=float(last_day_price)-float(Average_Price)
                    print(total_price_diff)

                    volume_value=t_prx

                    PnL=total_price_diff*int(swaps_ticks_val)*float(volume_value)
                    PnL=round(PnL,3)
                    print(PnL,'PnL')
                    print('end date not exist')

                    priced_price= avg_priced
                    unpriced_price=forward_data

            else:
                PnL=0.0
                messagebox.showinfo("Information", "Pricing not started")
                priced_price= avg_priced
                unpriced_price=forward_data
    else:
        
        Price_value=premium_discount.get()
        Today_mtm_price=price_data_db_checking.loc[price_data_db_checking['DATE'] == end_date_value]
        if len(Today_mtm_price)>0:
            MTM_Price=Today_mtm_price[contract_value_key].tolist()
            MTM_Price=list(np.float_(MTM_Price))
            MTM_Price_value=sum(MTM_Price)
            volume_value=t_prx
            PnL=(float(MTM_Price_value)-float(Price_value))*int(swaps_ticks_val)*float(volume_value)
            PnL=round(PnL,3)

        else:
            volume_value=t_prx
            MTM_Price_value=0.0
            PnL=float(Price_value)*int(swaps_ticks_val)*float(volume_value)
            PnL=round(PnL,3)
        


    
    
    start_date=start_date_value.strftime('%d-%b-%y')
    end_date=end_date_value.strftime('%d-%b-%y')
    
   

 
    

    try:
        if (physical_unit_entry.get()=='Select' or Port_entry_value=='Select' or Terminal_entry_value=='Select'  or Container_value=="Select" or Counter_party_value=='Select' or strategy_value=='Select' or kbbl_value == "" and kMT_value == "" or holiday_value=='Select' or Start_date.get()=="" or product_value=='Select' or End_date.get()==""  or Pricing_contract_value=="Select"):
            messagebox.showerror("Information", "Some fields left blank")
        else:

            kgl=1
            cursor.execute("INSERT INTO PHYSICAL_BLOTTER (DATE,TRADER,COUNTER_PARTY,BOOK,STRATEGY,DERIVATIVE,PRODUCT,PRICING_CONTRACT,kbbl,kMT,PRICING_METHOD,PREMIUM_DISCOUNT,PRICING_TERM,BL_DATE,START_DATE,END_DATE,HOLIDAY,UNIT,TOTAL_DAYS,PRICED_DAYS,UNPRICED_DAYS,TOTAL_VOLUME,PRICED_VOLUME,UNPRICED_VOLUME,POSITION,PRICED_PRICE,UNPRICED_PRICE,CONV_kbbl_MT,CONV_MT_kbbl,NOTES,kgal,Container,Port,Terminal,Vessel_Name,Tank_Number,External_Terminal,Shore_Received,Difference,Nominated_qty,Density,PnL)VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(date_value,trader_value,Counter_party_value,book_value,strategy_value,derivative_value,product_value,Pricing_contract_value,kbbl_value,kMT_value,pricing_method_value,premium_discount_value,pricing_term_value,bl_date_value,start_date,end_date,holiday_value,physical_unit,total_swap_days,priced_days,unpriced_days,t_prx,priced_volume,un_priced_volume,position_value,priced_price,unpriced_price,conv_kbbl__MT,conv_MT__kbbl,notes_value,kgl,Container_value,Port_entry_value,Terminal_entry_value,Vessel_name_value,Tank_number_value,Truck_plate_value,0.0,0.0,nominated_qty_value,density_value,PnL,))
            
            physical_tree.insert("", 'end',  values=(date_value,trader_value,Counter_party_value,book_value,strategy_value,derivative_value,product_value,Pricing_contract_value,kbbl_value,kMT_value,pricing_method_value,premium_discount_value,pricing_term_value,bl_date_value,start_date,end_date,holiday_value,physical_unit,total_swap_days,priced_days,unpriced_days,t_prx,priced_volume,un_priced_volume,position_value,priced_price,unpriced_price,conv_kbbl__MT,conv_MT__kbbl,Container_value,Port_entry_value,Terminal_entry_value,Vessel_name_value,Tank_number_value,Truck_plate_value,notes_value,0.0,0.0,nominated_qty_value,density_value,PnL))
            my_conn.commit()
           
            messagebox.showinfo("Information", "Records inserted successfully")
            clear()
    except:
        messagebox.showerror("error",'Please check all fields, *Exp Month')
        raise
        
def delete():
    try:
    
        selected_physical = physical_tree.selection()[0]
        selected_physical_=physical_tree.item(selected_physical)## get selected item
    except:
        messagebox.showinfo("Information", "Select a record to delete")
        raise
        
   
    result =messagebox.askyesno("Confirm","Are you sure what to delete?")
    if str(result)=='True':
        physical_tree.delete(selected_physical)
        print(selected_physical_)

        date = selected_physical_['values'][0]
        trader=selected_physical_['values'][1]
        counter_party=selected_physical_['values'][2]
        book_entry_value=selected_physical_['values'][3]
        strat_entry_value=selected_physical_['values'][4]
        derivative_var_value=selected_physical_['values'][5]
        Product_entry_value=selected_physical_['values'][6]
        contract_entry_value=selected_physical_['values'][7]
        kbbl_entry_value=selected_physical_['values'][8]
        kMT_entry_value=selected_physical_['values'][9]
        pricing_method_value=selected_physical_['values'][10]
        premium_discount_value=selected_physical_['values'][11]
        pricing_term_value=selected_physical_['values'][12]
        bl_date_entry_value=selected_physical_['values'][13]
        start_date_entry_value=selected_physical_['values'][14]
        end_date_entry_value=selected_physical_['values'][15]
        holiday_entry_value=selected_physical_['values'][16]
        unit_value=selected_physical_['values'][17]
        total_days_value=selected_physical_['values'][18]
        priced_days_value=selected_physical_['values'][19]
        unpriced_days_value=selected_physical_['values'][20]
        total_volume_value=selected_physical_['values'][21]
        priced_volume_value=selected_physical_['values'][22]
        unpriced_volume_value=selected_physical_['values'][23]
        position_value=selected_physical_['values'][24]
        priced_price_value=selected_physical_['values'][25]
        unpriced_price_value=selected_physical_['values'][26]
        cov_bbl_value=selected_physical_['values'][27]
        cov_MT_value=selected_physical_['values'][28]
        Container_value_dlt=selected_physical_['values'][29]
        port_value_dlt=selected_physical_['values'][30]
        terminal_value_dlt=selected_physical_['values'][31]
        vessel_name_dlt=selected_physical_['values'][32]
        tank_number_dlt=selected_physical_['values'][33]
        truck_plate_dlt=selected_physical_['values'][34]
        
        
        notes_value=selected_physical_['values'][35]
        nominated_qty_sel=selected_physical_['values'][38]
        density_sel=selected_physical_['values'][39]
        
        cursor.execute('DELETE FROM PHYSICAL_BLOTTER WHERE DATE=? AND TRADER=? AND COUNTER_PARTY=? AND BOOK=? AND STRATEGY=? AND DERIVATIVE=? AND  PRODUCT=? AND PRICING_CONTRACT=? AND kbbl=? AND kMT=? AND PRICING_METHOD=? AND PREMIUM_DISCOUNT=? AND PRICING_TERM=? AND BL_DATE=? AND START_DATE=? AND END_DATE=? AND HOLIDAY=? AND UNIT=? AND TOTAL_DAYS=? AND  PRICED_DAYS=? AND UNPRICED_DAYS=? AND TOTAL_VOLUME=? AND PRICED_VOLUME=? AND UNPRICED_VOLUME=? AND POSITION=? AND  PRICED_PRICE=? AND UNPRICED_PRICE=? AND CONV_kbbl_MT=? AND CONV_MT_kbbl=? AND Container=? AND Port=? AND Terminal=? AND Vessel_Name=? AND Tank_Number=? AND External_Terminal=? AND NOTES=? AND Nominated_qty=? AND Density=?',(date,trader,counter_party,book_entry_value,strat_entry_value,derivative_var_value,Product_entry_value,contract_entry_value,kbbl_entry_value,kMT_entry_value,pricing_method_value,premium_discount_value,pricing_term_value,bl_date_entry_value,start_date_entry_value,end_date_entry_value,holiday_entry_value,unit_value,total_days_value,priced_days_value,unpriced_days_value,total_volume_value,priced_volume_value,unpriced_volume_value,position_value,priced_price_value,unpriced_price_value,cov_bbl_value,cov_MT_value,Container_value_dlt,port_value_dlt,terminal_value_dlt,vessel_name_dlt,tank_number_dlt,truck_plate_dlt,notes_value,nominated_qty_sel,density_sel))

        if cursor.rowcount > 0:
            messagebox.showinfo("Information","Data Deleted Successfully")
            my_conn.commit()

        else:
            messagebox.showinfo("Information","Deletion failed")
        clear()
def update():
    try:
    
        selected_physical = physical_tree.selection()[0]
        selected_physical_=physical_tree.item(selected_physical,'values')## get selected item
    except:
        messagebox.showinfo("Information", "Select a record to Update")
        raise
    
    result =messagebox.askyesno("Confirm","Are you sure what to update?")
    if str(result)=='True':

        date = selected_physical_[0]
        trader=selected_physical_[1]
        counter_party=selected_physical_[2]
        book_entry_value=selected_physical_[3]
        strat_entry_value=selected_physical_[4]
        derivative_var_value=selected_physical_[5]
        Product_entry_value=selected_physical_[6]
        contract_entry_value=selected_physical_[7]
        kbbl_entry_value=selected_physical_[8]
        kMT_entry_value=selected_physical_[9]
        pricing_method_value=selected_physical_[10]
        premium_discount_edit=selected_physical_[11]
        pricing_term_edit=selected_physical_[12]
        bl_date_edit=selected_physical_[13]
        start_date_edit=selected_physical_[14]
        end_date_edit=selected_physical_[15]
        holiday_edit=selected_physical_[16]
        cov_bbl_edit=selected_physical_[27]
        cov_MT_edit=selected_physical_[28]
        Container_edit=selected_physical_[29]
        port_edit=selected_physical_[30]
        terminal_edit=selected_physical_[31]
        vessel_name_edit=selected_physical_[32]
        tank_name_edit=selected_physical_[33]
        truck_plate_edit=selected_physical_[34]
        notes_edit=selected_physical_[35]
        shore_received_edit=selected_physical_[36]
        difference_edit=selected_physical_[37]
        Nominated_qty_edit=selected_physical_[38]
        Density_edit=selected_physical_[39]

        
        date_update=selected_physical_[0]
        trader_update=Trader.get()
        Counter_update=Counter_party.get()
        book_update=book_entry.get()
        strategy_update=strat_entry.get()
        derivative_update=derivative_var.get()
        product_update=Product_entry.get()
        Pricing_contract_update=Pricing_contract_entry.get()
        kbbl_update=kbbl_entry.get()
        kMT_update=kMT_entry.get()
        pricing_method_update=pricing_method_entry.get()
        premium_discount_update=premium_discount.get()
        pricing_term_update=pricing_term_entry.get()
        holiday_update=Holiday_entry.get()
        Container_update=Container_entry.get()
        
        port_update=Port_entry.get()
        terminal_update=Terminal_entry.get()
        vessel_name_update=Container_Vessel.get()
        tank_number_update=Container_Tank.get()
        truck_plate_update=Container_Truck.get()

        notes_update=Notes.get()
        nominated_qty_update=nominated_qty.get()
        density_update=density.get()
        
        try:
            density_update=density.get()
            density_update=float(density_update)
        except:    
            messagebox.showerror("error",'Enter Numeric Value for Density')
            raise

        
        
        if kbbl_entry.get()!='' and kMT_entry.get()!='':
            try:
                kbbl_inp=float(kbbl_entry.get())
                kmt_inp=float(kMT_entry.get())
                
                conv_kbbl__MT_update=float(kbbl_entry.get())/float(kMT_entry.get())
                conv_kbbl__MT_update=round(conv_kbbl__MT_update,2)

                conv_MT__kbbl_update=float(kMT_entry.get())/float(kbbl_entry.get())
                conv_MT__kbbl_update=round(conv_MT__kbbl_update,2)

                Volume_value_update=kbbl_entry.get()
            except Exception as exception:
                messagebox.showerror("error",'Enter integer for kbbl and KMT') 
                raise ("error in kbbl and KMT")
        
        elif kbbl_entry.get()!='' and kMT_entry.get()=='':
            try:
                kbbl_inp=float(kbbl_entry.get())
            
                conv_kbbl__MT_update=kbbl_entry.get()
                conv_MT__kbbl_update=''
            
                Volume_value_update=kbbl_entry.get()
                
            except Exception as exception:
                messagebox.showerror("error",'Enter float for kbbl') 
                raise ("error in kbbl")


        elif kbbl_entry.get()=='' and kMT_entry.get()!='':
            try:
                kmt_inp=float(kMT_entry.get())
                conv_kbbl__MT_update=''
                conv_MT__kbbl_update=kMT_entry.get()
                Volume_value_update=kMT_entry.get()
                
            except Exception as exception:
                messagebox.showerror("error",'Enter integer for KMT') 
                raise ("error in KMT")


        elif kbbl_entry.get()=='' and kMT_entry.get()=='':
            messagebox.showerror("error",'Enter the volume in kbbl or KMT')

        print(conv_kbbl__MT_update,conv_MT__kbbl_update,Volume_value_update,)

        
        
        
        
        
        try:
            bl_day_update='01'
            bl_slash_update = '/'
            bl_hyphen='-'
            if bl_date.get()=='' :
                bl_date_value_update=''
                print("unpade",bl_date_value_update)
            else:
                if bl_date.get()!='':
                    bl_date_entry_update=bl_date.get()


                if bl_slash_update in bl_date_entry_update:
                      bl_reg_update=bl_slash_update
                else:
                    if bl_hyphen in bl_date_entry_update:
                        bl_reg_update=bl_hyphen
                print(bl_reg_update)

                if (len(bl_date_entry_update)>6):
                    bl_date_value_update=bl_date.get()

                elif (len(bl_date_entry_update)<=6):
                    bl_counter_update = bl_date_entry_update.count(bl_reg_update)
                    print("6")
                    if bl_counter_update==2:
                        print("2")
                        try:
                            bl_date_entry_update==bl_date.get()
                            if bl_reg_update=='/':
                                bl_date_formatted_update = datetime.strptime(bl_date_entry_update, '%d/%m/%y')
                                bl_date_value_update=bl_date_formatted_update.strftime('%d/%m/%y')
                            elif bl_reg_update=='-':
                                bl_date_formatted_update = datetime.strptime(bl_date_entry_update, '%d-%m-%y')
                                bl_date_value_update=bl_date_formatted_update.strftime('%d-%m-%y')
                                print("2",bl_date_value_update)
                        except ValueError as e:
                            print(e)
                            pass
                    elif bl_counter_update==1:
                        bl_date_entry_update=bl_date.get()
                        bl_date_value_update=bl_day_update+bl_reg_update+bl_date_entry_update
                        print("else",bl_date_value_update)


            if bl_date.get()!='':
                bl_date_formats_dates_update = ['%d-%m-%y','%d/%m/%y','%d-%b-%y','%d/%b/%y']
                for bl_date_format_update in bl_date_formats_dates_update:
                    try:
                        bl_date_formatted_update = datetime.strptime(bl_date_value_update, bl_date_format_update)
                        bl_date_value_update=bl_date_formatted_update.strftime('%d-%b-%y')
                        print("error check",bl_date_value_update)

                        break
                    except ValueError as e:
                        pass
                bl_date_error_up_check=datetime.strptime(bl_date_value_update, '%d-%b-%y')
                print(bl_date_error_up_check)
        except Exception as exception:
            messagebox.showerror("error",'Check bl date format') 
            raise ("error in bl date")
        
        bl_date_update=bl_date_value_update
        
        
        try:
            st_day_update='01'
            st_slash_update = '/'
            st_hyphen_update='-'

            try:
                len_start_mon_up=len(Start_date.get())
                x=6/(len_start_mon_up)
                st_date_entry_update=Start_date.get()    

            except Exception as exception:
                messagebox.showerror("error",'Enter Start_date') 
                raise ("error in Start_date")


            if st_slash_update in st_date_entry_update:
                st_reg_update=st_slash_update
            else:
                if st_hyphen_update in st_date_entry_update:
                    st_reg_update=st_hyphen_update
            print(st_reg_update)

            if (len(st_date_entry_update)>6):
                st_date_value_update=Start_date.get()

            elif (len(st_date_entry_update)<=6):
                start_counter_update = st_date_entry_update.count(st_reg_update)
                print("6")
                if start_counter_update==2:
                    print("2")
                    try:
                        st_date_entry_update=Start_date.get()
                        if st_reg_update=='/':
                            start_date_formatted_up = datetime.strptime(st_date_entry_update, '%d/%m/%y')
                            st_date_value_update=start_date_formatted_up.strftime('%d/%m/%y')
                        elif st_reg_update=='-':
                            start_date_formatted_up = datetime.strptime(st_date_entry_update, '%d-%m-%y')
                            st_date_value_update=start_date_formatted_up.strftime('%d-%m-%y')
                            print("2",st_date_value_update)
                    except ValueError as e:
                        print(e)
                        pass

                elif start_counter_update==1:
                    st_date_entry_update=Start_date.get()
                    st_date_value_update=st_day_update+st_reg_update+st_date_entry_update
                    print("else",st_date_value_update)

            if Start_date.get()!='':
                formats_date_up = ['%d-%m-%y','%d/%m/%y','%d-%b-%y','%d/%b/%y']
                for date_format_up in formats_date_up:
                    try:
                        
                        start_date_formatted_up = datetime.strptime(st_date_value_update, date_format_up)
                        st_date_value_update=start_date_formatted_up.strftime('%d-%b-%y').upper()
                        print('update',st_date_value_update)

                        break
                    except ValueError as e:
                        pass
            elif Start_date.get()=='':
                messagebox.showerror("error",'Enter start date')
        except Exception as exception:
            messagebox.showerror("error",'Check start date format') 
            raise ("error in start date")
        print('update',st_date_value_update,'++++++++++++')
        
        
        
        
        
        try:
            end_day_up='01'
            end_slash_up = '/'
            end_hyphen_up='-'

            try:
                len_end_mon_up=len(End_date.get())
                y=6/(len_end_mon_up)
                end_date_entry_update=End_date.get()  

            except :
                messagebox.showerror("error",'Enter End_date') 
                raise ("error in End_date")

            if end_slash_up in end_date_entry_update:
                end_reg_update=end_slash_up
            else:
                if end_hyphen_up in end_date_entry_update:
                    end_reg_update=end_hyphen_up
            print(end_reg_update)

            if (len(end_date_entry_update)>6):
                end_date_value_update=End_date.get()
                print(end_date_value_update)

            elif (len(end_date_entry_update)<=6):
                end_counter_up = end_date_entry_update.count(end_reg_update)
                print("6")
                if end_counter_up==2:
                    print("2")
                    try:
                        end_date_entry_update=End_date.get()
                        if end_reg_update=='/':
                            end_date_formatted_up = datetime.strptime(end_date_entry_update, '%d/%m/%y')
                            end_date_value_update=end_date_formatted_up.strftime('%d/%m/%y')
                        elif end_reg_update=='-':
                            end_date_formatted_up = datetime.strptime(end_date_entry_update, '%d-%m-%y')
                            end_date_value_update=end_date_formatted_up.strftime('%d-%m-%y')
                            print("2",end_date_value_update)
                    except ValueError as e:
                        print(e)
                        pass

                elif end_counter==1:
                    end_date_entry_update=End_date.get()
                    end_date_value_update=end_day_up+end_reg_update+end_date_entry_update
                    print("else",end_date_value_update)

            if End_date.get()!='':
                formats_date_end_up = ['%d-%m-%y','%d/%m/%y','%d-%b-%y','%d/%b/%y']
                for date_format_end_up in formats_date_end_up:
                    try:
                        end_date_formatted_up = datetime.strptime(end_date_value_update, date_format_end_up)
                        end_date_value_update=end_date_formatted_up.strftime('%d-%b-%y').upper()
                        print(end_date_value_update)
                        break
                    except ValueError as e:
                        pass
            elif End_date.get()=='':
                messagebox.showerror("error",'Enter End date')

        except Exception as exception:
            messagebox.showerror("error",'Check end date format') 
            raise ("error in end date")
            
        try:
            if Start_date.get()!='' and End_date.get()!='':
                today_update=datetime.strptime(date_update, "%d-%b-%y")
                st_date_value_update=datetime.strptime(st_date_value_update, "%d-%b-%y")
                end_date_value_update=datetime.strptime(end_date_value_update, "%d-%b-%y")

                print(st_date_value_update)
                print(end_date_value_update)

        except Exception as exception:
    #         raise ("error in start date")
            messagebox.showerror("error",'Check date format') 
            raise ("error in date")

        if st_date_value_update<=end_date_value_update:


            business_days_update = len(pd.bdate_range(st_date_value_update,end_date_value_update))
            print("Total business days in range : " + str(business_days_update))
        else:
            messagebox.showerror("error",'end_date should be greater than start date') 

        physical_holiday_data = pd.read_sql('SELECT * FROM HOLIDAY_SETTINGS', my_conn)
        my_conn.commit()
        physical_holiday_data.Date=pd.to_datetime(physical_holiday_data.Date)
        holiday_search=physical_holiday_data[(physical_holiday_data["Date"] >= st_date_value_update) & (physical_holiday_data["Date"] <= end_date_value_update) & (physical_holiday_data['Holiday_type'] == holiday_update)]


        holidays_update=len(holiday_search)
        print("holidays_update in between start and end",holidays_update)
        total_days_edit=selected_physical_[18]
        print('total_days_edit',total_days_edit)
        total_physical_days_update=business_days_update-holidays_update
        print("total physical days",total_physical_days_update)



        end_date_value_update=end_date_value_update
        st_date_value_update=st_date_value_update

        print(st_date_value_update)
        print(end_date_value_update)
        print(today_update)



        if today_update <= st_date_value_update:
            print("first")

            unpriced_days_update=total_physical_days_update
            priced_days_update=0
            
            print(unpriced_days_update)
            print(priced_days_update)
            
            
            priced_days_edit=selected_physical_[19]
            unpriced_days_edit=selected_physical_[20]
            print(priced_days_edit)
            print(unpriced_days_edit)


        elif (today_update > st_date_value_update) and (today_update<=end_date_value_update):

            business_days_update = len(pd.bdate_range(today_update,end_date_value_update))
            print("second")
            holiday_search=physical_holiday_data[(physical_holiday_data["Date"] >= today_update) & (physical_holiday_data["Date"] <= end_date_value_update) &(physical_holiday_data['Holiday_type'] == holiday_update)]
            holidays_update_from_tday=len(holiday_search)
            print("business_days_update",business_days_update)
            print("holidays_update_from_tday",holidays_update_from_tday)
            unpriced_days_update=business_days_update-holidays_update_from_tday
            priced_days_update=int(total_physical_days_update)-unpriced_days_update
            print(unpriced_days_update)
            print(priced_days_update)
            
            priced_days_edit=selected_physical_[19]
            unpriced_days_edit=selected_physical_[20]
            print(priced_days_edit)
            print(unpriced_days_edit)



        elif today_update > end_date_value_update:
            unpriced_days_update=0
            priced_days_update=int(total_physical_days_update)
            print(unpriced_days_update)
            print(priced_days_update)
 
            
            priced_days_edit=selected_physical_[19]
            unpriced_days_edit=selected_physical_[20]
            print(priced_days_edit)
            print(unpriced_days_edit)
            
        
        total_volume_edit=selected_physical_[21]
        priced_volume_edit=selected_physical_[22]
        unpriced_volume_edit=selected_physical_[23]
        position_edit=selected_physical_[24]
        priced_price_edit=selected_physical_[25]
        unpriced_price_edit=selected_physical_[26]




        if pricing_method_entry.get()=="Fixed":
            if end_date_value_update==st_date_value_update:
                t_prx_update=Volume_value_update
                priced_volume_update=Volume_value_update
                un_priced_volume_update=0
                position_update=priced_volume_update
                premium_discount_update=premium_discount.get()
                priced_price_update=premium_discount_update
                unpriced_price_update='-'
            else:
                messagebox.showerror("error",'Start and end date should be same for Fixed')
                raise
                
            

        elif pricing_method_entry.get()=="Float":
            premium_discount_update=premium_discount.get()

            print(priced_days_update)
            print(unpriced_days_update)
            print(total_physical_days_update)
            
            try:
                priced_vol_up=(float(Volume_value_update)/float(total_physical_days_update))*priced_days_update
            except ZeroDivisionError:
                messagebox.showerror("error",'end_date should be greater than start date')
            
            priced_volume_update=round(priced_vol_up,2)
            
            un_priced_volume_update=(float(Volume_value_update)/float(total_physical_days_update))*unpriced_days_update
            un_priced_volume_update=round(un_priced_volume_update,2)
            print(priced_volume_update)
            print(un_priced_volume_update)
            
            t_prx_update=Volume_value_update
    #         t_prx_update=round(t_prx_update,2)
            print("total_volume",t_prx_update)
            
            position_update=priced_volume_update
            print(position_update)
            
            priced_price_update=premium_discount_update
            print(priced_price_update)
            
            unpriced_price_update='-'
            print(unpriced_price_update)
            
        physical_unit_update=physical_unit_entry.get()    
        unit_edit=selected_physical_[17]

        
        st_date_value_update=st_date_value_update.strftime('%d-%b-%y')
        end_date_value_update=end_date_value_update.strftime('%d-%b-%y')
        
        try:
            if (physical_unit_entry.get()=='Select' or Container_update=='Select' or Counter_update=='Select' or strategy_update=='Select'or product_update=='Select' or Pricing_contract_update=='Select' or kbbl_update=='' and kMT_update=='' or pricing_method_update=='Select' or st_date_value_update=='' or end_date_value_update=='' or holiday_update=='Select'):
                messagebox.showerror("Information", "Some fields left blank")
                raise
            else:
                cursor.execute('UPDATE PHYSICAL_BLOTTER SET DATE=?, TRADER=? ,COUNTER_PARTY=?, BOOK=?,  STRATEGY=?, DERIVATIVE=?,PRODUCT=? , PRICING_CONTRACT=? , kbbl=? , kMT=?, PRICING_METHOD=? , PREMIUM_DISCOUNT=? ,PRICING_TERM=? ,BL_DATE=?,START_DATE=? , END_DATE=? ,HOLIDAY=? , UNIT=?,TOTAL_DAYS=?,PRICED_DAYS=? , UNPRICED_DAYS=?, TOTAL_VOLUME=? , PRICED_VOLUME=? , UNPRICED_VOLUME=? , POSITION=? , PRICED_PRICE=? , UNPRICED_PRICE=?,CONV_kbbl_MT=?,CONV_MT_kbbl=?,Container=?,Port=? ,Terminal=? ,Vessel_Name=? ,Tank_Number=? ,External_Terminal=?,NOTES=?,Nominated_qty=?,Density=?  WHERE DATE=? AND TRADER=? AND COUNTER_PARTY=? AND BOOK=? AND STRATEGY=? AND DERIVATIVE=? AND PRODUCT=? AND PRICING_CONTRACT=? AND kbbl=? AND kMT=? AND PRICING_METHOD=? AND PREMIUM_DISCOUNT=? AND PRICING_TERM=? AND BL_DATE=? AND START_DATE=? AND END_DATE=? AND HOLIDAY=? AND UNIT=? AND TOTAL_DAYS=? AND  PRICED_DAYS=? AND UNPRICED_DAYS=? AND TOTAL_VOLUME=? AND PRICED_VOLUME=? AND UNPRICED_VOLUME=? AND POSITION=? AND PRICED_PRICE=? AND UNPRICED_PRICE=? AND CONV_kbbl_MT=? AND CONV_MT_kbbl=? AND Container=? AND Port=? AND Terminal=? AND Vessel_Name=? AND Tank_Number=? AND External_Terminal=? AND NOTES=? AND Nominated_qty=? AND Density=?' , (date_update,trader_update,Counter_update,book_update,strategy_update,derivative_update,product_update,Pricing_contract_update,kbbl_update,kMT_update,pricing_method_update,premium_discount_update,pricing_term_update,bl_date_update,st_date_value_update,end_date_value_update,holiday_update,physical_unit_update,total_physical_days_update,priced_days_update,unpriced_days_update,t_prx_update,priced_volume_update,un_priced_volume_update,position_update,priced_price_update,unpriced_price_update,conv_kbbl__MT_update,conv_MT__kbbl_update,Container_update,port_update,terminal_update,vessel_name_update,tank_number_update,truck_plate_update,notes_update,nominated_qty_update,density_update,date,trader,counter_party,book_entry_value,strat_entry_value,derivative_var_value,Product_entry_value,contract_entry_value,kbbl_entry_value,kMT_entry_value,pricing_method_value,premium_discount_edit,pricing_term_edit,bl_date_edit,start_date_edit,end_date_edit,holiday_edit,unit_edit,total_days_edit,priced_days_edit,unpriced_days_edit,total_volume_edit,priced_volume_edit,unpriced_volume_edit,position_edit,priced_price_edit,unpriced_price_edit,cov_bbl_edit,cov_MT_edit,Container_edit,port_edit,terminal_edit,vessel_name_edit,tank_name_edit,truck_plate_edit,notes_edit,Nominated_qty_edit,Density_edit))
                my_conn.commit()

                physical_tree.item(selected_physical, text="", values=(date_update,trader_update,Counter_update,book_update,strategy_update,derivative_update,product_update,Pricing_contract_update,kbbl_update,kMT_update,pricing_method_update,premium_discount_update,pricing_term_update,bl_date_update,st_date_value_update,end_date_value_update,holiday_update,physical_unit_update,total_physical_days_update,priced_days_update,unpriced_days_update,t_prx_update,priced_volume_update,un_priced_volume_update,position_update,priced_price_update,unpriced_price_update,conv_kbbl__MT_update,conv_MT__kbbl_update,Container_update,port_update,terminal_update,vessel_name_update,tank_number_update,truck_plate_update,notes_update,shore_received_edit,difference_edit,nominated_qty_update,density_update))
                messagebox.showinfo("Information","Data Updated Successfully")
                clear()
        except:
            messagebox.showerror("error",'Please check all fields')
            raise

                
        
def port_select(e):
    Port_entry.set('Select')
    Terminal_entry.set('Select')
    Container_Tank.set('Select')
    Container_Vessel.delete(0,END)
    Container_Truck.delete(0,END)

    if Container_entry.get()=="Tank":
        Container_Vessel.config(state= "disabled")
        Container_Tank.config(state= "normal")
        
        port_values = pd.read_sql_query('SELECT * FROM TANK_CAPACITY', my_conn)
        port_values=port_values['Port'].unique().tolist()
        Port_entry.config(values=(port_values))
    
    elif  Container_entry.get()=="Vessel" :
        Container_Tank.config(state= "disabled")
        Container_Vessel.config(state= "normal")
            

        Ports=()
        cursor.execute("SELECT DISTINCT  Port FROM PORT")
        Ports_select = cursor.fetchall()
        for x in Ports_select:
            Ports+=tuple(x)
        Port_entry.config(values=(Ports))   
        


def terminal_select(e):
    Terminal_entry.set('Select')
    Container_Tank.set('Select')
#     Container_id_entry.delete(0,END)
    if Container_entry.get()=='Tank' or  Container_entry.get()=='PLT':
        port_selected=Port_entry.get()
        port_values = pd.read_sql_query('SELECT * FROM TANK_CAPACITY', my_conn)
        select_terminal = port_values.loc[port_values['Port'] == port_selected] 
        terminal_values=select_terminal['Terminal'].unique().tolist()
        Terminal_entry.config(values=(terminal_values))
    
    elif Container_entry.get()=="Vessel" or Container_entry.get()=="Truck":
        
        Terminals=()
        cursor.execute("SELECT DISTINCT  Terminal FROM TERMINAL")
        terminals_select = cursor.fetchall()
        for x in terminals_select:
            Terminals+=tuple(x)
        Terminal_entry.config(values=(Terminals))    

        
            
        
def tank_no_select(e):
    Container_Tank.set('Select')
    if Container_entry.get()=="Tank" or Container_entry.get()=="PLT"  :
        port_selected=Port_entry.get()
        terminal_selected=Terminal_entry.get()
        tank_values = pd.read_sql_query('SELECT * FROM TANK_CAPACITY', my_conn)
        
        select_tank_no = tank_values.loc[(tank_values['Port'] == port_selected) & (tank_values['Terminal'] == terminal_selected) ] 
        print(tank_values)
        Tank_Num_values=select_tank_no['Tank_Num'].unique().tolist()
        Container_Tank.config(values=(Tank_Num_values))


        
        
def purchace_sales_raise(frame):
    frame.tkraise()
    purchase_contract_entry.set('Select')
    purchase_strategy_entry.delete(0,END)
    

        
        
def purchace_sales_details(e):
    
    purchase_contract_selected=purchase_contract_entry.get()
    
    physical_pricing_contract_df = pd.read_sql_query('SELECT * FROM PHYSICAL_BLOTTER WHERE PRICING_CONTRACT = (?) ' , my_conn,params=(purchase_contract_selected,))
    physical_contract_reference_num=physical_pricing_contract_df['STRATEGY'].unique().tolist()
    physical_contract_reference_num=' '.join(map(str,  physical_contract_reference_num))
    purchase_strategy_entry.delete(0,END)
    purchase_strategy_entry.insert(0,physical_contract_reference_num)
    

    head=Label(f5, text="Purchase and Sales Details of Cargo", font=('Times',16,'bold'),bg="#4CAF50",fg='white')
    head.place(x=20,y=130)
    
    head2=Label(f5, text="Inventory Tranfer Details", font=('Times',16,'bold'),bg="#4CAF50",fg='white')
    head2.place(x=20,y=430)

    purchase_sale_frame=Frame(f5, relief=SOLID,bg='white')
    purchase_summary_tree = ttk.Treeview(purchase_sale_frame, show="headings",selectmode='browse',style="mystyle.Treeview",height=10)
    purchase_summary_tree.tag_configure('odd', background='#FFEFD5')
    purchase_summary_tree.tag_configure('even', background='white')
    purchase_summary_tree.grid(row=1, columnspan=1)
   

    
    



    purchace_summary_df   = pd.read_sql_query('SELECT * FROM PHYSICAL_BLOTTER WHERE STRATEGY = (?) ' , my_conn,params=(physical_contract_reference_num,))

    purchace_summary_df=purchace_summary_df.drop(['kgal','kl','kcbm'], axis=1)
    print('+++',purchace_summary_df)

    my_conn.commit()
    purchace_summary_df=purchace_summary_df[['DATE', 'TRADER', 'COUNTER_PARTY', 'BOOK', 'STRATEGY', 'DERIVATIVE','PRODUCT', 'PRICING_CONTRACT', 'kbbl', 'kMT', 'PRICING_METHOD','PREMIUM_DISCOUNT', 'PRICING_TERM', 'BL_DATE', 'START_DATE', 'END_DATE','HOLIDAY', 'UNIT', 'TOTAL_DAYS', 'PRICED_DAYS', 'UNPRICED_DAYS','TOTAL_VOLUME', 'PRICED_VOLUME', 'UNPRICED_VOLUME', 'POSITION','PRICED_PRICE', 'UNPRICED_PRICE', 'CONV_kbbl_MT', 'CONV_MT_kbbl',"Container",'Port','Terminal','Vessel_Name','Tank_Number','External_Terminal','NOTES','Shore_Received','Difference','Nominated_qty','Density']]
    purchace_summary_df.columns = ['Date', 'Trader', 'Counter Party', 'Book', 'Strategy', 'Derivative', 'Product', 'Pricing Contract', 'kbbl', 'kMT', 'Pricing Method', 'Premium_Discount', 'Pricing Term', 'Bl_Date', 'Start Date', 'End Date', 'Holiday', 'Unit', 'Total Days', 'Priced Days', 'Unpriced Days', 'Total Volume', 'Priced Volume', 'Unpriced Volume', 'Position', 'Priced Price', 'Unpriced Price', 'CONV_kbbl_MT', 'CONV_MT_kbbl', "Container",'Port','Terminal','Vessel_Name','Tank_Number','External_Terminal','Notes','Shore_Received','Difference','Nominated_qty','Density']
    cols = list(purchace_summary_df.columns)
    purchase_summary_tree["columns"] = cols
    purchase_summary_tree["show"] = "headings"
    

    for i in cols:
        purchase_summary_tree.column(i,width = 43, minwidth = 120)

        purchase_summary_tree.column(i, anchor="center")
        purchase_summary_tree.heading(i, text=i, anchor='center')
        purchase_summary_tree.bind('<ButtonRelease-1>',physical_blotter_selectItem)

    for item in purchase_summary_tree.get_children():
        purchase_summary_tree.delete(item)

    df_rows_data = purchace_summary_df.to_numpy().tolist() 
    print(df_rows_data)

    for index in range(len(df_rows_data)):
        if index %2==0:
            purchase_summary_tree.insert("",'end',values=df_rows_data[index],tags=('even'))
        else:
            purchase_summary_tree.insert("",'end',values=df_rows_data[index],tags=('odd'))

        # # ----vertical scrollbar------------
    vbar = ttk.Scrollbar(purchase_sale_frame, orient=VERTICAL, command=purchase_summary_tree.yview)
    purchase_summary_tree.configure(yscrollcommand=vbar.set)
    #tree.grid(row=0, column=0, sticky=NSEW)
    vbar.grid(row=1, column=1, sticky=NS)

    # # ----horizontal scrollbar----------
    hbar = ttk.Scrollbar(purchase_sale_frame, orient=HORIZONTAL, command=purchase_summary_tree.xview)
    purchase_summary_tree.configure(xscrollcommand=hbar.set)
    hbar.grid(row=2, column=0, sticky=EW)
    purchase_sale_frame.place(x=20, y=163)
    
    
    purchase_summary_inventory_frame=Frame(f5, relief=SOLID,bg='white')
    
    inventory_summary_tree = ttk.Treeview(purchase_summary_inventory_frame, show="headings",selectmode='browse',style="mystyle.Treeview",height=10)
    inventory_summary_tree.tag_configure('odd', background='#FFEFD5')
    inventory_summary_tree.tag_configure('even', background='white')
    inventory_summary_tree.grid(row=1, columnspan=1)
    
    inventory_summary_data = pd.read_sql_query('SELECT * FROM INVENTORY_TRANSFER WHERE Reference_number=(?) ' , my_conn,params=(physical_contract_reference_num,)) 

    inventory_summary_data=inventory_summary_data[['Date','Source_Container','Source_Name', 'Source_Port', 'Source_Terminal', 'Source_Pricing_Contract','Source_Strategy', 'Source_Product', 'Source_cargo_LD_QTY', 'Source_Unit', 'Source_Price', 'Dest_Container', 'Dest_Trade_Strategy', 'Dest_Port', 'Dest_Terminal', 'Dest_Vessel_Op', 'Dest_Tank_Num', 'Dest_Tank_Density', 'Dest_Cargo_LD_Qty', 'Difference', 'Reference_number']]
    inventory_summary_data.columns=['Date','Source Mode','Source Name', 'Source Port', 'Source Terminal','Source Pricing Contract','Source Strategy', 'Source Cargo', 'Source Transferred Quantity','Source Unit', 'Source Price', 'Destination Mode', 'Destination Reference Number', 'Destination Port', 'Destination Terminal', 'Destination Vessel_name', 'Destination Tank Number', 'Density', 'Received Quantity', 'Difference', 'Reference Number']
    
    
    cols = list(inventory_summary_data.columns)
    inventory_summary_tree["columns"] = cols
    inventory_summary_tree["show"] = "headings" 

    for i in cols:
        inventory_summary_tree.column(i,width = 82, minwidth = 120)

        inventory_summary_tree.column(i, anchor="center")
        inventory_summary_tree.heading(i, text=i, anchor='center')


    for item in inventory_summary_tree.get_children():
        inventory_summary_tree.delete(item)

    inv_rows_data = inventory_summary_data.to_numpy().tolist() 
    print(inv_rows_data)

    for index in range(len(inv_rows_data)):

        if index %2==0:
            inventory_summary_tree.insert("",'end',values=inv_rows_data[index],tags=('even'))
        else:
            inventory_summary_tree.insert("",'end',values=inv_rows_data[index],tags=('odd'))

        # # ----vertical scrollbar------------
    vbar = ttk.Scrollbar(purchase_summary_inventory_frame, orient=VERTICAL, command=inventory_summary_tree.yview)
    inventory_summary_tree.configure(yscrollcommand=vbar.set)
    #tree.grid(row=0, column=0, sticky=NSEW)
    vbar.grid(row=1, column=1, sticky=NS)

    # # ----horizontal scrollbar----------
    hbar = ttk.Scrollbar(purchase_summary_inventory_frame, orient=HORIZONTAL, command=inventory_summary_tree.xview)
    inventory_summary_tree.configure(xscrollcommand=hbar.set)
    hbar.grid(row=2, column=0, sticky=EW)
    purchase_summary_inventory_frame.place(x=20,y=465)

    
    physical = pd.read_sql_query('SELECT * FROM PHYSICAL_BLOTTER WHERE STRATEGY = (?) ' , my_conn,params=(physical_contract_reference_num,))

    physical['Shore_Received'] = physical['Shore_Received'].astype(float)
    physical['Difference'] = physical['Difference'].astype(float)
    physical_purchase=physical[physical['Shore_Received']>0]

    if len(physical_purchase)>0:

        physical_purchased_qty=physical_purchase['TOTAL_VOLUME'].sum()

        shore_received=physical_purchase['Shore_Received'].unique().tolist()
        shore_received_qty=sum(shore_received)

        bill_shore_difference=physical_purchase['Difference'].unique().sum()
        
        print(shore_received)
        print(shore_received_qty)



        sales_value=physical[physical['Shore_Received']<0]
        print('+++++++++++++++++++',sales_value)
        if len(sales_value)>0:
            sales_value_qty=sales_value['Shore_Received'].unique().tolist()
            sales_value_qty=sum(sales_value_qty)
            print('sales_value_qty',sales_value_qty)
        else:
            sales_value_qty=0.0

        
        sum_list=[]
        
        df=physical[physical['Shore_Received']!=0]
        purchase_sale=df['TOTAL_VOLUME'].sum() 
        print(df['TOTAL_VOLUME'])
        print('purchase_sale===',purchase_sale)
        
        purchase_sales_difference=df['Difference'].unique().sum()
        print(purchase_sales_difference)

        purchase_sale_qty=float(purchase_sale)+float(purchase_sales_difference)
        sum_list.append(purchase_sale)
        sum_list.append(purchase_sales_difference)
        
        print('purchase_sale_qty',sum_list)
        floats = [float(x) for x in sum_list]
        
        purchase_sale_qty=sum(floats)
        purchase_sale_qty=round(purchase_sale_qty,4)
        print('purchase_sale_qty',floats)
        print(purchase_sale_qty)
        
        inventory_summary_data = pd.read_sql_query('SELECT * FROM INVENTORY_TRANSFER WHERE Reference_number=(?) ' , my_conn,params=(physical_contract_reference_num,)) 
        
        if len(inventory_summary_data)!=0:

            inventory_diff=inventory_summary_data['Difference']
            inventory_diff=inventory_diff.sum()

        else:
            inventory_diff=0.0
        print(inventory_diff)

        current_qty=float(purchase_sale_qty)+float(inventory_diff)
        print('current_qty',current_qty)
        

#     else:

#         physical_purchased_qty=physical_purchase['TOTAL_VOLUME'].sum()
#         current_qty=physical_purchased_qty
#         remarks='floating'
        
#         print('physical_purchased_qty',physical_purchased_qty)
#         print('shore_received_qty',shore_received_qty)
#         print(bill_shore_difference,'bill_shore_difference')
        
    summary_dict={'Billed Quantity (MT)':[physical_purchased_qty],'Shore Received':[shore_received_qty],'Bill-Shore Difference':[bill_shore_difference],'Sold Quantity':[sales_value_qty],'Inventory Transfer Difference':[inventory_diff],'Remaining Quantity':[current_qty]}
    
    summary_df = pd.DataFrame.from_dict(summary_dict)
    print(summary_df)
    
    
    
    
    
   
    
    summary_frame=Frame(f5, relief=SOLID,bg='white')
    Purchase_summary_label=Label(f5, text="Purchase Summary", font=('Times',16,'bold'),bg="#f2be54",fg='black')
    Purchase_summary_label.place(x=1200,y=12)

    summary_tree = ttk.Treeview(summary_frame, show="headings",selectmode='browse',style="mystyle.Treeview",height=2)
    summary_tree.tag_configure('odd', background='#FFEFD5')
    summary_tree.tag_configure('even', background='white')
    summary_tree.grid(row=1, columnspan=1)

    cols = list(summary_df.columns)
    summary_tree["columns"] = cols
    summary_tree["show"] = "headings" 

    for i in cols:
        summary_tree.column(i,width = 160, minwidth = 155)

        summary_tree.column(i, anchor="center")
        summary_tree.heading(i, text=i, anchor='center')


    for item in summary_tree.get_children():
        summary_tree.delete(item)

    summary_df = summary_df.to_numpy().tolist() 
    print(summary_df)

    for index in range(len(summary_df)):

        if index %2==0:
            summary_tree.insert("",'end',values=summary_df[index],tags=('even'))
        else:
            summary_tree.insert("",'end',values=summary_df[index],tags=('odd'))

        # # ----vertical scrollbar------------
#     vbar = ttk.Scrollbar(summary_frame, orient=VERTICAL, command=summary_tree.yview)
#     summary_tree.configure(yscrollcommand=vbar.set)
#     #tree.grid(row=0, column=0, sticky=NSEW)
#     vbar.grid(row=1, column=1, sticky=NS)

#     # # ----horizontal scrollbar----------
#     hbar = ttk.Scrollbar(summary_frame, orient=HORIZONTAL, command=summary_tree.xview)
#     summary_tree.configure(xscrollcommand=hbar.set)
#     hbar.grid(row=2, column=0, sticky=EW)
    summary_frame.place(x=870,y=50)

    
        

        


        
def download_csv():
    try:
    
        history_download = pd.read_sql('SELECT * FROM PHYSICAL_BLOTTER', my_conn)
        my_conn.commit()


        history_download=history_download[['DATE', 'TRADER', 'COUNTER_PARTY', 'BOOK', 'STRATEGY', 'DERIVATIVE','PRODUCT', 'PRICING_CONTRACT', 'kbbl', 'kMT', 'PRICING_METHOD','PREMIUM_DISCOUNT', 'PRICING_TERM', 'BL_DATE', 'START_DATE', 'END_DATE','HOLIDAY', 'UNIT', 'TOTAL_DAYS', 'PRICED_DAYS', 'UNPRICED_DAYS','TOTAL_VOLUME', 'PRICED_VOLUME', 'UNPRICED_VOLUME', 'POSITION','PRICED_PRICE', 'UNPRICED_PRICE', 'CONV_kbbl_MT', 'CONV_MT_kbbl',"Container",'Port','Terminal','Vessel_Name','Tank_Number','External_Terminal','NOTES','Shore_Received','Difference']]
        history_download.columns = ['Date', 'Trader', 'Counter Party', 'Book', 'Strategy', 'Derivative', 'Product', 'Pricing Contract', 'kbbl', 'kMT', 'Pricing Method', 'Premium_Discount', 'Pricing Term', 'Bl_Date', 'Start Date', 'End Date', 'Holiday', 'Unit', 'Total Days', 'Priced Days', 'Unpriced Days', 'Total Volume', 'Priced Volume', 'Unpriced Volume', 'Position', 'Priced Price', 'Unpriced Price', 'CONV_kbbl_MT', 'CONV_MT_kbbl', "Container",'Port','Terminal','Vessel_Name','Tank_Number','External_Terminal','Notes','Shore_Received','Difference']
        history_download.to_csv('physical_blotter_trade_history.csv')
        messagebox.showinfo("Information", "Physical Blotter Data Downloaded")
    except:
        messagebox.showinfo("Information", "error in  downloading")
        
        
    


for frame in (f1, f2,f3,f4,f5):
    frame.grid(row=1, column=1,pady=10)
    frame.place(x=1,y=36)

heading_frame = Frame(f1,bg="#1AA9D0", relief=SOLID)
Label(heading_frame, text="PHYSICAL  BLOTTER", font = ('Times',16,'bold'), bg='#1AA9D0', fg='white').grid(row=0, column=0, sticky=W, pady=4)
heading_frame.place(x=900,y=10)


pos_heading_frame = Frame(f2,bg="#1AA9D0", relief=SOLID)
Label(pos_heading_frame, text="POSITION", font = ('Times',20,'bold'), bg='#1AA9D0', fg='white').grid(row=0, column=0, sticky=W, pady=4)
pos_heading_frame.place(x=750,y=20)

hist_heading_frame = Frame(f3,bg="#1AA9D0", relief=SOLID)
Label(hist_heading_frame, text="HISTORY", font = ('Times',20,'bold'), bg='#1AA9D0', fg='white').grid(row=0, column=0, sticky=W, pady=4)
hist_heading_frame.place(x=750,y=20)

down_frame=Frame(f3,bg="#1AA9D0", relief=SOLID)
download_btn=Button(down_frame ,text="Download",bg='#388087', pady=3,fg='white',font=('Times', 15),command=download_csv)
download_btn.grid(row=0,column=0)
down_frame.place(x=850,y=750)

# heading.place(x=10,y=10)    
#*********************************Date**********************************************************#
Label(f1_left_frame, text="Date", font=f, bg="White").grid(row=0, column=0, sticky=W, pady=4)
Date = OptionMenu(f1_left_frame, current_date, date_variable)
Date.grid(row=0, column=1, pady=3, padx=20)
Date.config(width=12, font=('Times', 12,'bold'))


#*********************************Trader WIDGET**********************************************************#
Label(f1_left_frame, text="Trader", font=f,bg="White").grid(row=1, column=0, sticky=W, pady=4)
Trader = ttk.Combobox(f1_left_frame, value=(Trader), state='readonly')
Trader.grid(row=1, column=1, pady=3, padx=20)
Trader.config(width=15, font=('Times', 12))

#********************************* Default Trader WIDGET**********************************************************#
cursor.execute("SELECT Default_trader FROM Default_values")
trader_fetch=cursor.fetchall()
for dflt_trader in trader_fetch:
    Trader.set(dflt_trader[0])
Trader.config(width=15, font=('Times', 12))


#********************************* Counter-Party WIDGET**********************************************************#
Label(f1_left_frame, text="Counter-Party", font=f,bg="White").grid(row=2, column=0, sticky=W, pady=4)
Counter_party = ttk.Combobox(f1_left_frame, value=(counter_party_val), state='readonly')
Counter_party.grid(row=2, column=1, pady=3, padx=20)
Counter_party.config(width=15, font=('Times', 12))
Counter_party.set('Select')



#*********************************Book WIDGET**********************************************************#
Label(f1_left_frame, text="Book", font=f,bg="White").grid(row=3, column=0, sticky=W, pady=4)
book_entry = ttk.Combobox(f1_left_frame, value=(book), state='readonly')
book_entry.grid(row=3, column=1, pady=3, padx=20)
book_entry.config(width=15, font=('Times', 12))


#********************************* Default Book WIDGET**********************************************************#
cursor.execute("SELECT Default_book FROM Default_values")
book_fetch=cursor.fetchall()
for dflt_book in book_fetch:
    book_entry.set(dflt_book[0])
book_entry.config(width=15, font=('Times', 12))


#*********************************Strategy WIDGET**********************************************************#
Label(f1_left_frame, text="Strategy", font=f,bg="White").grid(row=4, column=0, sticky=W, pady=4)
strat_entry = ttk.Combobox(f1_left_frame, value=(strategy), state='readonly')
strat_entry.grid(row=4, column=1, pady=3, padx=20)
strat_entry.config(width=15, font=('Times', 12))
strat_entry.set('Select')

#*********************************Derivative WIDGET**********************************************************#
Label(f1_left_frame, text="Derivative", font=f,bg="White").grid(row=5, column=0, sticky=W, pady=4)
derivative_entry = OptionMenu(f1_left_frame, derivative_var, derivative)
derivative_entry.grid(row=5, column=1, pady=3, padx=20)
derivative_entry.config(width=12, font=('Times', 12))

#*********************************Buy/Sell WIDGET**********************************************************#
Label(f1_left_frame, text="Buy/Sell", font=f,bg="White").grid(row=6, column=0, sticky=W, pady=4)

#*********************************Product WIDGET**********************************************************#
Label(f1_left_frame, text="Product", font=f,bg="White").grid(row=7, column=0, sticky=W, pady=4)
Product_entry = ttk.Combobox(f1_left_frame,value=(product),state='readonly')
Product_entry.grid(row=7, column=1, pady=3, padx=20)
Product_entry.config(width=15, font=('Times', 12))
Product_entry.set('Select')

#*********************************Pricing WIDGET**********************************************************#
Label(f1_left_frame, text="Pricing Contract", font=f,bg="White").grid(row=8, column=0, sticky=W, pady=4)
Pricing_contract_entry = ttk.Combobox(f1_left_frame,value=(pricing),state='readonly')
Pricing_contract_entry.grid(row=8, column=1, pady=3, padx=20)
Pricing_contract_entry.config(width=15, font=('Times', 12))
Pricing_contract_entry.set(pricing[0])

Label(f1_left_frame, text="Unit", font=f,bg="White").grid(row=9, column=0, sticky=W, pady=4)
physical_unit_entry = ttk.Combobox(f1_left_frame,value=('MT','BBL','m³'),state='readonly')
physical_unit_entry.grid(row=9, column=1, pady=3, padx=20)
physical_unit_entry.config(width=15, font=('Times', 12))
physical_unit_entry.set('Select')
    
    
Label(f1_left_frame, text="kbbl", font=f,bg="White",).grid(row=10, column=0, sticky=W, pady=4)
kbbl_entry= Entry(f1_left_frame, font=f,bg="White",width=17)
kbbl_entry.grid(row=10, column=1, pady=3, padx=20)
kbbl_entry.bind("<Leave>", lambda e:kbbl_event_tab(e))
kbbl_entry.bind('<Tab>', lambda e: kbbl_event(e))



Label(f1_left_frame, text="kMT", font=f,bg="White",).grid(row=11, column=0, sticky=W, pady=4)
kMT_entry = Entry(f1_left_frame, font=f,bg="White",width=17)
kMT_entry.grid(row=11, column=1, pady=3, padx=20)
kMT_entry.bind("<Leave>", kMT_event_tab)
# kMT_entry.bind('<Tab>', lambda e: kMT_event(e))


Label(f1_left_frame, text="Nominated Quantity", font=f,bg="White",).grid(row=12, column=0, sticky=W, pady=4)
nominated_qty = Entry(f1_left_frame, font=f,bg="White",width=17)
nominated_qty.grid(row=12, column=1, pady=3, padx=20)

Label(f1_left_frame, text="Density", font=f,bg="White",).grid(row=13, column=0, sticky=W, pady=4)
density = Entry(f1_left_frame, font=f,bg="White",width=17)
density.grid(row=13, column=1, pady=3, padx=20)




#*********************************Pricing Term WIDGET**********************************************************#
Label(f1_left_frame, text="Pricing Method", font=f,bg="White").grid(row=14, column=0, sticky=W, pady=4)
pricing_method_entry = ttk.Combobox(f1_left_frame,value=('Float','Fixed'),state='readonly')
pricing_method_entry.grid(row=14, column=1, pady=3, padx=20)
pricing_method_entry.config(width=15, font=('Times', 12))
pricing_method_entry.set('Select')

Label(f1_left_frame, text="Premium Discount / Price", font=f,bg="White",).grid(row=15, column=0, sticky=W, pady=4)
premium_discount = Entry(f1_left_frame, font=f,bg="White",width=17)
premium_discount.grid(row=15, column=1, pady=3, padx=20)


#*********************************Pricing Term WIDGET**********************************************************#
Label(f1_left_frame, text="Pricing Term", font=f,bg="White").grid(row=17, column=0, sticky=W, pady=4)
pricing_term_entry = ttk.Combobox(f1_left_frame,value=(pricing_term_value))
pricing_term_entry.grid(row=17, column=1, pady=3, padx=20)
pricing_term_entry.config(width=15, font=('Times', 12))
pricing_term_entry.set('Select')


Label(f1_left_frame, text=" BL Date", font=f,bg="White").grid(row=16, column=0, sticky=W, pady=4)
bl_date= Entry(f1_left_frame, font=f,bg="White",width=17)
bl_date.grid(row=16, column=1, pady=3, padx=20)



#*********************************Start Date WIDGET**********************************************************#

Label(f1_left_frame, text=" Start Date", font=f,bg="White").grid(row=19, column=0, sticky=W, pady=4)
Start_date= Entry(f1_left_frame, font=f,bg="White",width=17)
Start_date.grid(row=19, column=1, pady=3, padx=20)

#*********************************End Date WIDGET**********************************************************#

Label(f1_left_frame, text=" End Date", font=f,bg="White").grid(row=20, column=0, sticky=W, pady=4)
End_date = Entry(f1_left_frame, font=f,bg="White",width=17)
End_date.grid(row=20, column=1, pady=3, padx=20)

End_date.bind("<Leave>", lambda e:end_date_event_tab(e))


Label(f1_left_frame, text="No of Days", font=f,bg="White",fg="blue").grid(row=18, column=0, sticky=W, pady=4)
# 16

#*********************************Holiday WIDGET**********************************************************#

Label(f1_left_frame, text="Holiday", font=f,bg="White").grid(row=21, column=0, sticky=W, pady=4)
Holiday_entry = ttk.Combobox(f1_left_frame,value=(holiday_set),state='readonly')
Holiday_entry.grid(row=21 ,column=1, pady=3, padx=20)
Holiday_entry.config(width=15, font=('Times', 12))
Holiday_entry.set('Select')


Label(f1_left_frame, text="Delivery Mode", font=f,bg="White").grid(row=22, column=0, sticky=W, pady=4)
Container_entry =ttk.Combobox(f1_left_frame,value=('Vessel','Tank','PLT'),state='readonly')
Container_entry.grid(row=22, column=1, pady=3, padx=20)
Container_entry.config(width=15, font=('Times', 12))
Container_entry.set('Select')
Container_entry.bind("<<ComboboxSelected>>", port_select)


Label(f1_left_frame, text="Port", font=f,bg="White").grid(row=23, column=0, sticky=W, pady=4)
Port_entry = ttk.Combobox(f1_left_frame,state='readonly')
Port_entry.grid(row=23, column=1, pady=3, padx=20)
Port_entry.config(width=15, font=('Times', 12))
Port_entry.bind("<<ComboboxSelected>>", terminal_select)

Label(f1_left_frame, text="Terminal", font=f,bg="White").grid(row=24, column=0, sticky=W, pady=4)
Terminal_entry= ttk.Combobox(f1_left_frame,state='readonly')
Terminal_entry.grid(row=24, column=1, pady=3, padx=20)
Terminal_entry.config(width=15, font=('Times', 12))
Terminal_entry.bind("<<ComboboxSelected>>", tank_no_select)



Label(f1_left_frame, text="Vessel Name", font=f,bg="White").grid(row=25, column=0, sticky=W, pady=4)
Container_Vessel =ttk.Entry(f1_left_frame, font=f,width=17)
Container_Vessel.grid(row=25, column=1, pady=3, padx=20)

Label(f1_left_frame, text="Tank_Number", font=f,bg="White").grid(row=26, column=0, sticky=W, pady=4)
Container_Tank= ttk.Combobox(f1_left_frame,state='readonly')
Container_Tank.grid(row=26, column=1, pady=3, padx=20)
Container_Tank.config(width=15, font=('Times', 12))


Label(f1_left_frame, text="External Terminal", font=f,bg="White").grid(row=27, column=0, sticky=W, pady=4)
Container_Truck= Entry(f1_left_frame, font=f,bg="White",width=17)
Container_Truck.grid(row=27, column=1, pady=3, padx=20)




#*********************************Notes WIDGET**********************************************************#
Label(f1_left_frame, text="Notes", font=f,bg="White").grid(row=28, column=0, sticky=W, pady=4)
Notes = Entry(f1_left_frame, font=f,bg="White",width=17)
Notes.grid(row=28, column=1, pady=3, padx=10)

#*********************************Login button WIDGET**********************************************************#





button_frame=Frame(f1, background="white", width=2000, height=2000)

add_btn = Button(button_frame , width=8, text='Add', bg='#388087',fg='white',font=('Times', 12),command=physical_add)
add_btn.grid(row=29, column=0,sticky=W,padx=10,pady=10)

# ********************************Clear Button************************************************
clear_btn = Button(button_frame , width=8, text='Clear',bg='#388087',fg='white', font=('Times', 12),command=clear)
clear_btn.grid(row=29, column=1,sticky=W,padx=20,pady=10)

# #********************************edit Button************************************************
edit_btn = Button(button_frame, width=8, text='Update', bg='#388087',fg='white', font=('Times', 12),command=update)
edit_btn.grid(row=30, column=0,sticky=W,pady=5,padx=10)

# #************************************Delete button************************************************************#
delete_btn = Button(button_frame ,width=8, text='Delete',  bg='#388087',fg='white',font=('Times', 12),command=delete)
delete_btn.grid(row=30, column=1,sticky=W,padx=20,pady=5)
button_frame.place(x=330,y=880)


def bill_shore_delete():
    
    
    selected_bill =  bill_shore_tree.selection()[0]
    selected_bill_=bill_shore_tree.item(selected_bill)
    print(selected_bill)
    shore_contract_delete = bill_shore_contract_entry.get().strip()
    shore_stat_delete=bill_shore_start_entry.get().strip()
    shore_product_delete = bill_shore_product_entry.get().strip()
    shore_billed_qty_delete = bill_shore_billed_qty_entry.get().strip()
    shore_unit_delete = bill_shore_unit_entry.get().strip()
    shore_mode_delete = bill_shore_mode_entry.get().strip()
    shore_port_delete = bill_shore_port_entry.get().strip()
    shore_terminal_delete = bill_shore_terminal_entry.get().strip()
    shore_name_delete = bill_shore_name_entry.get().strip()
    shore_tank_num_delete=bill_tank_name_entry.get().strip()
    shore_discharge_delete = bill_shore_discharge_entry.get().strip()
    shore_discharge_delete=float(shore_discharge_delete)
    shore_bill_date_delete=bill_shore_bill_date_entry.get()
    

    cursor.execute('UPDATE PHYSICAL_BLOTTER SET Shore_Received =? ,Difference=? WHERE PRICING_CONTRACT=? AND STRATEGY = ? ', (0.0,0.0,shore_contract_delete,shore_stat_delete))
    
    if shore_mode_delete=='Tank':
        tank_update(shore_port_delete,shore_terminal_delete,shore_tank_num_delete,'EMPTY')

    bill_shore_tree.delete(selected_bill)
    bill_shore_clear()
    my_conn.commit()   

    
    

def bill_shore_clear():
    
    bill_shore_contract_entry.set('Select')
    bill_shore_start_entry.delete(0,END)
    bill_shore_product_entry.delete(0,END)
    bill_shore_billed_qty_entry.delete(0,END)
    bill_shore_unit_entry.delete(0,END)
    bill_shore_mode_entry.delete(0,END)
    bill_shore_port_entry.delete(0,END)
    bill_shore_terminal_entry.delete(0,END)
    bill_shore_name_entry.delete(0,END)
    bill_shore_bill_date_entry.delete(0,END)
    bill_shore_discharge_entry.delete(0,END)
    bill_shore_difference_entry.delete(0,END)
    bill_shore_bill_date_entry.delete(0,END)
    bill_tank_name_entry.delete(0,END)




def bill_shore_selectItem(e):
    
    bill_shore_contract_entry.set('Select')
    bill_shore_start_entry.delete(0,END)
    bill_shore_product_entry.delete(0,END)
    bill_shore_billed_qty_entry.delete(0,END)
    bill_shore_unit_entry.delete(0,END)
    bill_shore_mode_entry.delete(0,END)
    bill_shore_port_entry.delete(0,END)
    bill_shore_terminal_entry.delete(0,END)
    bill_shore_name_entry.delete(0,END)
    bill_shore_bill_date_entry.delete(0,END)
    bill_shore_discharge_entry.delete(0,END)
    bill_shore_difference_entry.delete(0,END)
    bill_tank_name_entry.delete(0,END)

    
    
    selected = bill_shore_tree.focus()
     # Grab record values
    values = bill_shore_tree.item(selected, 'values')

    bill_shore_start_entry.insert(0,values[0])
    bill_shore_product_entry.insert(0,values[1])
    bill_shore_contract_entry.set(values[2])
    bill_shore_bill_date_entry.insert(0,values[3])
    bill_shore_billed_qty_entry.insert(0,values[4])
    bill_shore_discharge_entry.insert(0,values[5])
    bill_shore_unit_entry.insert(0,values[6])
    bill_shore_difference_entry.insert(0,values[7])
    bill_shore_mode_entry.insert(0,values[8])
    bill_shore_port_entry.insert(0,values[9])
    bill_shore_terminal_entry.insert(0,values[10])
    bill_shore_name_entry.insert(0,values[11])
    bill_tank_name_entry.insert(0,values[12])
    print('===========',values[12])
    
    


def bill_shore_contract_event(e):
    
    bill_shore_start_entry.delete(0,END)
    bill_shore_product_entry.delete(0,END)
    bill_shore_billed_qty_entry.delete(0,END)
    bill_shore_unit_entry.delete(0,END)
    bill_shore_mode_entry.delete(0,END)
    bill_shore_port_entry.delete(0,END)
    bill_shore_terminal_entry.delete(0,END)
    bill_shore_name_entry.delete(0,END)
    bill_shore_bill_date_entry.delete(0,END)
    bill_tank_name_entry.delete(0,END)

    
    

    bill_shore_details=physical_bill_shore_data.loc[physical_bill_shore_data['PRICING_CONTRACT']==bill_shore_contract_entry.get()]
    print(bill_shore_details)
    
    bill_shore_bill_date=bill_shore_details['BL_DATE'].unique().tolist()
    print('+++',bill_shore_bill_date)
    bill_shore_bill_date=' '.join(map(str, bill_shore_bill_date))
    bill_shore_bill_date_entry.insert(0,bill_shore_bill_date)
    
    bill_shore_strat=bill_shore_details['STRATEGY'].unique().tolist()
    bill_shore_strat=' '.join(map(str, bill_shore_strat))
    bill_shore_start_entry.insert(0,bill_shore_strat)
    
    
    
    
    bill_shore_product=bill_shore_details['PRODUCT'].unique().tolist()
    bill_shore_product=' '.join(map(str, bill_shore_product))
    bill_shore_product_entry.insert(0,bill_shore_product)
    
    bill_shore_billed_vol=bill_shore_details['TOTAL_VOLUME'].sum()
    bill_shore_billed_qty_entry.insert(0,bill_shore_billed_vol)
    bill_shore_billed_qty_entry.config(fg='red')
    
    bill_shore_unit=bill_shore_details['UNIT'].unique().tolist()
    bill_shore_unit=' '.join(map(str, bill_shore_unit))
    bill_shore_unit_entry.insert(0,bill_shore_unit)
    bill_shore_unit_entry.config(fg='red')
    
    bill_shore_container=bill_shore_details['Container'].unique().tolist()
    bill_shore_container=' '.join(map(str, bill_shore_container))
    bill_shore_mode_entry.insert(0,bill_shore_container)
    
    bill_shore_port=bill_shore_details['Port'].unique().tolist()
    bill_shore_port=' '.join(map(str, bill_shore_port))
    bill_shore_port_entry.insert(0,bill_shore_port)
    
    bill_shore_terminal=bill_shore_details['Terminal'].unique().tolist()
    bill_shore_terminal=' '.join(map(str, bill_shore_terminal))
    print(bill_shore_terminal)
    bill_shore_terminal_entry.insert(0,bill_shore_terminal)
    
    if bill_shore_container=='Vessel':
        
        bill_shore_cont_name=bill_shore_details['Vessel_Name'].unique().tolist()
        bill_shore_cont_name=' '.join(map(str, bill_shore_cont_name))
        bill_shore_name_entry.insert(0,bill_shore_cont_name)

    elif bill_shore_container=='Tank':
        
        bill_shore_tank_number=bill_shore_details['Tank_Number'].unique().tolist()

        bill_shore_tank_number=' '.join(map(str, bill_shore_tank_number))
        print(bill_shore_tank_number)
        bill_tank_name_entry.insert(0,bill_shore_tank_number)

    
    
    


def bill_shore_add():
#     shore_date_entry= Shore_Date.get()
    
    shore_contract_value = bill_shore_contract_entry.get().strip()
    shore_stat_value = bill_shore_start_entry.get().strip()
    shore_product_value = bill_shore_product_entry.get().strip()
    shore_billed_qty_value = bill_shore_billed_qty_entry.get().strip()
    shore_unit_value = bill_shore_unit_entry.get().strip()
    shore_mode_value = bill_shore_mode_entry.get().strip()
    shore_port_value = bill_shore_port_entry.get().strip()
    shore_terminal_value = bill_shore_terminal_entry.get().strip()
    shore_name_value = bill_shore_name_entry.get().strip()
    shore_discharge_value = bill_shore_discharge_entry.get().strip()
    shore_discharge_value=float(shore_discharge_value)
    difference_entry = bill_shore_difference_entry.get().strip()
#     difference_entry_val = float(difference_entry)
    bill_tank_name_value=bill_tank_name_entry.get().strip()
    print(bill_tank_name_value)
    
    
    if bill_shore_contract_entry.get()=='Select' or bill_shore_discharge_entry.get()=='':
        messagebox.showerror("error",'Please check all fields')
        raise
    
    else:
        
          
        billed_qty=shore_billed_qty_value
        billed_qty_val=float(billed_qty)
        print(billed_qty_val,type(billed_qty_val))

        discharged_qty = shore_discharge_value
        discharged_qty_val = float(discharged_qty)
        print(discharged_qty_val,type(discharged_qty_val))

        gain_loss_value=abs(float(discharged_qty_val))-abs(float(billed_qty_val))
        
        
        
        cursor.execute('UPDATE PHYSICAL_BLOTTER SET Shore_Received =? ,Difference=? WHERE PRICING_CONTRACT=? AND STRATEGY = ? ', (shore_discharge_value,gain_loss_value,shore_contract_value,shore_stat_value))
        my_conn.commit()   
        print(shore_product_value)
        
        bill_shore_tree.insert("", 'end',  values=(shore_stat_value,shore_product_value,shore_contract_value,bill_shore_bill_date_entry.get(),shore_billed_qty_value,shore_discharge_value,shore_unit_value,difference_entry,shore_mode_value,shore_port_value,shore_terminal_value,shore_name_value,bill_tank_name_value,''))
        my_conn.commit()
        if shore_mode_value=='Tank':
            tank_update(shore_port_value,shore_terminal_value,bill_tank_name_entry.get().strip(),shore_product_value)
        bill_shore_clear()
        messagebox.showinfo("Information", "Records inserted successfully")



        
def bill_shore_update():
    
    
    selected_bill =  bill_shore_tree.selection()[0]
    selected_bill_=bill_shore_tree.item(selected_bill)
    print(selected_bill)
    shore_contract_update = bill_shore_contract_entry.get().strip()
    shore_stat_update=bill_shore_start_entry.get().strip()
    
    
    shore_product_update = bill_shore_product_entry.get().strip()
    shore_billed_qty_update = bill_shore_billed_qty_entry.get().strip()
    shore_unit_update = bill_shore_unit_entry.get().strip()
    shore_mode_update = bill_shore_mode_entry.get().strip()
    shore_port_update = bill_shore_port_entry.get().strip()
    shore_terminal_update = bill_shore_terminal_entry.get().strip()
    shore_name_update = bill_shore_name_entry.get().strip()
    shore_discharge_update = bill_shore_discharge_entry.get().strip()
    shore_discharge_update=float(shore_discharge_update)
    shore_bill_date_update=bill_shore_bill_date_entry.get()
    bill_tank_num_update=bill_tank_name_entry.get()
    
    
    
    
    if bill_shore_contract_entry.get()=='Select' or bill_shore_discharge_entry.get()=='':
        messagebox.showerror("error",'Please check all fields')
        raise
    
    else:
        
          
        billed_qty_update=bill_shore_billed_qty_entry.get().strip()
        billed_qty_update_val=float(billed_qty_update)
       
        discharged_qty_update = bill_shore_discharge_entry.get().strip()
        discharged_qty_update_val = float(discharged_qty_update)
        
        gain_loss_update=float(discharged_qty_update_val)-float(billed_qty_update_val)
        
        
        
        cursor.execute('UPDATE PHYSICAL_BLOTTER SET Shore_Received =? ,Difference=? WHERE PRICING_CONTRACT=? AND STRATEGY = ? ', (discharged_qty_update,gain_loss_update,shore_contract_update,shore_stat_update))
        my_conn.commit()   
        
        if shore_mode_update=='Tank':
            
            tank_update(shore_port_update,shore_terminal_update,bill_tank_num_update,shore_product_update)

        bill_shore_tree.item(selected_bill, text="", values=(shore_stat_update,shore_product_update,shore_contract_update,shore_bill_date_update,shore_billed_qty_update,shore_discharge_update,shore_unit_update,gain_loss_update,shore_mode_update,shore_port_update,shore_terminal_update,shore_name_update,bill_tank_num_update))
        messagebox.showinfo("Information","Data Updated Successfully")
        bill_shore_clear()



bill_shore_frame=Frame(f4, relief=SOLID,bg='white')

#*********************************Date**********************************************************#
Label(bill_shore_frame, text="Date", font=('Times', 12), bg="White").grid(row=0, column=0, sticky=W, pady=10)
Shore_Date = OptionMenu(bill_shore_frame, current_date, date_variable)
Shore_Date.grid(row=0, column=1, pady=10, padx=10)
Shore_Date.config(width=15, font=('Times', 12))


physical_bill_shore_data = pd.read_sql('SELECT * FROM PHYSICAL_BLOTTER', my_conn)

bill_shore_contact= physical_bill_shore_data['PRICING_CONTRACT'].unique().tolist()
# bill_shore_contact_value=' '.join(map(str, bill_shore_contact))

#*********************************Trader WIDGET**********************************************************#
Label(bill_shore_frame, text="Pricing Contract", font=('Times',12),bg="White").grid(row=1, column=0, sticky=W, pady=10)
bill_shore_contract_entry = ttk.Combobox(bill_shore_frame, value=(bill_shore_contact), state='readonly')
bill_shore_contract_entry .grid(row=1, column=1, pady=10, padx=10)
bill_shore_contract_entry .config(width=16,height=20, font=('Times',12))

bill_shore_contract_entry.bind("<<ComboboxSelected>>",bill_shore_contract_event)


Label(bill_shore_frame, text="Strategy", font=('Times',12),bg="White",).grid(row=1, column=2, sticky=W, pady=10,padx=10)
bill_shore_start_entry = Entry(bill_shore_frame, font=('Times',12),bg="White",width=17)
bill_shore_start_entry.grid(row=1, column=3, pady=10, padx=10)

Label(bill_shore_frame, text="Product", font=('Times',12),bg="White",).grid(row=1, column=4, sticky=W, pady=10,padx=10)
bill_shore_product_entry = Entry(bill_shore_frame, font=('Times',12),bg="White",width=17)
bill_shore_product_entry.grid(row=1, column=5, pady=10, padx=10)

Label(bill_shore_frame, text="Billed Quantity", font=('Times',12),bg="White",fg='red').grid(row=1, column=6, sticky=W, pady=10,padx=10)
bill_shore_billed_qty_entry = Entry(bill_shore_frame, font=('Times',12),bg="White",fg='red',width=17)
bill_shore_billed_qty_entry.grid(row=1, column=7, pady=10, padx=10)

Label(bill_shore_frame, text="Unit", font=('Times',12),bg="White",).grid(row=1, column=8, sticky=W, pady=10,padx=10)
bill_shore_unit_entry = Entry(bill_shore_frame,font=('Times',12),bg="White",width=17)
bill_shore_unit_entry.grid(row=1, column=9, pady=10, padx=10)

Label(bill_shore_frame, text="Delivery Mode", font=('Times',12),bg="White",).grid(row=2, column=2, sticky=W, pady=10,padx=10)
bill_shore_mode_entry = Entry(bill_shore_frame, font=('Times',12),bg="White",width=17)
bill_shore_mode_entry.grid(row=2, column=3, pady=10, padx=10)

Label(bill_shore_frame, text="Port", font=('Times',12),bg="White",).grid(row=2, column=4, sticky=W, pady=10,padx=10)
bill_shore_port_entry = Entry(bill_shore_frame,font=('Times',12),bg="White",width=17)
bill_shore_port_entry.grid(row=2, column=5, pady=10, padx=10)

Label(bill_shore_frame, text="Terminal", font=('Times',12),bg="White",).grid(row=2, column=6, sticky=W, pady=10,padx=10)
bill_shore_terminal_entry = Entry(bill_shore_frame, font=('Times',12),bg="White",width=17)
bill_shore_terminal_entry.grid(row=2, column=7, pady=10, padx=10)


Label(bill_shore_frame, text="Vessel", font=('Times',12),bg="White",).grid(row=2, column=8, sticky=W, pady=10,padx=10)
bill_shore_name_entry = Entry(bill_shore_frame, font=('Times',12),bg="White",width=17)
bill_shore_name_entry.grid(row=2, column=9, pady=10, padx=10)

Label(bill_shore_frame, text="Tank", font=('Times',12),bg="White",).grid(row=3, column=8, sticky=W, pady=10,padx=10)
bill_tank_name_entry = Entry(bill_shore_frame, font=('Times',12),bg="White",width=17)
bill_tank_name_entry.grid(row=3, column=9, pady=10, padx=10)


Label(bill_shore_frame, text="Shore Discharged Quantity",font=('Times',12),bg="White",fg='red').grid(row=3, column=0, sticky=W,pady=10)
bill_shore_discharge_entry = Entry(bill_shore_frame, font=('Times',12),bg="White",width=22,fg='red')
bill_shore_discharge_entry.grid(row=3, column=1, pady=10, padx=10)
bill_shore_discharge_entry.bind("<Leave>", lambda e:discharged_difference(e))

Label(bill_shore_frame, text="Billed-Shore Difference", font=('Times',12),bg="White",fg='red').grid(row=3, column=2, sticky=W,pady=10)
bill_shore_difference_entry = Entry(bill_shore_frame, font=('Times',12),bg="White",width=17,fg='red')
bill_shore_difference_entry.grid(row=3, column=3, pady=10, padx=10)

Label(bill_shore_frame, text="BL Date", font=('Times',12),bg="White").grid(row=0, column=2, sticky=W,pady=10)
bill_shore_bill_date_entry = Entry(bill_shore_frame, font=('Times',12),bg="White",width=17)
bill_shore_bill_date_entry.grid(row=0, column=3, sticky=W,pady=10,padx=10)




add_btn_bill_shore = Button(bill_shore_frame , width=8, text='Add', bg='#003763',fg='white',font=('Times', 12),command=bill_shore_add)
add_btn_bill_shore.grid(row=5, column=2,sticky=W,padx=10,pady=10)

# ********************************Clear Button************************************************
clear_btn_bill_shore = Button(bill_shore_frame , width=8, text='Clear',bg='#003763',fg='white', font=('Times', 12),command= bill_shore_clear)
clear_btn_bill_shore.grid(row=5, column=3,sticky=W,padx=10,pady=10)

# #********************************edit Button************************************************
edit_btn_bill_shore = Button(bill_shore_frame, width=8, text='Update', bg='#003763',fg='white', font=('Times', 12),command=bill_shore_update)
edit_btn_bill_shore.grid(row=5, column=4,sticky=W,pady=10,padx=10)

# #************************************Delete button************************************************************#
delete_btn_bill_shore = Button(bill_shore_frame, width=8, text='Delete',  bg='#003763',fg='white',font=('Times', 12),command= bill_shore_delete)
delete_btn_bill_shore.grid(row=5, column=5,sticky=W,padx=10,pady=10)


purchase_summary_sales_frame=Frame(f5, relief=SOLID,bg='white')

Label(purchase_summary_sales_frame, text="Purchase Contract", font=('Times', 13),bg="White").grid(row=1, column=0, sticky=W, pady=10)
purchase_contract_entry = ttk.Combobox(purchase_summary_sales_frame, value=(physical_purchase_contract_value), state='readonly')
purchase_contract_entry .grid(row=1, column=1, pady=10, padx=10)
purchase_contract_entry .config(width=15,height=5, font=('Times',15))
purchase_contract_entry.set('Select')
purchase_contract_entry.bind("<<ComboboxSelected>>",purchace_sales_details)

Label(purchase_summary_sales_frame, text="Strategy Number (Reference Number)", font=('Times',13),bg="White",).grid(row=1, column=2, sticky=W, pady=10,padx=10)
purchase_strategy_entry = Entry(purchase_summary_sales_frame, font=('Times',13),bg="White",width=15)
purchase_strategy_entry.grid(row=1, column=3, pady=10, padx=10)









#************************************tree style***************************
style = ttk.Style()

style.theme_use('default')
style.configure("Treeview", background="white", foreground="black", highlightthickness=0, bd=0, font=('Verdana', 9))

style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'), background="#153e5c", foreground="white")
style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])
style.map('Treeview', background=[('selected', '#0B5A81')])

#***********************swaps tree view*********************************************************************************






f1_right_frame = Frame(f1, bd=1, relief=SOLID, padx=2, pady=2)
physical_tree = ttk.Treeview(f1_right_frame, show="headings",selectmode='browse',style="mystyle.Treeview",height=38)
physical_tree.tag_configure('odd', background='#FFEFD5')
physical_tree.tag_configure('even', background='white')
physical_tree.grid(row=1, columnspan=1)
physical_data = pd.read_sql('SELECT * FROM PHYSICAL_BLOTTER', my_conn)
physical_data=physical_data.drop(['kgal','kl','kcbm'], axis=1)
print('+++',physical_data)
# physical_data= physical_data[physical_data['DATE']== date_variable]
my_conn.commit()
physical_data=physical_data[['DATE', 'TRADER', 'COUNTER_PARTY', 'BOOK', 'STRATEGY', 'DERIVATIVE','PRODUCT', 'PRICING_CONTRACT', 'kbbl', 'kMT', 'PRICING_METHOD','PREMIUM_DISCOUNT', 'PRICING_TERM', 'BL_DATE', 'START_DATE', 'END_DATE','HOLIDAY', 'UNIT', 'TOTAL_DAYS', 'PRICED_DAYS', 'UNPRICED_DAYS','TOTAL_VOLUME', 'PRICED_VOLUME', 'UNPRICED_VOLUME', 'POSITION','PRICED_PRICE', 'UNPRICED_PRICE', 'CONV_kbbl_MT', 'CONV_MT_kbbl',"Container",'Port','Terminal','Vessel_Name','Tank_Number','External_Terminal','NOTES','Shore_Received','Difference','Nominated_qty','Density','PnL']]
physical_data.columns = ['Date', 'Trader', 'Counter Party', 'Book', 'Strategy', 'Derivative', 'Product', 'Pricing Contract', 'kbbl', 'kMT', 'Pricing Method', 'Premium_Discount', 'Pricing Term', 'Bl_Date', 'Start Date', 'End Date', 'Holiday', 'Unit', 'Total Days', 'Priced Days', 'Unpriced Days', 'Total Volume', 'Priced Volume', 'Unpriced Volume', 'Position', 'Priced Price', 'Unpriced Price', 'CONV_kbbl_MT', 'CONV_MT_kbbl', "Container",'Port','Terminal','Vessel_Name','Tank_Number','External_Terminal','Notes','Shore_Received','Difference','Nominated_qty','Density','PnL']
cols = list(physical_data.columns)
physical_tree["columns"] = cols
physical_tree["show"] = "headings" 

for i in cols:
    physical_tree.column(i,width = 37, minwidth = 120)

    physical_tree.column(i, anchor="center")
    physical_tree.heading(i, text=i, anchor='center')
    physical_tree.bind('<ButtonRelease-1>',physical_blotter_selectItem)

for item in physical_tree.get_children():
    physical_tree.delete(item)

df_rows_data = physical_data.to_numpy().tolist() 
print(df_rows_data)

for index in range(len(df_rows_data)):
    if index %2==0:
        physical_tree.insert("",'end',values=df_rows_data[index],tags=('even'))
    else:
        physical_tree.insert("",'end',values=df_rows_data[index],tags=('odd'))

    # # ----vertical scrollbar------------
vbar = ttk.Scrollbar(f1_right_frame, orient=VERTICAL, command=physical_tree.yview)
physical_tree.configure(yscrollcommand=vbar.set)
#tree.grid(row=0, column=0, sticky=NSEW)
vbar.grid(row=1, column=1, sticky=NS)

# # ----horizontal scrollbar----------
hbar = ttk.Scrollbar(f1_right_frame, orient=HORIZONTAL, command=physical_tree.xview)
physical_tree.configure(xscrollcommand=hbar.set)
hbar.grid(row=2, column=0, sticky=EW)
f1_right_frame.place(x=350, y=40)


position_tree = ttk.Treeview(f2_frame, show="headings",selectmode='browse',style="mystyle.Treeview",height=40)
position_tree.tag_configure('odd', background='white')
position_tree.tag_configure('even', background='#FFEFD5')
position_tree.tag_configure('first', background='#f2be54')
position_tree.grid(row=1, column=0,columnspan=1)

# ----vertical scrollbar------------
vbar = ttk.Scrollbar(f2_frame, orient=VERTICAL, command=position_tree.yview)
position_tree.configure(yscrollcommand=vbar.set)
#tree.grid(row=0, column=0, sticky=NSEW)
vbar.grid(row=1, column=1, sticky=NS)

# ----horizontal scrollbar----------
hbar = ttk.Scrollbar(f2_frame, orient=HORIZONTAL, command=position_tree.xview)
position_tree.configure(xscrollcommand=hbar.set)
hbar.grid(row=3, column=0, sticky=EW)




bill_shore_right_frame = Frame(f4, bd=1, relief=SOLID, padx=2, pady=2)
bill_shore_tree = ttk.Treeview(bill_shore_right_frame, show="headings",selectmode='browse',style="mystyle.Treeview",height=15)

bill_shore_tree.tag_configure('odd', background='#FFEFD5')
bill_shore_tree.tag_configure('even', background='white')
bill_shore_tree.grid(row=1, columnspan=1)
bill_shore_data = pd.read_sql('SELECT * FROM PHYSICAL_BLOTTER', my_conn)
bill_shore_data=bill_shore_data.loc[bill_shore_data['Shore_Received']!='0.0']
print(bill_shore_data)
my_conn.commit()
bill_shore_data=bill_shore_data[['STRATEGY', 'PRODUCT', 'PRICING_CONTRACT', 'BL_DATE', 'TOTAL_VOLUME','Shore_Received','UNIT','Difference',"Container",'Port','Terminal','Vessel_Name','Tank_Number','External_Terminal']]
bill_shore_data.columns = ['Strategy', 'Product', 'Pricing Contract',  'Bl_Date', 'Bill of Landing Quantity', 'Shore_Received','Unit','Difference', "Container",'Port','Terminal','Vessel_Name','Tank_Number','External_Terminal']
cols = list(bill_shore_data.columns)
bill_shore_tree["columns"] = cols
bill_shore_tree["show"] = "headings" 

for i in cols:
    bill_shore_tree.column(i,width = 103, minwidth = 120)

    bill_shore_tree.column(i, anchor="center")
    bill_shore_tree.heading(i, text=i, anchor='center')
    bill_shore_tree.bind('<ButtonRelease-1>',bill_shore_selectItem)

df_rows = bill_shore_data.to_numpy().tolist() 
print(df_rows)

for item in bill_shore_tree.get_children():
    bill_shore_tree.delete(item)


for index in range(len(df_rows)):
    if index %2==0:
        bill_shore_tree.insert("",'end',values=df_rows[index],tags=('even'))
    else:
        bill_shore_tree.insert("",'end',values=df_rows[index],tags=('odd'))

    # # ----vertical scrollbar------------
vbar = ttk.Scrollbar(bill_shore_right_frame, orient=VERTICAL, command=bill_shore_tree.yview)
bill_shore_tree.configure(yscrollcommand=vbar.set)
#tree.grid(row=0, column=0, sticky=NSEW)
vbar.grid(row=1, column=1, sticky=NS)

# # ----horizontal scrollbar----------
hbar = ttk.Scrollbar(bill_shore_right_frame, orient=HORIZONTAL, command=bill_shore_tree.xview)
bill_shore_tree.configure(xscrollcommand=hbar.set)
hbar.grid(row=2, column=0, sticky=EW)
bill_shore_right_frame.place(x=40, y=400)




f1_btn_frame = Frame(f1, bd=1, relief=SOLID, padx=1, pady=1)

today_btn=Button(f1_btn_frame ,text="Today",bg='#388087', pady=3,fg='white',font=('Times', 11),command=lambda:load_data('Today'))
today_btn.grid(row=1,column=3)


yest_btn=Button(f1_btn_frame,text="Yesterday",height=1,bg='#388087', pady=3,fg='white',font=('Times', 11),command=lambda:load_data('Yesterday'))
yest_btn.grid(row=1,column=4)


month_btn=Button(f1_btn_frame,text="Month",height=1,bg='#388087', pady=3,fg='white',font=('Times', 11),command=lambda:load_data('Month'))
month_btn.grid(row=1,column=5)



six_month_btn=Button(f1_btn_frame,text="Last 6 Month",height=1,bg='#388087', pady=3,fg='white',font=('Times', 11),command=lambda:load_data('Last 6 Month'))
six_month_btn.grid(row=1,column=6)


year_btn=Button(f1_btn_frame,text="Year",height=1,bg='#388087', pady=3,fg='white',font=('Times', 11),command=lambda:load_data('Year'))
year_btn.grid(row=1,column=7)

show_all_btn=Button(f1_btn_frame,text="Show All",height=1,bg='#388087', pady=3,fg='white',font=('Times', 11),command=lambda:load_data('Show All'))
show_all_btn.grid(row=1,column=8)


f1_btn_frame.place(x=800,y=850)
f1_left_frame.place(x=5, y=2)
f2_frame.place(x=10, y=100)
bill_shore_frame.place(x=40,y=100)
purchase_summary_sales_frame.place(x=20,y=50)





def on_enter(e):
    b1.config(bg='slategray', foreground= "white")

def on_leave(e):
    b1.config(background= '#003763', foreground= 'white')


navBar=Frame(root,width=100, height=80)
navBar.grid(row=0,column=0,sticky='nswe')
navBar.config(bg="#388087")

b1=Button(navBar,text="Physical Blotter",width=20, height=2, bg='#003763', font=('Tahoma', 10, 'bold'), fg='white',command=lambda:raise_frame(f1))
b1.grid(row=0,column=1)

b1.bind('<Enter>', on_enter)
b1.bind('<Leave>', on_leave)

def on_enter(e):
    b2.config(bg='slategray', foreground= "white")

def on_leave(e):
    b2.config(background= '#003763', foreground= 'white')



b2=Button(navBar,text="Position",width=12, height=2, bg='#003763', font=('Tahoma', 10, 'bold'), fg='white',command=lambda:raise_frame_position(f2))
# command=lambda:raise_frame_position(f2)
b2.grid(row=0,column=4)
b2.bind('<Enter>', on_enter)
b2.bind('<Leave>', on_leave)

def on_enter(e):
    b3.config(bg='slategray', foreground= "white")

def on_leave(e):
    b3.config(background= '#003763', foreground= 'white')



b3=Button(navBar,text="History",width=12, height=2, bg='#003763', font=('Tahoma', 10, 'bold'), fg='white',command=lambda:raise_hist(f3))
# command=lambda:raise_hist(f3)
b3.grid(row=0,column=5)
b3.bind('<Enter>', on_enter)
b3.bind('<Leave>', on_leave)


b5=Button(navBar,text="Bill and Shore Difference",width=22, height=2, bg='#003763', font=('Tahoma', 10, 'bold'), fg='white',command=lambda:bill_shore_raise_frame(f4))
b5.grid(row=0,column=2)

def on_enter(e):
    b4.config(bg='slategray', foreground= "white")

def on_leave(e):
    b4.config(background= '#f44336', foreground= 'white')



b4=Button(navBar,text="Exit",width=12, height=2, bg='#f44336', font=('Tahoma', 10, 'bold'), fg='white',command=homeCallBack)
# ,command=homeCallBack
b4.grid(row=0,column=7)
b4.bind('<Enter>', on_enter)
b4.bind('<Leave>', on_leave)

b6=Button(navBar,text="Purchase Summary",width=22, height=2, bg='#003763', font=('Tahoma', 10, 'bold'), fg='white',command=lambda:purchace_sales_raise(f5))
b6.grid(row=0,column=3)

b6=Button(navBar,text="Refresh",width=20, height=2, bg='#4CAF50', font=('Tahoma', 10, 'bold'), fg='white',command=lambda:refresh())
b6.grid(row=0,column=6)


label1.place(x=1,y=1)
label2.place(x=1,y=1)
label3.place(x=1,y=1)
label4.place(x=1,y=1)
label5.place(x=1,y=1)

raise_frame(f1)

root.state('zoomed')
root.mainloop()

