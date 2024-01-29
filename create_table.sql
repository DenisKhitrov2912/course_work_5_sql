CREATE TABLE vacancies
(
    vacancy_id serial PRIMARY KEY,
    vacancy_number bigint,
    name varchar(100),
	city varchar(50),
	url varchar(100)
);

CREATE TABLE employers
(
    employer_id serial PRIMARY KEY,
    vacancy_id int,
    employer_name varchar(100),
    city varchar(50),
    vacancy_url varchar(100), 

    CONSTRAINT fk_employers_vacancies FOREIGN KEY(vacancy_id) REFERENCES vacancies(vacancy_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE salary
(
    salary_id serial PRIMARY KEY,
    employer_id int,
    start_salary varchar(50),
	end_salary varchar(50),
    currency varchar(10),
    vacancy_url varchar(100),

    CONSTRAINT fk_salary_employers FOREIGN KEY(employer_id) REFERENCES employers(employer_id) ON DELETE CASCADE ON UPDATE CASCADE
);
