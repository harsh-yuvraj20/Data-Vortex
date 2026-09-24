"""Services package initialization."""
try:
    from services.data_service import DataService
    from services.round1_service import Round1Service
    from services.nlp_service import NLPService
    from services.round3_service import Round3Service
    from services.insight_service import InsightService
except ImportError:
    from .data_service import DataService
    from .round1_service import Round1Service
    from .nlp_service import NLPService
    from .round3_service import Round3Service
    from .insight_service import InsightService
