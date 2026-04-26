from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_required, current_user
from .. import db
from ..models import Section

bp = Blueprint("sections", __name__, url_prefix="/sections")


@bp.route("/", methods=["GET", "POST"])
@login_required
def list_sections():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            flash("Section name cannot be empty.", "danger")
        else:
            db.session.add(Section(name=name, user_id=current_user.id))
            db.session.commit()
        return redirect(url_for("sections.list_sections"))

    sections = (
        Section.query
        .filter_by(user_id=current_user.id)
        .order_by(Section.name)
        .all()
    )
    return render_template("sections/list.html", sections=sections)


@bp.route("/new", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if name:
            section = Section(name=name, user_id=current_user.id)
            db.session.add(section)
            db.session.commit()
            return redirect(url_for("sections.detail", section_id=section.id))
        flash("Section name cannot be empty.", "danger")

    return render_template("sections/form.html", section=None)


@bp.route("/<int:section_id>")
@login_required
def detail(section_id):
    section = db.get_or_404(Section, section_id)
    if section.user_id != current_user.id:
        abort(403)
    return render_template("sections/detail.html", section=section)


@bp.route("/<int:section_id>/edit", methods=["GET", "POST"])
@login_required
def edit(section_id):
    section = db.get_or_404(Section, section_id)
    if section.user_id != current_user.id:
        abort(403)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if name:
            section.name = name
            db.session.commit()
            return redirect(url_for("sections.detail", section_id=section.id))
        flash("Section name cannot be empty.", "danger")

    return render_template("sections/form.html", section=section)


@bp.route("/<int:section_id>/delete", methods=["POST"])
@login_required
def delete(section_id):
    section = db.get_or_404(Section, section_id)
    if section.user_id != current_user.id:
        abort(403)

    db.session.delete(section)
    db.session.commit()
    return redirect(url_for("sections.list_sections"))
