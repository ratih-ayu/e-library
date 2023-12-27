Create table genre (
genre_id int primary key,
genre_name varchar (100) not null);

create table books (
	book_id int primary key,
	title varchar (200) unique not null,
	author varchar (100) not null,
	quantity int not null check(quantity>=0),
	genre_id int not null,
	constraint fk_genre_id
		foreign key (genre_id)
		references genre(genre_id),
location_id int not null,
constraint fk_location_id
		foreign key (location_id)
		references location_info(location_id));

create table user_info (
	user_id int primary key,
	user_name varchar(50) not null,
	phone_number varchar (13) not null,
	email varchar(50) not null,
	date_register timestamp);

create table loan_book(
	loan_id int primary key,
	loan_date DATE,
	loan_due_date DATE GENERATED ALWAYS AS (loan_date + INTERVAL '14 days') STORED,
	return_date DATE,
	user_id int,
	constraint fk_user_id
		foreign key (user_id)
		references user_info(user_id),
	book_id int,
	constraint fk_book_id
		foreign key (book_id)
		references books(book_id),
	loan_status varchar(50) not null);

CREATE OR REPLACE TRIGGER update_loan_count_trigger
 AFTER INSERT OR DELETE
    ON public.loan_book
    FOR EACH ROW
    EXECUTE FUNCTION public.update_loan_count();

create table location_info (
	location_id int primary key,
	location_name varchar(50) not null,
	location_address varchar(100) not null);

create table loan_queue(
	queue_id int primary key,
	user_id int,
	constraint fk_user_id
		foreign key (user_id)
 	references user_info(user_id),
	book_id int,
	constraint fk_book_id
 		foreign key (book_id)
		references books(book_id),
	queue_start_date DATE,
	queue_end_date DATE,
	queue_status varchar(30));
	
CREATE OR REPLACE FUNCTION public.update_loan_count()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF
AS $BODY$
BEGIN
    IF TG_OP = 'INSERT' THEN
        -- Check if the user has exceeded the maximum allowed books (2)
        IF (SELECT COUNT(*) FROM public.loan_book WHERE user_id = NEW.user_id) > 2 THEN
            RAISE EXCEPTION 'User has reached the maximum allowed loan books';
        END IF;
    END IF;

    RETURN NULL;
END;
$BODY$;


		