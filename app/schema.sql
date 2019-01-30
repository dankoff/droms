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
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
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
  custIP TEXT NOT NULL,
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
