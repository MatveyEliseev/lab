создание бд
CREATE TABLE users(
	id BIGINT NOT NULL PRIMARY KEY,
	first_name VARCHAR(64) NOT NULL
);

вставка данных 
INSERT INTO users (id,first_name)
VALUES (1,'vasia');

обновлдение данных
UPDATE  users SET 
first_name = 'matvey'
WHERE id = 1 (where-для поиска)

удаление данных

DELETE FROM users 
WHERE id = 1

выборка данных 
SELECT id,first_name FROM users
WHERE id = 1

внешний ключ 
CREATE TABLE spendings(
	id BIGINT NOT NULL PRIMARY KEY,
	price INT NOT NULL,
	user_id BIGINT NOT NULL,
	
	CONSTRAINT user_id_fk FOREIGN KEY(user_id) REFERENCES users (id)
);

присоединение колонок к друг другу 
SELECT spendings.*, users.first_name FROM spendings
JOIN users ON users.id = spendings.user_id

добавление колонок к сущ бд
ALTER TABLE spendings ADD COLUMN category_id BIGINT;
ALTER TABLE spendings ADD CONSTRAINT category_fk FOREIGN KEY (category_id) REFERENCES categories (id);
