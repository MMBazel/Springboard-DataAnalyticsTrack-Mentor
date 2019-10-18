-- Prompt: The Product Managers on your team have come to you with a question;
-- “How many check-in’s does a user tend to have before signing up their own company 
-- for the product?” Help them answer this question and deliver the answer with
-- enough context and nuance as you feel is appropriate. 
-- Make sure to also show the code you used to obtain this answer.


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
