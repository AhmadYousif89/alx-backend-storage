-- SQL script that creates a trigger that resets the attribute valid_email to 0 only when the email has been changed.

DELIMITER ..
CREATE TRIGGER revalidate_email
BEFORE UPDATE ON users FOR EACH ROW 
BEGIN
    IF NEW.email != OLD.email THEN
        SET NEW.valid_email = 0;
    END IF;
END ..
