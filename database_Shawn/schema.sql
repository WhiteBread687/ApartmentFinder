CREATE DATABASE IF NOT EXISTS apartment_finder
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE apartment_finder;

CREATE TABLE HousingType (
    TypeID INT AUTO_INCREMENT PRIMARY KEY,
    TypeName VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB;

CREATE TABLE Property (
    PropertyID INT AUTO_INCREMENT PRIMARY KEY,
    Address VARCHAR(255) NOT NULL,
    City VARCHAR(100) NOT NULL,
    State CHAR(2) NOT NULL,
    Zip VARCHAR(10) NOT NULL,
    TypeID INT NOT NULL,

    FOREIGN KEY (TypeID) REFERENCES HousingType(TypeID)
) ENGINE=InnoDB;

CREATE TABLE ApartmentUnit (
    UnitID INT AUTO_INCREMENT PRIMARY KEY,
    PropertyID INT NOT NULL,
    UnitNumber VARCHAR(30) NOT NULL,
    Rent DECIMAL(10, 2) NOT NULL,
    Beds INT NOT NULL,
    Baths DECIMAL(4, 1) NOT NULL,
    SquareFeet INT,
    DateAvailable DATE,

    FOREIGN KEY (PropertyID) REFERENCES Property(PropertyID),
    UNIQUE (PropertyID, UnitNumber),

    CHECK (Rent >= 0),
    CHECK (Beds >= 0),
    CHECK (Baths >= 0),
    CHECK (SquareFeet IS NULL OR SquareFeet > 0)
) ENGINE=InnoDB;

CREATE TABLE Amenity (
    AmenityID INT AUTO_INCREMENT PRIMARY KEY,
    AmenityName VARCHAR(100) NOT NULL UNIQUE,
    AmenityGroup VARCHAR(100) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE UnitAmenity (
    UnitID INT NOT NULL,
    AmenityID INT NOT NULL,

    PRIMARY KEY (UnitID, AmenityID),
    FOREIGN KEY (UnitID) REFERENCES ApartmentUnit(UnitID),
    FOREIGN KEY (AmenityID) REFERENCES Amenity(AmenityID)
) ENGINE=InnoDB;