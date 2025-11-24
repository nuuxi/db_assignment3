from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    given_name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    profile_description = db.Column(db.Text)
    password = db.Column(db.String(255), nullable=False)

    caregiver = db.relationship(
        "Caregiver", back_populates="user", uselist=False, cascade="all, delete"
    )
    member = db.relationship(
        "Member", back_populates="user", uselist=False, cascade="all, delete"
    )

    @validates("email")
    def validate_email(self, key, address):
        if "@" not in address:
            raise ValueError("Email must contain @")
        return address


class Caregiver(db.Model):
    __tablename__ = "caregiver"

    caregiver_user_id = db.Column(
        db.Integer, db.ForeignKey("user.user_id"), primary_key=True
    )
    photo = db.Column(db.String(255))
    gender = db.Column(db.String(20))
    caregiving_type = db.Column(db.String(50))
    hourly_rate = db.Column(db.Numeric(6, 2))

    user = db.relationship("User", back_populates="caregiver")
    job_applications = db.relationship(
        "JobApplication",
        back_populates="caregiver",
        cascade="all, delete-orphan",
    )
    appointments = db.relationship(
        "Appointment",
        back_populates="caregiver",
        cascade="all, delete-orphan",
    )


class Member(db.Model):
    __tablename__ = "member"

    member_user_id = db.Column(
        db.Integer, db.ForeignKey("user.user_id"), primary_key=True
    )
    house_rules = db.Column(db.Text)
    dependent_description = db.Column(db.Text)

    user = db.relationship("User", back_populates="member")
    address = db.relationship(
        "Address", back_populates="member", uselist=False, cascade="all, delete-orphan"
    )
    jobs = db.relationship(
        "Job", back_populates="member", cascade="all, delete-orphan"
    )
    appointments = db.relationship(
        "Appointment",
        back_populates="member",
        cascade="all, delete-orphan",
    )


class Address(db.Model):
    __tablename__ = "address"

    member_user_id = db.Column(
        db.Integer, db.ForeignKey("member.member_user_id"), primary_key=True
    )
    house_number = db.Column(db.String(20))
    street = db.Column(db.String(100))
    town = db.Column(db.String(100))

    member = db.relationship("Member", back_populates="address")


class Job(db.Model):
    __tablename__ = "job"

    job_id = db.Column(db.Integer, primary_key=True)
    member_user_id = db.Column(
        db.Integer, db.ForeignKey("member.member_user_id"), nullable=False
    )
    required_caregiving_type = db.Column(db.String(50))
    other_requirements = db.Column(db.Text)
    date_posted = db.Column(db.Date)

    member = db.relationship("Member", back_populates="jobs")
    applications = db.relationship(
        "JobApplication",
        back_populates="job",
        cascade="all, delete-orphan",
    )


class JobApplication(db.Model):
    __tablename__ = "job_application"
    caregiver_user_id = db.Column(
        db.Integer, db.ForeignKey("caregiver.caregiver_user_id"), primary_key=True
    )
    job_id = db.Column(db.Integer, db.ForeignKey("job.job_id"), primary_key=True)
    date_applied = db.Column(db.Date)

    caregiver = db.relationship("Caregiver", back_populates="job_applications")
    job = db.relationship("Job", back_populates="applications")


class Appointment(db.Model):
    __tablename__ = "appointment"

    appointment_id = db.Column(db.Integer, primary_key=True)
    caregiver_user_id = db.Column(
        db.Integer, db.ForeignKey("caregiver.caregiver_user_id"), nullable=False
    )
    member_user_id = db.Column(
        db.Integer, db.ForeignKey("member.member_user_id"), nullable=False
    )
    appointment_date = db.Column(db.Date)
    appointment_time = db.Column(db.Time)
    work_hours = db.Column(db.Integer)
    status = db.Column(db.String(20))

    caregiver = db.relationship("Caregiver", back_populates="appointments")
    member = db.relationship("Member", back_populates="appointments")

