from ninja import NinjaAPI
from users.api import router as auth_router
from courses.api import router as course_router   # ⬅️ ini WAJIB

api = NinjaAPI()

api.add_router("/auth/", auth_router)
api.add_router("/courses/", course_router)  # ⬅️ ini WAJIB