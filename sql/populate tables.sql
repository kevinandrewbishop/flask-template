USE website;

TRUNCATE clients;
LOAD DATA INFILE 'C:/Virtual/flask test/sql/clients.txt' 
INTO TABLE clients FIELDS TERMINATED BY ',';

TRUNCATE trainers;
LOAD DATA INFILE 'C:/Virtual/flask test/sql/trainers.txt' 
INTO TABLE trainers FIELDS TERMINATED BY ',';

TRUNCATE transactions;
LOAD DATA INFILE 'C:/Virtual/flask test/sql/transactions.txt' 
INTO TABLE transactions FIELDS TERMINATED BY ',';


SELECT * FROM transactions;
DESCRIBE transactions;