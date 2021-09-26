
import face_recognition as f

def recognize_face(p): f.face_locations(f.load_image_file(p)) 
