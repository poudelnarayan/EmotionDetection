from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from tensorflow.keras.models import load_model
from keras.models import model_from_json
import numpy as np
from base64 import b64decode
from django.middleware.csrf import get_token
from PIL import Image
import io
from django.http import JsonResponse
import cv2


def take_photo(request):
    csrf_token = get_token(request)
    if request.method == 'POST':
        data = request.POST.get('photo_data')
        binary = b64decode(data.split(',')[1])
        image = Image.open(io.BytesIO(binary))
        numpy_array = np.array(image)
        # Save the image file on the server
        with open('videocap/static/videocap/images/photos.jpg', 'wb') as f:
            f.write(binary)
        emotion_dict = {0: "Angry", 1: "happy", 2: "neutral",
                        3: "sad"}
        json_file = open('trained_model/emotion_model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        emotion_model = model_from_json(loaded_model_json)
        emotion_model.load_weights("trained_model/emotion_model.h5")
        print("Loaded model from disk")

        gray_image = cv2.cvtColor(numpy_array, cv2.COLOR_BGR2GRAY)
        cropped_img = np.expand_dims(np.expand_dims(
            cv2.resize(gray_image, (48, 48)), -1), 0)

        emotion_prediction = emotion_model.predict(cropped_img)
        maxindex = int(np.argmax(emotion_prediction))
        print("*******************************************")

        return JsonResponse({'redirectUrl': reverse('view_emotion', kwargs={'detected_emotion': emotion_dict[maxindex]})})
    else:
        return render(request, 'videocap/take_photo.html', {'csrf_token': csrf_token})


def view_emotion(request, detected_emotion):
    context = {
        'detected_emotion': detected_emotion,
    }
    print(context)
    return render(request, 'videocap/view_emotion.html', context)
