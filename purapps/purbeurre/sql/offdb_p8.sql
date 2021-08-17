-- DROP SCHEMA IF EXISTS public CASCADE;

-- CREATE SCHEMA IF NOT EXISTS public;

-- -----------------------------------------------------
-- Table public.nutriscore
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS public.nutriscore 
(
    id serial,
    type character(1) UNIQUE,
    PRIMARY KEY (id)
);

-- -----------------------------------------------------
-- Table public.products
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS public.product
(
    id integer primary key generated always as identity,
    name character varying(150) DEFAULT NULL UNIQUE,
    brand character varying(150) DEFAULT NULL,
    stores character varying(150) DEFAULT NULL,
    url character varying(255) DEFAULT NULL UNIQUE,
    nutriscore_id integer DEFAULT NULL,
    FOREIGN KEY (nutriscore_id) REFERENCES public.nutriscore (id) ON DELETE CASCADE
);


-- -----------------------------------------------------
-- Table `pb_off`.`categories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS public.categorie
(
    id integer primary key generated always as identity,
    name character varying(120) UNIQUE
);

-- -----------------------------------------------------
-- Table public.substitutes
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS public.substitutes (
    id integer primary key generated always as identity,
    substitute_id integer,
    substituted_id integer,
    FOREIGN KEY (substitute_id) REFERENCES public.product (id) ON DELETE CASCADE,
    FOREIGN KEY (substituted_id) REFERENCES public.product (id) ON DELETE CASCADE
);

-- -----------------------------------------------------
-- Table public.categories_products
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS public.categorie_product
(
    product_id int NOT NULL,    
    categorie_id int NOT NULL,
    PRIMARY KEY (categorie_id, product_id),
    FOREIGN KEY (product_id) REFERENCES public.product (id) ON UPDATE CASCADE,
    FOREIGN KEY (categorie_id) REFERENCES public.categorie (id) ON DELETE NO ACTION ON UPDATE NO ACTION
);



-- SELECT p.name, nutriscore.type, p.brand, p.stores, p.url, p.id
--         FROM product p
--         JOIN nutriscore
--         ON nutriscore.id = p.nutriscore_id
--         JOIN categorie_product
--         ON categorie_product.product_id = p.id
--         JOIN categorie
--         ON categorie_product.categorie_id = categorie.id
--         WHERE categorie.id = 2 and nutriscore.type < (
--             SELECT string_agg(DISTINCT nutriscore.type, ', ') AS liste
--             FROM product
--             JOIN nutriscore
--             ON nutriscore.id = product.nutriscore_id
--             JOIN categorie_product
--             ON categorie_product.product_id = product.id
--             JOIN categorie
--             ON categorie_product.categorie_id = categorie.id
--             WHERE categorie.id = 1  )
--             ORDER BY random() LIMIT 1;

-- SELECT p.name, n.type, p.brand, p.stores, p.url, p.id
--         FROM purbeurre_product p
--         JOIN purbeurre_nutriscore n
--         ON n.id = p.nutriscore_id
--         JOIN purbeurre_product_categories cp
--         ON cp.product_id = p.id
--         JOIN purbeurre_category c
--         ON cp.category_id = c.id
--         WHERE c.id = 2 and n.type < (
--             SELECT string_agg(DISTINCT purbeurre_nutriscore.type, ', ') AS liste
--             FROM purbeurre_product
--             JOIN purbeurre_nutriscore
--             ON purbeurre_nutriscore.id = purbeurre_product.nutriscore_id
--             JOIN purbeurre_product_categories
--             ON purbeurre_product_categories.product_id = purbeurre_product.id
--             JOIN purbeurre_category
--             ON purbeurre_product_categories.category_id = purbeurre_category.id
--             WHERE purbeurre_category.id = 2  )
--             ORDER BY random() LIMIT 1;