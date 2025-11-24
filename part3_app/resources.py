from __future__ import annotations

from datetime import date, time
from decimal import Decimal
from typing import Any, Callable, Dict, Iterable, List

from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from .models import Appointment, Caregiver, Job, JobApplication, Member, User, Address, db

bp = Blueprint("crud", __name__)


def _cast_value(value: str | None, parser: str) -> Any:
    if value is None or value == "":
        return None
    if parser == "int":
        return int(value)
    if parser == "decimal":
        return Decimal(value)
    if parser == "date":
        return date.fromisoformat(value)
    if parser == "time":
        return time.fromisoformat(value)
    return value


def _format_value(value: Any, parser: str) -> str:
    if value is None:
        return ""
    if parser == "date" and isinstance(value, date):
        return value.isoformat()
    if parser == "time" and isinstance(value, time):
        return value.strftime("%H:%M")
    if parser == "decimal":
        return f"{Decimal(value):.2f}"
    return str(value)


def _pk_path(pk_fields: Iterable[str]) -> str:
    return "/".join(f"<int:{field}>" for field in pk_fields)


def _fetch_record(model, pk_fields: List[str], pk_values: Dict[str, Any]):
    return model.query.filter_by(**pk_values).first_or_404()


RESOURCES: Dict[str, Dict[str, Any]] = {
    "users": {
        "title": "Users",
        "model": User,
        "pk": ["user_id"],
        "list_columns": [
            {"name": "user_id", "label": "ID"},
            {"name": "email", "label": "Email"},
            {"name": "given_name", "label": "Given Name"},
            {"name": "surname", "label": "Surname"},
            {"name": "city", "label": "City"},
        ],
        "form_fields": [
            {"name": "email", "label": "Email", "input_type": "email", "parser": "string", "required": True},
            {"name": "given_name", "label": "Given Name", "input_type": "text", "parser": "string", "required": True},
            {"name": "surname", "label": "Surname", "input_type": "text", "parser": "string", "required": True},
            {"name": "city", "label": "City", "input_type": "text", "parser": "string"},
            {"name": "phone_number", "label": "Phone Number", "input_type": "text", "parser": "string"},
            {"name": "profile_description", "label": "Profile Description", "input_type": "textarea", "parser": "string"},
            {"name": "password", "label": "Password", "input_type": "text", "parser": "string", "required": True},
        ],
    },
    "caregivers": {
        "title": "Caregivers",
        "model": Caregiver,
        "pk": ["caregiver_user_id"],
        "list_columns": [
            {"name": "caregiver_user_id", "label": "User ID"},
            {"name": "gender", "label": "Gender"},
            {"name": "caregiving_type", "label": "Type"},
            {"name": "hourly_rate", "label": "Hourly Rate"},
        ],
        "form_fields": [
            {"name": "caregiver_user_id", "label": "User ID", "input_type": "number", "parser": "int", "required": True},
            {"name": "photo", "label": "Photo URL", "input_type": "text", "parser": "string"},
            {"name": "gender", "label": "Gender", "input_type": "text", "parser": "string"},
            {"name": "caregiving_type", "label": "Caregiving Type", "input_type": "text", "parser": "string"},
            {"name": "hourly_rate", "label": "Hourly Rate", "input_type": "number", "parser": "decimal"},
        ],
    },
    "members": {
        "title": "Members",
        "model": Member,
        "pk": ["member_user_id"],
        "list_columns": [
            {"name": "member_user_id", "label": "User ID"},
            {"name": "house_rules", "label": "House Rules"},
            {"name": "dependent_description", "label": "Dependent"},
        ],
        "form_fields": [
            {"name": "member_user_id", "label": "User ID", "input_type": "number", "parser": "int", "required": True},
            {"name": "house_rules", "label": "House Rules", "input_type": "textarea", "parser": "string"},
            {"name": "dependent_description", "label": "Dependent Description", "input_type": "textarea", "parser": "string"},
        ],
    },
    "addresses": {
        "title": "Addresses",
        "model": Address,
        "pk": ["member_user_id"],
        "list_columns": [
            {"name": "member_user_id", "label": "Member ID"},
            {"name": "house_number", "label": "House #"},
            {"name": "street", "label": "Street"},
            {"name": "town", "label": "Town"},
        ],
        "form_fields": [
            {"name": "member_user_id", "label": "Member ID", "input_type": "number", "parser": "int", "required": True},
            {"name": "house_number", "label": "House Number", "input_type": "text", "parser": "string"},
            {"name": "street", "label": "Street", "input_type": "text", "parser": "string"},
            {"name": "town", "label": "Town", "input_type": "text", "parser": "string"},
        ],
    },
    "jobs": {
        "title": "Jobs",
        "model": Job,
        "pk": ["job_id"],
        "list_columns": [
            {"name": "job_id", "label": "Job ID"},
            {"name": "member_user_id", "label": "Member ID"},
            {"name": "required_caregiving_type", "label": "Type"},
            {"name": "date_posted", "label": "Posted"},
        ],
        "form_fields": [
            {"name": "member_user_id", "label": "Member ID", "input_type": "number", "parser": "int", "required": True},
            {"name": "required_caregiving_type", "label": "Required Type", "input_type": "text", "parser": "string"},
            {"name": "other_requirements", "label": "Other Requirements", "input_type": "textarea", "parser": "string"},
            {"name": "date_posted", "label": "Date Posted", "input_type": "date", "parser": "date"},
        ],
    },
    "job_applications": {
        "title": "Job Applications",
        "model": JobApplication,
        "pk": ["caregiver_user_id", "job_id"],
        "list_columns": [
            {"name": "caregiver_user_id", "label": "Caregiver ID"},
            {"name": "job_id", "label": "Job ID"},
            {"name": "date_applied", "label": "Applied"},
        ],
        "form_fields": [
            {"name": "caregiver_user_id", "label": "Caregiver ID", "input_type": "number", "parser": "int", "required": True},
            {"name": "job_id", "label": "Job ID", "input_type": "number", "parser": "int", "required": True},
            {"name": "date_applied", "label": "Date Applied", "input_type": "date", "parser": "date"},
        ],
    },
    "appointments": {
        "title": "Appointments",
        "model": Appointment,
        "pk": ["appointment_id"],
        "list_columns": [
            {"name": "appointment_id", "label": "Appointment ID"},
            {"name": "caregiver_user_id", "label": "Caregiver ID"},
            {"name": "member_user_id", "label": "Member ID"},
            {"name": "appointment_date", "label": "Date"},
            {"name": "status", "label": "Status"},
        ],
        "form_fields": [
            {"name": "caregiver_user_id", "label": "Caregiver ID", "input_type": "number", "parser": "int", "required": True},
            {"name": "member_user_id", "label": "Member ID", "input_type": "number", "parser": "int", "required": True},
            {"name": "appointment_date", "label": "Date", "input_type": "date", "parser": "date"},
            {"name": "appointment_time", "label": "Time", "input_type": "time", "parser": "time"},
            {"name": "work_hours", "label": "Work Hours", "input_type": "number", "parser": "int"},
            {"name": "status", "label": "Status", "input_type": "text", "parser": "string"},
        ],
    },
}


@bp.route("/")
def dashboard():
    counts = {
        name: cfg["model"].query.count()
        for name, cfg in RESOURCES.items()
    }
    return render_template("dashboard.html", counts=counts, resources=RESOURCES)


def _upsert_record(model, fields, form_data, instance=None):
    target = instance or model()
    for field in fields:
        field_name = field["name"]
        parser = field.get("parser", "string")
        value = _cast_value(form_data.get(field_name), parser)
        setattr(target, field_name, value)
    db.session.add(target)
    db.session.commit()
    return target


def register_resource_routes(app):
    app.register_blueprint(bp)

    for resource_name, config in RESOURCES.items():
        model = config["model"]
        pk_fields = config["pk"]
        fields = config["form_fields"]
        pk_segment = _pk_path(pk_fields)

        def list_view(resource=resource_name, cfg=config):
            records = cfg["model"].query.order_by(
                *[getattr(cfg["model"], pk) for pk in cfg["pk"]]
            ).all()
            rows = [
                {
                    "record": record,
                    "pk": {pk: getattr(record, pk) for pk in cfg["pk"]},
                }
                for record in records
            ]
            return render_template(
                "resource_list.html",
                resource=resource,
                config=cfg,
                rows=rows,
                resources=RESOURCES,
                getattr_fn=getattr,
            )

        def create_view(resource=resource_name, cfg=config):
            if request.method == "POST":
                _upsert_record(cfg["model"], cfg["form_fields"], request.form)
                flash(f"{cfg['title']} record created.", "success")
                return redirect(url_for(f"{resource}_list"))
            return render_template(
                "resource_form.html",
                resource=resource,
                config=cfg,
                form_values={},
                action="Create",
                resources=RESOURCES,
            )

        def edit_view(resource=resource_name, cfg=config, pk_fields=pk_fields, **kwargs):
            pk_values = {field: kwargs[field] for field in pk_fields}
            record = _fetch_record(cfg["model"], pk_fields, pk_values)
            if request.method == "POST":
                _upsert_record(cfg["model"], cfg["form_fields"], request.form, record)
                flash(f"{cfg['title']} record updated.", "success")
                return redirect(url_for(f"{resource}_list"))
            form_values = {
                field["name"]: _format_value(
                    getattr(record, field["name"]),
                    field.get("parser", "string"),
                )
                for field in cfg["form_fields"]
            }
            return render_template(
                "resource_form.html",
                resource=resource,
                config=cfg,
                form_values=form_values,
                action="Edit",
                pk_values=pk_values,
                resources=RESOURCES,
            )

        def delete_view(resource=resource_name, cfg=config, pk_fields=pk_fields, **kwargs):
            pk_values = {field: kwargs[field] for field in pk_fields}
            record = _fetch_record(cfg["model"], pk_fields, pk_values)
            db.session.delete(record)
            db.session.commit()
            flash(f"{cfg['title']} record deleted.", "info")
            return redirect(url_for(f"{resource}_list"))

        app.add_url_rule(
            f"/{resource_name}",
            endpoint=f"{resource_name}_list",
            view_func=list_view,
            methods=["GET"],
        )
        app.add_url_rule(
            f"/{resource_name}/create",
            endpoint=f"{resource_name}_create",
            view_func=create_view,
            methods=["GET", "POST"],
        )
        app.add_url_rule(
            f"/{resource_name}/edit/{pk_segment}",
            endpoint=f"{resource_name}_edit",
            view_func=edit_view,
            methods=["GET", "POST"],
        )
        app.add_url_rule(
            f"/{resource_name}/delete/{pk_segment}",
            endpoint=f"{resource_name}_delete",
            view_func=delete_view,
            methods=["POST"],
        )

