CREATE TABLE `users` (
  `name` varchar(300) NOT NULL,
  `userid` varchar(300) NOT NULL,
  `userpath` varchar(300) NOT NULL,
  `tasks` varchar(1000) DEFAULT "[]",
  `score` int(11) DEFAULT 0,
  `entropy` varchar(300) DEFAULT "0"
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE USER 'punditadmin'@'localhost' IDENTIFIED with mysql_native_password BY '729e34d3479c369aafa534cd59123604eea08a4a2f1353f99cf1646ab4d26aebbfe279e32e5b3c17cd3adbc0256f72be';
GRANT ALL PRIVILEGES ON pundit.* TO 'punditadmin'@'localhost';
FLUSH PRIVILEGES;