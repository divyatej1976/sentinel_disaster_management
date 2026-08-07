RISK_LEVEL_PLAIN_LANGUAGE = {
    "Low": "The current risk in this area is low. Continue normal precautions.",
    "Medium": "The current risk in this area is elevated. Stay alert and follow guidance from local health authorities.",
    "High": "The current risk in this area is high. Local health authorities recommend increased precautions.",
}

def run(hazard, risk: dict, resources: dict, knowledge: dict | None, template: str) -> dict:
    # Gather context from the hazard module
    context = hazard.report_context(risk, resources, knowledge)
    
    report = {
        "template_used": template,
        "hazard_title": context.get("hazard_title", "Unknown Hazard"),
        "hazard_context": context.get("hazard_context", ""),
    }

    if template == "officer":
        # Full detail
        report["risk_level"] = risk.get("risk_level")
        report["confidence_score"] = risk.get("confidence_score")
        report["reasoning"] = risk.get("reasoning", [])
        report["top_risk_drivers"] = risk.get("top_risk_drivers", [])
        report["mitigation_strategies"] = risk.get("mitigation_strategies", [])
        report["resources"] = resources
        
        # Knowledge citations
        if knowledge and "citations" in knowledge:
            report["citations"] = knowledge["citations"]
        else:
            report["citations"] = []
            
    elif template == "citizen":
        # Plain-language summary
        report["risk_level"] = risk.get("risk_level")
        report["confidence_score"] = risk.get("confidence_score")
        
        # Use deterministic plain-language mapping based on risk level
        report["summary"] = RISK_LEVEL_PLAIN_LANGUAGE.get(
            risk.get("risk_level"), 
            "Risk level is unknown. Please stand by for updates."
        )
            
    elif template == "executive":
        # Condensed
        report["risk_level"] = risk.get("risk_level")
        report["confidence_score"] = risk.get("confidence_score")
        
        # Rough magnitude indicator rather than summing mismatched units
        report["resource_scale_index"] = sum(resources.values()) if resources else 0
        
        # Top 1-2 mitigation strategies
        mitigations = risk.get("mitigation_strategies", [])
        report["key_mitigations"] = mitigations[:2]
        
    else:
        raise ValueError(f"Unknown template: {template}")
        
    return report
