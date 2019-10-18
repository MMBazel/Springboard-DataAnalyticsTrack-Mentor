# Python Notebook - Envoy Interview

import matplotlib.pyplot as plt

datasets

users_df = datasets['Task 1: [DATA] Users']

users_df.info()

users_df.head()

users_df.tail()

users_df.groupby('company_type').describe()

events_df = datasets['Task 1: [DATA] Events']

events_df.info()

events_df.head()

events_df.tail()

events_df.groupby('event_type').count()

events_df.groupby(['event_type','user_id']).count()

table_checkIn_freq = datasets['Task 2: [TABLE] Frequency of Check-Ins']

print(table_checkIn_freq.head())
print(table_checkIn_freq.tail())

plt.hist(table_checkIn_freq.total_prior_check_in)
plt.ylabel('Count of Users')
plt.xlabel('# of Check-Ins before Company Sign-up')
plt.suptitle('Distribution of Check-In #s before Sign-up')
plt.title('Red = Avg # of Check-Ins | Green = Mid of Check-Ins')
plt.vlines(x=table_checkIn_freq.total_prior_check_in.mean(),ymin=0,ymax=350,color='r',label='avg')
plt.vlines(x=table_checkIn_freq.total_prior_check_in.median(),ymin=0,ymax=350,color='G',label='MED')

table_checkIn_freq.info()

table_checkIn_freq.total_prior_check_in.describe()

table_time_to_signup = datasets['Task 3: [TABLE] Frequency - Time to Sign-Up']

table_time_to_signup.info()

print(table_time_to_signup.head())
print('\n')
print(table_time_to_signup.tail())

table_time_to_signup.hours_signup.describe()

plt.hist(table_time_to_signup.hours_signup)
plt.ylabel('Count of Users')
plt.xlabel('Hrs(#) from first use to Company Sign-up')
plt.suptitle('Distribution of Hrs(#) before Sign-up')
plt.title('Red = Avg # of Check-Ins | Green = Mid of Check-Ins')
plt.vlines(x=table_time_to_signup.hours_signup.mean(),ymin=table_time_to_signup.hours_signup.min(),ymax=table_time_to_signup.hours_signup.count(),color='r',label='avg')
plt.vlines(x=table_time_to_signup.hours_signup.median(),ymin=table_time_to_signup.hours_signup.min(),ymax=table_time_to_signup.hours_signup.count(),color='G',label='MED')

### “How often is the user who signs up a company for the product also an admin of that company? 

table_signUps_by_admins = datasets['Task 4A: % Signups by Admins']

table_signUps_by_admins

### Also, what is the typical breakdown of Admins/Non-Admins at companies?” 

table_admins_vs_nonadmins = datasets['Task 4B: [TABLE] Composition of Admin/Non-Admin']

print(table_admins_vs_nonadmins.head())
print(table_admins_vs_nonadmins.tail())

table_admins_vs_nonadmins.total_users.describe()

admins_vs_nonadmins_comp = datasets['Task 4B: Composition of Admin/Non-Admin by Company Type']

admins_vs_nonadmins_comp

admins_vs_nonadmins_total = datasets['Task 4B: Composition of Admin/Non-Admin - Total']

admins_vs_nonadmins_total

plt.hist(table_admins_vs_nonadmins.total_users[table_admins_vs_nonadmins.total_users<60])
plt.ylabel('Count of Companies')
plt.xlabel('Total Users')
plt.suptitle('Distribution of Users(#) per company')
plt.title('Red = Avg # of Check-Ins | Green = Mid of Check-Ins')
plt.vlines(x=table_admins_vs_nonadmins.total_users.mean(),ymin=table_admins_vs_nonadmins.total_users.min(),ymax=table_admins_vs_nonadmins.total_users.count(),color='r',label='avg')
plt.vlines(x=table_admins_vs_nonadmins.total_users.median(),ymin=table_admins_vs_nonadmins.total_users.min(),ymax=table_admins_vs_nonadmins.total_users.count(),color='G',label='MED')

######################################################
####################### Task 1 #######################
######################################################

# Task 1: [DATA] Events

select *
from arvindr12.dummy_events

# Task 1: [DATA] Users

select *
from arvindr12.dummy_users

######################################################
####################### Task 2 #######################
######################################################


# Task 2: [TABLE] Frequency of Check-Ins


SELECT d.user_id,
          sum(d.prior_check_in) AS total_prior_check_in,
          NTILE(100) over (
                           ORDER BY sum(d.prior_check_in)) AS percentile
   FROM
     (SELECT c.user_id,
             c.created_at,
             c.event_type,
             earliest_sign_up_date,
             (CASE
                  WHEN c.created_at < earliest_sign_up_date then 1
                  ELSE null
              END) AS prior_check_in --3. If an event was before the earliest sign up date, flag
FROM arvindr12.dummy_events AS c --2. Join back to events table
left join -- 1. Pull list of earliest sign up date by user

          (SELECT a.user_id,
                  min(a.created_at) AS earliest_sign_up_date
         FROM arvindr12.dummy_events AS a
         WHERE a.event_type ='sign_up'
         group by 1) AS b
        ON (b.user_id = c.user_id)
      WHERE earliest_sign_up_date is not null ) AS d
   GROUP BY 1
   HAVING sum(d.prior_check_in) > 0
   ORDER BY 2 ASC
   
   
   
   

######################################################
####################### Task 3 #######################
######################################################

# Task 3: [TABLE] Frequency - Time to Sign-Up

SELECT t1.user_id,
       earliest_check_in_date,
       earliest_sign_up_date,
       age(earliest_sign_up_date,earliest_check_in_date) AS time_to_signup,
       round(EXTRACT(epoch
                     FROM age(earliest_sign_up_date,earliest_check_in_date)/3600)) AS hours_signup,
       NTILE(100) over (
                        ORDER BY (age(earliest_sign_up_date,earliest_check_in_date))) AS percentile
FROM -- Get earliest check in date

  (SELECT a.user_id,
          min(a.created_at) AS earliest_check_in_date
   FROM arvindr12.dummy_events AS a
   WHERE a.event_type ='check_in'
   GROUP BY 1) t1
inner join
  (SELECT a.user_id,
          min(a.created_at) AS earliest_sign_up_date
   FROM arvindr12.dummy_events AS a
   WHERE a.event_type ='sign_up'
   GROUP BY 1) t2
  ON (t1.user_id = t2.user_id)
WHERE t1.earliest_check_in_date < t2. earliest_sign_up_date
ORDER BY 4 ASC

######################################################
####################### Task 4 #######################
######################################################

# Task 4A: % Signups by Admins
SELECT t2.is_admin,
       count(t1.user_id)
FROM arvindr12.dummy_events AS t1
LEFT JOIN
  (SELECT user_id,
          is_admin
   FROM arvindr12.dummy_users) AS t2
  ON (t1.user_id = t2.user_id)
WHERE t1.event_type='sign_up'
group by 1



# Task 4B: [TABLE] Composition of Admin/Non-Admin
SELECT t1.company_type,
       t1.company_id,
       (CASE WHEN t1.is_admin='true' then t1.count_users else 0 END) AS admin_num,
       (CASE WHEN t1.is_admin='false' then t1.count_users else 0 END) AS nonadmin_num,
       (((CASE WHEN t1.is_admin='true' then t1.count_users else 0 END))+
       ((CASE WHEN t1.is_admin='false' then t1.count_users else 0 END))) as total_users,
        round((CASE WHEN t1.is_admin='true' then t1.count_users else 0 END)/
        (((CASE WHEN t1.is_admin='true' then t1.count_users else 0 END))+
        ((CASE WHEN t1.is_admin='false' then t1.count_users else 0 END)))*100) perc_admins
FROM
  (SELECT company_type,
          company_id,
          is_admin,
          count(user_id) AS count_users
   FROM arvindr12.dummy_users
   GROUP BY 1,
            2,
            3) t1
            
            
# Task 4B: Composition of Admin/Non-Admin - Total

SELECT round(avg(t2.admin_num)) as mean_admin_num,
       round(avg(t2.nonadmin_num)) as mean_nonadmin_num,
       round(avg(t2.total_users)) as mean_total_users,
       min(t2.perc_admins) as min_perc_admins,
       round(avg(t2.perc_admins)) as mean_perc_admins,
       max(t2.perc_admins) as max_perc_admins
FROM
  (SELECT t1.company_type,
          t1.company_id,
          (CASE
               WHEN t1.is_admin='true' then t1.count_users
               ELSE 0
           END) AS admin_num,
          (CASE
               WHEN t1.is_admin='false' then t1.count_users
               ELSE 0
           END) AS nonadmin_num,
          (((CASE
                 WHEN t1.is_admin='true' then t1.count_users
                 ELSE 0
             END))+ ((CASE
                          WHEN t1.is_admin='false' then t1.count_users
                          ELSE 0
                      END))) AS total_users,
          round((CASE
                     WHEN t1.is_admin='true' then t1.count_users
                     ELSE 0
                 END)/ (((CASE
                              WHEN t1.is_admin='true' then t1.count_users
                              ELSE 0
                          END))+ ((CASE
                                       WHEN t1.is_admin='false' then t1.count_users
                                       ELSE 0
                                   END)))*100) perc_admins
   FROM
     (SELECT company_type,
             company_id,
             is_admin,
             count(user_id) AS count_users
      FROM arvindr12.dummy_users
      GROUP BY 1,
               2,
               3) t1) t2
               
               
               
# Task 4B: Composition of Admin/Non-Admin by Company Type

-- The Sales Managers come to you with a set of questions;
-- “How often is the user who signs up a company for the product also an admin of that company?
-- Also, what is the typical breakdown of Admins/Non-Admins at companies?”
-- Help them answer these questions and deliver the answers with
-- enough context and nuance as you feel is appropriate. Make sure to also show the code you used to
-- obtain these answers
-- Also, what is the typical breakdown of Admins/Non-Admins at companies?”

SELECT t2.company_type,
       round(avg(t2.admin_num)) as mean_admin_num,
       round(avg(t2.nonadmin_num)) as mean_nonadmin_num,
       round(avg(t2.total_users)) as mean_total_users,
       min(t2.perc_admins) as min_perc_admins,
       round(avg(t2.perc_admins)) as mean_perc_admins,
       max(t2.perc_admins) as max_perc_admins
FROM
  (SELECT t1.company_type,
          t1.company_id,
          (CASE
               WHEN t1.is_admin='true' then t1.count_users
               ELSE 0
           END) AS admin_num,
          (CASE
               WHEN t1.is_admin='false' then t1.count_users
               ELSE 0
           END) AS nonadmin_num,
          (((CASE
                 WHEN t1.is_admin='true' then t1.count_users
                 ELSE 0
             END))+ ((CASE
                          WHEN t1.is_admin='false' then t1.count_users
                          ELSE 0
                      END))) AS total_users,
          round((CASE
                     WHEN t1.is_admin='true' then t1.count_users
                     ELSE 0
                 END)/ (((CASE
                              WHEN t1.is_admin='true' then t1.count_users
                              ELSE 0
                          END))+ ((CASE
                                       WHEN t1.is_admin='false' then t1.count_users
                                       ELSE 0
                                   END)))*100) perc_admins
   FROM
     (SELECT company_type,
             company_id,
             is_admin,
             count(user_id) AS count_users
      FROM arvindr12.dummy_users
      GROUP BY 1,
               2,
               3) t1) t2
GROUP BY 1

