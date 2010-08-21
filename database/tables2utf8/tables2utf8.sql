/*

Wordpress has a problem with encodings. Read more here: http://trac.wordpress.org/ticket/3517

If you want to move out of wordpress, or use data that it generated in another application, 
you're in serious trouble.

This script helped me to transform the data that I needed into real UTF8 data.

Use and adapt it as you wish!

Sole | www.soledadpenades.com

*/

SET AUTOCOMMIT=0;
START TRANSACTION;

ALTER TABLE `wp_categories`
	MODIFY cat_name BLOB,
	MODIFY category_description BLOB;
	
ALTER TABLE `wp_comments`
	MODIFY comment_author BLOB,
	MODIFY comment_author_url BLOB,
	MODIFY comment_content BLOB;

ALTER TABLE `wp_posts`
	MODIFY post_title BLOB, 
	MODIFY post_content BLOB, 
	MODIFY post_excerpt BLOB, 
	MODIFY post_password BLOB, 
	MODIFY to_ping BLOB, 
	MODIFY pinged BLOB, 
	MODIFY post_content_filtered BLOB;
	
ALTER TABLE `wp_users`
	MODIFY user_pass BLOB,
	MODIFY user_nicename BLOB,
	MODIFY user_email BLOB,
	MODIFY user_url BLOB,
	MODIFY display_name BLOB;

ALTER DATABASE axoneseones charset=utf8;

ALTER TABLE `wp_categories` charset=utf8;

ALTER TABLE `wp_categories`
	MODIFY cat_name varchar(55) CHARACTER SET utf8,
	MODIFY category_description varchar(200) CHARACTER SET utf8;

ALTER TABLE `wp_comments`
	MODIFY comment_author tinytext CHARACTER SET utf8,
	MODIFY comment_author_url varchar(200) CHARACTER SET utf8,
	MODIFY comment_content text CHARACTER SET utf8;

ALTER TABLE `wp_posts` charset=utf8;

ALTER TABLE `wp_posts`
	MODIFY post_title text CHARACTER SET utf8,
	MODIFY post_content longtext CHARACTER SET utf8, 
	MODIFY post_excerpt text CHARACTER SET utf8, 
	MODIFY post_password varchar(20) CHARACTER SET utf8, 
	MODIFY post_name varchar(200) CHARACTER SET utf8, 
	MODIFY to_ping text CHARACTER SET utf8, 
	MODIFY pinged text CHARACTER SET utf8, 
	MODIFY post_content_filtered text CHARACTER SET utf8;
	
ALTER TABLE `wp_users`
	MODIFY user_login varchar(60) CHARACTER SET utf8,
	MODIFY user_pass varchar(64) CHARACTER SET utf8,
	MODIFY user_nicename varchar(50) CHARACTER SET utf8,
	MODIFY user_email varchar(100) CHARACTER SET utf8,
	MODIFY user_url varchar(100) CHARACTER SET utf8,
	MODIFY display_name varchar(250) CHARACTER SET utf8;
	
COMMIT;