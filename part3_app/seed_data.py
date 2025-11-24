from datetime import date, time

from .app import create_app, db
from .models import Appointment, Caregiver, Job, JobApplication, Member, User, Address

app = create_app()


def seed():
    with app.app_context():
        if User.query.first():
            print("Database already seeded.")
            return

        users = [
            User(email="raim@mail.com", given_name="Raim", surname="Sultan", city="Almaty", phone_number="+77014578987", profile_description="Father that needs help", password="password1"),
            User(email="nurkhan@mail.com", given_name="Nurkhan", surname="Bekbol", city="Zhezkazgan", phone_number="+77011245789", profile_description="Needs a babysitter", password="password2"),
            User(email="beks@mail.com", given_name="Beks", surname="Beka", city="Shymkent", phone_number="+77013652147", profile_description="Babysitter with a 2 years experience", password="password3"),
            User(email="ali@mail.com", given_name="Ali", surname="Mukha", city="Talgar", phone_number="+77017894567", profile_description="Playmate specialist", password="password4"),
            User(email="alina@mail.com", given_name="Alina", surname="Ema", city="Shymkent", phone_number="+77011265875", profile_description="Elderly caregiver", password="password5"),
            User(email="zhan@mail.com", given_name="Zhan", surname="Zhen", city="Astana", phone_number="+77018574962", profile_description="Looking for elderly caregiver", password="password6"),
            User(email="erzhan@mail.com", given_name="Erzhan", surname="Temir", city="Astana", phone_number="+770112457897", profile_description="Babysitter and tutor", password="password7"),
            User(email="rash@mail.com", given_name="Rash", surname="Zhok", city="Oral", phone_number="+770173918465", profile_description="Elderly care expert", password="password8"),
            User(email="mariam@mail.com", given_name="Mariam", surname="Mariam", city="Aktau", phone_number="+77017859642", profile_description="Playmate for toddlers", password="password9"),
            User(email="artur@mail.com", given_name="Artur", surname="Neartur", city="Atyrau", phone_number="+77012145236", profile_description="Babysitter", password="password10"),
        ]
        db.session.add_all(users)
        db.session.flush()

        caregivers = [
            Caregiver(caregiver_user_id=3, photo="beks.jpg", gender="Male", caregiving_type="babysitter", hourly_rate=7.5),
            Caregiver(caregiver_user_id=4, photo="ali.jpg", gender="Male", caregiving_type="playmate", hourly_rate=12.0),
            Caregiver(caregiver_user_id=5, photo="alina.jpg", gender="Female", caregiving_type="elderly", hourly_rate=12.0),
            Caregiver(caregiver_user_id=7, photo="erzhan.jpg", gender="Male", caregiving_type="babysitter", hourly_rate=8.0),
            Caregiver(caregiver_user_id=8, photo="rash.jpg", gender="Male", caregiving_type="elderly", hourly_rate=13.0),
            Caregiver(caregiver_user_id=9, photo="mariam.jpg", gender="Female", caregiving_type="playmate", hourly_rate=9.0),
            Caregiver(caregiver_user_id=10, photo="artur.jpg", gender="Male", caregiving_type="babysitter", hourly_rate=7.5),
        ]
        db.session.add_all(caregivers)

        members = [
            Member(member_user_id=1, house_rules="No pets.", dependent_description="5-year-old son."),
            Member(member_user_id=2, house_rules="Hygiene is essential.", dependent_description="3-year-old daughter."),
            Member(member_user_id=6, house_rules="No smoking and vapiing.", dependent_description="Elderly mother needs support."),
        ]
        db.session.add_all(members)

        addresses = [
            Address(member_user_id=1, house_number="10", street="Karatau", town="Almaty"),
            Address(member_user_id=2, house_number="34", street="Ortalyk", town="Zhezkazgan"),
            Address(member_user_id=6, house_number="89", street="Sidney", town="Astana"),
        ]
        db.session.add_all(addresses)

        jobs = [
            Job(member_user_id=1, required_caregiving_type="babysitter", other_requirements="punctual", date_posted=date(2025, 10, 1)),
            Job(member_user_id=2, required_caregiving_type="babysitter", other_requirements="experienced", date_posted=date(2025, 10, 2)),
            Job(member_user_id=6, required_caregiving_type="elderly", other_requirements="kind", date_posted=date(2025, 10, 3)),
            Job(member_user_id=1, required_caregiving_type="playmate", other_requirements="creative", date_posted=date(2025, 10, 4)),
            Job(member_user_id=2, required_caregiving_type="babysitter", other_requirements="patient", date_posted=date(2025, 10, 5)),
            Job(member_user_id=6, required_caregiving_type="elderly", other_requirements="responsible", date_posted=date(2025, 10, 6)),
        ]
        db.session.add_all(jobs)
        db.session.flush()

        job_applications = [
            JobApplication(caregiver_user_id=3, job_id=1, date_applied=date(2025, 9, 5)),
            JobApplication(caregiver_user_id=7, job_id=1, date_applied=date(2025, 8, 6)),
            JobApplication(caregiver_user_id=10, job_id=2, date_applied=date(2025, 7, 6)),
            JobApplication(caregiver_user_id=3, job_id=2, date_applied=date(2025, 11, 7)),
            JobApplication(caregiver_user_id=5, job_id=3, date_applied=date(2025, 10, 7)),
            JobApplication(caregiver_user_id=8, job_id=3, date_applied=date(2025, 8, 8)),
        ]
        db.session.add_all(job_applications)

        appointments = [
            Appointment(caregiver_user_id=3, member_user_id=1, appointment_date=date(2025, 10, 10), appointment_time=time(9, 0), work_hours=3, status="accepted"),
            Appointment(caregiver_user_id=7, member_user_id=1, appointment_date=date(2025, 10, 11), appointment_time=time(11, 0), work_hours=4, status="pending"),
            Appointment(caregiver_user_id=5, member_user_id=6, appointment_date=date(2025, 10, 12), appointment_time=time(10, 0), work_hours=5, status="accepted"),
            Appointment(caregiver_user_id=8, member_user_id=6, appointment_date=date(2025, 10, 13), appointment_time=time(13, 0), work_hours=4, status="declined"),
        ]
        db.session.add_all(appointments)

        db.session.commit()
        print("Seed data inserted.")


if __name__ == "__main__":
    seed()

