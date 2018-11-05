import json, pickle, re, time 
from flask import Flask, render_template, request, make_response, jsonify
from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

app = Flask(__name__)

MAX_SEQUENCE_LENGTH = 100
with open("model/tokenizer.pickle", "rb") as handle:
	tokenizer = pickle.load(handle) 
model = load_model("model/model.h5")
model._make_predict_function()	# https://github.com/keras-team/keras/issues/6462
label2emotion = {0:"others", 1:"happy", 2: "sad", 3:"angry"}


@app.route("/app", methods=["GET", "POST"])
def hello_word(name=None):
	if(request.method == "POST"):
		request_body = request.get_json()
		turn_1 = request_body.get("turn_1", "")
		turn_2 = request_body.get("turn_2", "")
		turn_3 = request_body.get("turn_3", "")
		emotion = get_emotion(turn_1, turn_2, turn_3)
		response = make_response(json.dumps({'success': True, 'emotion': emotion}))
		response.status_code = 200
		response.headers['Content-Type'] = 'application/json'
		return response
	
	return render_template("index.html", name = name)


@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    return jsonify({'ip': request.remote_addr}), 200
    

def get_emotion(turn1, turn2, turn3):
	test_data = [turn1, turn2, turn3]
	repeated_chars = [".", "?", "!", ","]
	# convert multiple instances of . ? ! , to a single instance
	for idx in range(len(test_data)):
		for c in repeated_chars:
			turn_split = test_data[idx].split(c)
			while True:
				try:
					turn_split.remove('')
				except:
					break
			c_space = " " + c + " "
			test_data[idx] = c_space.join(turn_split)
		# remove duplicate spaces
		duplicate_space_pattern = re.compile(r'\ +')
		test_data[idx] = re.sub(duplicate_space_pattern, ' ', test_data[idx])
		# convert to lower case
		test_data[idx] = test_data[idx].lower()

	test_data = " <eos> ".join(test_data)
	test_data_sequence = tokenizer.texts_to_sequences([test_data])
	test_data_sequence = pad_sequences(test_data_sequence, maxlen=MAX_SEQUENCE_LENGTH)
	prediction = model.predict([test_data_sequence, test_data_sequence], batch_size=200)
	prediction = prediction.argmax(axis=1)[0]
	
	return label2emotion[prediction]


if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)
	