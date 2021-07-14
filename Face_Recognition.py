import numpy as np
import cv2
import dlib

# Models Loaded
face_detector = dlib.get_frontal_face_detector()
pose_predictor_68_point = dlib.shape_predictor(
    '/home/bassam/Desktop/projects/Student-Facial-Recognition/shape_predictor_68_face_landmarks.dat')
face_encoder = dlib.face_recognition_model_v1(
    '/home/bassam/Desktop/projects/Student-Facial-Recognition/dlib_face_recognition_resnet_model_v1.dat')


def whirldata_face_detectors(img, number_of_times_to_upsample=1):
    return face_detector(img, number_of_times_to_upsample)


def whirldata_face_encodings(face_image, num_jitters=1):
    face_locations = whirldata_face_detectors(face_image)
    pose_predictor = pose_predictor_68_point
    predictors = [pose_predictor(face_image, face_location) for face_location in face_locations]
    return \
        [np.array(face_encoder.compute_face_descriptor(face_image, predictor, num_jitters)) for predictor in
         predictors][0]


def return_euclidean_distance(feature_1, feature_2):
    feature_1 = np.array(feature_1)
    feature_2 = np.array(feature_2)
    dist = np.sqrt(np.sum(np.square(feature_1 - feature_2)))
    return dist


path = "images/bassam2.jpg"
path2 = "images/adamu4.jpg"

# unknown_image = cv2.imread(path)
# enc1 = whirldata_face_encodings(unknown_image)
# image2 = cv2.imread(path2)
# enc2 = whirldata_face_encodings(image2)
#
# distance = return_euclidean_distance(enc1, enc2)
# print(distance)
# if distance < 0.5:
#     print("RECOGNIZED")
# else:
#     print("NOT RECOGNIZED")
