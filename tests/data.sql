INSERT INTO restaurant (name, contact)
VALUES
  ('testRestaurant', 'testContact');

INSERT INTO workPlace (name, restName)
VALUES
  ('TestBar', 'testRestaurant'),
  ('TestKitchen', 'testRestaurant');

INSERT INTO menu (name, description, restName)
VALUES
  ('testMenu1', 'testMenu1Desc', 'testRestaurant'),
  ('testMenu2', 'testMenu2Desc', 'testRestaurant');

INSERT INTO restTable (noOfSeats, restName, seatsLeft, free)
VALUES
  (4, 'testRestaurant', 4, 1),
  (2, 'testRestaurant', 1, 1),
  (2, 'testRestaurant', 0, 0);

INSERT INTO communication (source, message)
VALUES
  ('TestBar', 'Test Message From TestBar'),
  ('TestKitchen', 'Test Message From TestKitchen');

INSERT INTO staff (username, password, type, workPlace)
VALUES
  ('chef1', 'pbkdf2:sha256:50000$5EdxPGQv$40b05504c670d54d1a5d4c2ca6613606254f15dfc3fe6ae62c3eb105c251f537',
   'Cook', 'Kitchen'),
  ('waiter1', 'pbkdf2:sha256:50000$jbZh9rIJ$5b76efbbcb941a6351cef29f3f89e3501b2f9f70c350188183a76a063e334f53',
   'Waiter', 'Bar');

INSERT INTO section (name, menu, description)
VALUES
  ('testSection1', 'testMenu1', 'testSection1Desc'),
  ('testSection2', 'testMenu1', 'testSection2Desc'),
  ('testSection3', 'testMenu2', '');

INSERT INTO custOrder (custIP, totalCost, tableNo, created, completed, paid)
VALUES
  ('1.1.1.1', 10.00, 1, '2019-01-01 00:00:10', 1, 0),
  ('1.1.1.1', 15.50, 1, '2019-01-01 00:00:20', 0, 0),
  ('1.2.3.4', 9.99, 2, '2019-01-01 00:00:30', 1, 1);

INSERT INTO item (name, description, cost, section, menu, diet, spicy)
VALUES
  ('testItem1', 'testItem1Desc', 1.00, 'testSection1', 'testMenu1', 'Vegetarian', 'Mild'),
  ('testItem2', 'testItem2Desc', 2.50, 'testSection2', 'testMenu1', 'Vegan', ''),
  ('testItem3', 'testItem3Desc', 5.00, 'testSection3', 'testMenu2', '', 'Hot');

INSERT INTO orderDetail (itemId, orderId, quantity)
VALUES
  (1, 1, 2),
  (2, 1, 1),
  (3, 2, 2),
  (2, 2, 1),
  (1, 2, 1),
  (1, 3, 3),
  (3, 3, 1);
