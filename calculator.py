from flask import Flask, request, jsonify

app = Flask(__name__)

MATERIALS = {
    "Mild Steel": 7.85,
    "Aluminum": 2.70,
    "Stainless Steel": 8.00,
    "Copper": 8.96,
}

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    material = data.get('material')
    density = MATERIALS.get(material, 7.85)  # Default density for Mild Steel
    shape = data.get('shape')
    units = data.get('units', 'metric')  # 'metric' or 'imperial'
    
    if shape == 'sheet':
        length = data['length'] / (25.4 if units == 'imperial' else 1)
        width = data['width'] / (25.4 if units == 'imperial' else 1)
        thickness = data['thickness'] / (25.4 if units == 'imperial' else 1)
        volume = length * width * thickness
    elif shape == 'box_pipe':
        outer_width = data['outer_width'] / (25.4 if units == 'imperial' else 1)
        outer_height = data['outer_height'] / (25.4 if units == 'imperial' else 1)
        wall_thickness = data['wall_thickness'] / (25.4 if units == 'imperial' else 1)
        length = data['length'] / (25.4 if units == 'imperial' else 1)
        outer_volume = outer_width * outer_height * length
        inner_width = outer_width - 2 * wall_thickness
        inner_height = outer_height - 2 * wall_thickness
        inner_volume = inner_width * inner_height * length
        volume = outer_volume - inner_volume
    elif shape == 'cylinder':
        radius = data['radius'] / (25.4 if units == 'imperial' else 1)
        height = data['height'] / (25.4 if units == 'imperial' else 1)
        volume = 3.1416 * (radius ** 2) * height
    else:
        return jsonify({"error": "Invalid shape"}), 400

    weight = volume * density
    weight = weight / 1000 if units == 'metric' else weight * 0.00220462  # kg or lbs
    return jsonify({"weight": round(weight, 2)})

if __name__ == '__main__':
    app.run(port=5000)
  
