# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 00:02:01 2019

@author: ashley
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


wkg_dir = 'C:/Users/ashle/Documents/Personal Data/Northwestern/2019-04  fall MSDS498_Sec56 Capstone/final dataset/'



df_customers = pd.read_csv(wkg_dir+'olist_customers_dataset.csv')
df_geolocation = pd.read_csv(wkg_dir+'olist_geolocation_dataset.csv')
df_order_items = pd.read_csv(wkg_dir+'olist_order_items_dataset.csv')
df_order_pmts = pd.read_csv(wkg_dir+'olist_order_payments_dataset.csv')
df_order_reviews = pd.read_csv(wkg_dir+'olist_order_reviews_dataset.csv')
df_orders = pd.read_csv(wkg_dir+'olist_orders_dataset.csv')
df_products = pd.read_csv(wkg_dir+'olist_products_dataset.csv')
df_sellers = pd.read_csv(wkg_dir+'olist_sellers_dataset.csv')
df_prdct_cat_translate = pd.read_csv(wkg_dir+'product_category_name_translation.csv')



#check out the datasets
#======================
df_order_items.info()
#112,650

df_orders.info()   #99,441
#checks:
sum(pd.isnull(df_orders.order_id))  #0; perfect, is always populated
len(pd.unique(df_orders.order_id))   #same as # of rows ==>  is unique, as desired
sum(pd.isnull(df_orders.order_status))  #0; perfect, is always populated
sum(pd.isnull(df_orders.customer_id))  #0; perfect, is always populated


df_customers.info()  #99,441
sum(pd.isnull(df_customers.customer_id))  #0, perfect
len(pd.unique(df_customers.customer_id))   #same as # of rows ==>  is unique, as desired
sum(pd.isnull(df_customers.customer_unique_id))   #0, perfect
len(pd.unique(df_customers.customer_unique_id))    #96,096   ==>  some "customer_ids" are dups of the same customer_unique_id



df_order_reviews.info()    #100,000 reviews, for 99,441 orders
sum(pd.isnull(df_order_reviews.order_id))   #0, perfect, always populated
len(pd.unique(df_order_reviews.order_id))   #but is not always unique.  Not fatal, just note
sum(pd.isnull(df_order_reviews.review_score))   #0, perfect, always populated
pd.value_counts(df_order_reviews.review_score)   #1 thru 5, mostly 5s and 4s


df_products.info()    #32,951
sum(pd.isnull(df_products.product_id))   #0, perfect, always populated
len(pd.unique(df_products.product_id))   #same as # of rows ==>  is unique, as desired
sum(pd.isnull(df_products.product_category_name))   #610.   



df_prdct_cat_translate.info()   #71
sum(pd.isnull(df_prdct_cat_translate.product_category_name))   #0, perfect, always populated
len(pd.unique(df_prdct_cat_translate.product_category_name))   #same as # of rows ==>  is unique, as desired
sum(pd.isnull(df_prdct_cat_translate.product_category_name_english))   #0, perfect, always populated   




df_sellers.info()   #3095
sum(pd.isnull(df_sellers.seller_id))   #0, perfect, always populated
len(pd.unique(df_sellers.seller_id))   #same as # of rows ==>  is unique, as desired
sum(pd.isnull(df_sellers.seller_city))   #0, perfect, always populated



df_order_pmts.info()   #103,886
sum(pd.isnull(df_order_pmts.order_id))   #0, perfect, always populated
len(pd.unique(df_order_pmts.order_id))   #1 less than # of orders ==> one has no pmt.  track down and check later
sum(pd.isnull(df_order_pmts.payment_type))   #0, perfect, always populated



df_geolocation.info()   #1,000,163
sum(pd.isnull(df_geolocation.geolocation_zip_code_prefix))   #0, perfect, always populated
len(pd.unique(df_geolocation.geolocation_zip_code_prefix))   ##tons of dups - 
#    df_geolocation2 = df_geolocation.drop_duplicates(['geolocation_zip_code_prefix', 'geolocation_lat', 'geolocation_lng', 'geolocation_city', 'geolocation_state'])
#    df_geolocation2.info()
#    df_geolocation2.head()

df_geolocation.head(100)


#df_geolocation2 = df_geolocation.groupby(by=['geolocation_zip_code_prefix', 'geolocation_lat', 'geolocation_lng', 'geolocation_city', 'geolocation_state'], as_index=False).size()




# ====================================================
# merge the normalized datasets into one big flat file
# ====================================================

#add order details to the order_items table (start from here, is more detailed)
df_merged = df_order_items.merge(df_orders, how='left', on='order_id')
df_merged.info()  #still have 112,650 rows, good
sum(pd.isnull(df_merged.order_id))  #0, perfect
sum(pd.isnull(df_merged.order_status))  #0, perfect, no problems joining on order_id between these two tables


#add customer info
df_merged = df_merged.merge(df_customers, how='left', on='customer_id')
df_merged.info()  #still have 112,650 rows, good
sum(pd.isnull(df_merged.customer_id))  #0, perfect
sum(pd.isnull(df_merged.customer_unique_id))  #0, perfect, no problems joining on order_id between these two tables


#add review info.  
df_merged = df_merged.merge(df_order_reviews, how='left', on='order_id')
df_merged.info()  #now have 113,322 b/c a few orders have multiple reviews
sum(pd.isnull(df_merged.order_id))   #0, perfect, always populated
sum(pd.isnull(df_merged.review_score))   #0, perfect, always populated  ==> join always succeeded



#add product info.  
#check:    sum(pd.isnull(df_merged.product_id))   #0, perfect, always populated  
df_merged = df_merged.merge(df_products, how='left', on='product_id')
df_merged.info()  #still have 113,322 
sum(pd.isnull(df_merged.product_category_name))   #1612 -- pretty sure this is OK (and/or not fixable if not :) )


#add product category name, in English.  
df_merged = df_merged.merge(df_prdct_cat_translate, how='left', on='product_category_name')
df_merged.info()  #still have 113,322 
sum(pd.isnull(df_merged.product_category_name))   #1612 -- pretty sure this is OK (and/or not fixable if not :) )
sum(pd.isnull(df_merged.product_category_name_english))   #1636 -- a few records didn't join?  not a big deal but maybe check later.



#add seller info.  
#check:    sum(pd.isnull(df_merged.seller_id))   #0, perfect, always populated  
df_merged = df_merged.merge(df_sellers, how='left', on='seller_id')
df_merged.info()  #still have 113,322 
sum(pd.isnull(df_merged.seller_city))   #0, perfect, the join always succeeded




#add payments info.  
df_merged = df_merged.merge(df_order_pmts, how='left', on='order_id')
df_merged.info()  #now have 118,318 as a few orders have multiple pmt dtls rows (and/or dup order ids?)
sum(pd.isnull(df_merged.payment_type))   #3,   almost perfect,  the join always succeeded except for 3 records


#write out to CSV file to share
df_merged.to_csv(wkg_dir+'Merged_dataset.csv')






# ==============================
# add lat/longs for the customer
# ==============================
#customer_id	a.customer_unique_id	a.customer_zip_code_prefix	a.customer_city	a.customer_state	b.order_id	b.order_status	b.order_purchase_timestamp	b.order_approved_at	b.order_delivered_carrier_date	b.order_delivered_customer_date	b.order_estimated_delivery_date	c.payment_type	c.payment_installments	c.payment_value


#            Lat_Avg=pd.NamedAgg('geolocation_lat', aggfunc='mean'),

#sum(pd.isnull(df_geolocation.geolocation_zip_code_prefix))  #0, perfect always populated
#sum(pd.isnull(df_geolocation.geolocation_city))  #0, perfect always populated
#sum(pd.isnull(df_geolocation.geolocation_state))  #0, perfect always populated
#sum(pd.isnull(df_geolocation.geolocation_lat))  #0, perfect always populated
#add lat/long info for the customers
df_geo_avg_by_zip_city_state = df_geolocation.groupby(['geolocation_zip_code_prefix', 'geolocation_city', 'geolocation_state']).agg(
            Nbr_Rcds=('geolocation_lat', 'count'),
            Lat_Avg=('geolocation_lat', 'mean'),
            Lat_Min=('geolocation_lat', 'min'),
            Lat_Max=('geolocation_lat', 'max'),
            Long_Avg=('geolocation_lng', 'mean'),
            Long_Min=('geolocation_lng', 'min'),
            Long_Max=('geolocation_lng', 'max'))

#not sure why this was necessary (setting as_index=False gets rid of the multi-index, but did not return the groupby columns as col's in the output?!??) 
# but this turns the MultiIndex for the rows into columns of data as desired.
df_geo_avg_by_zip_city_state = df_geo_avg_by_zip_city_state.reset_index()
df_geo_avg_by_zip_city_state.info()   #27,912 rows
df_geo_avg_by_zip_city_state.head()

df_geo_avg_by_zip_city_state
#after reviewing, drop extra columns and simplify the names
df_geo_avg_by_zip_city_state2 = df_geo_avg_by_zip_city_state[['geolocation_zip_code_prefix', 'geolocation_city', 'geolocation_state', 'Lat_Avg', 'Long_Avg']]
df_geo_avg_by_zip_city_state2.columns = ['zip_prefix', 'city', 'state', 'lat', 'long']




df_geo_avg_by_zip_city = df_geolocation.groupby(['geolocation_zip_code_prefix', 'geolocation_city']).agg(
            Nbr_Rcds=('geolocation_lat', 'count'),
            Lat_Avg=('geolocation_lat', 'mean'),
            Lat_Min=('geolocation_lat', 'min'),
            Lat_Max=('geolocation_lat', 'max'),
            Long_Avg=('geolocation_lng', 'mean'),
            Long_Min=('geolocation_lng', 'min'),
            Long_Max=('geolocation_lng', 'max'))

df_geo_avg_by_zip_city = df_geo_avg_by_zip_city.reset_index()
df_geo_avg_by_zip_city.info()   #27,907 rows
df_geo_avg_by_zip_city.head()

#after reviewing, drop extra columns and simplify the names
df_geo_avg_by_zip_city2 = df_geo_avg_by_zip_city[['geolocation_zip_code_prefix', 'geolocation_city', 'Lat_Avg', 'Long_Avg']]
df_geo_avg_by_zip_city2.columns = ['zip_prefix', 'city', 'lat', 'long']
df_geo_avg_by_zip_city2.info()



df_geo_avg_by_zip = df_geolocation.groupby(['geolocation_zip_code_prefix']).agg(
            Nbr_Rcds=('geolocation_lat', 'count'),
            Lat_Avg=('geolocation_lat', 'mean'),
            Lat_Min=('geolocation_lat', 'min'),
            Lat_Max=('geolocation_lat', 'max'),
            Long_Avg=('geolocation_lng', 'mean'),
            Long_Min=('geolocation_lng', 'min'),
            Long_Max=('geolocation_lng', 'max'))

df_geo_avg_by_zip = df_geo_avg_by_zip.reset_index()
df_geo_avg_by_zip.info()

df_geo_avg_by_zip2 = df_geo_avg_by_zip[['geolocation_zip_code_prefix', 'Lat_Avg', 'Long_Avg']]
df_geo_avg_by_zip2.columns = ['zip_prefix', 'lat', 'long']
df_geo_avg_by_zip2.info()



df_merged.info()

df_merged2 = df_merged.merge(df_geo_avg_by_zip_city_state2, how='left', left_on=['customer_zip_code_prefix', 'customer_city', 'customer_state'], right_on=['zip_prefix', 'city', 'state'])
#df_merged2.info()  #stiil have 118,318 as expected
sum(pd.isnull(df_merged2.lat))  #369     
sum(pd.isna(df_merged2.customer_zip_code_prefix))  #0     
sum(pd.isnull(df_merged.customer_city))  #0     
sum(pd.isnull(df_merged.customer_state))  #0 
    #apparently some of the custs are from zip/city/states not in the lat/long lookup table.   retry by zip and state
    
#prune out these join columns that have been added in unnecessarily
df_merged2.drop(['zip_prefix', 'city', 'state'], axis='columns', inplace=True)
#add a row ID so we can easily join in missing results if we find them in the subsequent steps
df_merged2.insert(0, 'Rww_ID', range(0, len(df_merged2)))




#try joining on just zip & city and see if that succeeds (maybe the states were null or conflicting??)
   
#for the 2nd attempt at joining on zip&city, prune out the lat & long columns as a) they are null anyway and b) they cause diff lat&long cols to get created like lat_y, long_y
cols = [col for col in df_merged2.columns if col not in ['lat', 'long']]
df_merge_by_zip_and_city = df_merged2[ pd.isnull(df_merged2.lat) ][ cols ].merge(df_geo_avg_by_zip_city2, how='left', left_on=['customer_zip_code_prefix', 'customer_city'], right_on=['zip_prefix', 'city'])
df_merge_by_zip_and_city.drop(['zip_prefix', 'city'], axis='columns', inplace=True)
df_merge_by_zip_and_city.info()    #369 rows attempted but still no success in joining
sum(pd.isnull(df_merge_by_zip_and_city.lat))    #369 rows attempted but still no success in joining


#try one last time to see if the customer zips are found in the lookup table     
df_merge_by_zip = df_merged2[ pd.isnull(df_merged2.lat) ][ cols ].merge(df_geo_avg_by_zip2, how='left', left_on=['customer_zip_code_prefix'], right_on=['zip_prefix'])
df_merge_by_zip.drop(['zip_prefix'], axis='columns', inplace=True)
df_merge_by_zip.info()    #369 rows attempted, 52 lat/longs found
sum(pd.isnull(df_merge_by_zip.lat))    #317.    52 rows were found, 317 were not


#copy the rows for which we did NOT find a lat long  in the last attempt 
rw_ids_fnd_by_zip_only = df_merge_by_zip[pd.notnull(df_merge_by_zip.lat)].Rww_ID
df_merged3 = df_merged2[ ~  df_merged2.Rww_ID.isin(rw_ids_fnd_by_zip_only)  ].copy()

#len(  df_merged2[ ~  df_merged2.Rww_ID.isin(rw_ids_fnd_by_zip_only)  ]  )

#add in the rows for which we found a lat long  in the last attempt 
df_merged3 = df_merged3.append( df_merge_by_zip[ pd.notnull(df_merge_by_zip.lat) ].copy() )

#rename the lat, long columns as lat_cust, long_cust
new_col_names = [col for col in df_merged3.columns[:-2]]
new_col_names.append('lat_customer')
new_col_names.append('long_customer')
df_merged3.columns = new_col_names

df_merged3.info()







# ==============================
#repeat for the seller lat/longs
# ==============================
df_merged4 = df_merged3.merge(df_geo_avg_by_zip_city_state2, how='left', left_on=['seller_zip_code_prefix', 'seller_city', 'seller_state'], right_on=['zip_prefix', 'city', 'state'])
#df_merged4.info()  #stiil have 118,318 as expected
sum(pd.isnull(df_merged4.lat))  #3244     
sum(pd.isna(df_merged3.seller_zip_code_prefix))  #0     
sum(pd.isnull(df_merged3.seller_city))  #0     
sum(pd.isnull(df_merged3.seller_state))  #0 
    #apparently some of the sellers are from zip/city/states not in the lat/long lookup table.   retry by zip and state
    
#prune out these join columns that have been added in unnecessarily
df_merged4.drop(['zip_prefix', 'city', 'state'], axis='columns', inplace=True)


#try joining on just zip & city and see if that succeeds (maybe the states were null or conflicting??)
   
#for the 2nd attempt at joining on zip&city, prune out the lat & long columns as a) they are null anyway and b) they cause diff lat&long cols to get created like lat_y, long_y
cols = [col for col in df_merged4.columns if col not in ['lat', 'long']]
df_merge_by_seller_zip_and_city = df_merged4[ pd.isnull(df_merged4.lat) ][ cols ].merge(df_geo_avg_by_zip_city2, how='left', left_on=['seller_zip_code_prefix', 'seller_city'], right_on=['zip_prefix', 'city'])
df_merge_by_seller_zip_and_city.drop(['zip_prefix', 'city'], axis='columns', inplace=True)
df_merge_by_seller_zip_and_city.info()    #666 rows w/ lat/long now
sum(pd.isnull(df_merge_by_seller_zip_and_city.lat))    #still 2578 rows w/ no success in joining



#copy the rows for which we did NOT find a lat long  in the last attempt 
rw_ids_fnd_by_seller_zip_and_state = df_merge_by_seller_zip_and_city[pd.notnull(df_merge_by_seller_zip_and_city.lat)].Rww_ID
#copy everything else into a new dataset
df_merged5 = df_merged4[ ~  df_merged4.Rww_ID.isin(rw_ids_fnd_by_seller_zip_and_state)  ].copy()


#add in the rows for which we found a lat long  in the last attempt 
df_merged5 = df_merged5.append( df_merge_by_seller_zip_and_city[ pd.notnull(df_merge_by_seller_zip_and_city.lat) ].copy() )
     
df_merged5.info()
#118,318, with 115,740 not null for lat/long


#try one last time to see if the customer zips are found in the lookup table     
df_merge_by_seller_zip = df_merged5[ pd.isnull(df_merged5.lat) ][ cols ].merge(df_geo_avg_by_zip2, how='left', left_on=['seller_zip_code_prefix'], right_on=['zip_prefix'])
df_merge_by_seller_zip.drop(['zip_prefix'], axis='columns', inplace=True)
df_merge_by_seller_zip.info()    #2578 rows attempted, 2313 lat/longs found
sum(pd.isnull(df_merge_by_seller_zip.lat))    #265 rows still don't have a lat/long





#copy the rows for which we did NOT find a lat long  in the last attempt 
rw_ids_fnd_by_seller_zip_only = df_merge_by_seller_zip[pd.notnull(df_merge_by_seller_zip.lat)].Rww_ID
df_merged6 = df_merged5[ ~  df_merged5.Rww_ID.isin(rw_ids_fnd_by_seller_zip_only)  ].copy()

#len(  df_merged5[ ~  df_merged5.Rww_ID.isin(rw_ids_fnd_by_seller_zip_only)  ]  )

#add in the rows for which we found a lat long  in the last attempt 
df_merged6 = df_merged6.append( df_merge_by_seller_zip[ pd.notnull(df_merge_by_seller_zip.lat) ].copy() )

#rename the lat, long columns as lat_cust, long_cust
new_col_names = [col for col in df_merged6.columns[:-2]]
new_col_names.append('lat_seller')
new_col_names.append('long_seller')
df_merged6.columns = new_col_names

df_merged6.info()



df_merged6.to_csv(wkg_dir+'Merged_dataset_w_LatLong.csv')
