-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers that computes and store the average weighted score for all students.
-- Procedure ComputeAverageWeightedScoreForUsers must not take any input.

DELIMITER ..
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    UPDATE users AS user,
    (
        SELECT user.id, SUM(score * weight) / SUM(weight) AS aws
        FROM users AS user JOIN corrections AS c ON user.id = c.user_id
        JOIN projects AS p ON c.project_id = p.id
        GROUP BY user.id
    )
    AS RESULT SET user.average_score = RESULT.aws
    WHERE user.id = RESULT.id;
END ..
