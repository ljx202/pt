from flask import Blueprint, send_file, request, jsonify
import os
from config import Config
from utils.file_utils import get_merged_file

download_bp = Blueprint('download', __name__)

@download_bp.route('/files', methods=['GET'])
def list_files():
    upload_dir = Config.UPLOAD_FOLDER
    files = [f for f in os.listdir(upload_dir) if os.path.isfile(os.path.join(upload_dir, f))]
    return jsonify({'files': files})

@download_bp.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404

        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@download_bp.errorhandler(Exception)
def handle_exception(e):
    return jsonify(error=str(e)), 500