from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.expense import Expense
from datetime import datetime

expense_bp = Blueprint("expenses", __name__)

@expense_bp.route("/", methods=["GET"])
@jwt_required()
def get_expenses():
    user_id = get_jwt_identity()
    expenses = Expense.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "id": e.id,
        "description": e.description,
        "amount": e.amount,
        "date": e.date.strftime("%Y-%m-%d"),
        "category": e.category
    } for e in expenses])

@expense_bp.route("/", methods=["POST"])
@jwt_required()
def add_expense():
    data = request.json
    user_id = get_jwt_identity()
    expense = Expense(
        description=data["description"],
        amount=data["amount"],
        date=datetime.strptime(data["date"], "%Y-%m-%d"),
        category=data["category"],
        user_id=user_id
    )
    db.session.add(expense)
    db.session.commit()
    return jsonify({"message": "Expense added successfully"}), 201
