import db.crud.admins as crud_admins
from db.models import Admin
from config import MAIN_ADMIN


async def create_default_db():
    if await crud_admins.read_admin(MAIN_ADMIN):
        return "botva"
    admin = Admin(
        peer_id=MAIN_ADMIN
    )
    await crud_admins.create_admin(admin)
    print("DONE")
