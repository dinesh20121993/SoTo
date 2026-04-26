from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_required, current_user
from .. import db
from ..models import ShoppingItem, Section

bp = Blueprint("shopping", __name__, url_prefix="/sections/<int:section_id>/shopping")


def _get_owned_section(section_id):
    section = db.get_or_404(Section, section_id)
    if section.user_id != current_user.id:
        abort(403)
    return section


def _parse_form():
    name = request.form.get("name", "").strip()

    try:
        quantity = max(1, int(request.form.get("quantity", 1)))
    except (ValueError, TypeError):
        quantity = 1

    estimated_cost = None
    cost_str = request.form.get("estimated_cost", "").strip()
    if cost_str:
        try:
            estimated_cost = float(cost_str)
            if estimated_cost < 0:
                estimated_cost = None
        except ValueError:
            flash("Invalid cost — value cleared.", "info")

    try:
        priority = int(request.form.get("priority", ShoppingItem.PRIORITY_MEDIUM))
        if priority not in (ShoppingItem.PRIORITY_LOW, ShoppingItem.PRIORITY_MEDIUM, ShoppingItem.PRIORITY_HIGH):
            priority = ShoppingItem.PRIORITY_MEDIUM
    except (ValueError, TypeError):
        priority = ShoppingItem.PRIORITY_MEDIUM

    return name, quantity, estimated_cost, priority


@bp.route("/new", methods=["GET", "POST"])
@login_required
def create(section_id):
    section = _get_owned_section(section_id)

    if request.method == "POST":
        name, quantity, estimated_cost, priority = _parse_form()
        if name:
            db.session.add(ShoppingItem(
                name=name,
                quantity=quantity,
                estimated_cost=estimated_cost,
                priority=priority,
                section_id=section.id,
            ))
            db.session.commit()
            return redirect(url_for("sections.detail", section_id=section.id))
        flash("Item name cannot be empty.", "danger")

    return render_template("shopping/form.html", section=section, item=None)


@bp.route("/<int:item_id>/edit", methods=["GET", "POST"])
@login_required
def edit(section_id, item_id):
    section = _get_owned_section(section_id)
    item = db.get_or_404(ShoppingItem, item_id)
    if item.section_id != section.id:
        abort(403)

    if request.method == "POST":
        name, quantity, estimated_cost, priority = _parse_form()
        if name:
            item.name = name
            item.quantity = quantity
            item.estimated_cost = estimated_cost
            item.priority = priority
            db.session.commit()
            return redirect(url_for("sections.detail", section_id=section.id))
        flash("Item name cannot be empty.", "danger")

    return render_template("shopping/form.html", section=section, item=item)


@bp.route("/<int:item_id>/purchase", methods=["POST"])
@login_required
def purchase(section_id, item_id):
    section = _get_owned_section(section_id)
    item = db.get_or_404(ShoppingItem, item_id)
    if item.section_id != section.id:
        abort(403)

    item.is_purchased = not item.is_purchased
    db.session.commit()
    return redirect(url_for("sections.detail", section_id=section.id))


@bp.route("/<int:item_id>/delete", methods=["POST"])
@login_required
def delete(section_id, item_id):
    section = _get_owned_section(section_id)
    item = db.get_or_404(ShoppingItem, item_id)
    if item.section_id != section.id:
        abort(403)

    db.session.delete(item)
    db.session.commit()
    return redirect(url_for("sections.detail", section_id=section.id))
