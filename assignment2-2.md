## DBMS 2-2 과제

2015004539 박소영



###시나리오

1. 강의실 수가 20개 이상인 건물의 데이터를 출력 

SELECT name FROM Building Where rooms>=20;



2. student 테이블에 자신의 신상정보를 열에 맞게 추가 

INSERT INTO students VALUES ("2015004539","soyoung","박소영","female","3","2001032069");



3. 건물 테이블에서 이름이 'IT/BT'인 건물의 정보를 '정보통신관'으로 변경 

UPDATE Building SET name="정보통신관" WHERE name="IT / BT";



4. 건물과 강의실의 테이블을 연결하여 수용인원이 100명 이상인 강의실의 건물번 호와 건물의 이름을 출력 

SELECT B.name, B.building_id FROM Building B WHERE B.building_id IN (SELECT R.building_id FROM Room R WHERE R.capacity>=100);



5. 강좌 테이블에서 학과 부분을 분리하고 (ITE3070 -> ITE, 3070) 학과별 과목 수를 추출하여 개설된 강의 수가 가장 많은 상위 10개의 학과를 출력

select p.name, count(*) from (select substr(course_id,1,3) as name from class) p group by p.name order by count(p.name) desc limit 10;