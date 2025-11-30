DROP TABLE IF EXISTS creative_daily_fact;

CREATE TABLE creative_daily_fact AS
SELECT
	fb.date::date AS date,
    fb.campaign_id,
    fb.campaign_name,
    fb.spend,
    fb.clicks,
    
    split_part(fb.campaign_name, ' ', 1) AS articleid,
    split_part(fb.campaign_name, ' ', 2) AS type,
    split_part(fb.campaign_name, ' ', 3) AS version,
    split_part(fb.campaign_name, ' ', 4) AS os,
    regexp_replace(regexp_substr(fb.campaign_name, '\((.*?)\)'), '\(|\)', '', 'g') AS author,
    split_part(fb.campaign_name, ' ', 6) AS media,

    mp.adset_id,
	
    COALESCE(gm.banner_revenue, 0) AS banner_revenue,
    COALESCE(gm.video_revenue, 0) AS video_revenue,
    (COALESCE(gm.banner_revenue, 0) + COALESCE(gm.video_revenue, 0)) AS total_revenue,

    cr.created_date::date AS created_date,
    cr.headline,
    cr.media_link,
    cr.revenue_spend AS revenue_indicator,


    -- Метрики
    (COALESCE(gm.banner_revenue, 0) + COALESCE(gm.video_revenue, 0))
       - COALESCE(fb.spend, 0) AS profit,

    CASE
        WHEN fb.spend = 0 THEN NULL
        ELSE (COALESCE(gm.banner_revenue, 0) + COALESCE(gm.video_revenue, 0)) / fb.spend
    END AS roas,

    (fb.date::date - cr.created_date::date) AS day_since_created,

    (fb.date::date - cr.created_date::date) BETWEEN 0 AND 3 AS in_test_window

FROM facebook_table fb


LEFT JOIN mapping_table mp
    ON fb.campaign_id = mp.campaign_id

LEFT JOIN gam_table gm
    ON mp.adset_id = gm.adset_id
   AND fb.date = gm.date

LEFT JOIN creative_table cr
   ON split_part(fb.campaign_name, ' ', 1)::int = cr.articleid
  AND split_part(fb.campaign_name, ' ', 2) = cr.type
  AND split_part(fb.campaign_name, ' ', 3) = cr.version
  AND split_part(fb.campaign_name, ' ', 6) = cr.media
  AND regexp_replace(regexp_substr(fb.campaign_name, '\((.*?)\)'), '\(|\)', '', 'g') = cr.author;





  