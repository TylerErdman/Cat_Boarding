IF DB_ID('Cat_Boarding') IS NULL
	CREATE DATABASE Cat_Boarding;

GO
Use Cat_Boarding;

GO

IF OBJECT_ID('Ownership', 'U') IS NOT NULL
      DROP TABLE Ownership;

IF OBJECT_ID('Book', 'U') IS NOT NULL
      DROP TABLE Book;

IF OBJECT_ID('Cat', 'U') IS NOT NULL
      DROP TABLE Cat;

IF OBJECT_ID('Room', 'U') IS NOT NULL
      DROP TABLE Room;

IF OBJECT_ID('Owner', 'U') IS NOT NULL
      DROP TABLE Owner;

CREATE TABLE Owner
 (
	 Owner_ID				    INT			    NOT NULL    IDENTITY,
	 Owner_First_Name		    VARCHAR(30)	    NOT NULL,
	 Owner_Last_Name			VARCHAR(30)		NOT NULL,
	 Owner_Area_Code			VARCHAR(3)      NOT NULL,
	 Owner_Phone_Number			VARCHAR(8)      NOT NULL,
	 Owner_Address				VARCHAR(30)     NOT NULL,
	 Owner_City					VARCHAR(30)     NOT NULL,
	 Owner_State				VARCHAR(2)      NOT NULL,
	 Owner_Zipcode				VARCHAR(5)      NOT NULL,
	 Owner_Date_Added			DATE			NOT NULL   DEFAULT(GETDATE()),
	 PRIMARY KEY(Owner_ID)
  );

CREATE TABLE Room
 (
	 Room_ID			   INT			    NOT NULL        IDENTITY,
	 Room_Name			   VARCHAR(30)	    NOT NULL,
	 Room_Capacity		   INT	            NOT NULL,
	 PRIMARY KEY(Room_ID)
  );

CREATE TABLE Cat
 (
	 Cat_ID			   INT			    NOT NULL        IDENTITY,
	 Cat_Name		   VARCHAR(30)	    NOT NULL,
	 Cat_Color	       VARCHAR(30)		NOT NULL,
	 Cat_Breed	       VARCHAR(30)		NOT NULL,
	 Cat_Birthday	   DATE				NOT NULL,
	 PRIMARY KEY(Cat_ID)
  );

CREATE TABLE Ownership
 (
	 Cat_ID			   INT			    NOT NULL,
	 Owner_ID		   INT			    NOT NULL,
	 PRIMARY KEY(Cat_ID, Owner_ID),
	 FOREIGN KEY(Cat_ID) REFERENCES Cat(Cat_ID),
	 FOREIGN KEY(Owner_ID) REFERENCES Owner(Owner_ID)
  );

CREATE TABLE Book
 (
	 Book_ID		   INT			    NOT NULL		IDENTITY,
	 Cat_ID			   INT			    NOT NULL,
	 Room_ID		   INT			    NOT NULL,
	 Check_In          DATE				NOT NULL        DEFAULT(GETDATE()),
	 Check_Out		   DATE				NOT NULL,
	 PRIMARY KEY(Book_ID),
	 FOREIGN KEY(Cat_ID) REFERENCES Cat(Cat_ID),
	 FOREIGN KEY(Room_ID) REFERENCES Room(Room_ID) 
  );

GO

-- Owners
INSERT INTO Owner(Owner_First_Name, Owner_Last_Name, Owner_Area_Code, Owner_Phone_Number, Owner_Address, Owner_City, Owner_State, Owner_Zipcode)
			VALUES('Abigail', 'Allen', '515', '478-6099', '909 S R St Apt 66', 'Indianola', 'IA', '50125');
INSERT INTO Owner(Owner_First_Name, Owner_Last_Name, Owner_Area_Code, Owner_Phone_Number, Owner_Address, Owner_City, Owner_State, Owner_Zipcode)
			VALUES('Lani', 'Cruse', '515', '478-5162', '1500 N 9th St Unit 79', 'Indianola', 'IA', '50125');
INSERT INTO Owner(Owner_First_Name, Owner_Last_Name, Owner_Area_Code, Owner_Phone_Number, Owner_Address, Owner_City, Owner_State, Owner_Zipcode)
			VALUES('Tyler', 'Erdman', '515', '494-0040', '1500 N 9th St Unit 79', 'Indianola', 'IA', '50125');

-- Cats
INSERT INTO Cat(Cat_Name, Cat_Color, Cat_Breed, Cat_Birthday)
			VALUES('Checkers','Black and White', 'Domestic Longhair', '2018-02-14');
INSERT INTO Cat(Cat_Name, Cat_Color, Cat_Breed, Cat_Birthday)
			VALUES('Sir Elton', 'White and Blue', 'Domestic Shorthair', '2019-04-24');
INSERT INTO Cat(Cat_Name, Cat_Color, Cat_Breed, Cat_Birthday)
			VALUES('Olive Oil', 'Turtle Shell Calico','Domestic Shorthair', '2021-05-25');
INSERT INTO Cat(Cat_Name, Cat_Color, Cat_Breed, Cat_Birthday)
			VALUES('Kurie', 'White and Brown','Domestic Shorthair', '2018-06-27');

-- Rooms
INSERT INTO Room(Room_Name, Room_Capacity)
			VALUES('Underwater', 3);
INSERT INTO Room(Room_Name, Room_Capacity)
			VALUES('Outer Space', 2);
INSERT INTO Room(Room_Name, Room_Capacity)
			VALUES('Pirates', 5);
INSERT INTO Room(Room_Name, Room_Capacity)
			VALUES('School', 3);
INSERT INTO Room(Room_Name, Room_Capacity)
			VALUES('Jungle', 7);

-- Ownership
INSERT INTO Ownership(Cat_ID, Owner_ID)
			VALUES(1, 3);
INSERT INTO Ownership(Cat_ID, Owner_ID)
			VALUES(2, 2);
INSERT INTO Ownership(Cat_ID, Owner_ID)
			VALUES(2, 3);
INSERT INTO Ownership(Cat_ID, Owner_ID)
			VALUES(3, 1);
INSERT INTO Ownership(Cat_ID, Owner_ID)
			VALUES(4, 1);

-- Book 
INSERT INTO Book(Cat_ID, Room_ID, Check_In, Check_Out)
			VALUES(1, 1, '2022-01-12', '2022-02-01');
INSERT INTO Book(Cat_ID, Room_ID, Check_In, Check_Out)
			VALUES(3, 1, '2022-04-10', '2022-04-17');
INSERT INTO Book(Cat_ID, Room_ID, Check_In, Check_Out)
			VALUES(2, 1, '2022-04-15', '2022-05-01');
INSERT INTO Book(Cat_ID, Room_ID, Check_In, Check_Out)
			VALUES(1, 1, '2022-04-18', '2022-05-01');
INSERT INTO Book(Cat_ID, Room_ID, Check_In, Check_Out)
			VALUES(4, 3, '2022-04-09', '2022-04-22');

