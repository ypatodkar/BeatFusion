from flask import Flask, request, jsonify, send_file
# from tabla_overlay import generate_tabla_bpm_map
from mix_stems import mix_stems
from batch_seperate import list_songs, batch_separate
from GenerateBPMMapping import generate_bpm_map
from tabla_overlay import overlay_tabla


app = Flask(__name__)


@app.route('/api/songs', methods=['GET'])
def api_list_songs():
    # Returns an array of song filenames
    return jsonify(list_songs())


@app.route('/api/generate-tabla-bpm', methods=['POST'])
def api_generate_tabla_bpm():
    data = request.get_json() or {}
    root = data.get('tabla_root')
    output = data.get('output_path')
    bpm_map = generate_bpm_map(root, output)
    return jsonify(bpm_map)


@app.route('/api/mix-stems', methods=['POST'])
def api_mix_stems():
    data = request.get_json()

    song = data['song_name']
    remove = data.get('remove_stem')
    input_dir = data.get('input_dir')
    out = data.get('output_path')
    result_path = mix_stems(song, remove, input_dir, out)
    return send_file(result_path, as_attachment=True)


@app.route('/api/batch-separate', methods=['POST'])
def api_batch_separate():
    data = request.get_json()
    song = data.get('song')
    model = data.get('model')

    if not song or not model:
        return jsonify({'error': 'Missing song or model'}), 400

    try:
        folder = batch_separate(song, model)
        return jsonify({'output_folder': folder})
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/api/generate-bpm-map', methods=['POST'])
def api_generate_bpm_map():

    data = request.get_json() or {}


    root = data.get('tabla_dataset_root')
    output = data.get('output_path')
    bpm_map = generate_bpm_map(root, output)
    return jsonify(bpm_map)

# --- Flask Endpoint ---
@app.route('/api/overlay', methods=['POST'])
def api_overlay():
    data = request.get_json() or {}
    song = data.get('song')
    mix = data.get('mix')  # 'vocals+tabla' or 'vocals+piano+bass'
    model = data.get('model', 'htdemucs_6s')
    if not song or not mix:
        return jsonify({'error': 'Missing song or mix type'}), 400
    try:
        result_path = overlay_tabla(song, mix, model)
        return jsonify({'output_path': result_path})
    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
