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
len(pd.unique(df_order_pmts.order_id))   #1 less than # of orders ==> one is duplicated somewhere.  track down and check later
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


df_merged.to_csv(wkg_dir+'Merged_dataset.csv')

#customer_id	a.customer_unique_id	a.customer_zip_code_prefix	a.customer_city	a.customer_state	b.order_id	b.order_status	b.order_purchase_timestamp	b.order_approved_at	b.order_delivered_carrier_date	b.order_delivered_customer_date	b.order_estimated_delivery_date	c.payment_type	c.payment_installments	c.payment_value


#add lat/long info for the customers
#df_merged = df_merged.merge(df_geolocation, how='left', left_on='customer_zip_code_prefix', right_on='geolocation_zip_code_prefix')
#df_merged.info()  #now have 118,318 as a few orders have multiple pmt dtls rows (and/or dup order ids?)
#
