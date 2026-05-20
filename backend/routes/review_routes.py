from flask import Blueprint, request, jsonify

from services.ai_review_service import analyze_code
from services.code_parser import parse_code
from services.code_runner import run_code

review_bp = Blueprint("review", __name__)

@review_bp.route("/review", methods=["POST"])
def review():

    data = request.json
    code = data.get("code", "")
    language = data.get("language")

    issues, score = analyze_code(code, language=language)
    stats = parse_code(code)

    return jsonify({
        "issues": issues,
        "score": score,
        "stats": stats
    })

@review_bp.route("/run", methods=["POST"])
def execute_code():
    data = request.json
    code = data.get("code", "")
    language = data.get("language")
    stdin = data.get("stdin", "")
    
    result = run_code(code, language, stdin)
    return jsonify(result)