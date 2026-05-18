from ninja import Router
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .schema import RegisterSchema, LoginSchema
from .auth import create_token, AuthBearer

router = Router()

# =====================
# REGISTER
# =====================
@router.post("/register")
def register(request, data: RegisterSchema):
    User.objects.create_user(
        username=data.username,
        password=data.password
    )
    return {"message": "User created"}


# =====================
# LOGIN
# =====================
@router.post("/login")
def login(request, data: LoginSchema):
    user = authenticate(username=data.username, password=data.password)

    if not user:
        return {"error": "Invalid credentials"}

    token = create_token({"user_id": user.id})

    return {"access_token": token}


# =====================
# GET CURRENT USER
# =====================
@router.get("/me", auth=AuthBearer())
def get_me(request):
    user = request.auth
    return {
        "id": user.id,
        "username": user.username
    }