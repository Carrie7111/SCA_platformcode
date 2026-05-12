import math
import os
import traceback
from collections import OrderedDict
from typing import List, Dict, Any, Optional


class ModuleDesc:
    def __init__(self, pkg_name, name, desc, is_visible):
        self.pkg_name = pkg_name
        self.name = name
        self.desc = desc
        self.is_visible = is_visible


class Module:
    def __init__(self):
        self.module_description = ""
        self.module_version = ""
        self.help_file = ""
        self.config: Dict[str, Any] = {}

    def set_config(self, key: str, value: Any):
        self.config[key] = value

    def get_config(self, key: str) -> Any:
        return self.config.get(key)


class Trace:
    def __init__(self, title="", data=None, samples=None):
        self.title = title
        self.data = data
        self.samples = samples if samples is not None else []

    def get_number_of_samples(self) -> int:
        return len(self.samples)

    def get_sample(self, index: int = None):
        if index is None:
            return self.samples
        return self.samples[index]

    def get_sample_data(self):
        return self.samples


class TraceSet:
    def __init__(self, path):
        self.path = path
        self.traces: List[Trace] = []

    def get_number_of_samples(self) -> int:
        return self.traces[0].get_number_of_samples() if self.traces else 0

    def get_trace(self, idx: int) -> Trace:
        return self.traces[idx]

    def close(self):
        pass


class DataOperationException(Exception):
    pass


class PathFinder:
    def __init__(self, sample=None, step_min=0, step_max=0):
        self.sample = sample if sample is not None else []
        self.step_min = step_min
        self.step_max = step_max
        self.winning_path = None
        self.path = None
        self.calls = 0
        self.end = 0
        self.best = 0.0
        self.verbose = False
        self.report = False
        self.aborted = False

    def search_path(self, begin, sum_val, index):
        self.calls += 1
        section = self.end - begin
        range_step = self.step_max - self.step_min
        mod = section % self.step_min
        div_val = section // self.step_min

        if div_val * range_step < mod:
            return 0.0
        if sum_val + (div_val - 1) < self.best:
            return 0.0

        if self.step_min <= section <= self.step_max:
            self.winning_path = self.path[:index]
            return sum_val

        for i in range(range_step + 1):
            if self.aborted:
                break
            j = begin + self.step_min + i
            self.path[index] = j
            v = self.search_path(j, sum_val + self.sample[j], index + 1)
            if v > self.best:
                self.best = v
        return self.best

    def find_path(self, begin, end, threshold):
        self.calls = 0
        self.end = end
        self.best = 0.0
        max_depth = (end - begin) // self.step_min + 1
        self.path = [0] * max_depth
        self.winning_path = None
        self.search_path(begin, 0.0, 0)

        if self.winning_path and len(self.winning_path) > 0:
            avg = self.best / len(self.winning_path)
            if avg < threshold:
                return None
        return self.winning_path

    def get_correlation_sum(self):
        return self.best


module_desc = ModuleDesc(
    pkg_name="Resample",
    name="PatternResample",
    desc="",
    is_visible=False
)


class PatternResample(Module):
    THRESHOLD = "threshold"
    BOUNDARY_THRESHOLD = "boundary.threshold"
    ACTION = "action"
    ALIGN = "align"
    COMPRESSION_START = "compression.start"
    COMPRESSION_END = "compression.end"
    DISTANCE_MINIMAL = "distance.minimal"
    DISTANCE_MAXIMAL = "distance.maximal"
    PATTERN = "pattern"
    PATTERN_FILE_PATH = "pattern.file.path"
    AREA_SELECTION_METHOD = "area.selection.method"
    DETECTION_METHOD = "detection.method"
    BEGIN_INDEX = "begin.index"
    END_INDEX = "end.index"

    CORRELATE = 0
    FILTER = 1
    LEFT = 0
    RIGHT = 1
    DETECT_THRESHOLD = 0
    DETECT_PATH = 1
    MAX_HARMONICS = 10
    MAX_DEPTH = 10

    def __init__(self):
        super().__init__()
        self.pattern: List[float] = []
        self.sy = []
        self.s2y = []
        self.first = []
        self.s_pattern = 0.0
        self.s2_pattern = 0.0
        self.threshold = 0.0
        self.average_distance = 0.0
        self.average_spectrum = []
        self.fft_correlation_size = 0
        self.fft_spectrum_size = 0
        self.pattern_start = 0
        self.pattern_length = 0
        self.selection_start = 0
        self.selection_end = 0
        self.action = self.CORRELATE
        self.detection_method = self.DETECT_PATH
        self.recent_trace_index = 0
        self.total_number_of_result_traces = 0
        self.patterns = 0
        self.align = self.LEFT
        self.ns = 0
        self.begin_index = 0
        self.end_index = 0
        self.min_distance = 0
        self.max_distance = 0
        self.begin_compression = 0
        self.end_compression = 0
        self.pattern_file_path = ""
        self.aborted = False

    def init_module(self):
        self.module_description = "Resample traces based upon correlation with a pattern"
        self.module_version = "1.2"
        self.help_file = "doc/manual/modulesPatternResample.html"

        self.threshold = 0.0
        self.action = self.CORRELATE
        self.align = self.LEFT
        self.min_distance = 0
        self.max_distance = 0
        self.begin_compression = 0
        self.end_compression = 0
        self.begin_index = 0
        self.end_index = 0
        self.detection_method = self.DETECT_PATH
        self.pattern_file_path = ""

        self.set_config(self.THRESHOLD, self.threshold)
        self.set_config(self.ACTION, self.action)
        self.set_config(self.ALIGN, self.align)
        self.set_config(self.DISTANCE_MINIMAL, self.min_distance)
        self.set_config(self.DISTANCE_MAXIMAL, self.max_distance)
        self.set_config(self.COMPRESSION_START, self.begin_compression)
        self.set_config(self.COMPRESSION_END, self.end_compression)
        self.set_config(self.PATTERN_FILE_PATH, self.pattern_file_path)
        self.set_config(self.BEGIN_INDEX, self.begin_index)
        self.set_config(self.END_INDEX, self.end_index)
        self.set_config(self.DETECTION_METHOD, self.detection_method)

    @staticmethod
    def init_dialog():
        return None

    def action_performed(self, e):
        pass

    @staticmethod
    def accept_file(_dir, name):
        return name.endswith(".trs")

    def set_dialog_values(self, t: Trace = None, _nt=0, _sft=0, _snt=0, _sfs=0, _sns=0):
        if t:
            self.ns = t.get_number_of_samples()
        self.set_dialog_values_simple()

    def set_dialog_values_simple(self):
        self.action = self.get_config(self.ACTION)
        self.align = self.get_config(self.ALIGN)
        self.detection_method = self.get_config(self.DETECTION_METHOD)
        self.threshold = float(self.get_config(self.THRESHOLD))
        self.begin_index = int(self.get_config(self.BEGIN_INDEX))
        self.end_index = int(self.get_config(self.END_INDEX))
        self.min_distance = int(self.get_config(self.DISTANCE_MINIMAL))
        self.max_distance = int(self.get_config(self.DISTANCE_MAXIMAL))
        self.begin_compression = int(self.get_config(self.COMPRESSION_START))
        self.end_compression = int(self.get_config(self.COMPRESSION_END))
        self.pattern_file_path = self.get_config(self.PATTERN_FILE_PATH)

    def get_dialog_values(self):
        self.action = self.get_config(self.ACTION)
        self.align = self.get_config(self.ALIGN)
        self.detection_method = self.get_config(self.DETECTION_METHOD)
        self.threshold = float(self.get_config(self.THRESHOLD))
        self.begin_index = int(self.get_config(self.BEGIN_INDEX))
        self.end_index = int(self.get_config(self.END_INDEX))
        self.min_distance = int(self.get_config(self.DISTANCE_MINIMAL))
        self.max_distance = int(self.get_config(self.DISTANCE_MAXIMAL))
        self.begin_compression = int(self.get_config(self.COMPRESSION_START))
        self.end_compression = int(self.get_config(self.COMPRESSION_END))
        self.pattern_file_path = self.get_config(self.PATTERN_FILE_PATH)

    def init_process(self):
        self.selection_start = 0
        self.selection_end = self.ns
        self.recent_trace_index = 0
        self.patterns = 0

        self.fft_correlation_size = 1
        while self.fft_correlation_size < self.ns:
            self.fft_correlation_size <<= 1
        self.fft_spectrum_size = self.fft_correlation_size if self.fft_correlation_size <= self.ns else self.fft_correlation_size >> 1

        self.sy = [0.0] * self.fft_correlation_size
        self.s2y = [0.0] * self.fft_correlation_size

        if self.action == self.CORRELATE:
            self.average_spectrum = [0.0] * (1 + self.fft_correlation_size // 2)

        return self.load_pattern(self.pattern_file_path)

    def load_pattern(self, filename):
        try:
            if not filename:
                print("No pattern selected")
                return False

            f = filename
            if not os.path.exists(f):
                return False

            ts = TraceSet(f)
            ts_len = ts.get_number_of_samples()

            if ts_len < self.ns:
                self.pattern_start = 0
                self.pattern_length = ts_len
            else:
                self.pattern_start = self.selection_start
                self.pattern_length = self.selection_end - self.selection_start

            t = ts.get_trace(0)
            samples = t.get_sample()
            ts.close()

            self.pattern = [0.0] * self.fft_correlation_size
            for i in range(self.pattern_length):
                self.pattern[i] = samples[self.pattern_start + i]

            self.s_pattern = self.get_sum(self.pattern, self.pattern_length)
            self.s2_pattern = self.get_var(self.pattern, self.s_pattern, self.pattern_length)
            return True
        except Exception:
            traceback.print_exc()
            return False

    @staticmethod
    def get_sum(arr, n):
        return sum(arr[:n])

    @staticmethod
    def get_var(arr, sum_val, n):
        sq = sum(x * x for x in arr[:n])
        return sq - (sum_val ** 2) / n

    @staticmethod
    def get_stats(in_arr, s, s2, length):
        n = len(s)
        for i in range(n):
            s[i] = in_arr[i] ** 2

        s2[0] = sum(s[:length])
        for i in range(1, n):
            j = i + length - 1
            if j >= n:
                j %= n
            s2[i] = s2[i - 1] - s[i - 1] + s[j]

        s[0] = sum(in_arr[:length])
        for i in range(1, n):
            j = i + length - 1
            if j >= n:
                j %= n
            s[i] = s[i - 1] - in_arr[i - 1] + in_arr[j]

        for i in range(n):
            s2[i] -= (s[i] ** 2) / length

    def correlation(self, xf, sx, s2x, y, length):
        self.get_stats(y, self.sy, self.s2y, length)
        c = [0.0] * len(xf)
        for i in range(len(c)):
            c[i] = xf[i] * y[i]

        if s2x <= 0:
            return c

        for i in range(len(c)):
            sy_i = self.sy[i]
            s2y_i = self.s2y[i]
            if s2y_i <= 0:
                c[i] = 0.0
            else:
                c[i] = (c[i] - sx * sy_i / length) / math.sqrt(s2x * s2y_i)
        return c

    def process(self, t: Trace) -> Trace:
        sample = [0.0] * self.fft_correlation_size
        src = t.get_sample()
        for i in range(min(len(src), self.fft_correlation_size)):
            sample[i] = src[i]

        c = self.correlation(self.pattern, self.s_pattern, self.s2_pattern, sample, self.pattern_length)

        if self.action == self.CORRELATE:
            res = [float(c[i]) for i in range(self.ns)]
            return Trace(t.title, t.data, res)
        else:
            extract_len = self.end_compression - self.begin_compression
            if self.detection_method == self.DETECT_THRESHOLD:
                positions = self.find_matches(c, self.threshold, self.selection_start, self.selection_end, 0, extract_len)
            else:
                positions = self.find_matches_with_back_tracking(
                    c, self.threshold, self.selection_start, self.selection_end,
                    0, extract_len, self.max_distance * self.MAX_DEPTH
                )

            pos_list = sorted(positions)
            found = len(pos_list)
            patterns_needed = self.patterns if self.patterns != 0 else found
            out_arr = [0.0] * patterns_needed

            for i in range(min(patterns_needed, found)):
                x = i if self.align == self.LEFT else (found - 1 - i)
                y_idx = i if self.align == self.LEFT else (patterns_needed - 1 - i)
                pos = pos_list[x]
                total = 0.0
                cnt = 0
                for j in range(extract_len):
                    idx = pos + self.begin_compression + j
                    if 0 <= idx < len(sample):
                        total += sample[idx]
                        cnt += 1
                if cnt > 0:
                    out_arr[y_idx] = total / cnt
            return Trace(t.title, t.data, out_arr)

    @staticmethod
    def find_matches(c, threshold, begin, end, _max_num, _extract_len):
        peaks = []
        for i in range(begin, end):
            if c[i] >= threshold:
                peaks.append((-c[i], i))
        peaks.sort()
        res = OrderedDict()
        for _, idx in peaks:
            res[idx] = True
        return set(res.keys())

    def find_matches_with_back_tracking(self, c, threshold, begin, end, _max_num, extract_len, max_gap):
        pf = PathFinder(c, self.min_distance, self.max_distance)
        peaks = []
        for i in range(begin, end):
            if c[i] >= threshold:
                peaks.append((-c[i], i))
        peaks.sort()
        if not peaks:
            return set()

        res = {peaks[0][1]: True}
        avg_corr = c[peaks[0][1]]
        remaining = [idx for (sc, idx) in peaks[1:]]

        while remaining and not self.aborted:
            found_path = None
            found_peak = None
            local_thr = avg_corr / 2

            for p in remaining:
                if c[p] < local_thr:
                    continue
                neighbors = [x for x in res if abs(x - p) < max_gap]
                if not neighbors:
                    continue
                n = neighbors[0]
                if n < p:
                    path = pf.find_path(n, p, local_thr)
                else:
                    path = pf.find_path(p, n, local_thr)
                if path:
                    found_path = path
                    found_peak = p
                    break

            if not found_path:
                break

            for x in found_path:
                res[x] = True
                if x in remaining:
                    remaining.remove(x)
            res[found_peak] = True
            if found_peak in remaining:
                remaining.remove(found_peak)
            n_old = len(res) - len(found_path) - 1
            avg_corr = (avg_corr * n_old + pf.get_correlation_sum() + c[found_peak]) / len(res)
        return set(res.keys())