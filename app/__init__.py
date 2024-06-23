from flask import Flask, send_from_directory
import os

def create_app():
    app = Flask(__name__)

    with app.app_context():
        from .routes import register_routes
        register_routes()

    @app.route('/image/<path:filename>')
    def serve_image(filename):
        image_folder = os.path.join(app.root_path, 'image')
        return send_from_directory(image_folder, filename)

    return app

