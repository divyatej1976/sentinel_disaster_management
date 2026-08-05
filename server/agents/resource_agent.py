def run(hazard, risk_level: str, population: int) -> dict:
    """
    Generic Resource Agent wrapper.
    Delegates hazard-specific formula logic back to the hazard module.
    """
    return hazard.resource_formulas(risk_level, population)
