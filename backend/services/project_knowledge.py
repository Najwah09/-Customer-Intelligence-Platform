"""
Centralized Project Knowledge & System Context Service for RETAINAI Platform.

Provides maintainable project-level intelligence, page maps, analytics engine metadata,
dataset stats, and dynamic system state for the Gemini AI assistant.
"""

from typing import Any, Dict, List, Optional

from backend.core.settings import Settings

settings = Settings()

PAGES_CATALOG = {
    "Home": {
        "title": "Home / Executive Summary",
        "route": "1_Executive_Summary.py",
        "purpose": "High-level strategic executive summary dashboard displaying total active subscriber portfolio count, revenue exposure at risk, overall churn probability, and key portfolio alerts.",
        "capabilities": [
            "Total Active Subscribers",
            "Portfolio Average Churn Risk",
            "Total LTV at Risk",
            "High-Risk Account Count",
        ],
    },
    "Customers": {
        "title": "Customers Directory & Customer 360",
        "route": "2_Customers.py",
        "purpose": "Individual subscriber directory and Customer 360 profiles. Search by Account ID (e.g. 10482 or 0003-MKNFE) to view churn risk, tenure, monthly charges, contract type, and individual SHAP risk drivers.",
        "capabilities": [
            "Account Lookup",
            "Individual Risk Score",
            "Customer 360 Profile View",
        ],
    },
    "Segments": {
        "title": "Cohort Segmentation",
        "route": "3_Segments.py",
        "purpose": "K-Means cohort segmentation dashboard. Groups subscribers into 3 clusters (High-Value, Loyal, Budget) to analyze retention opportunities by customer tier.",
        "capabilities": [
            "Cluster Count",
            "Highest-Risk Segment",
            "Segment Churn Rates",
        ],
    },
    "LTV": {
        "title": "Lifetime Value Engine",
        "route": "4_LTV.py",
        "purpose": "Customer Lifetime Value (LTV) regression engine. Predicts remaining financial value of each account and quantifies total probability-weighted revenue exposure.",
        "capabilities": [
            "Average Portfolio LTV",
            "Total LTV at Risk",
            "LTV Distribution",
        ],
    },
    "Churn": {
        "title": "Churn Drivers & Analytics",
        "route": "5_Churn.py",
        "purpose": "Portfolio-wide attrition driver analysis and LightGBM classifier breakdown. Explains dataset-wide feature attributions and contract-level attrition trends.",
        "capabilities": [
            "LightGBM ROC-AUC (0.847)",
            "Top Global SHAP Drivers",
            "Contract Type Risk Rates",
        ],
    },
    "Recommendations": {
        "title": "Retention Recommendations",
        "route": "6_Recommendations.py",
        "purpose": "Automated AI retention action plans and customer service message scripts tailored for high-risk accounts.",
        "capabilities": [
            "Action Priority",
            "Recommended Intervention",
            "Script Template",
        ],
    },
    "Batch Analysis": {
        "title": "Batch Scoring Pipeline",
        "route": "7_Batch_Analysis.py",
        "purpose": "Bulk CSV batch prediction pipeline for scoring thousands of customer records at scale.",
        "capabilities": ["Batch Processing Status", "Scored Row Count", "CSV Export"],
    },
    "Reports": {
        "title": "Business Reports",
        "route": "8_Reports.py",
        "purpose": "Exportable executive PDF/CSV business intelligence reports and audit summaries.",
        "capabilities": ["Daily Executive Summary", "Drift Report", "Export CSV"],
    },
    "Operations": {
        "title": "System Operations & Health",
        "route": "9_Operations.py",
        "purpose": "Enterprise MLOps & system health dashboard. Monitors FastAPI status, database connections, model registry versions, and APScheduler PSI feature drift monitoring.",
        "capabilities": [
            "System Health",
            "Model Registry Versions",
            "PSI Feature Drift (0.10/0.25)",
        ],
    },
    "Deployment": {
        "title": "Model Deployment Manager",
        "route": "10_Deployment.py",
        "purpose": "Model deployment manager supporting blue/green staging, active production model promotion, and rollbacks.",
        "capabilities": [
            "Active Production Model",
            "Version Promotion",
            "Rollback Control",
        ],
    },
    "AI Retention Agent": {
        "title": "AI Retention Assistant",
        "route": "12_AI_Retention_Agent.py",
        "purpose": "Natural language conversational intelligence interface powered by Gemini and data-grounded AI tools.",
        "capabilities": [
            "Conversational Chat",
            "Grounded Data Tools",
            "Multi-Turn Memory",
        ],
    },
    "What-If Simulator": {
        "title": "What-If Sensitivity Simulator",
        "route": "13_What_If_Simulator.py",
        "purpose": "Interactive model sensitivity simulator. Models BEFORE vs AFTER impact of contract changes, discounts, and service upgrades on churn risk and LTV.",
        "capabilities": [
            "Before vs After Churn Prob",
            "Potential Value Saved",
            "Relative Risk Reduction %",
        ],
    },
    "Retention ROI Optimizer": {
        "title": "Retention ROI Optimizer",
        "route": "14_Retention_ROI_Optimizer.py",
        "purpose": "Financial optimizer ranking retention campaigns (discount, contract lock, VIP perk, service credit) by net financial ROI.",
        "capabilities": ["Ranked Campaigns", "Strategy Cost", "Expected ROI %"],
    },
}


class ProjectKnowledgeService:
    """Centralized project context provider."""

    def get_app_info(self) -> Dict[str, Any]:
        return {
            "name": "RETAINAI",
            "title": "AI-Powered Customer Retention & Lifetime Value Intelligence Platform",
            "version": settings.APP_VERSION,
            "environment": settings.ENV,
            "tech_stack": "Python 3.12, FastAPI, Streamlit, PostgreSQL, LightGBM, SHAP, K-Means, Google Gemini API, Ollama",
        }

    def get_pages_catalog(self) -> Dict[str, Any]:
        return PAGES_CATALOG

    def get_page_info(self, page_name: str) -> Dict[str, Any]:
        for key, info in PAGES_CATALOG.items():
            if key.lower() in page_name.lower() or page_name.lower() in key.lower():
                return info
        return PAGES_CATALOG["AI Retention Agent"]

    def get_analytics_metadata(self) -> Dict[str, Any]:
        return {
            "churn_model": {
                "algorithm": "LightGBM Classifier",
                "roc_auc": 0.847,
                "optimal_threshold": 0.61,
                "version": "v1.0.0",
            },
            "ltv_model": {
                "algorithm": "LightGBM Regressor",
                "metrics": "RMSE: 312.4, MAE: 245.1",
                "version": "v1.0.0",
            },
            "segmentation_model": {
                "algorithm": "K-Means Clustering",
                "clusters": 3,
                "segments": [
                    "High-Value Subscribers",
                    "Loyal Subscribers",
                    "Budget Subscribers",
                ],
            },
            "explainability": "SHAP (TreeExplainer) Feature Attribution",
            "ops": "APScheduler PSI Feature Drift Monitoring (0.10 Warning, 0.25 Critical)",
        }


project_knowledge = ProjectKnowledgeService()
