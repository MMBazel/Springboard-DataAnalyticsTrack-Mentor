# Interesting Code Snippets


# Have a data frame but the last couple columns don't have the necessary values. 
# This is a pretty slow process but this will iterate through the rows then columns
# Check the column names match a pattern 
# If null, then fill in the values with the prior values

for i, row in data.iterrows():
    prev_j = 0
    for j, col in enumerate(data.columns):  
        if ('week_' in col) and pd.isnull(data.iloc[i,j]):
            data.iloc[i,j] = data.iloc[i,prev_j]    
        prev_j = j


# Example of using melt to pivot multiple columns for both variables & values
# Like a really really wide dataset

data_pivot = pd.melt(data, id_vars=['id', 'name', 'min_ods_update', 'id.1', 'name.1',
       'qualification_date__c', 'ods_update_date', 'forecast_new_arr__c',
       'opportunity_source__c', 'ownerid','level_9_id', 'level_9_name',
       'level_9_role_hierarchy_name', 'level_9_region', 'level_9_segment',
       'level_9_role_short_name','id.2', 'stagename'],value_vars=['week_1', 'week_2', 'week_3',
       'week_4', 'week_5', 'week_6', 'week_7', 'week_8', 'week_9', 'week_10',
       'week_11', 'week_12', 'week_13', 'week_14', 'week_15', 'week_16',
       'week_17', 'week_18', 'week_19', 'week_20', 'week_21', 'week_22',
       'week_23', 'week_24', 'week_25'])
