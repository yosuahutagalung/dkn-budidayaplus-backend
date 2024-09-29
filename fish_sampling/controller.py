from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import FishSampling
from pond.models import Pond
from .schemas import FishSamplingCreateSchema, FishSamplingEditSchema
from ninja_jwt.authentication import JWTAuth
from ninja_extra import route, api_controller

@api_controller("/fish-sampling", tags=["Fish Sampling"], permissions=[])
class FishSamplingController:

    @route.post("/", auth=JWTAuth())
    def create_fish_sampling(self, request, payload: FishSamplingCreateSchema):
        pond = get_object_or_404(Pond, pond_id=payload.pond_id)
        reporter = get_object_or_404(User, id=request.auth.id)
        fish_sampling = FishSampling.objects.create(
            pond=pond,
            reporter=reporter,
            fish_weight=payload.fish_weight,
            fish_length=payload.fish_length,
            sample_date=payload.sample_date
        )
        return {"id": str(fish_sampling.sampling_id), "reporter": str(fish_sampling.reporter)}

    @route.get("/{sampling_id}/", auth=JWTAuth())
    def get_fish_sampling(self, sampling_id: str):
        fish_sampling = get_object_or_404(FishSampling, sampling_id=sampling_id)
        return {"id": str(fish_sampling.sampling_id), "reporter": str(fish_sampling.reporter)}

    @route.get("/", auth=JWTAuth())
    def list_fish_samplings(self, request):
        user = request.auth
        fish_samplings = FishSampling.objects.filter(reporter=user)
        return [{"id": str(fish_sampling.sampling_id), "reporter": str(fish_sampling.reporter)} for fish_sampling in fish_samplings]

    @route.put("/{sampling_id}/", auth=JWTAuth())
    def update_fish_sampling(self, sampling_id: str, payload: FishSamplingEditSchema):
        fish_sampling = get_object_or_404(FishSampling, sampling_id=sampling_id)
        pond = get_object_or_404(Pond, pond_id=payload.pond_id)
        reporter = get_object_or_404(User, id=payload.reporter_id)
        fish_sampling.pond = pond
        fish_sampling.reporter = reporter
        fish_sampling.fish_weight = payload.fish_weight
        fish_sampling.fish_length = payload.fish_length
        fish_sampling.sample_date = payload.sample_date
        fish_sampling.save()
        return {"id": str(fish_sampling.sampling_id), "reporter": str(fish_sampling.reporter)}

    @route.delete("/{sampling_id}/", auth=JWTAuth())
    def delete_fish_sampling(self, sampling_id: str):
        fish_sampling = get_object_or_404(FishSampling, sampling_id=sampling_id)
        fish_sampling.delete()
        return {"success": True}