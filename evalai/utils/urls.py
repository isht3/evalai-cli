from enum import Enum

class Urls(Enum):
    challenge_list = "/api/challenges/challenge/all"
    past_challenge_list = "/api/challenges/challenge/past"
    future_challenge_list = "/api/challenges/challenge/future"
    phase_list = "/api/challenges/challenge/{}/challenge_phase"
    phase_details = "/api/challenges/challenge/{}/challenge_phase/{}"