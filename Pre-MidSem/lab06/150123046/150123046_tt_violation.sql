-- 150123046_tt_violation.sql
DROP PROCEDURE IF EXISTS tt_violation; #trivial
DELIMITER $$ #makes $$ the DELIMITER
CREATE PROCEDURE tt_violation()
BEGIN
	DECLARE r VARCHAR(20); #variable for roll_number
	DECLARE n VARCHAR(50); #variable for name
	DECLARE c1, c2 VARCHAR(20); #variable for course_ids
	DECLARE s1, s2, e1, e2 TIME; #variable for start and end times
	DECLARE rcc_done, dt_done BOOLEAN DEFAULT FALSE; #variable for continue handlers

	DECLARE cur_rcc CURSOR FOR SELECT DISTINCT t1.roll_number, t1.name, t1.course_id, t2.course_id FROM cwsl AS t1, cwsl AS t2 WHERE t1.roll_number = t2.roll_number AND t1.course_id > t2.course_id ORDER BY roll_number, t1.course_id, t2.course_id; #cursor for roll_number, name and distinct pairs of course_ids that the student with the given roll_number is enrolled-in, to be used later
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET rcc_done = TRUE;

	CREATE TEMPORARY TABLE IF NOT EXISTS tt_clash (roll_number VARCHAR(20), name VARCHAR(50), course_id1 VARCHAR(20), course_id2 VARCHAR(20), PRIMARY KEY (roll_number, name, course_id1, course_id2)); #temporary table for storing the output cases before displaying

	OPEN cur_rcc;
	rcc_loop: LOOP
		FETCH FROM cur_rcc INTO r, n, c1, c2;
		IF rcc_done THEN
			CLOSE cur_rcc;
			LEAVE rcc_loop;
		END IF;
		BLOCK_dt: BEGIN
			DECLARE cur_dt CURSOR FOR SELECT DISTINCT tc1.start_time, tc2.start_time, tc1.end_time, tc2.end_time FROM ett AS tc1, ett AS tc2 WHERE ((tc1.course_id = c1) AND (tc2.course_id = c2) AND (tc1.exam_date = tc2.exam_date)) ORDER BY tc1.start_time, tc2.start_time, tc1.end_time, tc2.end_time; #cursor for start and end times of courses that the outer cursor includes
			DECLARE CONTINUE HANDLER FOR NOT FOUND SET dt_done = TRUE;
			SET dt_done = FALSE;
			OPEN cur_dt;
			dt_loop: LOOP
				FETCH FROM cur_dt INTO s1, s2, e1, e2;
				IF dt_done THEN
					CLOSE cur_dt;
					LEAVE dt_loop;
				END IF;

				IF ((s1 <= s2 AND s2 <= e1) OR (s1 <= e2 AND e2 <= e1)) THEN #check for intersection of the exam-time periods
					INSERT INTO tt_clash (roll_number, name, course_id1, course_id2) VALUES (r, n, c1, c2) ON DUPLICATE KEY UPDATE roll_number=r, name=n, course_id1=c1, course_id2=c2; #insert entries of output into the temporary table
					CLOSE cur_dt;
					LEAVE dt_loop;
				END IF;

			END LOOP dt_loop;
		END BLOCK_dt;
	END LOOP rcc_loop;

	SELECT * FROM tt_clash ORDER BY roll_number, name, course_id1, course_id2; #displaying the output
	DROP TABLE IF EXISTS tt_clash;

END$$
DELIMITER ; #makes ; the DELIMITER again
