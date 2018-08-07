from flask import Flask,render_template,jsonify,request
import pafy
from pydub import AudioSegment
import api
app = Flask('MyFirstFlask')



@app.route('/download_vid', methods=['POST'])
def download_vid():
    url = request.form['download_path']
    v = pafy.new(url)
    s = v.allstreams[len(v.allstreams)-1]
    filename = s.download("static/test.mp4")
    audio = AudioSegment.from_file("/Users/mcassettix/github/flask_examples/not_so_simple_flask/static/" + "test.mp4", format=None)
    audio.export("/Users/mcassettix/github/flask_examples/not_so_simple_flask/static/" + "test" + ".mp3", format="mp3", bitrate="312k")
    features = api.make_and_extract()
    print(features)
    response = api.make_prediction(features)
    return jsonify(response)



@app.route('/')
def download():
    return render_template('my_template.html')




app.run(debug=True)
