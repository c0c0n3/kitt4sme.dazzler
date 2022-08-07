from datetime import datetime
from typing import Dict, List, Tuple

import pandas as pd

from dazzler.dash.board.viqe import ReportFrame


def mk_entity_series_row(time_index_iso: str,
                         conformance_indicator: float,
                         okay: bool) -> dict:
    return {
        'index': datetime.fromisoformat(time_index_iso),
        'conformance_indicator': conformance_indicator,
        'okay': okay
    }


EntitySeriesRow = Tuple[str, float, bool]


def mk_entity_series_frame(rows: List[EntitySeriesRow]) -> pd.DataFrame:
    rs = [mk_entity_series_row(*t) for t in rows]
    return pd.DataFrame(rs)


def mk_raw_material_entity_type_series() -> Dict[str, pd.DataFrame]:
    return {
        'steel-slab:1': mk_entity_series_frame([
            ('2022-08-06 17:42:37.524000+00:00', 0.2, True),
            ('2022-08-06 17:42:44.493000+00:00', 0.3, True)
        ]),
        'steel-slab:2': mk_entity_series_frame([
            ('2022-08-06 17:42:37.528000+00:00', 1.0, False),
            ('2022-08-06 17:42:44.496000+00:00', 0.9, False)
        ]),
        'steel-slab:3': mk_entity_series_frame([
            ('2022-08-06 17:42:37.529000+00:00', 0.0, True),
            ('2022-08-06 17:42:44.496000+00:00', 0.1, True)
        ])
    }


def test_raw_material_report_from_entity_type_series():
    ql_data = mk_raw_material_entity_type_series()
    report_frame = ReportFrame(ql_data).build()

    assert len(report_frame.index) == 3

    id_values = report_frame['id'].tolist()
    conformance_values = report_frame['conformance'].tolist()
    scrap_values = report_frame['scrap'].tolist()

    assert id_values == ['steel-slab:1', 'steel-slab:2', 'steel-slab:3']
    assert conformance_values == [0.3, 0.9, 0.1]
    assert scrap_values == [False, True, False]
