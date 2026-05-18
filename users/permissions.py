def is_admin(user):
    return user.profile.role == 'admin'

def is_instructor(user):
    return user.profile.role == 'instructor'

def is_student(user):
    return user.profile.role == 'student'