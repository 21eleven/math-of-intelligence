 CREATE TABLE `article_html` (
	  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
	  `title` mediumtext NOT NULL,
	  `html` longtext,
	  `url` mediumtext,
	  `topic` varchar(245) DEFAULT NULL,
	  `journal` varchar(245) DEFAULT NULL,
	  `open` int(11) DEFAULT NULL,
	  `date` varchar(245) DEFAULT NULL,
	  `type` varchar(245) DEFAULT NULL,
	  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6401 DEFAULT CHARSET=latin1;

CREATE TABLE `articles` (
	  `id` int(11) NOT NULL AUTO_INCREMENT,
	  `title` mediumtext NOT NULL,
	  `text` longtext NOT NULL,
	  `url` mediumtext,
	  `topic` varchar(245) DEFAULT NULL,
	  `journal` varchar(245) DEFAULT NULL,
	  `date` varchar(245) DEFAULT NULL,
	  `type` varchar(245) DEFAULT NULL,
	  `wc` int(11) DEFAULT NULL,
	  PRIMARY KEY (`id`),
	  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5100 DEFAULT CHARSET=latin1;
