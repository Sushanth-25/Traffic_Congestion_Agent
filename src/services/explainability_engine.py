"""
Explainability Engine (XAI)
============================
Core component for generating explainable AI outputs.

This is what makes our solution UNIQUE - true XAI for traffic analysis!

Features:
- Confidence scoring with uncertainty quantification
- Factor attribution (SHAP-like breakdown)
- Evidence trail with source citations
- Human-readable explanation generation

Author: IBM Hackathon Team
Date: February 2026
"""

import json
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import math


@dataclass
class ConfidenceScore:
    """Represents a confidence score with breakdown."""
    overall: float  # 0-1
    components: Dict[str, float]
    uncertainties: List[str]
    reliability_grade: str  # A, B, C, D


@dataclass
class FactorAttribution:
    """SHAP-like factor attribution for explainability."""
    factor_name: str
    contribution_percentage: float
    direction: str  # "increases" or "decreases" congestion
    confidence: float
    evidence: str
    source: str


@dataclass
class EvidenceTrail:
    """Trail of evidence supporting the analysis."""
    sources: List[Dict[str, str]]
    data_points: List[Dict[str, Any]]
    reasoning_chain: List[str]


@dataclass
class ExplainableOutput:
    """Complete explainable output for traffic analysis."""
    summary: str  # 1-2 sentence summary
    detailed_explanation: str
    confidence: ConfidenceScore
    factor_attributions: List[FactorAttribution]
    evidence: EvidenceTrail
    recommendations: List[str]
    uncertainty_disclosure: str
    timestamp: str


class ExplainabilityEngine:
    """
    Engine for generating explainable AI outputs.

    This transforms raw analysis into transparent, trustworthy insights
    that traffic operators can understand and act upon.
    """

    def __init__(self):
        self.knowledge_sources = self._load_knowledge_sources()

    def _load_knowledge_sources(self) -> Dict[str, str]:
        """Load knowledge base sources for citation."""
        return {
            "traffic_classification": "Traffic Congestion Classification Guidelines, Section 2",
            "weather_impact": "Weather Impact on Traffic Congestion, Section 2-3",
            "time_patterns": "Time-Based Traffic Patterns Analysis, Section 1-2",
            "incident_management": "Incident Management Guidelines, Section 1-2",
            "bangalore_mobility": "Bangalore Urban Mobility Framework, Section 2",
            "highway_capacity": "Highway Capacity Manual (HCM) 2022, Chapter 4",
            "irc_standards": "Indian Road Congress (IRC) Standards, IRC:106-1990",
        }

    def generate_confidence_score(
        self,
        data_quality: float,
        source_reliability: float,
        pattern_match_strength: float,
        data_recency_hours: float = 0
    ) -> ConfidenceScore:
        """
        Generate a detailed confidence score with breakdown.

        This is critical for XAI - operators need to know HOW confident we are!
        """
        # Component weights
        weights = {
            "data_quality": 0.30,
            "source_reliability": 0.25,
            "pattern_match": 0.25,
            "data_recency": 0.20
        }

        # Calculate recency score (decays over time)
        recency_score = max(0.5, 1.0 - (data_recency_hours / 24) * 0.5)

        components = {
            "data_quality": data_quality,
            "source_reliability": source_reliability,
            "pattern_match": pattern_match_strength,
            "data_recency": recency_score
        }

        # Weighted average
        overall = sum(components[k] * weights[k] for k in weights)

        # Identify uncertainties
        uncertainties = []
        if data_quality < 0.7:
            uncertainties.append("Data quality below optimal threshold")
        if source_reliability < 0.8:
            uncertainties.append("Using simulated/cached data")
        if pattern_match_strength < 0.7:
            uncertainties.append("Unusual pattern detected - historical match weak")
        if recency_score < 0.8:
            uncertainties.append(f"Data is {data_recency_hours:.1f} hours old")

        # Reliability grade
        if overall >= 0.85:
            grade = "A"
        elif overall >= 0.70:
            grade = "B"
        elif overall >= 0.55:
            grade = "C"
        else:
            grade = "D"

        return ConfidenceScore(
            overall=round(overall, 2),
            components={k: round(v, 2) for k, v in components.items()},
            uncertainties=uncertainties,
            reliability_grade=grade
        )

    def generate_factor_attributions(
        self,
        factors: List[Dict[str, Any]]
    ) -> List[FactorAttribution]:
        """
        Generate SHAP-like factor attributions.

        This shows operators EXACTLY what's contributing to congestion.
        """
        attributions = []

        for factor in factors:
            attribution = FactorAttribution(
                factor_name=factor.get("factor", "Unknown"),
                contribution_percentage=factor.get("contribution_pct", 0),
                direction="increases",  # All factors here increase congestion
                confidence=factor.get("confidence", 0.7),
                evidence=factor.get("description", ""),
                source=factor.get("source", "Analysis Engine")
            )
            attributions.append(attribution)

        return attributions

    def build_evidence_trail(
        self,
        traffic_data: Dict[str, Any],
        weather_data: Dict[str, Any],
        time_context: Dict[str, Any],
        factors: List[Dict[str, Any]]
    ) -> EvidenceTrail:
        """
        Build a transparent evidence trail for the analysis.

        This is crucial for TRUST - operators can see exactly what data we used.
        """
        # Collect sources
        sources = [
            {
                "type": "Live Traffic Data",
                "source": traffic_data.get("data_source", "Traffic API"),
                "timestamp": traffic_data.get("timestamp", "N/A"),
                "reliability": "High" if "Live" in str(traffic_data.get("data_source", "")) else "Medium"
            },
            {
                "type": "Weather Data",
                "source": "OpenWeatherMap API",
                "timestamp": weather_data.get("timestamp", "N/A"),
                "reliability": "High"
            },
            {
                "type": "Historical Patterns",
                "source": "Bangalore Traffic Dataset (8,936 records)",
                "timestamp": "2022-2024 baseline",
                "reliability": "Medium"
            }
        ]

        # Add knowledge base sources
        for factor in factors:
            source_name = factor.get("source", "")
            if source_name and source_name not in [s["source"] for s in sources]:
                sources.append({
                    "type": "Knowledge Base",
                    "source": source_name,
                    "timestamp": "Static reference",
                    "reliability": "High"
                })

        # Data points used
        data_points = [
            {"metric": "Current Speed", "value": f"{traffic_data.get('current_speed', 'N/A')} km/h"},
            {"metric": "Congestion Level", "value": f"{traffic_data.get('congestion_level', 'N/A')}%"},
            {"metric": "Weather Condition", "value": weather_data.get("condition", "N/A")},
            {"metric": "Time Period", "value": time_context.get("period", "N/A")},
            {"metric": "Day Type", "value": "Weekend" if time_context.get("is_weekend") else "Weekday"},
        ]

        # Reasoning chain
        reasoning = [
            f"1. Retrieved live traffic data for {traffic_data.get('location', 'location')}",
            f"2. Current congestion level: {traffic_data.get('congestion_level', 'N/A')}% ({traffic_data.get('congestion_category', 'N/A')})",
            f"3. Weather impact assessed: {weather_data.get('weather_impact', 'None')} ({weather_data.get('condition', 'N/A')})",
            f"4. Time context: {time_context.get('period', 'N/A')} on {time_context.get('day_of_week', 'N/A')}",
            "5. Cross-referenced with historical patterns for this day/time",
            "6. Applied factor attribution analysis to identify causes",
            "7. Generated confidence score based on data quality and pattern match",
        ]

        return EvidenceTrail(
            sources=sources,
            data_points=data_points,
            reasoning_chain=reasoning
        )

    def generate_recommendations(
        self,
        congestion_level: float,
        factors: List[Dict[str, Any]],
        weather_condition: str
    ) -> List[str]:
        """Generate actionable recommendations based on analysis."""
        recommendations = []

        # Congestion-based recommendations
        if congestion_level >= 85:
            recommendations.append("🚨 URGENT: Activate congestion management protocols")
            recommendations.append("📢 Issue public advisory for alternate routes")
        elif congestion_level >= 60:
            recommendations.append("⚠️ Monitor closely - approaching critical levels")
            recommendations.append("Consider adjusting signal timing at major intersections")

        # Factor-specific recommendations
        for factor in factors:
            factor_name = factor.get("factor", "").lower()

            if "time" in factor_name and factor.get("contribution_pct", 0) > 25:
                recommendations.append("Peak hour mitigation: Stagger departure advisories")

            if "weather" in factor_name and factor.get("contribution_pct", 0) > 15:
                if "rain" in weather_condition.lower():
                    recommendations.append("Weather advisory: Reduce speed limits, increase headway")
                elif "fog" in weather_condition.lower():
                    recommendations.append("Fog protocol: Activate fog lights at signals, issue visibility warnings")

            if "incident" in factor_name:
                recommendations.append("Dispatch incident response team for faster clearance")
                recommendations.append("Activate alternate route signage")

        # Always include
        if not recommendations:
            recommendations.append("Continue routine monitoring")

        recommendations.append("Update status in 15 minutes for real-time tracking")

        return recommendations[:5]  # Max 5 recommendations

    def generate_uncertainty_disclosure(
        self,
        confidence: ConfidenceScore
    ) -> str:
        """
        Generate honest uncertainty disclosure.

        This is KEY for trust - acknowledge what we don't know!
        """
        if not confidence.uncertainties:
            return "✅ Analysis based on high-quality, real-time data with strong pattern match."

        disclosure = "⚠️ Uncertainty factors to consider:\n"
        for uncertainty in confidence.uncertainties:
            disclosure += f"  • {uncertainty}\n"

        if confidence.reliability_grade in ["C", "D"]:
            disclosure += "\n🔄 Recommend manual verification for critical decisions."

        return disclosure.strip()

    def generate_full_explanation(
        self,
        location: str,
        traffic_data: Dict[str, Any],
        weather_data: Dict[str, Any],
        time_context: Dict[str, Any],
        factors: List[Dict[str, Any]],
        historical_comparison: Dict[str, Any]
    ) -> ExplainableOutput:
        """
        Generate a complete explainable output.

        This is the MAIN method that creates the full XAI response!
        """
        # Generate confidence score
        data_quality = 0.85 if "Live" in str(traffic_data.get("data_source", "")) else 0.65
        source_reliability = traffic_data.get("confidence", 0.75)
        pattern_match = historical_comparison.get("pattern_confidence", 0.7)

        confidence = self.generate_confidence_score(
            data_quality=data_quality,
            source_reliability=source_reliability,
            pattern_match_strength=pattern_match,
            data_recency_hours=0  # Live data
        )

        # Generate factor attributions
        attributions = self.generate_factor_attributions(factors)

        # Build evidence trail
        evidence = self.build_evidence_trail(
            traffic_data, weather_data, time_context, factors
        )

        # Generate recommendations
        recommendations = self.generate_recommendations(
            traffic_data.get("congestion_level", 0),
            factors,
            weather_data.get("condition", "Clear")
        )

        # Generate uncertainty disclosure
        uncertainty = self.generate_uncertainty_disclosure(confidence)

        # Generate summary
        congestion_cat = traffic_data.get("congestion_category", "Moderate")
        primary_factor = factors[0]["factor"] if factors else "traffic volume"
        summary = (
            f"{location} is experiencing {congestion_cat.lower()} congestion "
            f"({traffic_data.get('congestion_level', 0):.0f}% capacity utilization). "
            f"Primary cause: {primary_factor.lower()}."
        )

        # Generate detailed explanation
        detailed = self._generate_detailed_explanation(
            location, traffic_data, weather_data, time_context,
            factors, historical_comparison
        )

        return ExplainableOutput(
            summary=summary,
            detailed_explanation=detailed,
            confidence=confidence,
            factor_attributions=attributions,
            evidence=evidence,
            recommendations=recommendations,
            uncertainty_disclosure=uncertainty,
            timestamp=datetime.now().isoformat()
        )

    def _generate_detailed_explanation(
        self,
        location: str,
        traffic_data: Dict[str, Any],
        weather_data: Dict[str, Any],
        time_context: Dict[str, Any],
        factors: List[Dict[str, Any]],
        historical_comparison: Dict[str, Any]
    ) -> str:
        """Generate detailed human-readable explanation."""

        explanation_parts = []

        # Current status
        explanation_parts.append(
            f"**Current Status**: {location} shows {traffic_data.get('congestion_category', 'moderate')} "
            f"congestion with vehicles moving at {traffic_data.get('current_speed', 'N/A')} km/h "
            f"(normal free-flow: {traffic_data.get('free_flow_speed', 'N/A')} km/h). "
            f"Travel time is {traffic_data.get('travel_time_ratio', 1):.1f}x normal."
        )

        # Time context
        if time_context.get("is_peak_hour"):
            explanation_parts.append(
                f"**Time Factor**: This is {time_context.get('period', 'peak hour')} on "
                f"{time_context.get('day_of_week', 'a weekday')}, which typically sees "
                f"{'high' if not time_context.get('is_weekend') else 'moderate'} commuter traffic. "
                f"According to our Time Patterns Analysis, this period accounts for the highest "
                f"traffic volumes of the day."
            )

        # Weather impact
        weather_impact = weather_data.get("weather_impact", "None")
        if weather_impact != "None":
            explanation_parts.append(
                f"**Weather Impact**: Current {weather_data.get('condition', 'weather')} conditions "
                f"are causing a {weather_impact.lower()} impact on traffic flow. "
                f"According to our Weather Impact Guidelines, this typically reduces "
                f"average speeds by {weather_data.get('impact_percentage', 0)}% due to "
                f"reduced visibility and road grip."
            )

        # Historical comparison
        hist_avg = historical_comparison.get("historical_avg_congestion", 75)
        current = traffic_data.get("congestion_level", 75)
        comparison = "higher" if current > hist_avg else "lower"
        diff = abs(current - hist_avg)

        explanation_parts.append(
            f"**Historical Context**: Current congestion ({current:.0f}%) is {diff:.0f}% "
            f"{comparison} than the typical {hist_avg:.0f}% average for this day and time. "
            f"This comparison is based on {historical_comparison.get('data_points', 'historical')} "
            f"records from our Bangalore traffic dataset."
        )

        # Factor breakdown
        if factors:
            factor_text = "**Contributing Factors**:\n"
            for i, factor in enumerate(factors[:4], 1):
                factor_text += (
                    f"{i}. **{factor.get('factor', 'Unknown')}** ({factor.get('contribution_pct', 0):.0f}% contribution): "
                    f"{factor.get('description', 'N/A')} "
                    f"[Source: {factor.get('source', 'Analysis Engine')}]\n"
                )
            explanation_parts.append(factor_text)

        return "\n\n".join(explanation_parts)

    def format_for_display(self, output: ExplainableOutput) -> str:
        """Format explainable output for display/API response."""

        # Factor visualization (text-based bar chart)
        factor_bars = ""
        for attr in output.factor_attributions[:4]:
            bar_length = int(attr.contribution_percentage / 5)
            bar = "█" * bar_length + "░" * (20 - bar_length)
            factor_bars += f"  {attr.factor_name:<20} [{bar}] {attr.contribution_percentage:.0f}%\n"

        # Sources list
        sources_text = "\n".join([
            f"  • [{s['type']}] {s['source']} ({s['reliability']} reliability)"
            for s in output.evidence.sources[:5]
        ])

        # Recommendations
        recs_text = "\n".join([f"  {r}" for r in output.recommendations])

        return f"""
═══════════════════════════════════════════════════════════════════
                    EXPLAINABLE TRAFFIC ANALYSIS
═══════════════════════════════════════════════════════════════════

📍 SUMMARY
{output.summary}

📊 CONFIDENCE SCORE: {output.confidence.overall * 100:.0f}% (Grade: {output.confidence.reliability_grade})
  ├─ Data Quality: {output.confidence.components.get('data_quality', 0) * 100:.0f}%
  ├─ Source Reliability: {output.confidence.components.get('source_reliability', 0) * 100:.0f}%
  ├─ Pattern Match: {output.confidence.components.get('pattern_match', 0) * 100:.0f}%
  └─ Data Recency: {output.confidence.components.get('data_recency', 0) * 100:.0f}%

🔍 FACTOR ATTRIBUTION (Why is this happening?):
{factor_bars}
📚 EVIDENCE & SOURCES:
{sources_text}

💡 RECOMMENDATIONS:
{recs_text}

⚠️ UNCERTAINTY DISCLOSURE:
{output.uncertainty_disclosure}

───────────────────────────────────────────────────────────────────
Generated: {output.timestamp}
═══════════════════════════════════════════════════════════════════
"""


# ==================== INTEGRATION WITH LANGFLOW ====================

def create_xai_response(combined_insight) -> Dict[str, Any]:
    """
    Create an XAI response from a CombinedTrafficInsight object.
    This is what LangFlow will call!
    """
    engine = ExplainabilityEngine()

    # Convert dataclasses to dicts for the engine
    traffic_dict = asdict(combined_insight.traffic) if hasattr(combined_insight.traffic, '__dataclass_fields__') else combined_insight.traffic
    weather_dict = asdict(combined_insight.weather) if hasattr(combined_insight.weather, '__dataclass_fields__') else combined_insight.weather

    explanation = engine.generate_full_explanation(
        location=combined_insight.location,
        traffic_data=traffic_dict,
        weather_data=weather_dict,
        time_context=combined_insight.time_context,
        factors=combined_insight.contributing_factors,
        historical_comparison=combined_insight.historical_comparison
    )

    # Format for display
    formatted = engine.format_for_display(explanation)

    # Also return structured data for frontend visualization
    return {
        "formatted_text": formatted,
        "structured": {
            "summary": explanation.summary,
            "confidence": asdict(explanation.confidence),
            "factors": [asdict(f) for f in explanation.factor_attributions],
            "recommendations": explanation.recommendations,
            "uncertainty": explanation.uncertainty_disclosure
        }
    }


# ==================== TEST ====================

if __name__ == "__main__":
    print("🔬 Testing Explainability Engine...")
    print("=" * 60)

    engine = ExplainabilityEngine()

    # Mock data
    traffic_data = {
        "location": "Koramangala",
        "current_speed": 18.5,
        "free_flow_speed": 45.0,
        "congestion_level": 85.2,
        "congestion_category": "Severe",
        "travel_time_ratio": 2.4,
        "data_source": "TomTom Live API",
        "confidence": 0.92,
        "incidents_nearby": 1,
        "timestamp": datetime.now().isoformat()
    }

    weather_data = {
        "condition": "Light Rain",
        "temperature": 24.5,
        "weather_impact": "Moderate",
        "impact_percentage": 20,
        "timestamp": datetime.now().isoformat()
    }

    time_context = {
        "current_time": "18:30",
        "day_of_week": "Tuesday",
        "is_weekend": False,
        "period": "Evening Peak",
        "is_peak_hour": True
    }

    factors = [
        {
            "factor": "Time Pattern",
            "description": "Evening Peak on Tuesday",
            "impact": "High",
            "contribution_pct": 35,
            "confidence": 0.95,
            "source": "Time Pattern Analysis Guidelines"
        },
        {
            "factor": "Weather Conditions",
            "description": "Light Rain - Moderate impact",
            "impact": "Medium",
            "contribution_pct": 25,
            "confidence": 0.88,
            "source": "Weather Impact Guidelines"
        },
        {
            "factor": "Traffic Volume",
            "description": "High capacity utilization at 85%",
            "impact": "High",
            "contribution_pct": 30,
            "confidence": 0.92,
            "source": "Traffic Congestion Classification"
        },
        {
            "factor": "Active Incident",
            "description": "1 incident reported nearby",
            "impact": "Medium",
            "contribution_pct": 10,
            "confidence": 0.80,
            "source": "Incident Management Guidelines"
        }
    ]

    historical = {
        "historical_avg_congestion": 78.5,
        "typical_conditions": "Heavy",
        "data_points": 1364,
        "pattern_confidence": 0.85
    }

    # Generate full explanation
    output = engine.generate_full_explanation(
        location="Koramangala",
        traffic_data=traffic_data,
        weather_data=weather_data,
        time_context=time_context,
        factors=factors,
        historical_comparison=historical
    )

    # Display formatted output
    print(engine.format_for_display(output))

    print("\n✅ Explainability Engine test complete!")

