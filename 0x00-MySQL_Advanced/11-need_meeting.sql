-- SQL script that creates a view need_meeting that lists all students that have a score under 80 (strict) and no last_meeting or more than 1 month.
-- The view need_meeting should return all students name when: 
-- -- the student has a score under 80 (strict) AND (no last_meeting date or more than a month ago)

DROP VIEW IF EXISTS need_meeting;
CREATE VIEW need_meeting AS SELECT name FROM students
WHERE score < 80 AND (last_meeting IS NULL OR last_meeting < ADDDATE(CURDATE(), INTERVAL -1 MONTH));
