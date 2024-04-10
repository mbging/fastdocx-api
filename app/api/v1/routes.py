from fastapi import APIRouter

from app.api.v1.endpoints.render import router as render_router

routers = APIRouter()
router_list = [render_router]

for router in router_list:
    # router.tags = routers.tags.append("v1")
    routers.include_router(router)
