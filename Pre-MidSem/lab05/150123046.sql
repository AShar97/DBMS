-- a
-- select course_id from ScheduledIn where room_number = 2001 group by course_id order by course_id;
select distinct course_id from ScheduledIn where room_number = 2001 order by course_id;

-- b
-- select course_id from ScheduledIn where letter = 'C' group by course_id order by course_id;
select distinct course_id from ScheduledIn where letter = 'C' order by course_id;

-- c
-- select division from ScheduledIn where room_number = 'L2' or room_number = 'L3' group by division order by division;
select distinct division from ScheduledIn where room_number = 'L2' or room_number = 'L3' order by division;

-- d
select distinct course_id
from (select P.course_id, P.room_number as prn, Q.room_number as qrn
	from ScheduledIn as P JOIN ScheduledIn as Q on P.course_id = Q.course_id) as T
where prn != qrn
order by course_id;

-- e
-- select distinct name from Department where department_id in (select department_id from ScheduledIn where room_number = 'L1' or room_number = 'L2' or room_number = 'L3' or room_number = 'L4' group by department_id) order by name;
select distinct name from Department where department_id in (select distinct department_id from ScheduledIn where room_number = 'L1' or room_number = 'L2' or room_number = 'L3' or room_number = 'L4') order by name;

-- f
-- select distinct name from Department where department_id not in (select department_id from ScheduledIn where room_number = 'L1' or room_number = 'L2' group by department_id) order by name;
select distinct name from Department where department_id not in (select distinct department_id from ScheduledIn where room_number = 'L1' or room_number = 'L2') order by name;

-- g
select distinct name
from Department
where department_id not in (select distinct P.department_id
	from Department as P CROSS JOIN Slot as Q
	where (P.department_id, Q.letter) not in (select distinct department_id, letter
		from ScheduledIn))
order by name;

-- h
select letter, count(course_id) as c from (select distinct letter, course_id from ScheduledIn) as T group by letter order by c asc;

-- i
select room_number, count(course_id) as c from (select distinct room_number, course_id from ScheduledIn) as T group by room_number order by c desc;

-- j
-- drop table h;
-- create table h as (select letter, count(course_id) as c from (select distinct letter, course_id from ScheduledIn) as T group by letter order by c asc);
-- select letter from h where c = (select min(c) from h);
-- drop table h;
select letter
from (select letter, count(course_id) as c from (select distinct letter, course_id from ScheduledIn) as T group by letter) as H
where c = (select min(c)
	from (select letter, count(course_id) as c from (select distinct letter, course_id from ScheduledIn) as T group by letter) as H)
order by letter;


-- k
select distinct letter from ScheduledIn where course_id like '%M' order by letter;
-- All distinct pairs -- select distinct letter, course_id from ScheduledIn where course_id like '%M';

-- l
select distinct P.name, Q.letter
from Department as P CROSS JOIN Slot as Q
where (P.department_id, Q.letter) not in (select distinct department_id, letter
	from ScheduledIn)
order by P.name;
