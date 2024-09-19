from ninja import Router

router = Router()

@router.post("/ponds/")
def add_pond(request):
    return

@router.get("/ponds/{pond_id}/")
def get_pond(request):
    return

@router.get("/ponds/")
def list_ponds(request):
    return

@router.delete("/ponds/{pond_id}/")
def delete_pond(request, pond_id: str):
    return

@router.put("/ponds/{pond_id}/")
def update_pond(request, pond_id: str):
    return