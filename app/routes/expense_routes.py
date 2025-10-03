from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.expense import Expense
from datetime import datetime

expense_bp = Blueprint("expenses", __name__)

# ------------------- GET ALL EXPENSES -------------------
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

# ------------------- GET SINGLE EXPENSE -------------------
@expense_bp.route("/<int:expense_id>", methods=["GET"])
@jwt_required()
def get_expense(expense_id):
    user_id = get_jwt_identity()
    expense = Expense.query.filter_by(id=expense_id, user_id=user_id).first_or_404()
    return jsonify({
        "id": expense.id,
        "description": expense.description,
        "amount": expense.amount,
        "date": expense.date.strftime("%Y-%m-%d"),
        "category": expense.category
    })

# ------------------- ADD EXPENSE -------------------
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

# ------------------- UPDATE EXPENSE -------------------
@expense_bp.route("/<int:expense_id>", methods=["PUT"])
@jwt_required()
def update_expense(expense_id):
    user_id = get_jwt_identity()
    data = request.json
    expense = Expense.query.filter_by(id=expense_id, user_id=user_id).first_or_404()
    
    expense.description = data.get("description", expense.description)
    expense.amount = data.get("amount", expense.amount)
    if "date" in data:
        expense.date = datetime.strptime(data["date"], "%Y-%m-%d")
    expense.category = data.get("category", expense.category)
    
    db.session.commit()
    return jsonify({"message": "Expense updated successfully"})

# ------------------- DELETE EXPENSE -------------------
@expense_bp.route("/<int:expense_id>", methods=["DELETE"])
@jwt_required()
def delete_expense(expense_id):
    user_id = get_jwt_identity()
    expense = Expense.query.filter_by(id=expense_id, user_id=user_id).first_or_404()
    
    db.session.delete(expense)
    db.session.commit()
    return jsonify({"message": "Expense deleted successfully"})
