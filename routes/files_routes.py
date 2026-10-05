import os
import uuid

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    send_file
)

from werkzeug.utils import secure_filename

from database import db
from models.file import File


files_bp = Blueprint(
    "files",
    __name__,
    url_prefix="/files"
)


# =========================================================
# HELPER
# =========================================================

def get_user_folder(user_id):

    base_folder = os.path.join(
        "instance",
        "uploads"
    )

    user_folder = os.path.join(
        base_folder,
        str(user_id)
    )

    os.makedirs(
        user_folder,
        exist_ok=True
    )

    return user_folder


# =========================================================
# MY FILES
# =========================================================

@files_bp.route("/")
def files():

    if "user_id" not in session:
        return redirect(
            url_for("auth.login")
        )

    user_id = session["user_id"]

    search = request.args.get(
        "search",
        ""
    ).strip()

    query = File.query.filter_by(
        user_id=user_id
    )

    if search:

        query = query.filter(
            File.original_name.ilike(
                f"%{search}%"
            )
        )

    user_files = query.order_by(
        File.uploaded_at.desc()
    ).all()

    total_size = sum(
        file.file_size
        for file in user_files
    )

    return render_template(
        "files.html",
        files=user_files,
        total_files=len(user_files),
        total_size=total_size,
        search=search
    )


# =========================================================
# UPLOAD
# =========================================================

@files_bp.route(
    "/upload",
    methods=["POST"]
)
def upload():

    if "user_id" not in session:
        return redirect(
            url_for("auth.login")
        )

    uploaded_file = request.files.get(
        "file"
    )

    if not uploaded_file:

        flash(
            "Please select a file.",
            "error"
        )

        return redirect(
            url_for("files.files")
        )

    if uploaded_file.filename == "":

        flash(
            "Please select a file.",
            "error"
        )

        return redirect(
            url_for("files.files")
        )

    original_name = secure_filename(
        uploaded_file.filename
    )

    if not original_name:

        flash(
            "Invalid file name.",
            "error"
        )

        return redirect(
            url_for("files.files")
        )

    user_id = session["user_id"]

    user_folder = get_user_folder(
        user_id
    )

    extension = os.path.splitext(
        original_name
    )[1]

    stored_name = (
        uuid.uuid4().hex
        + extension
    )

    file_path = os.path.join(
        user_folder,
        stored_name
    )

    uploaded_file.save(
        file_path
    )

    file_size = os.path.getsize(
        file_path
    )

    file_type = (
        uploaded_file.mimetype
        or "Unknown"
    )

    new_file = File(
        user_id=user_id,
        original_name=original_name,
        stored_name=stored_name,
        file_path=file_path,
        file_size=file_size,
        file_type=file_type
    )

    db.session.add(
        new_file
    )

    db.session.commit()

    flash(
        "File uploaded successfully.",
        "success"
    )

    return redirect(
        url_for("files.files")
    )


# =========================================================
# DOWNLOAD
# =========================================================

@files_bp.route(
    "/download/<int:file_id>"
)
def download(file_id):

    if "user_id" not in session:
        return redirect(
            url_for("auth.login")
        )

    user_id = session["user_id"]

    file = File.query.filter_by(
        id=file_id,
        user_id=user_id
    ).first_or_404()

    if not os.path.exists(
        file.file_path
    ):

        flash(
            "File no longer exists.",
            "error"
        )

        return redirect(
            url_for("files.files")
        )

    return send_file(
        file.file_path,
        as_attachment=True,
        download_name=file.original_name
    )


# =========================================================
# DELETE
# =========================================================

@files_bp.route(
    "/delete/<int:file_id>",
    methods=["POST"]
)
def delete(file_id):

    if "user_id" not in session:
        return redirect(
            url_for("auth.login")
        )

    user_id = session["user_id"]

    file = File.query.filter_by(
        id=file_id,
        user_id=user_id
    ).first_or_404()

    if os.path.exists(
        file.file_path
    ):

        os.remove(
            file.file_path
        )

    db.session.delete(
        file
    )

    db.session.commit()

    flash(
        "File deleted successfully.",
        "success"
    )

    return redirect(
        url_for("files.files")
    )