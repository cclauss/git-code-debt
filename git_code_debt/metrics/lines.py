from __future__ import absolute_import
from __future__ import unicode_literals

import collections

from identify import identify

from git_code_debt.metric import Metric
from git_code_debt.metrics.base import DiffParserBase
from git_code_debt.metrics.base import MetricInfo
from git_code_debt.metrics.common import ALL_TAGS
from git_code_debt.metrics.common import UNKNOWN


class LinesOfCodeParser(DiffParserBase):
    """Counts lines of code in a repository, overall and by file types."""

    def get_metrics_from_stat(self, _, file_diff_stats):
        total_lines = 0
        lines_by_file_type = collections.defaultdict(int)

        for file_diff_stat in file_diff_stats:
            lines_changed = (
                len(file_diff_stat.lines_added) -
                len(file_diff_stat.lines_removed)
            )

            # Track total overall
            total_lines += lines_changed

            filename = file_diff_stat.filename.decode('UTF-8')
            tags = identify.tags_from_filename(filename) or {UNKNOWN}

            for tag in tags:
                lines_by_file_type[tag] += lines_changed

        # Yield overall metric and one per type of expected mapping types
        yield Metric('TotalLinesOfCode', total_lines)
        for tag, val in lines_by_file_type.items():
            if tag in ALL_TAGS and val:
                yield Metric('TotalLinesOfCode_{}'.format(tag), val)

    def get_metrics_info(self):
        metric_names = ['TotalLinesOfCode_{}'.format(tag) for tag in ALL_TAGS]
        metric_names.append('TotalLinesOfCode')
        return [MetricInfo(metric_name) for metric_name in metric_names]
