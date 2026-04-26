from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sqlalchemy import nullslast
from .. import db
from ..models import Section, Goal, ShoppingItem

bp = Blueprint("dashboard", __name__)


@bp.route("/")
@login_required
def index():
    sections = Section.query.filter_by(user_id=current_user.id).all()

    stats = {}
    for section in sections:
        total_goals = len(section.goals)
        completed_goals = sum(1 for g in section.goals if g.is_completed)
        total_items = len(section.shopping_items)
        purchased_items = sum(1 for i in section.shopping_items if i.is_purchased)
        stats[section.id] = {
            "total_goals": total_goals,
            "completed_goals": completed_goals,
            "total_items": total_items,
            "purchased_items": purchased_items,
        }

    top_goals = (
        db.session.query(Goal)
        .join(Section)
        .filter(Section.user_id == current_user.id, Goal.is_completed == False)
        .order_by(Goal.priority.desc(), nullslast(Goal.deadline.asc()))
        .limit(10)
        .all()
    )

    top_items = (
        db.session.query(ShoppingItem)
        .join(Section)
        .filter(Section.user_id == current_user.id, ShoppingItem.is_purchased == False)
        .order_by(ShoppingItem.priority.desc(), nullslast(ShoppingItem.estimated_cost.asc()))
        .limit(10)
        .all()
    )

    return render_template(
        "dashboard/index.html",
        sections=sections,
        stats=stats,
        top_goals=top_goals,
        top_items=top_items,
    )
