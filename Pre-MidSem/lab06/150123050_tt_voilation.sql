  /* PLEASE WAIT AFTER CALLING TT_VOILATION (IT TAKES 4min 40sec to print the output)*/



  drop procedure tt_voilation; -- DELETING PREVIOUS tt_voilation

  drop table ett_voi; -- DELETING PREVIOUS ett_voi

  CREATE table ett_voi(roll_number int,name char(50),cid1 char(20),cid2 char(20)); -- TABLE CREATED FOR STORING OUTPUT..

  DELIMITER $$

  /*BEGIN PROCEDURE tt_voilation */
  CREATE PROCEDURE tt_voilation()
  BEGIN
    
    

    /**DECLARTION OF VARIABLES , ERROR handler and CURSORS */
    DECLARE out_cur_done BOOLEAN DEFAULT FALSE;
    
    /*VARIABLE FOR OUTER_CURSOR*/
    DECLARE r1 INT;
    DECLARE n1 char(50); 
    DECLARE cid1 char(10);
    DECLARE st1 time;
    DECLARE ed1 date;

    /*VARIABLES FOR INNER_CURSOR*/
    DECLARE r2 INT;
    DECLARE cid2 char(10);
    DECLARE st2 time;
    DECLARE ed2 date;

    /* OUTER CURSOR DECLARATION WHICH WILL ITERATE ON ROLL NUMBERS ONE BY ONE :- */

    DECLARE out_cur CURSOR FOR select roll_number,name,cwsl.course_id,start_time,exam_date 
                               from cwsl join ett on cwsl.course_id = ett.course_id;

    /*CONTINUE HANDLER FOR EXITING THE LOOP WHEN CURSOR HAS FETCHED ALL RECORDS */

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET out_cur_done = TRUE;
    
    OPEN out_cur;
    
    
    read_loop: LOOP
      
      
      FETCH out_cur INTO r1,n1,cid1,st1,ed1;


      IF out_cur_done THEN
        LEAVE read_loop;
      END IF;
      
      BLOCK_INR: BEGIN

        DECLARE inr_cur_done BOOLEAN DEFAULT FALSE;

        DECLARE inr_cur CURSOR FOR (select cwsl.roll_number,cwsl.course_id,ett.start_time,ett.exam_date 
                                 from cwsl join ett on cwsl.course_id = ett.course_id 
                                 where cwsl.roll_number = r1);

        
        DECLARE CONTINUE HANDLER FOR NOT FOUND SET inr_cur_done = TRUE;    
        
        OPEN inr_cur;

        
        inner_loop : LOOP
      
          FETCH inr_cur INTO r2,cid2,st2,ed2;
          
          IF inr_cur_done THEN
            LEAVE inner_loop;
          END IF;
      
    
            IF (cid1 > cid2) AND (ed1 = ed2) AND (st1 = st2) THEN

              insert into ett_voi values(r1,n1,cid1,cid2);

            END IF;

        END LOOP inner_loop;

        CLOSE inr_cur;

      END BLOCK_INR;

    END LOOP read_loop;

  CLOSE out_cur;

  select distinct * from ett_voi;

  END $$

  DELIMITER ; 
