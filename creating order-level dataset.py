# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 00:02:01 2019

@author: ashley
"""

import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt


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
df_orders.info()   #99,441
    #note all the delivery info is PER ORDER, regardless of how many items are in the order
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


df_sellers.info()   #3095
sum(pd.isnull(df_sellers.seller_id))   #0, perfect, always populated
len(pd.unique(df_sellers.seller_id))   #same as # of rows ==>  is unique, as desired
sum(pd.isnull(df_sellers.seller_city))   #0, perfect, always populated



df_geolocation.info()   #1,000,163
sum(pd.isnull(df_geolocation.geolocation_zip_code_prefix))   #0, perfect, always populated
len(pd.unique(df_geolocation.geolocation_zip_code_prefix))   ##tons of dups - 
#    df_geolocation2 = df_geolocation.drop_duplicates(['geolocation_zip_code_prefix', 'geolocation_lat', 'geolocation_lng', 'geolocation_city', 'geolocation_state'])
#    df_geolocation2.info()
#    df_geolocation2.head()

df_geolocation.head(100)


#df_geolocation2 = df_geolocation.groupby(by=['geolocation_zip_code_prefix', 'geolocation_lat', 'geolocation_lng', 'geolocation_city', 'geolocation_state'], as_index=False).size()



#need aggregation to get to 1 value max per order.  items => products and product categories, so need a way to roll up these values
    #make a concatenated list of categories??  ex. "health and beauty, home goods"??  so we can do like operations?
    #make a concatenated list of sellers??  ex. "123,  5353"??  so we can do like operations?
    # count # of products- is this always the same as the # of items???  I don't see a quantity field anywhere
    #sum up weight, linear cm, ...; price, freight_value;  # of photos
    #min shipping limit date, max shipping limit date
    

df_order_items.info()
#112,650
    #check data dictionary/queries:   shipping_limit_date,   freight value
    #df_order_items.loc[1:50, ['price', 'freight_value']]  #not sure; presumably freight value is the shipping cost, not an "insured for value"
#checks:
sum(pd.isnull(df_order_items.order_item_id))   #0, perfect, this is always populated
len(pd.unique(df_order_items.order_item_id))   #21    integers 1-21
sum(pd.isnull(df_order_items.order_id))   #0, perfect, this is always populated
len(pd.unique(df_order_items.order_id))   #98,666 distinct order IDs


df_products.info()    #32,951
sum(pd.isnull(df_products.product_id))   #0, perfect, always populated
len(pd.unique(df_products.product_id))   #same as # of rows ==>  is unique, as desired
sum(pd.isnull(df_products.product_category_name))   #610.   


df_products.loc[:,['product_name_lenght', 'product_description_lenght']].head()
pd.unique(df_products.loc[:,'product_name_lenght'])
pd.unique(df_products.loc[:,'product_description_lenght'])
pd.unique(df_products.loc[:,'product_photos_qty'])


df_prdct_cat_translate.info()   #71
sum(pd.isnull(df_prdct_cat_translate.product_category_name))   #0, perfect, always populated
len(pd.unique(df_prdct_cat_translate.product_category_name))   #same as # of rows ==>  is unique, as desired
sum(pd.isnull(df_prdct_cat_translate.product_category_name_english))   #0, perfect, always populated   




#need aggregation to get to 1 value max per order.
    #check:  is sum of pmt_values, summed over the pmts == sum(price+freight_value), summed over the items?

df_order_pmts.info()   #103,886
sum(pd.isnull(df_order_pmts.order_id))   #0, perfect, always populated
len(pd.unique(df_order_pmts.order_id))   #1 less than # of orders ==> one has no pmt.  track down and check later
sum(pd.isnull(df_order_pmts.payment_type))   #0, perfect, always populated

df_order_pmts.head().transpose()   #103,886

#do all the pmts for an order have the same "payment_installments"  - ex. 1 of 8, 2 of 8, ..., 8 of 8?

pd.value_counts(df_order_pmts.loc[ df_order_pmts.order_id.duplicated(keep=False), 'order_id' ])

df_order_pmts.loc[ df_order_pmts.order_id == '510bff1cf06be1143d3b6698df2fd486', ['payment_sequential', 'payment_installments'] ]
pd.value_counts(df_order_pmts.payment_installments).sort_index()  #about half the orders have 1 installment; about half have multiple

df_order_pmts.loc[ df_order_pmts.payment_installments != 21, ['payment_sequential', 'payment_installments'] ]
df_order_pmts.loc[ df_order_pmts.payment_installments == 21, ]


df_multipmt_multiinstall = df_order_pmts.loc[ ( ( df_order_pmts.payment_installments != 1 ) & ( df_order_pmts.payment_sequential != 1 ) ) ,  ]

df_multipmt_multiinstall = df_multipmt_multiinstall.sort_values(['order_id', 'payment_installments', 'payment_sequential'])

df_multipmt_multiinstall2 = df_order_pmts.merge(df_multipmt_multiinstall.order_id, how='inner')
df_multipmt_multiinstall2 = df_multipmt_multiinstall2.sort_values(['order_id', 'payment_installments', 'payment_sequential'])
#payment_sequential:  a customer may pay an order with more than one payment method. If he does so, a sequence will be created to accommodate all payments
#number of installments chosen by the customer.

#pd.options(columns = 140)

df_order_reviews.info()    #100,000 reviews, for 99,441 orders
sum(pd.isnull(df_order_reviews.order_id))   #0, perfect, always populated
len(pd.unique(df_order_reviews.order_id))   #but is not always unique.  Not fatal, just note
sum(pd.isnull(df_order_reviews.review_score))   #0, perfect, always populated
pd.value_counts(df_order_reviews.review_score)   #1 thru 5, mostly 5s and 4s







# ====================================================
# merge the normalized datasets into one big flat file
# ====================================================

#add customer info
df_merged = df_orders.merge(df_customers, how='left', on='customer_id')
df_merged.info()  #still have 99,441 rows, good
sum(pd.isnull(df_merged.customer_id))  #0, perfect
sum(pd.isnull(df_merged.customer_unique_id))  #0, perfect, no problems joining on order_id between these two tables




#add payments info.  
# -----------------
# a) summarize pmt info to total per order
df_pmt_smry_by_order = df_order_pmts.groupby(['order_id']).agg(
            ttl_pd=('payment_value', 'sum'),
            pmt_mthds_used=('payment_sequential', 'count'),
            installments_used_ttl=('payment_installments', 'sum'),
            payment_types_used=('payment_type', 'nunique')
            )
df_pmt_smry_by_order = df_pmt_smry_by_order.reset_index()   #for some reason, can't get as_index to keep the order_id as a column.  However, this turns it back into a column
df_pmt_smry_by_order.info()
df_pmt_smry_by_order.head()



#            payment_types_mfu=('payment_type', 'lambda srs: pd.value_counts(srs.payment_type).index[0]')   #this works when not naming it (see next line); not sure how to name it
#                   df_order_pmts.groupby('order_id', as_index=False).agg(lambda x: pd.value_counts(x.payment_type).index[0])
#df_pmt_smry_by_order2 = df_order_pmts.groupby('order_id', as_index=False).agg({
#            "payment_value": np.sum,
#            "payment_sequential": pd.Series.nunique,
#            "payment_installments": np.sum,
#            "payment_type": lambda x: pd.value_counts(x.payment_type).index[0]  })

# b) find the most frequently used pmt type.    Note by default the value counts are sorted desc, so the biggest one is on top (index 0)
df_pmt_mfu_type = df_order_pmts.loc[:, ['order_id','payment_type']].groupby('order_id', as_index=False).agg(lambda x: pd.value_counts(x.payment_type).index[0])
df_pmt_mfu_type.columns = ['order_id', 'payment_type_mfu']
df_pmt_mfu_type.head()

 
#df_order_pmts.info()
#pd.value_counts(df_order_pmts.payment_type).index[0]
#df_order_pmts.groupby('order_id', as_index=False).agg(sum)

# c) join this field in with the rest
df_merged = df_merged.merge(df_pmt_mfu_type, how='left', on='order_id')
df_merged.info()  #still have 99,441 rows, good
sum(pd.isnull(df_merged.payment_type_mfu))   #1,   almost perfect,  the join always succeeded except for 1 order

# d) join the other payment related fields in with the rest
df_merged = df_merged.merge(df_pmt_smry_by_order, how='left', on='order_id')
df_merged.info()  #still have 99,441 rows, good
sum(pd.isnull(df_merged.ttl_pd))   #1,   almost perfect,  the join always succeeded except for 1 order





#add item-related info
# --------------------
    #includes sellers!!! (==> state, lat/long), product info (==> category)
    #shipping limit date!
    #price, freight - can just sum these as per data dictionary on Kaggle
    

#a) get a count of items per order to add to order level table
df_items_per_order =  df_order_items.groupby('order_id').agg(
        nbr_items=('order_id', 'count'),
        #Max_Item_ID=('order_item_id', 'max'),  #checking, this just counts up from one, so it's an equivalent way to get nbr_items
        ttl_price=('price', 'sum'),
        ttl_freight=('freight_value', 'sum'),
        ship_limit_final=('shipping_limit_date', 'max'),
        ship_limit_initial=('shipping_limit_date', 'min'),
        nbr_sellers=('seller_id', 'nunique'),
        nbr_products=('product_id', 'nunique'))
        
df_items_per_order = df_items_per_order.reset_index()
df_items_per_order.info()

#pd.value_counts(df_items_per_order.nbr_sellers)   #97k orders w/ 1 seller :),  1.2k w/ 2 sellers, 54 w/ 3, ... 2 orders w/ 5 sellers (max)
#pd.value_counts(df_items_per_order.nbr_products)   #95k orders w/ 1 product :),  2.8k w/ 2 products, 298 w/ 3, ... 1 order w/ 8 products (max)

# b) find the seller_id and product_id for the most frequently used sellers and products (per order)
df_seller_mfu = df_order_items.loc[:, ['order_id','seller_id']].groupby('order_id', as_index=False).agg(lambda x: pd.value_counts(x.seller_id).index[0])
df_seller_mfu.columns = ['order_id', 'seller_id_mfu']  #clarify
df_seller_mfu.info()
df_seller_mfu.head()
    #not sure how this would sort if the order had say 8 items with 4 from one seller and 4 from another seller

df_product_mfu = df_order_items.loc[:, ['order_id','product_id']].groupby('order_id', as_index=False).agg(lambda x: pd.value_counts(x.product_id).index[0])
df_product_mfu.columns = ['order_id', 'product_id_mfu']
df_product_mfu.info()



# c) add item count, ttl_price, .... to the orders table.   
df_merged = df_merged.merge(df_items_per_order, how='left', on='order_id')
df_merged.info()  #still have 99,441 rows, good
sum(pd.isnull(df_merged.order_id))  #0, perfect
sum(pd.isnull(df_merged.order_status))  #0, perfect, no problems joining on order_id between these two tables
sum(pd.isnull(df_merged.nbr_items))  #775 orders with 0 items?   cancelled?? special status? etc
    #pd.value_counts(df_merged.loc[ pd.isnull(df_merged.nbr_items), 'order_status'])
    #unavailable    603
    #canceled       164
    #created          5
    #invoiced         2
    #shipped          1


# d) add mfu_seller, mfu_product info to the orders table.   
df_merged = df_merged.merge(df_seller_mfu, how='left', on='order_id')
df_merged.info()  #still have 99,441 rows, good
df_merged = df_merged.merge(df_product_mfu, how='left', on='order_id')
df_merged.info()  #still have 99,441 rows, good

#TODO:   get maxdist seller and add for use in predictions???

#pick up attributes of the seller (if singular) or mfu_seller if multiple
df_merged = df_merged.merge(df_sellers, how='left', left_on='seller_id_mfu', right_on='seller_id')
df_merged.info()  #still have 99,441 rows, good
sum(pd.isnull(df_merged.seller_city))   #775, as per orders w/ 0 items






# add product info.  
# ==================
# a) sum details of the products
df_prods_by_order = df_order_items.merge(df_products, how='left', on='product_id')
#df_prods_by_order.index = df_prods_by_order.order_id
#df_prods_by_order.info()

df_prod_smry_by_order = df_prods_by_order.groupby('order_id').agg(
        nbr_photos = ('product_photos_qty', 'sum'),
        ttl_wt = ('product_weight_g', 'sum'),
        ttl_length = ('product_length_cm', 'sum'),
        ttl_height = ('product_height_cm', 'sum'),
        ttl_width = ('product_width_cm', 'sum'))

df_prod_smry_by_order = df_prod_smry_by_order.reset_index()
df_prod_smry_by_order.info()

df_prods_by_order = df_prods_by_order.merge(df_prdct_cat_translate, how='left', on='product_category_name')
#df_prods_by_order.info()


#translate the category names from Portuguese to English
df_prods_by_order_small = df_prods_by_order.loc[:, ['order_id','product_category_name_english']].copy()
df_prods_by_order_small.info()
df_prods_by_order_small.columns = ['order_id', 'product_ctgry']
df_prods_by_order_small.product_ctgry
df_prods_by_order_small = df_prods_by_order_small.loc[ ~ pd.isna(df_prods_by_order_small.product_ctgry) ]   #the mfu query below wasn't happy when there were orders but the product ctgry was na

#find the mfu product ctgry (in English)
df_product_category_mfu = df_prods_by_order_small.groupby('order_id', as_index=False).agg(lambda x: pd.value_counts(x.product_ctgry).index[0])
df_product_category_mfu.columns = ['order_id', 'product_ctgry_mfu']  #clarify
df_product_category_mfu.info()



#pick up product summary details
df_merged = df_merged.merge(df_prod_smry_by_order, how='left', on='order_id')
df_merged.info()  #still have 99,441 rows, good


df_merged = df_merged.merge(df_product_category_mfu, how='left', on='order_id')
df_merged.info()  #still have 99,441 rows, good
sum(pd.isnull(df_merged.product_ctgry_mfu))   #2185   -- pretty sure this is OK (and/or not fixable if not :) )






#add review info.  
# ==================
#a) summarize reviews by order
df_order_reviews.info()
df_review_smry = df_order_reviews.groupby('order_id').agg(
            nbr_rws = ('review_id', 'count'),
            avg_score = ('review_score', 'mean'), 
            earliest_review_dt = ('review_answer_timestamp', 'min'),
            latest_review_dt = ('review_answer_timestamp', 'max'))
            
df_review_smry = df_review_smry.reset_index()
df_review_smry.info()
df_review_smry.describe()

# b) merge info back to the orders table
df_merged = df_merged.merge(df_review_smry, how='left', on='order_id')
df_merged.info()  #now have 113,322 b/c a few orders have multiple reviews
sum(pd.isnull(df_merged.order_id))   #0, perfect, always populated
sum(pd.isnull(df_merged.avg_score))   #0, perfect, always populated  ==> join always succeeded





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





df_merged2 = df_merged.merge(df_geo_avg_by_zip_city_state2, how='left', left_on=['customer_zip_code_prefix', 'customer_city', 'customer_state'], right_on=['zip_prefix', 'city', 'state'])
#df_merged2.info()  #stiil have 99,441  as expected
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
df_merge_by_zip_and_city.info()    #318 rows attempted but still no success in joining
sum(pd.isnull(df_merge_by_zip_and_city.lat))    #318 rows attempted but still no success in joining


#try one last time to see if the customer zips are found in the lookup table     
df_merge_by_zip = df_merged2[ pd.isnull(df_merged2.lat) ][ cols ].merge(df_geo_avg_by_zip2, how='left', left_on=['customer_zip_code_prefix'], right_on=['zip_prefix'])
df_merge_by_zip.drop(['zip_prefix'], axis='columns', inplace=True)
df_merge_by_zip.info()    #318 rows attempted, 40 lat/longs found
sum(pd.isnull(df_merge_by_zip.lat))    #318.    40 rows were found, 317 were not


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
df_merged4.info()  #stiil have 99,441 as expected
sum(pd.isnull(df_merged4.lat))  #3442     
sum(pd.isna(df_merged3.seller_zip_code_prefix))  #775     
sum(pd.isnull(df_merged3.seller_city))  #775     
sum(pd.isnull(df_merged3.seller_state))  #775 
    #apparently some of the sellers are from zip/city/states not in the lat/long lookup table.   retry by zip and state
    
#prune out these join columns that have been added in unnecessarily
df_merged4.drop(['zip_prefix', 'city', 'state'], axis='columns', inplace=True)


#try joining on just zip & city and see if that succeeds (maybe the states were null or conflicting??)
   
#for the 2nd attempt at joining on zip&city, prune out the lat & long columns as a) they are null anyway and b) they cause diff lat&long cols to get created like lat_y, long_y
cols = [col for col in df_merged4.columns if col not in ['lat', 'long']]
df_merge_by_seller_zip_and_city = df_merged4[ pd.isnull(df_merged4.lat) ][ cols ].merge(df_geo_avg_by_zip_city2, how='left', left_on=['seller_zip_code_prefix', 'seller_city'], right_on=['zip_prefix', 'city'])
df_merge_by_seller_zip_and_city.drop(['zip_prefix', 'city'], axis='columns', inplace=True)
df_merge_by_seller_zip_and_city.info()    #576 rows w/ lat/long now
sum(pd.isnull(df_merge_by_seller_zip_and_city.lat))    #still 2866 rows w/ no success in joining



#copy the rows for which we did NOT find a lat long  in the last attempt 
rw_ids_fnd_by_seller_zip_and_state = df_merge_by_seller_zip_and_city[pd.notnull(df_merge_by_seller_zip_and_city.lat)].Rww_ID
#copy everything else into a new dataset
df_merged5 = df_merged4[ ~  df_merged4.Rww_ID.isin(rw_ids_fnd_by_seller_zip_and_state)  ].copy()


#add in the rows for which we found a lat long  in the last attempt 
df_merged5 = df_merged5.append( df_merge_by_seller_zip_and_city[ pd.notnull(df_merge_by_seller_zip_and_city.lat) ].copy() )
     
df_merged5.info()
#99,441, with 96,575 not null for lat/long


#try one last time to see if the customer zips are found in the lookup table     
df_merge_by_seller_zip = df_merged5[ pd.isnull(df_merged5.lat) ][ cols ].merge(df_geo_avg_by_zip2, how='left', left_on=['seller_zip_code_prefix'], right_on=['zip_prefix'])
df_merge_by_seller_zip.drop(['zip_prefix'], axis='columns', inplace=True)
df_merge_by_seller_zip.info()    #2866 rows attempted, 1872 lat/longs found
sum(pd.isnull(df_merge_by_seller_zip.lat))    #994 rows still don't have a lat/long





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



df_merged6.to_csv(wkg_dir+'Order_level_dataset.csv')
