"""Components package initialization."""
try:
    from components.header import render_header
    from components.sidebar import render_sidebar
    from components.metric_cards import render_kpi_card
    from components.charts import (
        create_data_funnel_chart,
        create_temporal_trajectory_chart,
        create_platform_distribution_chart,
        create_distribution_pie_or_bar,
        create_entity_frequency_chart,
    )
    from components.tables import render_interactive_table
    from components.filters import render_post_filters
    from components.findings import render_finding_card, render_limitation_callout
    from components.theme import apply_custom_theme, render_vortex_graphic
except ImportError:
    from .header import render_header
    from .sidebar import render_sidebar
    from .metric_cards import render_kpi_card
    from .charts import (
        create_data_funnel_chart,
        create_temporal_trajectory_chart,
        create_platform_distribution_chart,
        create_distribution_pie_or_bar,
        create_entity_frequency_chart,
    )
    from .tables import render_interactive_table
    from .filters import render_post_filters
    from .findings import render_finding_card, render_limitation_callout
    from .theme import apply_custom_theme, render_vortex_graphic
