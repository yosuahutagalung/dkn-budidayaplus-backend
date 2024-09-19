from ninja import Router

router = Router()

@router.post("/fish-sampling")
def create_fish_sampling(request):
    return

@router.get("/fish-sampling")
def list_fish_sampling(request):
    return 

@router.put("/fish-sampling/{sample_id}")
def update_fish_sampling(request):
    return

@router.delete("/fish-sampling/{sample_id}")
def delete_fish_sampling(request):
    return