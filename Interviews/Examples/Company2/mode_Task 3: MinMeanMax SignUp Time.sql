-- The Product Managers on your team have a follow-up question;
-- “For users whose first experience using the product was using it to “check-in”
-- at a location, how long does it tend to take them to
-- sign up for the product starting from the first time they used it?”
-- Help them answer this question
-- and deliver the answer with enough context and nuance as you feel is appropriate.
-- Make sure to also
-- show the code you used to obtain this answer.

SELECT distinct(count(f.user_id)) AS users,
       min(f.hours_signup) AS min_hrs_signUp,
       round(avg(f.hours_signup)) AS mean_hrs_signUp,
       max(f.hours_signup) AS max_hrs_signUp
FROM
  (SELECT t1.user_id,
          earliest_check_in_date,
          earliest_sign_up_date,
          age(earliest_sign_up_date,earliest_check_in_date) AS time_to_signup,
          round(EXTRACT(epoch
                        FROM age(earliest_sign_up_date,earliest_check_in_date)/3600)) AS hours_signup,
          NTILE(100) over (
                           ORDER BY (age(earliest_sign_up_date,earliest_check_in_date))) AS percentile
   FROM -- Get earliest check in date

     (SELECT a.user_id,
             min(a.created_at) filter (
                                       WHERE a.event_type ='check_in') over (partition BY a.user_id
                                                                             ORDER BY a.user_id DESC) AS earliest_check_in_date,
                               min(a.created_at) filter (
                                                         WHERE a.event_type ='sign_up') over (partition BY a.user_id
                                                                                              ORDER BY a.user_id DESC) AS earliest_sign_up_date
      FROM arvindr12.dummy_events AS a) t1
   WHERE t1.earliest_check_in_date < t1. earliest_sign_up_date
   ORDER BY 4 ASC) f
