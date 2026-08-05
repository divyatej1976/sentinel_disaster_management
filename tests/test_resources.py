import pytest
from server.hazards.disease import DiseaseHazard

def test_exact_values_clean_division():
    """Test exact resource values for populations that cleanly divide by 100k."""
    hazard = DiseaseHazard()
    population = 200000  # Factor = 2.0
    
    # Low Risk
    low_res = hazard.resource_formulas("Low", population)
    assert low_res["ambulances"] == 2
    assert low_res["isolation_beds"] == 20
    assert low_res["ppe_kits"] == 100
    assert low_res["medical_staff"] == 10

    # Medium Risk
    med_res = hazard.resource_formulas("Medium", population)
    assert med_res["ambulances"] == 6
    assert med_res["isolation_beds"] == 60
    assert med_res["ppe_kits"] == 300
    assert med_res["medical_staff"] == 30

    # High Risk
    high_res = hazard.resource_formulas("High", population)
    assert high_res["ambulances"] == 20
    assert high_res["isolation_beds"] == 200
    assert high_res["ppe_kits"] == 1000
    assert high_res["medical_staff"] == 100

def test_rounding_behavior_ceiling():
    """Test that fractional resource allocations round UP to nearest integer."""
    hazard = DiseaseHazard()
    population = 150000  # Factor = 1.5
    
    med_res = hazard.resource_formulas("Medium", population)
    # Expected: 3 * 1.5 = 4.5 -> ceil(4.5) = 5
    assert med_res["ambulances"] == 5
    # Expected: 30 * 1.5 = 45 -> ceil(45) = 45
    assert med_res["isolation_beds"] == 45
    # Expected: 150 * 1.5 = 225 -> ceil(225) = 225
    assert med_res["ppe_kits"] == 225
    # Expected: 15 * 1.5 = 22.5 -> ceil(22.5) = 23
    assert med_res["medical_staff"] == 23

def test_unknown_risk_level_raises():
    """Test that an unknown risk level raises a explicit ValueError."""
    hazard = DiseaseHazard()
    with pytest.raises(ValueError, match="Invalid risk_level 'Critical'"):
        hazard.resource_formulas("Critical", 100000)
        
    with pytest.raises(ValueError):
        hazard.resource_formulas("Unknown", 100000)

def test_zero_population():
    """Test that zero population returns all zeros rather than crashing."""
    hazard = DiseaseHazard()
    population = 0
    
    res = hazard.resource_formulas("High", population)
    assert res["ambulances"] == 0
    assert res["isolation_beds"] == 0
    assert res["ppe_kits"] == 0
    assert res["medical_staff"] == 0
