from flask import Flask, render_template, request, send_file
import qrcode
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.form.get('data')
    filename = request.form.get('filename')


    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        
        if not filename.endswith((".png", ".jpg")):
            filename += ".png"

        img = qr.make_image(fill_color="#2c3e50", back_color="white")
        
        img_io = io.BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        
        return send_file(img_io, mimetype='image/png', as_attachment=True, download_name=filename)
        
    except Exception as e:
        return f"An error occurred: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)