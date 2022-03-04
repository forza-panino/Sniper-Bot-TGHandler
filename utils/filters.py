from telegram.ext import Filters
from ..config import ADMIN_ID

admin_filter = Filters.user(user_id=ADMIN_ID)
allowed_users_filter = Filters.user(user_id=ADMIN_ID)
