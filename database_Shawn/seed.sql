USE apartment_finder;

INSERT INTO HousingType (TypeID, TypeName)
VALUES
    (1, 'Apartment'),
    (2, 'Duplex');

INSERT INTO Property
    (PropertyID, Address, City, State, Zip, TypeID)
VALUES
    (1, '100 Example Street', 'Moscow', 'ID', '83843', 1),
    (2, '200 Sample Avenue', 'Moscow', 'ID', '83843', 2);

INSERT INTO ApartmentUnit
    (UnitID, PropertyID, UnitNumber, Rent, Beds, Baths,
     SquareFeet, DateAvailable)
VALUES
    (1, 1, '101', 1250.00, 2, 1.0, 850, '2026-11-01'),
    (2, 1, '102', 1350.00, 2, 1.5, 950, '2026-11-01'),
    (3, 2, 'A',   1100.00, 1, 1.0, 700, '2026-11-15');

INSERT INTO Amenity
    (AmenityID, AmenityName, AmenityGroup)
VALUES
    (1, 'In-unit laundry', 'Laundry'),
    (2, 'Shared on-site laundry', 'Laundry'),
    (3, 'Dishwasher', 'Kitchen');

INSERT INTO UnitAmenity (UnitID, AmenityID)
VALUES
    (1, 2),
    (1, 3),
    (2, 1),
    (2, 3),
    (3, 2);