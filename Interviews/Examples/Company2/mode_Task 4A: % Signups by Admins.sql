-- The Sales Managers come to you with a set of questions;
-- “How often is the user who signs up a company for the product also an admin of that company?
-- Also, what is the typical breakdown of Admins/Non-Admins at companies?”
-- Help them answer these questions and deliver the answers with
-- enough context and nuance as you feel is appropriate. Make sure to also show the code you used to
-- obtain these answers
 -- “How often is the user who signs up a company for the product also an admin of that company?

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
