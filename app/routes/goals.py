from datetime import date
from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_required, current_user
from .. import db
from ..models import Goal, Section

bp = Blueprint("goals", __name__, url_prefix="/sections/<int:section_id>/goals")


def _get_owned_section(section_id):
    section = db.get_or_404(Section, section_id)
    if section.user_id != current_user.id:
        abort(403)
    return section


def _parse_form():
    name = request.form.get("name", "").strip()

    try:
        priority = int(request.form.get("priority", Goal.PRIORITY_MEDIUM))
        if priority not in (Goal.PRIORITY_LOW, Goal.PRIORITY_MEDIUM, Goal.PRIORITY_HIGH):
            priority = Goal.PRIORITY_MEDIUM
    except (ValueError, TypeError):
        priority = Goal.PRIORITY_MEDIUM

    deadline = None
    deadline_str = request.form.get("deadline", "").strip()
    if deadline_str:
        try:
            deadline = date.fromisoformat(deadline_str)
        except ValueError:
            flash("Invalid date — deadline cleared.", "info")

    return name, priority, deadline


@bp.route("/new", methods=["GET", "POST"])
@login_required
def create(section_id):
    section = _get_owned_section(section_id)

    if request.method == "POST":
        name, priority, deadline = _parse_form()
        if name:
            db.session.add(Goal(name=name, priority=priority, deadline=deadline, section_id=section.id))
            db.session.commit()
            return redirect(url_for("sections.detail", section_id=section.id))
        flash("Goal name cannot be empty.", "danger")

    return render_template("goals/form.html", section=section, goal=None)


@bp.route("/<int:goal_id>/edit", methods=["GET", "POST"])
@login_required
def edit(section_id, goal_id):
    section = _get_owned_section(section_id)
    goal = db.get_or_404(Goal, goal_id)
    if goal.section_id != section.id:
        abort(403)

    if request.method == "POST":
        name, priority, deadline = _parse_form()
        if name:
            goal.name = name
            goal.priority = priority
            goal.deadline = deadline
            db.session.commit()
            return redirect(url_for("sections.detail", section_id=section.id))
        flash("Goal name cannot be empty.", "danger")

    return render_template("goals/form.html", section=section, goal=goal)


@bp.route("/<int:goal_id>/complete", methods=["POST"])
@login_required
def complete(section_id, goal_id):
    section = _get_owned_section(section_id)
    goal = db.get_or_404(Goal, goal_id)
    if goal.section_id != section.id:
        abort(403)

    goal.is_completed = not goal.is_completed
    db.session.commit()
    return redirect(url_for("sections.detail", section_id=section.id))


@bp.route("/<int:goal_id>/delete", methods=["POST"])
@login_required
def delete(section_id, goal_id):
    section = _get_owned_section(section_id)
    goal = db.get_or_404(Goal, goal_id)
    if goal.section_id != section.id:
        abort(403)

    db.session.delete(goal)
    db.session.commit()
    return redirect(url_for("sections.detail", section_id=section.id))
