from flask import Flask, request, render_template, jsonify, Response
import pickle
import re
import cv2
import numpy as np
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from keras.models import load_model
from keras.preprocessing.image import img_to_array

# Load models and tools
predictor = pickle.load(open("model/model_xgb.pkl", "rb"))
scaler = pickle.load(open("model/scaler.pkl", "rb"))
cv = pickle.load(open("model/countVectorizer.pkl", "rb"))
STOPWORDS = set(stopwords.words("english"))

face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
emotion_classifier = load_model("model.h5")
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

app = Flask(__name__)

def preprocess_text(text_input):
    stemmer = PorterStemmer()
    review = re.sub("[^a-zA-Z]", " ", text_input)
    review = review.lower().split()
    review = [stemmer.stem(word) for word in review if word not in STOPWORDS]
    return " ".join(review)

def single_prediction(text_input):
    processed_text = preprocess_text(text_input)
    X_prediction = cv.transform([processed_text]).toarray()
    X_prediction_scl = scaler.transform(X_prediction)
    y_predictions = predictor.predict_proba(X_prediction_scl)
    y_predictions = y_predictions.argmax(axis=1)[0]
    return "Positive" if y_predictions == 1 else "Negative"

def detect_emotion(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x + w]
        roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)
        if np.sum([roi_gray]) != 0:
            roi = roi_gray.astype('float') / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)
            prediction = emotion_classifier.predict(roi)[0]
            label = emotion_labels[prediction.argmax()]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    return frame

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST','GET'])
def predict():
    text_input = request.form['text_input']
    prediction = single_prediction(text_input)
    return jsonify({'prediction': prediction})

def gen_frames():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            frame = detect_emotion(frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
