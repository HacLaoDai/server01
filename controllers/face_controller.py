from fastapi import APIRouter, Depends, HTTPException
from models.face_model import SetFaceRequest
from services.face_service import set_face_service
from controllers.auth_controller import get_current_user

router = APIRouter(prefix="/api/internal", tags=["Face"])

@router.post("/set-face")
def set_face(req: SetFaceRequest, user=Depends(get_current_user)):
    try:
        return {
            "result": "success",
            "data": set_face_service(req)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
