DROP TABLE IF EXISTS custOrder;
DROP TABLE IF EXISTS restTable;
DROP TABLE IF EXISTS orderDetails;
DROP TABLE IF EXISTS item;
DROP TABLE IF EXISTS section;
DROP TABLE IF EXISTS menu;
DROP TABLE IF EXISTS staff;
DROP TABLE IF EXISTS workPlace;
DROP TABLE IF EXISTS restaurant;
DROP TABLE IF EXISTS communication;

CREATE TABLE restaurant (
  name TEXT PRIMARY KEY,
  contact TEXT NOT NULL
);

INSERT INTO restaurant (name, contact)
VALUES
  ('my restaurant', 'my address');

CREATE TABLE workPlace (
  name TEXT PRIMARY KEY,
  restName TEXT NOT NULL,
  FOREIGN KEY (restName) REFERENCES restaurant (name)
);

INSERT INTO workPlace (name, restName)
VALUES
  ('Bar', 'my restaurant'),
  ('Kitchen', 'my restaurant');

CREATE TABLE staff (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  type TEXT NOT NULL,
  workPlace TEXT NOT NULL,
  FOREIGN KEY (workPlace) REFERENCES workPlace (name)
);

INSERT INTO staff (username, password, type, workPlace)
VALUES
  ('manager', 'pbkdf2:sha256:50000$5EdxPGQv$40b05504c670d54d1a5d4c2ca6613606254f15dfc3fe6ae62c3eb105c251f537',
   'Manager', 'Bar');

CREATE TABLE communication (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source TEXT NOT NULL,
  timeSent TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  message TEXT,
  FOREIGN KEY (source) REFERENCES workPlace (name)
);

CREATE TABLE custOrder (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  custIP TEXT NOT NULL,
  totalCost REAL NOT NULL,
  tableNo INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  completed INTEGER NOT NULL DEFAULT 0,
  paid INTEGER NOT NULL DEFAULT 0,
  FOREIGN KEY (tableNo) REFERENCES restTable (tableNo)
);

CREATE TABLE item (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  description TEXT NOT NULL,
  cost REAL NOT NULL,
  section TEXT NOT NULL,
  menu TEXT NOT NULL,
  diet TEXT,
  spicy TEXT,
  FOREIGN KEY (section, menu) REFERENCES section (name, menu)
);

CREATE TABLE orderDetail (
  itemId INTEGER NOT NULL,
  orderId INTEGER NOT NULL,
  quantity INTEGER NOT NULL,
  FOREIGN KEY (itemId) REFERENCES item (id),
  FOREIGN KEY (orderId) REFERENCES custOrder (id),
  PRIMARY KEY (itemId, orderId)
);

CREATE TABLE section (
  name TEXT NOT NULL,
  description TEXT NOT NULL,
  menu TEXT NOT NULL,
  FOREIGN KEY (menu) REFERENCES menu (name),
  PRIMARY KEY (name, menu)
);

CREATE TABLE menu (
  name TEXT PRIMARY KEY,
  description TEXT NOT NULL,
  restName TEXT NOT NULL,
  FOREIGN KEY (restName) REFERENCES restaurant (name)
);

CREATE TABLE restTable (
  tableNo INTEGER PRIMARY KEY AUTOINCREMENT,
  noOfSeats INTEGER NOT NULL,
  seatsLeft INTEGER NOT NULL,
  free INTEGER NOT NULL,
  restName TEXT NOT NULL,
  FOREIGN KEY (restName) REFERENCES restaurant (name)
);

INSERT INTO restTable (noOfSeats, seatsLeft, free, restName)
VALUES
  (4, 4, 1, 'my restaurant'),
  (2, 2, 1, 'my restaurant'),
  (6, 6, 1, 'my restaurant');
