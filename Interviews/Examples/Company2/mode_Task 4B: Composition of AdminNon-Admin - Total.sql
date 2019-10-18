-- The Sales Managers come to you with a set of questions;
-- “How often is the user who signs up a company for the product also an admin of that company?
-- Also, what is the typical breakdown of Admins/Non-Admins at companies?”
-- Help them answer these questions and deliver the answers with
-- enough context and nuance as you feel is appropriate. Make sure to also show the code you used to
-- obtain these answers
-- Also, what is the typical breakdown of Admins/Non-Admins at companies?”

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
