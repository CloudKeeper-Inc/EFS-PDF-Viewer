from flask import Flask, render_template, send_file, jsonify, request, make_response, abort
import os
import uuid

app = Flask(__name__)

# Hardcoded directory path
PDF_DIRECTORY = "<EFS_PATH>"

# Ensure the directory exists
if not os.path.exists(PDF_DIRECTORY):
    raise ValueError(f"The directory {PDF_DIRECTORY} does not exist.")

pdf_access_tokens = {}

def get_directory_structure(base_path):
    structure = []
    for item in os.listdir(base_path):
        item_path = os.path.join(base_path, item)
        if os.path.isdir(item_path):
            structure.append({
                "type": "directory",
                "name": item,
                "path": item_path,
                "contents": get_directory_structure(item_path)  # Recursively get contents
            })
        elif item.endswith(".pdf"):
            structure.append({
                "type": "file",
                "name": item,
                "path": item_path
            })
    return structure

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/directory_structure")
def directory_structure():
    structure = get_directory_structure(PDF_DIRECTORY)
    return jsonify(structure)

@app.route("/view_pdf")
def view_pdf():
    file_path = request.args.get("path")
    if not file_path or not os.path.exists(file_path):
        abort(404)

    # Generate a unique access token
    access_token = str(uuid.uuid4())
    pdf_access_tokens[access_token] = file_path

    # Render a new page with the embedded PDF viewer
    return render_template("view_pdf.html", access_token=access_token)

@app.route("/pdf/<access_token>")
def serve_pdf(access_token):
    # Check if the access token is valid
    if access_token not in pdf_access_tokens:
        abort(404)

    file_path = pdf_access_tokens[access_token]

    # Serve the PDF file with headers to disable caching and downloading
    response = make_response(send_file(file_path, mimetype="application/pdf"))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers["Content-Disposition"] = "inline"  # Display in the browser, don't download
    return response

if __name__ == "__main__":
    app.run(debug=True)

