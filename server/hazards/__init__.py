from .disease import DiseaseHazard
from .flood import FloodHazard

HAZARDS = {
    "disease": DiseaseHazard(),
    "flood": FloodHazard(),
}
