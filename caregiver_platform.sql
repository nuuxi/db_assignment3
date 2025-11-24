
DROP TABLE IF EXISTS JOB_APPLICATION CASCADE;
DROP TABLE IF EXISTS APPOINTMENT CASCADE;
DROP TABLE IF EXISTS JOB CASCADE;
DROP TABLE IF EXISTS ADDRESS CASCADE;
DROP TABLE IF EXISTS MEMBER CASCADE;
DROP TABLE IF EXISTS CAREGIVER CASCADE;
DROP TABLE IF EXISTS "USER" CASCADE;

CREATE TABLE "USER" (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    given_name VARCHAR(100) NOT NULL,
    surname VARCHAR(100) NOT NULL,
    city VARCHAR(100),
    phone_number VARCHAR(20),
    profile_description TEXT,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE CAREGIVER (
    caregiver_user_id INT PRIMARY KEY,
    photo VARCHAR(255),
    gender VARCHAR(20),
    caregiving_type VARCHAR(50),
    hourly_rate DECIMAL(6,2),
    FOREIGN KEY (caregiver_user_id) REFERENCES "USER"(user_id)
);

CREATE TABLE MEMBER (
    member_user_id INT PRIMARY KEY,
    house_rules TEXT,
    dependent_description TEXT,
    FOREIGN KEY (member_user_id) REFERENCES "USER"(user_id)
);

CREATE TABLE ADDRESS (
    member_user_id INT PRIMARY KEY,
    house_number VARCHAR(20),
    street VARCHAR(100),
    town VARCHAR(100),
    FOREIGN KEY (member_user_id) REFERENCES MEMBER(member_user_id)
);

CREATE TABLE JOB (
    job_id SERIAL PRIMARY KEY,
    member_user_id INT NOT NULL,
    required_caregiving_type VARCHAR(50),
    other_requirements TEXT,
    date_posted DATE,
    FOREIGN KEY (member_user_id) REFERENCES MEMBER(member_user_id)
);

CREATE TABLE JOB_APPLICATION (
    caregiver_user_id INT,
    job_id INT,
    date_applied DATE,
    PRIMARY KEY (caregiver_user_id, job_id),
    FOREIGN KEY (caregiver_user_id) REFERENCES CAREGIVER(caregiver_user_id),
    FOREIGN KEY (job_id) REFERENCES JOB(job_id)
);

CREATE TABLE APPOINTMENT (
    appointment_id SERIAL PRIMARY KEY,
    caregiver_user_id INT NOT NULL,
    member_user_id INT NOT NULL,
    appointment_date DATE,
    appointment_time TIME,
    work_hours INT,
    status VARCHAR(20),
    FOREIGN KEY (caregiver_user_id) REFERENCES CAREGIVER(caregiver_user_id),
    FOREIGN KEY (member_user_id) REFERENCES MEMBER(member_user_id)
);


INSERT INTO "USER" (email, given_name, surname, city, phone_number, profile_description, password) VALUES
('raim@mail.com','Raim','Sultan','Almaty','+77014578987','Father that needs help','password1'),
('nurkhan@mail.com','Nurkhan','Bekbol','Zhezkazgan','+77011245789','Needs a babysitter','password2'),
('beks@mail.com','Beks','Beka','Shymkent','+77013652147','Babysitter with a 2 years experience','password3'),
('ali@mail.com','Ali','Mukha','Talgar','+77017894567','Playmate specialist','password4'),
('alina@mail.com','Alina','Ema','Shymkent','+77011265875','Elderly caregiver','password5'),
('zhan@mail.com','Zhan','Zhen','Astana','+77018574962','Looking for elderly caregiver','password6'),
('erzhan@mail.com','Erzhan','Temir','Astana','+770112457897','Babysitter and tutor','password7'),
('rash@mail.com','Rash','Zhok','Oral','+770173918465','Elderly care expert','password8'),
('mariam@mail.com','Mariam','Mariam','Aktau','+77017859642','Playmate for toddlers','password9'),
('artur@mail.com','Artur','Neartur','Atyrau','+77012145236','Babysitter','password10');

INSERT INTO CAREGIVER (caregiver_user_id, photo, gender, caregiving_type, hourly_rate) VALUES
(3,'beks.jpg','Male','babysitter',7.5),
(4,'ali.jpg','Male','playmate', 12.0),
(5,'alina.jpg','Female','elderly',12.0),
(7,'erzhan.jpg','Male','babysitter',8.0),
(8,'rash.jpg','Male','elderly',13.0),
(9,'mariam.jpg','Female','playmate',9.0),
(10,'artur.jpg','Male','babysitter',7.5);

INSERT INTO MEMBER (member_user_id, house_rules, dependent_description) VALUES
(1,'No pets.','5-year-old son.'),
(2,'Hygiene is essential.','3-year-old daughter.'),
(6,'No smoking and vapiing.','Elderly mother needs support.');

INSERT INTO ADDRESS (member_user_id, house_number, street, town) VALUES
(1,'10','Karatau','Almaty'),
(2,'34','Ortalyk','Zhezkazgan'),
(6,'89','Sidney','Astana');

INSERT INTO JOB (member_user_id, required_caregiving_type, other_requirements, date_posted) VALUES
(1,'babysitter','punctual','2025-10-01'),
(2,'babysitter','experienced','2025-10-02'),
(6,'elderly','kind','2025-10-03'),
(1,'playmate','creative','2025-10-04'),
(2,'babysitter','pateitn','2025-10-05'),
(6,'elderly','responsible','2025-10-06');

INSERT INTO JOB_APPLICATION (caregiver_user_id, job_id, date_applied) VALUES
(3,1,'2025-09-05'),
(7,1,'2025-08-06'),
(10,2,'2025-07-06'),
(3,2,'2025-11-07'),
(5,3,'2025-10-07'),
(8,3,'2025-08-08');

INSERT INTO APPOINTMENT (caregiver_user_id, member_user_id, appointment_date, appointment_time, work_hours, status) VALUES
(3,1,'2025-10-10','09:00',3,'accepted'),
(7,1,'2025-10-11','11:00',4,'pending'),
(5,6,'2025-10-12','10:00',5,'accepted'),
(8,6,'2025-10-13','13:00',4,'declined');
