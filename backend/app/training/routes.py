from flask import Blueprint, request
from app.middleware.jwt_required import token_required
from app.training.controller import upload_document, process_document, train_clone, delete_document, list_documents
from app.utils.responses import api_response

training_bp = Blueprint("training", __name__)

@training_bp.route("/upload", methods=["POST"])
@token_required
def training_upload(current_user):
    if "document" not in request.files and not request.json:
        return api_response(error="No document provided", status=400)

    payload = request.json if request.json else {"document_type": request.form.get("document_type", "unknown"), "title": request.form.get("title", "uploaded document"), "content": request.form.get("content", "")}
    return upload_document(current_user, payload)

@training_bp.route("/list", methods=["GET"])
@token_required
def training_list(current_user):
    return list_documents(current_user)

@training_bp.route("/<string:document_id>", methods=["DELETE"])
@token_required
def training_delete(current_user, document_id):
    return delete_document(current_user, document_id)

@training_bp.route("/process", methods=["POST"])
@token_required
def training_process(current_user):
    payload = request.get_json(silent=True)
    return process_document(current_user, payload)

@training_bp.route("/train", methods=["POST"])
@token_required
def training_train(current_user):
    payload = request.get_json(silent=True)
    return train_clone(current_user, payload)
