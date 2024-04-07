AVG_PRICE_QUERY = """
WITH RECURSIVE orig_region_tree AS (
    SELECT slug, parent_slug
    FROM regions
    WHERE slug = %s
    UNION ALL
    SELECT r.slug, r.parent_slug
    FROM regions r
    JOIN orig_region_tree rt ON r.parent_slug = rt.slug
),
dest_region_tree AS (
    SELECT slug, parent_slug
    FROM regions
    WHERE slug = %s
    UNION ALL
    SELECT r.slug, r.parent_slug
    FROM regions r
    JOIN dest_region_tree rt ON r.parent_slug = rt.slug
),
date_series AS (
    SELECT generate_series(%s::date, %s::date, '1 day'::interval)::date AS day
)

SELECT  
    TO_CHAR(ds.day, 'YYYY-MM-DD') AS day,
    CASE WHEN COUNT(pd.day) < 3 THEN NULL ELSE ROUND(AVG(pd.price)) END AS average_price
FROM 
    date_series ds
LEFT JOIN 
    (
    SELECT  
        pd.day AS day,
        pd.price
    FROM 
        price_detail pd
    JOIN
        route r ON r.id = pd.route_id
    WHERE 
        (r.orig_code = %s OR r.orig_region IN (SELECT slug FROM orig_region_tree))
        AND (r.dest_code = %s OR r.dest_region IN (SELECT slug FROM dest_region_tree))
        AND pd.day BETWEEN %s AND %s
    ) AS pd ON ds.day = pd.day
GROUP BY 
    ds.day
ORDER BY 
    ds.day;
"""
