from flask import current_app as app, render_template, jsonify, request
from app.api.qr_api import read_from_port
from app.api.camera_api import *
from app.image_processing.image_sharpness import calculate_sharpness
import cv2

camera = CameraAPI()

def register_routes():
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/activate_port', methods=['POST'])
    def activate_port():
        port = "/dev/ttyS0"
        try:
            qr_data = read_from_port(port)
            if qr_data:
                return jsonify({
                    'QR Code': qr_data
                })
            else:
                return jsonify({'error': 'No data read from port'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/capture_image', methods=['POST'])
    def capture_image():
        try:
            with camera:
                filepath = 'app/static/image.bmp'  # Путь, куда сохранять изображение
                camera.capture_frame(filepath)
                return jsonify({'message': 'Image captured successfully.'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/parameters', methods=['GET'])
def get_parameters():
    try:
        with camera:
            exposure_time = camera.ExposureTime
            gamma = camera.Gamma
            width = camera.Width
            height = camera.Height
            offset_x = camera.OffsetX
            offset_y = camera.OffsetY

            parameters = {
                'ExposureTime': exposure_time,
                'Gamma': gamma,
                'Width': width,
                'Height': height,
                'OffsetX': offset_x,
                'OffsetY': offset_y
            }

            return jsonify(parameters), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/parameter/<param>', methods=['POST'])
def handle_parameter(param):
    try:
        with camera:
            new_value = int(request.json)

            if new_value is not None:
                setattr(camera, param, new_value)
                return jsonify({'message': f'{param} updated successfully'}), 200
            else:
                return jsonify({'error': f'Invalid value provided for {param}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/calculate_sharpness', methods=['POST'])
def calculate_sharpness_route():
    try:
        image = cv2.imread('app/static/image.bmp')
        sharpness = calculate_sharpness(image)
        return jsonify({"sharpness": sharpness}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
