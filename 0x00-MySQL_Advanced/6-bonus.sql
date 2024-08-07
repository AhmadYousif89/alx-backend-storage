-- SQL script that creates a stored procedure AddBonus that adds a new correction for a student.
-- Procedure AddBonus is taking 3 inputs (in this order): 
-- -- user_id, a users.id value (assuming user_id is linked to an existing users)
-- -- project_name, a new or already exists projects - if no projects.name found in the table, you should create it
-- -- score, the score value for the correction

DELIMITER ..
DROP PROCEDURE IF EXISTS AddBonus;
CREATE PROCEDURE AddBonus(IN user_id INT, IN project_name VARCHAR(255), IN score INT)
BEGIN
    DECLARE project_id INT;

    IF NOT EXISTS (SELECT id FROM projects WHERE name = project_name) THEN
        INSERT INTO projects (name) VALUES (project_name);
    END IF;

    SET project_id = (SELECT id FROM projects WHERE name = project_name);

    INSERT INTO corrections (user_id, project_id, score) VALUES (user_id, project_id, score);
END ..
