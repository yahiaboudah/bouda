def recognize_face(p):
    import face_recognition as f
    return f.face_locations(f.load_image_file(p))
