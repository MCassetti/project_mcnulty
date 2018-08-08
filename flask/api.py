import numpy as np
import pickle
import librosa
import numpy as np
import math
import random

pipeline = pickle.load(open('./model/model_new.pkl','rb'))
ssX = pickle.load(open('./model/ssX.pkl','rb'))
example = {
  'tempo': 120,
  'mean_harmonic_ratio': 4.855 ,
  'mean_spectral_centroid': 2000.28 ,
  'mean_spectral_flatness': 0.013,
  'count_delta_above_mean': 12 ,  # int
  'ratio_above_rmse_mean': 0.543,  # int
  'max_rmse': 0.201,    # int
  'mean_rmse': 0.079,    # M or F
  'mean_zcr': 0.066,  # int
}
def count_rmse_above_mean(rmse):
    lower_count = 0
    upper_count = 0
    for e in rmse:
        if e > np.mean(rmse): #arbitrarily chosen, will tune later
            upper_count+=1
        else:
            lower_count +=1
    return upper_count/lower_count

def count_delta_above_mean(rmse):
    dyn_change = 0
    for i in range(len(rmse)-3):
        diff = rmse[i+3]-rmse[i]
        if diff > np.mean(rmse):
            dyn_change += 1
    return dyn_change


def harmonic_ratio(signal):
    ratios = []
    y_harmonic, y_percussive = librosa.effects.hpss(signal)
    for i in range(len(y_harmonic)):
        if y_harmonic[i] > 0 and y_percussive[i] > 0: #tgety
            ratios.append(y_harmonic[i]/y_percussive[i])
    return np.median(ratios)

def extract_features(signal,sr):
    tempo, beat_frames = librosa.beat.beat_track(y=signal, sr=sr)
    features = {}
    features['tempo'] = tempo
    features['mean_harmonic_ratio'] = harmonic_ratio(signal)
    features['mean_spectral_centroid'] = np.mean(librosa.feature.spectral_centroid(signal))
    features['mean_spectral_flatness'] = np.mean(librosa.feature.spectral_flatness(signal))
    features['count_delta_above_mean'] = count_delta_above_mean(librosa.feature.rmse(signal)[0])
    features['ratio_above_rmse_mean'] = count_rmse_above_mean(librosa.feature.rmse(signal)[0])
    features['max_rmse'] =  np.max(librosa.feature.rmse(signal)[0])
    features['mean_rmse'] = np.mean(librosa.feature.rmse(signal)[0])
    features['mean_zcr'] = np.mean(librosa.feature.zero_crossing_rate(signal))

    return features


def make_prediction(features):

    X = np.asarray([features['tempo'], features['mean_harmonic_ratio'], features['mean_spectral_centroid'],
                  features['mean_spectral_flatness'], features['count_delta_above_mean'], features['ratio_above_rmse_mean'],
                  features['max_rmse'], features['mean_rmse'], features['mean_zcr']], dtype=np.float64).reshape(1,-1)
    X_scaled = ssX.transform(X)
    prob_metallica = pipeline.predict_proba(X_scaled)[0, 1]
    if int(prob_metallica > 0.5):
        tmp = 'metallica'
    else:
        tmp = 'rush'
    result = {
        'prediction': tmp,
        'prob_metallica': prob_metallica
    }
    return result

def predict_band(response):
    if ((response['prob_metallica'] > 0.8) or (response['prob_metallica'] < 0.2)):
        adj = "I'm highly confident"
    elif (((response['prob_metallica'] < 0.8) and (response['prob_metallica'] >= 0.7)) or
    ((response['prob_metallica'] < 0.3) and (response['prob_metallica'] >= 0.2))):
        adj = "I'm pretty confident confident"
    elif (((response['prob_metallica'] < 0.7) and (response['prob_metallica'] >= 0.6)) or
    ((response['prob_metallica'] < 0.4) and (response['prob_metallica'] >= 0.3))):
            adj = "I'm fairly confident"
    elif ((response['prob_metallica'] < 0.6) and (response['prob_metallica'] >= 0.4)):
        adj = "Maybe "

    else:
        adj = "I'm not really not sure if"

    return adj

def make_and_extract():
    y_total, sr = librosa.load("/Users/mcassettix/github/flask_examples/not_so_simple_flask/static/test.mp3")
    times = librosa.frames_to_time(np.arange(len(y_total)))
    try:
        max_time = len(y_total)/sr
        num_slices = math.floor(max_time/45)
        hop_length = num_slices * sr
        max_x = num_slices*45*sr
        max_offset = 5*sr
        rand_offset = random.choice(range(1,max_offset,100))
        frames = list(range(hop_length,max_x, hop_length))
        if num_slices >= 4:
            quarter_point = math.floor(num_slices/4)
        else:
            quarter_point = 1
        print("rand_offset :",rand_offset )
        y = y_total[frames[int(quarter_point)] + rand_offset:frames[int(quarter_point) + 1] + rand_offset ] #offset in case something in training set
    except:
        print("using whole file....")
        y = y_total

    features = extract_features(y,sr)
    return features

if __name__ == '__main__':
    print(make_prediction(example))
