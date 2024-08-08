-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser that computes and store the average weighted score for a student.

DELIMITER ..
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN student_id INT)
BEGIN
    DECLARE average_weighted_score FLOAT;
    
    SELECT SUM(score * weight) / SUM(weight) INTO average_weighted_score
    FROM users AS u JOIN corrections AS c ON u.id = c.user_id
    JOIN projects AS p ON c.project_id = p.id
    WHERE u.id = student_id;

    UPDATE users SET average_score = average_weighted_score WHERE id = student_id;
END ..
