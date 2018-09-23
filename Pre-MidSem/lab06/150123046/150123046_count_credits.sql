-- 150123046_count_credits.sql
DROP PROCEDURE IF EXISTS count_credits; #trivial
DELIMITER $$ #makes $$ the DELIMITER
CREATE PROCEDURE count_credits()
BEGIN
	DECLARE r VARCHAR(20); #variable for roll_number
	DECLARE n VARCHAR(50); #variable for name
	DECLARE cr, tcr INTEGER DEFAULT 0; #variable for current_course_credits and total_credits for a roll_number (read student), respectively
	DECLARE rn_done, cr_done BOOLEAN DEFAULT FALSE; #variable for continue handlers

	DECLARE cur_rn CURSOR FOR SELECT DISTINCT roll_number, name FROM cwsl ORDER BY roll_number; #cursor for roll_number and name, to be used later
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET rn_done = TRUE;

	CREATE TEMPORARY TABLE IF NOT EXISTS cc_clash (roll_number VARCHAR(20), name VARCHAR(50), total_credits INTEGER, PRIMARY KEY (roll_number)); #temporary table for storing the output cases before displaying

	OPEN cur_rn;
	rn_loop: LOOP
		FETCH FROM cur_rn INTO r, n;
		IF rn_done THEN
			CLOSE cur_rn;
			LEAVE rn_loop;
		END IF;

		SET tcr = 0; #initialise the value of total_credits at zero for each roll_number

		BLOCK_cr: BEGIN
			DECLARE cur_cr CURSOR FOR SELECT number_of_credits FROM cc WHERE course_id IN (SELECT course_id FROM cwsl WHERE roll_number = r); #cursor for credits of courses that the student with the roll_number in outer cursor is enrolled-in
			DECLARE CONTINUE HANDLER FOR NOT FOUND SET cr_done = TRUE;
			SET cr_done = FALSE;
			OPEN cur_cr;
			cr_loop: LOOP
				FETCH FROM cur_cr INTO cr;
				IF cr_done THEN
					CLOSE cur_cr;
					LEAVE cr_loop;
				END IF;

				SET tcr = tcr + cr; #increment the total_credits by the number_of_credits of the course in inner cursor

			END LOOP cr_loop;
		END BLOCK_cr;

		IF (tcr > 40) THEN
			INSERT INTO cc_clash (roll_number, name, total_credits) VALUES (r, n, tcr) ON DUPLICATE KEY UPDATE roll_number=r, name=n, total_credits=tcr; #insert entries of output into the temporary table 
		END IF;

	END LOOP rn_loop;

	SELECT * FROM cc_clash ORDER BY roll_number; #displaying the output
	DROP TABLE IF EXISTS cc_clash;

END$$
DELIMITER ; #makes ; the DELIMITER again
