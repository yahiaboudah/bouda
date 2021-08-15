def recognize_face(pp):
    import face_recognition as ff
    image = ff.load_image_file(pp)
    face_locations = ff.face_locations(image)
    return face_locations