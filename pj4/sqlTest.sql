
CREATE TABLE orders
  (
    order_id INTEGER PRIMARY KEY,
    sid INTEGER NOT NULL,
    cid INTEGER NOT NULL,
    status VARCHAR NOT NULL, -- waiting, delivering, completed
    did INTEGER,
    payment VARCHAR,
    timestmp TIMESTAMP,
  )

 -- 주문 정보 기록
INSERT INTO orders(sid, cid, status, did, payment, timestmp) VALUES (?, ?, "waiting", ?, ?, ?);

 -- Seller의 Order 목록 확인
SELECT order_id, status FROM orders WHERE sid = ?;

-- Order의 메뉴정보 확인
SELECT M.menu, B.cnt
    FROM menu M, basket B, orders O
    WHERE O.order_id = ?
        AND O.order_id = B.order_id
        AND B.menuid = M.menuid;

-- Order 취소

BEGIN TRANSACTION;
DELETE FROM orders WHERE order_id = ?;
DELETE FROM basket WHERE order_id = ?;
END TRANSACTION;

 -- Seller와 가장 가까운 배달부 5명 query
SELECT D.did, D.name, (D.lat - S.lat)^2 + (D.lng - S.lng)^2 AS distance
    FROM deliveries D, stores S
    WHERE D.stock < 5 AND S.sid = ?
    ORDER BY distance ASC
    limit 5;

 -- order에 배달부 할당
 UPDATE orders SET did=?, status="delivering" WHERE order_id = ?;


CREATE TABLE store_schedules (
    schedule_id INTEGER PRIMARY KEY,
    sid INTEGER,
    day_no INTEGER,
    holiday BOOLEAN,
    opened INTEGER,
    closed INTEGER
);

CREATE TABLE store_tags (
    tag_id INTEGER PRIMARY KEY,
    sid INTEGER,
    name VARCHAR
);

CREATE TABLE menues (
    menuid INTEGER PRIMARY KEY,
    menu VARCHAR,
    sid INTEGER
);

CREATE TABLE basket (
    basket_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    menuid INTEGER,
    cnt INTEGER
);


-- 구매자
-- ====================

-- 주문 내역 (배송 완료 이후)
SELECT O.order_id, S.sname, M.menu, O.payment, O.timestmp
    FROM orders O, stores S, menues M
    WHERE O.cid = ? AND O.sid=S.sid AND O.menuid = M.menuid
        AND O.status = "completed"
    ORDER BY O.timestmp DESC;

-- 주문 현황 (배송 완료 이전)
SELECT O.order_id, S.sname, M.menu, O.payment, O.timestmp, D.name
    FROM orders O, stores S, menues M, deliveries D
    WHERE O.cid = ? AND O.sid=S.sid AND O.menuid = M.menuid AND O.did = D.did
        AND O.status IN ("waiting", "delivering")
    ORDER BY O.timestmp DESC;

 -- 도착 확인
 UPDATE orders SET status="completed" WHERE order_id=?;


-- 현재 위치를 기준으로 주변의 영업 중인 가게 리스트 출력
SELECT S.sid, (S.lat - C.lat)^2 + (S.lng - C.lng)^2 as distance, S.sname
    FROM stores S, customers C, store_schedules SS
    WHERE S.sid = SS.sid
        AND day_no = ? AND SS.holiday = false AND SS.opened <= ? AND SS.closed >= ?
        AND C.cid = ?
    ORDER BY distance ASC
    limit 100;

-- 주소로 가게 검색
SELECT S.sid, S.sname
    FROM stores S
    WHERE S.address LIKES ?;

-- '%%' + keyword + '%%'

-- 태그로 가게 검색
SELECT T.sid, S.sname, T.name
    FROM store_tags T, stores S
    WHERE S.sid = T.sid AND T.tags = ?;

-- 이름으로 가게 검색
SELECT sid, sname FROM stores WHERE sname LIKES ?;

-- 메뉴 출력하기
SELECT M.menu FROM menues M, stores S WHERE M.sid = S.sid;

-- 배달부
-- =================

-- 배송 중인 메뉴 나열
SELECT O.order_id, S.sname, M.menu, C.name, C.phone, C.lat, C.lng, O.payment, O.timestmp
    FROM orders O, stores S, menues M, customers C
    WHERE O.did = ? AND O.sid=S.sid AND O.menuid = M.menuid AND O.cid = C.cid
        AND O.status = "delivering"
    ORDER BY O.timestmp DESC;
