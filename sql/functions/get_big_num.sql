USE freebee;

DELIMITER $$

DROP FUNCTION IF EXISTS get_big_num $$
CREATE FUNCTION get_big_num()
RETURNS INTEGER
BEGIN
	RETURN pow(2, 31) - 1;
END
$$

DELIMITER ;
