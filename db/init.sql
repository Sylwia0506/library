CREATE DATABASE IF NOT EXISTS library;
USE library;

GRANT ALL PRIVILEGES ON library.* TO 'user'@'%';
FLUSH PRIVILEGES;

INSERT INTO users (username, email, password, is_active) VALUES
('admin', 'admin@library.local', 'pbkdf2_sha256$600000$salt$hashedpassword123', TRUE),
('librarian', 'librarian@library.local', 'pbkdf2_sha256$600000$salt$hashedpassword456', TRUE),
('user1', 'user1@example.com', 'pbkdf2_sha256$600000$salt$hashedpassword789', TRUE),
('user2', 'user2@example.com', 'pbkdf2_sha256$600000$salt$hashedpassword012', TRUE),
('user3', 'user3@example.com', 'pbkdf2_sha256$600000$salt$hashedpassword345', TRUE);

INSERT INTO books (title, author, isbn, publication_year, available) VALUES
('Władca Pierścieni: Drużyna Pierścienia', 'J.R.R. Tolkien', '9788375780711', 2001, TRUE),
('Władca Pierścieni: Dwie Wieże', 'J.R.R. Tolkien', '9788375780728', 2001, TRUE),
('Władca Pierścieni: Powrót Króla', 'J.R.R. Tolkien', '9788375780735', 2001, TRUE),
('Harry Potter i Kamień Filozoficzny', 'J.K. Rowling', '9788380082113', 1997, TRUE),
('Harry Potter i Komnata Tajemnic', 'J.K. Rowling', '9788380082120', 1998, TRUE),
('Wiedźmin: Ostatnie Życzenie', 'Andrzej Sapkowski', '9788375780209', 1993, TRUE),
('Wiedźmin: Miecz Przeznaczenia', 'Andrzej Sapkowski', '9788375780216', 1992, TRUE),
('Duma i Uprzedzenie', 'Jane Austen', '9788375780100', 1813, TRUE),
('1984', 'George Orwell', '9788375780300', 1949, TRUE),
('Mistrz i Małgorzata', 'Michaił Bułhakow', '9788375780400', 1967, TRUE);

INSERT INTO reservations (book_id, user_id, status, reservation_date, return_date) VALUES
(1, 3, 'completed', '2024-01-01 10:00:00', '2024-01-15 14:30:00'),
(2, 3, 'completed', '2024-01-16 11:00:00', '2024-01-30 16:45:00'),
(3, 3, 'confirmed', '2024-02-01 09:30:00', NULL),
(4, 4, 'pending', '2024-02-15 13:20:00', NULL),
(5, 5, 'cancelled', '2024-02-10 15:00:00', NULL);


INSERT INTO system_logs (level, message, source, user_id) VALUES
('INFO', 'Użytkownik zalogowany pomyślnie', 'auth_system', 1),
('INFO', 'Nowa rezerwacja utworzona', 'reservation_system', 3),
('WARNING', 'Próba dostępu do niedostępnej książki', 'book_system', 4),
('ERROR', 'Błąd synchronizacji z zewnętrzną biblioteką', 'external_api', NULL),
('INFO', 'Książka zwrócona', 'reservation_system', 3);
