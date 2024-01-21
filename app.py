# app.py
from flask import Flask, render_template, request, jsonify
from genetik_algoritma import GenetikAlgoritma
from geopy.distance import geodesic
import random
import copy

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

kayitli_noktalar = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/kaydet', methods=['POST'])
def kaydet():
    data = request.get_json()
    noktalar = data.get('noktalar', [])
    global kayitli_noktalar
    kayitli_noktalar = noktalar
    return jsonify({'message': 'Noktalar başarıyla kaydedildi.'})

@app.route('/mesafe')
def mesafe():
    mesafe_matrisi = []
    for i in range(len(kayitli_noktalar)):
        mesafe_matrisi.append([])
        for j in range(len(kayitli_noktalar)):
            mesafe_matrisi[i].append(
                geodesic((kayitli_noktalar[i]['lat'], kayitli_noktalar[i]['lng']),
                         (kayitli_noktalar[j]['lat'], kayitli_noktalar[j]['lng'])).kilometers
            )
    return jsonify({'mesafe_matrisi': mesafe_matrisi})

@app.route('/genetik_algoritma', methods=['POST'])
def genetik_algoritma():
    data = request.form
    pop_size = int(data['pop_size'])
    iterasyon_sayisi = int(data['iterasyon_sayisi'])
    caprazlama_orani = float(data['caprazlama_orani'])
    mutasyon_orani = float(data['mutasyon_orani'])

    noktalar = [f"Nokta {i+1}" for i in range(len(kayitli_noktalar))]
    mesafe_matrisi = []
    for i in range(len(kayitli_noktalar)):
        mesafe_matrisi.append([])
        for j in range(len(kayitli_noktalar)):
            mesafe_matrisi[i].append(
                geodesic((kayitli_noktalar[i]['lat'], kayitli_noktalar[i]['lng']),
                         (kayitli_noktalar[j]['lat'], kayitli_noktalar[j]['lng'])).kilometers
            )

    ga = GenetikAlgoritma(pop_size, iterasyon_sayisi, caprazlama_orani, mutasyon_orani, noktalar, mesafe_matrisi)
    en_iyi_yol, en_iyi_uygunluk = ga.optimize_et()

    return render_template('sonuc.html', en_iyi_yol=en_iyi_yol, en_iyi_uygunluk=en_iyi_uygunluk, kayitli_noktalar=kayitli_noktalar)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
