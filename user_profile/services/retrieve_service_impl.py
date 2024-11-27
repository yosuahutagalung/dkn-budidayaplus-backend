from user_profile.models import UserProfile, Worker, Supervisor
from user_profile.services.retrieve_service import RetrieveService
from user_profile.schemas import WorkerSchema

class RetrieveServiceImpl(RetrieveService):
    @staticmethod
    def retrieve_profile(username): 
        return UserProfile.objects.get(user__username=username)

    @staticmethod
    def retrieve_profile_by_user(user):
        return UserProfile.objects.get(user=user)
    
    @staticmethod
    def get_workers(user):
        supervisor_profile = UserProfile.objects.get(user=user)
        try:
            supervisor = Supervisor.objects.get(user_profile=supervisor_profile)
        except Supervisor.DoesNotExist:
            raise ValueError("Non-supervisor tidak dapat akses ini")
        
        workers = Worker.objects.filter(supervisor=supervisor)

        ans = []
        for worker in workers:
            ans.append(WorkerSchema(
                id=worker.id,
                first_name=worker.user_profile.user.first_name,
                last_name=worker.user_profile.user.last_name,
            ))

        return ans
    
