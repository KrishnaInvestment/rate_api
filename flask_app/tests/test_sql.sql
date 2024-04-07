CREATE TABLE regions (
    slug text NOT NULL,
    name text NOT NULL,
    parent_slug text
);


CREATE TABLE route (
    id BIGSERIAL PRIMARY KEY,
    orig_code text,
    dest_code text,
    orig_region text,
    dest_region text
);

ALTER TABLE route
ADD CONSTRAINT route_id_unique UNIQUE (id);


-- First, create the price_detail table
CREATE TABLE price_detail (
    id bigint,
    route_id bigint,
    day date,
    price integer
);

-- Then, add a foreign key constraint to the route_id column
ALTER TABLE price_detail
ADD CONSTRAINT fk_route_id FOREIGN KEY (route_id) REFERENCES route(id);


INSERT INTO regions (slug, name, parent_slug) 
VALUES
    ('china_main', 'China Main', NULL),
    ('northern_europe', 'Northern Europe', NULL),
    ('kattegat', 'Kattegat', 'scandinavia'),
    ('norway_north_west', 'Norway North West', 'scandinavia'),
    ('norway_south_east', 'Norway South East', 'scandinavia'),
    ('norway_south_west', 'Norway South West', 'scandinavia'),
    ('china_east_main', 'China East Main', 'china_main'),
    ('china_south_main', 'China South Main', 'china_main'),
    ('scandinavia', 'Scandinavia', 'northern_europe');


INSERT INTO route (id, orig_code, dest_code, orig_region, dest_region) 
VALUES  
        (30, 'CNCWN', 'NOGJM', 'china_south_main', 'scandinavia'),
        (650, 'CNYTN', 'NOFRO', 'china_south_main', 'scandinavia'),
        (651, 'CNYTN', 'NOGJM', 'china_south_main', 'scandinavia'),
        (652, 'CNYTX', 'NOMJM', 'china_east_main', 'norway_south_west');

INSERT INTO price_detail (route_id, price, day)
VALUES 
       (30, 2664, '2016-01-01'),
       (30, 1768, '2016-01-01'),
       (30, 2000, '2016-01-01'),
       (651, 1770, '2016-01-01'),
       (651, 1983, '2016-01-01'),
       (651, 2672, '2016-01-01'),
       (652, 1584, '2016-01-01'),
       (652, 2000, '2016-01-01'),
       (651, 1983, '2016-01-02'),
       (651, 2672, '2016-01-02'),
       (651, 1770, '2016-01-02'),
       (30, 2664, '2016-01-02'),
       (30, 1768, '2016-01-02'),
       (30, 2663, '2016-01-05'),
       (30, 1767, '2016-01-05'),
       (651, 1769, '2016-01-05'),
       (651, 1768, '2016-01-06'),
       (651, 2671, '2016-01-06');