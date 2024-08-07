-- SQL script that creates a stored procedure ComputeAverageScoreForUser that computes and store the average score for a student.
-- Procedure ComputeAverageScoreForUser is taking 1 input (in this order):
-- -- user_id, a users.id value (assuming user_id is linked to an existing users)

DELIMITER ..
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
CREATE PROCEDURE ComputeAverageScoreForUser(IN u_id INT)
BEGIN
    DECLARE avg_score FLOAT;

    SELECT AVG(score) INTO avg_score FROM corrections WHERE user_id = u_id;

    UPDATE users SET average_score = avg_score WHERE id = u_id;
END ..
