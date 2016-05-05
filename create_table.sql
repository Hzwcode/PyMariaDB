create table if not exists publication
(
	isbn char(20) not null,
	title text not null,
	author text not null,
	pdate text not null,
	pcompany text not null,
	pagenum int null,
	tags text default null,
	id bigint not null auto_increment,
	primary key(id)
);
