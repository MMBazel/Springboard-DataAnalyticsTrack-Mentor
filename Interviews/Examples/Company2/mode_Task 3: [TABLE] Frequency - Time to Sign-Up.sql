-- The Product Managers on your team have a follow-up question;
-- “For users whose first experience using the product was using it to “check-in”
-- at a location, how long does it tend to take them to
-- sign up for the product starting from the first time they used it?”
-- Help them answer this question
-- and deliver the answer with enough context and nuance as you feel is appropriate.
-- Make sure to also
-- show the code you used to obtain this answer.

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
