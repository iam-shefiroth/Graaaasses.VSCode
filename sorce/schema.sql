CREATE TABLE amazon_review(
    amazon_url VARCHAR(400),
    product_name VARCHAR(100) NOT NULL,
    img VARCHAR(100) NOT NULL,
    positaitle1 VARCHAR(50) NOT NULL,
    positive1 VARCHAR(1000) NOT NULL,
    positaitle2 VARCHAR(50) NOT NULL,
    positive2 VARCHAR(1000) NOT NULL,
    positaitle3 VARCHAR(50) NOT NULL,
    positive3 VARCHAR(1000) NOT NULL,
    negatitle1 VARCHAR(50) NOT NULL,
    negative1 VARCHAR(1000) NOT NULL,
    negatitle2 VARCHAR(50) NOT NULL,
    negative2 VARCHAR(1000) NOT NULL,
    negatitle3 VARCHAR(50) NOT NULL,
    negative3 VARCHAR(1000) NOT NULL,
    posicount int NOT NULL,
    negacount int NOT NULL,
    PRIMARY KEY(amazon_url)
);