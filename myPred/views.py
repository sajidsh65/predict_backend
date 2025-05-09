# myPred/views.py
import os
import numpy as np
import pickle
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from tensorflow.keras.models import load_model # type: ignore
from tensorflow.keras.preprocessing.sequence import pad_sequences # type: ignore
import json

# Load tokenizer
with open(os.path.join('myPred', 'model', 'tokenizer.pkl'), 'rb') as f:
    tokenizer = pickle.load(f)

# Load models
model_IE = load_model(os.path.join('myPred', 'model', 'mbti_IE_model.keras'))
model_NS = load_model(os.path.join('myPred', 'model', 'mbti_NS_model.keras'))
model_TF = load_model(os.path.join('myPred', 'model', 'mbti_TF_model.keras'))
model_JP = load_model(os.path.join('myPred', 'model', 'mbti_JP_model.keras'))

# MBTI Mapping
mbti_map = {
    'IE': ['I', 'E'],
    'NS': ['N', 'S'],
    'TF': ['T', 'F'],
    'JP': ['J', 'P']
}

@csrf_exempt
def predict_mbti(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        text = data.get('text', '')

        if not text:
            return JsonResponse({'error': 'No input text provided.'}, status=400)

        # Tokenize & pad
        sequence = tokenizer.texts_to_sequences([text])
        padded = pad_sequences(sequence, maxlen=128)

        # Predict each trait
        pred_IE = model_IE.predict(padded)[0][0]
        pred_NS = model_NS.predict(padded)[0][0]
        pred_TF = model_TF.predict(padded)[0][0]
        pred_JP = model_JP.predict(padded)[0][0]

        result = (
            mbti_map['IE'][int(round(pred_IE))] +
            mbti_map['NS'][int(round(pred_NS))] +
            mbti_map['TF'][int(round(pred_TF))] +
            mbti_map['JP'][int(round(pred_JP))]
        )

        return JsonResponse({
            'mbti_type': result,
            'probabilities': {
                'IE': float(pred_IE),
                'NS': float(pred_NS),
                'TF': float(pred_TF),
                'JP': float(pred_JP)
            }
        })

    return JsonResponse({'error': 'Only POST method is allowed.'}, status=405)



# myPred/views.py (add this below your existing views)

from django.views.decorators.http import require_GET

mbti_qualities = {
    "INTJ": ["Strategic", "Independent", "Analytical", "Determined"],
    "ENFP": ["Enthusiastic", "Creative", "Sociable", "Spontaneous"],
    "ISTJ": ["Responsible", "Organized", "Practical", "Serious"],
    "ISFP": ["Sensitive", "Kind", "Artistic", "Reserved"],
    "INFJ": ["Insightful", "Idealistic", "Compassionate", "Creative"],
    "ENFJ": ["Empathetic", "Organized", "Charismatic", "Motivational"],
    "INFP": ["Idealistic", "Loyal", "Compassionate", "Creative"],
    "ESFP": ["Energetic", "Outgoing", "Spontaneous", "Playful"],
    "INTP": ["Analytical", "Curious", "Logical", "Innovative"],
    "ENTP": ["Inventive", "Outgoing", "Curious", "Persuasive"],
    "ISFJ": ["Supportive", "Responsible", "Reliable", "Loyal"],
    "ESFJ": ["Caring", "Sociable", "Organized", "Supportive"],
    "ISTP": ["Practical", "Independent", "Curious", "Adaptable"],
    "ESTP": ["Energetic", "Action-oriented", "Resourceful", "Charming"],
    "ISFJ": ["Supportive", "Responsible", "Loyal", "Kind"],
    "ESTJ": ["Efficient", "Practical", "Organized", "Leadership"]
}


@require_GET
def get_mbti_qualities(request):
    mbti_type = request.GET.get('type', '').upper()
    qualities = mbti_qualities.get(mbti_type)

    if not qualities:
        return JsonResponse({'error': 'Invalid or missing MBTI type.'}, status=400)

    return JsonResponse({'mbti_type': mbti_type, 'traits': qualities})

@require_GET
def get_qualities(request, mbti_type):
    mbti_type = mbti_type.upper()
    qualities = mbti_qualities.get(mbti_type)

    if not qualities:
        return JsonResponse({'error': 'Invalid or missing MBTI type.'}, status=400)

    return JsonResponse({'mbti_type': mbti_type, 'qualities': qualities})
