DROP TABLE IF EXISTS custOrder;
DROP TABLE IF EXISTS restTable;
DROP TABLE IF EXISTS orderDetails;
DROP TABLE IF EXISTS item;
DROP TABLE IF EXISTS section;
DROP TABLE IF EXISTS menu;
DROP TABLE IF EXISTS staff;
DROP TABLE IF EXISTS workPlace;
DROP TABLE IF EXISTS restaurant;

CREATE TABLE staff (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  type TEXT NOT NULL,
  workPlace TEXT NOT NULL,
  FOREIGN KEY (workPlace) REFERENCES workPlace (name)
);

CREATE TABLE workPlace (
  name TEXT PRIMARY KEY,
  restName TEXT NOT NULL,
  FOREIGN KEY (restName) REFERENCES restaurant (name)
);

CREATE TABLE custOrder (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  totalCost REAL NOT NULL,
  tableNo INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (tableNo) REFERENCES restTable (tableNo)
);

CREATE TABLE item (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  description TEXT NOT NULL,
  cost REAL NOT NULL,
  section TEXT NOT NULL,
  FOREIGN KEY (section) REFERENCES section (name)
);

CREATE TABLE orderDetails (
  itemId INTEGER NOT NULL,
  orderId INTEGER NOT NULL,
  quantity INTEGER NOT NULL,
  FOREIGN KEY (itemId) REFERENCES item (id),
  FOREIGN KEY (orderId) REFERENCES custOrder (id),
  PRIMARY KEY (itemId, orderId)
);

CREATE TABLE section (
  name TEXT PRIMARY KEY,
  description TEXT NOT NULL,
  menu TEXT NOT NULL,
  FOREIGN KEY (menu) REFERENCES menu (name)
);

CREATE TABLE menu (
  name TEXT PRIMARY KEY,
  description TEXT NOT NULL,
  restName TEXT NOT NULL,
  FOREIGN KEY (restName) REFERENCES restaurant (name)
);

CREATE TABLE restaurant (
  name TEXT PRIMARY KEY,
  contact TEXT NOT NULL
);

CREATE TABLE restTable (
  tableNo INTEGER PRIMARY KEY AUTOINCREMENT,
  noOfSeats INTEGER NOT NULL,
  restName TEXT NOT NULL,
  FOREIGN KEY (restName) REFERENCES restaurant (name)
);
