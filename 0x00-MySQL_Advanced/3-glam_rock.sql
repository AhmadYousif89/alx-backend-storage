-- SQL script that lists all bands with Glam rock as their main style, ranked by their longevity
-- Column names must be: band_name and lifespan (in years until 2022 - will use 2022 instead of YEAR(CURDATE()))
-- The script should return the band name and the number of years they have been active
-- columns (formed, split) will be used to calculate the lifespan
-- The script can be executed on any database

SELECT band_name, IFNULL(split, 2022) -  IFNULL(formed, 0) AS lifespan
FROM metal_bands WHERE style LIKE '%Glam rock%'
ORDER BY lifespan DESC;
