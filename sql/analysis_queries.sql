-- Student Performance Analysis SQL queries
-- Run against student_performance_db after loading data.

USE student_performance_db;

-- A. View student records
SELECT *
FROM students
LIMIT 10;

-- B. Average marks by subject
SELECT
    ROUND(AVG(mathematics_marks), 2) AS avg_mathematics,
    ROUND(AVG(science_marks), 2) AS avg_science,
    ROUND(AVG(english_marks), 2) AS avg_english,
    ROUND(AVG(social_science_marks), 2) AS avg_social_science,
    ROUND(AVG(computer_marks), 2) AS avg_computer
FROM students;

-- C. Students with attendance below 75%
SELECT student_id, student_name, class_name, attendance_percentage
FROM students
WHERE attendance_percentage < 75
ORDER BY attendance_percentage ASC;

-- D. Compare class performance
SELECT
    class_name,
    ROUND(AVG(
        (mathematics_marks + science_marks + english_marks
         + social_science_marks + computer_marks) / 5
    ), 2) AS average_score
FROM students
GROUP BY class_name
ORDER BY average_score DESC;

-- E. Top-performing students
SELECT
    student_id,
    student_name,
    class_name,
    ROUND((
        mathematics_marks + science_marks + english_marks
        + social_science_marks + computer_marks
    ) / 5, 2) AS average_score
FROM students
ORDER BY average_score DESC
LIMIT 10;

-- F. Subject-wise highest and lowest marks
SELECT
    MAX(mathematics_marks) AS max_mathematics, MIN(mathematics_marks) AS min_mathematics,
    MAX(science_marks) AS max_science, MIN(science_marks) AS min_science,
    MAX(english_marks) AS max_english, MIN(english_marks) AS min_english,
    MAX(social_science_marks) AS max_social_science, MIN(social_science_marks) AS min_social_science,
    MAX(computer_marks) AS max_computer, MIN(computer_marks) AS min_computer
FROM students;

-- G. Performance bands (project-defined thresholds)
SELECT
    CASE
        WHEN avg_score >= 80 THEN '80-100: Excellent'
        WHEN avg_score >= 60 THEN '60-79.99: Good'
        WHEN avg_score >= 40 THEN '40-59.99: Needs improvement'
        ELSE 'Below 40: At risk'
    END AS performance_band,
    COUNT(*) AS student_count
FROM (
    SELECT
        student_id,
        (mathematics_marks + science_marks + english_marks
         + social_science_marks + computer_marks) / 5 AS avg_score
    FROM students
) scored
GROUP BY performance_band
ORDER BY MIN(avg_score) DESC;
