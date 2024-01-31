CREATE TABLE employers
(
    employer_id serial PRIMARY KEY,
    employer_name varchar(100) UNIQUE
);


CREATE TABLE vacancies
(
    vacancy_id serial PRIMARY KEY,
    vacancy_number bigint,
    vacancy_name varchar(100),
	city varchar(50),
	url varchar(100),
	employer_id int,

	CONSTRAINT fk_vacancies_employers FOREIGN KEY(employer_id) REFERENCES employers(employer_id) ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE salary
(
    salary_id serial PRIMARY KEY,
    start_salary bigint,
	end_salary bigint,
    currency varchar(10),
    vacancy_url varchar(100),
    vacancy_id int,

    CONSTRAINT fk_salary_vacancies FOREIGN KEY(vacancy_id) REFERENCES vacancies(vacancy_id) ON DELETE CASCADE ON UPDATE CASCADE
);
