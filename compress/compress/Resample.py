import math
from typing import List, Dict, Any


class ModuleDesc:
    def __init__(self, pkg_name, name, desc, is_visible):
        self.pkg_name = pkg_name
        self.name = name
        self.desc = desc
        self.is_visible = is_visible


class Module:
    def __init__(self):
        self.module_title = ""
        self.prefix = ""
        self.module_description = ""
        self.module_version = ""
        self.help_file = ""
        self.sample_frequency = 1.0
        self.config: Dict[str, Any] = {}
        self.current_trace_index = -1
        self.number_of_samples = 0

    def set_config(self, key: str, value: Any):
        self.config[key] = value

    def get_config(self, key: str) -> Any:
        return self.config.get(key)


class Trace:
    def __init__(self, title="", data=None, samples=None, sample_freq=1.0):
        self.title = title
        self.data = data
        self.samples = samples if samples is not None else []
        self.sample_frequency = sample_freq

    def get_number_of_samples(self) -> int:
        return len(self.samples)

    def get_sample(self, index=None):
        if index is None:
            return self.samples.copy()
        return self.samples[index]

    def get_title(self):
        return self.title

    def get_data(self):
        return self.data


class DataOperationException(Exception):
    pass


module_desc = ModuleDesc(
    pkg_name="Resample",
    name="Resample",
    desc="",
    is_visible=False
)


class Resample(Module):
    COMPUTE_ONCE = 0
    COMPUTE_ALWAYS = 1
    NO_ALIGN = 0
    PEAK_ALIGN = 1
    CORRELATION_ALIGN = 2

    RECOMPUTE = "recompute"
    RESAMPLE = "resample"
    MARGIN = "margin"
    ALIGN = "align"
    SAMPLES_PER_PERIOD = "samples.per.period"

    def __init__(self):
        super().__init__()
        self.initial_resample_frequency = 1.0
        self.resample_frequency = 1.0
        self.factor = 1.0
        self.margin = 0.1
        self.period = 1.0
        self.fft_size = 0
        self.resample_length = 0
        self.resample_frequency_index = 0
        self.shift = 0
        self.first_shift = 0
        self.shift_low = 0
        self.shift_high = 0
        self.align = self.PEAK_ALIGN
        self.samples_per_period = 1
        self.int_period = 1
        self.half_period = 1
        self.half_compare_period = 1
        self.compare_period = 1
        self.recompute = False
        self.first = True

        self.ref_freq: List[float] = []
        self.test_sample: List[float] = []
        self.sr: List[float] = []
        self.s2r: List[float] = []

    def init_module(self):
        self.module_title = "Resample"
        self.prefix = "Resampled"
        self.module_description = "Resample traces with another frequency"
        self.module_version = "1.4"
        self.help_file = "doc/manual/modulesResample.html"

        self.resample_frequency = 1.0
        self.margin = 0.1
        self.recompute = False
        self.align = self.PEAK_ALIGN
        self.samples_per_period = 1

        self.set_config(self.RECOMPUTE, 0)
        self.set_config(self.RESAMPLE, self.resample_frequency)
        self.set_config(self.MARGIN, self.margin)
        self.set_config(self.ALIGN, self.align)
        self.set_config(self.SAMPLES_PER_PERIOD, self.samples_per_period)

    @staticmethod
    def init_dialog():
        return None

    def set_dialog_values(self):
        pass

    def get_dialog_values(self):
        self.recompute = self.get_config(self.RECOMPUTE) == 1
        self.align = self.get_config(self.ALIGN)
        self.resample_frequency = float(self.get_config(self.RESAMPLE))
        self.margin = float(self.get_config(self.MARGIN))
        self.samples_per_period = int(self.get_config(self.SAMPLES_PER_PERIOD))

    def init_process(self) -> bool:
        self.first = True
        self.initial_resample_frequency = self.resample_frequency
        self.resample_length = 0
        self.resample_frequency = 0.0
        self.shift = 0
        self.fft_size = 0

        if self.initial_resample_frequency == 1.0 and self.margin == 0.1:
            self.initial_resample_frequency = self.sample_frequency / 2
            self.margin = 1.0

        if self.initial_resample_frequency > self.sample_frequency / 2 and self.sample_frequency != 1:
            return False

        if not (0.0 <= self.margin <= 1.0):
            return False

        if self.samples_per_period < 1:
            return False

        return True

    def compute_frequency(self, t: Trace, initial: float) -> bool:
        n = t.get_number_of_samples()
        if self.fft_size < n:
            self.fft_size = 1
            while self.fft_size < n:
                self.fft_size <<= 1

        sample = [0.0] * self.fft_size
        src = t.get_sample()
        for i in range(min(n, self.fft_size)):
            sample[i] = src[i]

        estimate = int(self.fft_size * initial / self.sample_frequency)
        low = max(1, int(estimate * (1 - self.margin)))
        high = int(estimate * (1 + self.margin))
        freq = sample

        max_val = freq[estimate]
        self.resample_frequency_index = estimate
        for i in range(low, min(high, len(freq))):
            if freq[i] > max_val:
                max_val = freq[i]
                self.resample_frequency_index = i

        if self.margin == 0:
            self.resample_frequency = initial
        else:
            self.resample_frequency = self.resample_frequency_index * self.sample_frequency / self.fft_size

        self.period = self.sample_frequency / self.resample_frequency
        self.factor = self.samples_per_period / self.period
        self.int_period = math.ceil(self.period)
        self.half_period = math.ceil(self.period / 2)
        self.compare_period = math.ceil(10 * self.period)
        self.half_compare_period = math.ceil(5 * self.period)
        self.resample_length = math.ceil(self.number_of_samples * self.factor)

        return self.resample_length > 1

    def get_shift(self, sample: List[float]) -> int:
        peak_idx = self.shift_low
        peak_val = sample[peak_idx]
        for i in range(self.shift_low, self.shift_high):
            if sample[i] > peak_val:
                peak_val = sample[i]
                peak_idx = i
        return peak_idx

    def compute_first_alignment(self, sample: List[float]) -> int:
        if self.align == self.PEAK_ALIGN:
            self.shift_low = len(sample) // 2 - self.half_period
            self.shift_high = self.shift_low + self.int_period
        else:
            self.shift_low = len(sample) // 2 - self.half_compare_period
            self.shift_high = self.shift_low + self.compare_period

        self.shift_low = max(0, self.shift_low)
        self.shift_high = min(len(sample) - 1, self.shift_high)

        shift = self.get_shift(sample)
        periods = int(shift / self.period)
        peak_in_period = int(shift - periods * self.period)
        correction = math.ceil(self.period / 8) - peak_in_period
        return shift + correction

    def create_reference(self, sample: List[float]):
        self.fft_size = 1
        while self.fft_size < self.compare_period:
            self.fft_size <<= 1

        ref_sample = [0.0] * self.fft_size
        self.test_sample = [0.0] * self.fft_size
        for j in range(self.compare_period):
            ref_sample[j] = sample[self.shift_low + j]

        self.sr = [0.0] * self.compare_period
        self.s2r = [0.0] * self.compare_period
        self.get_stats(ref_sample, self.sr, self.s2r, self.int_period, self.compare_period)
        self.ref_freq = ref_sample

    @staticmethod
    def get_sum(arr: List[float], length: int) -> float:
        return sum(arr[:length])

    @staticmethod
    def get_var(arr: List[float], sum_val: float, length: int) -> float:
        sq = sum(x * x for x in arr[:length])
        return sq - (sum_val ** 2) / length

    @staticmethod
    def get_stats(in_arr: List[float], s: List[float], s2: List[float], len1: int, len2: int):
        n = min(len(s), len(in_arr))
        for i in range(n):
            s[i] = in_arr[i]
            s2[i] = s[i] * s[i]

        s0 = s[0]
        s20 = s2[0]
        for i in range(1, min(len1, n)):
            s[0] += s[i]
            s2[0] += s2[i]

        for i in range(1, len2):
            j = i + len1 - 1
            if j >= len(in_arr):
                break
            sn = s[i]
            s2n = s2[i]
            s[i] = s[i - 1] - s0 + in_arr[j]
            s2[i] = s2[i - 1] - s20 + (in_arr[j] ** 2)
            s0 = sn
            s20 = s2n

        for i in range(len2):
            s2[i] -= (s[i] ** 2) / len1

    def correlation(self, xf: List[float], sx: List[float], s2x: List[float], y: List[float], length: int) -> List[float]:
        sy_val = self.get_sum(y, length)
        s2y_val = self.get_var(y, sy_val, length)
        c = [0.0] * len(xf)
        for i in range(min(len(c), len(y))):
            c[i] = xf[i] * y[i]

        if s2y_val > 0:
            for i in range(self.int_period):
                if i < len(s2x) and s2x[i] > 0 and i < len(c):
                    c[i] = (c[i] - sx[i] * sy_val / length) / math.sqrt(s2x[i] * s2y_val)
                else:
                    c[i] = 0.0
        return c

    def get_best_correlation(self, sample: List[float]) -> int:
        test = [0.0] * self.fft_size
        for i in range(self.compare_period):
            test[i] = sample[self.shift_low + i]

        c = self.correlation(self.ref_freq, self.sr, self.s2r, test, self.int_period)
        best_idx = 0
        best_val = c[0]
        for i in range(1, self.int_period):
            if c[i] > best_val:
                best_val = c[i]
                best_idx = i
        return self.shift_low + self.half_period - best_idx

    def process(self, t: Trace) -> Trace | None:
        if self.first or self.recompute:
            if not self.compute_frequency(t, self.initial_resample_frequency):
                return None

        if self.align != self.NO_ALIGN:
            sample = t.get_sample()
            if self.first:
                self.first_shift = self.compute_first_alignment(sample)
                if self.align == self.CORRELATION_ALIGN:
                    self.create_reference(sample)

            if self.align == self.CORRELATION_ALIGN:
                self.shift = self.get_best_correlation(sample) - self.first_shift
            elif self.align == self.PEAK_ALIGN:
                self.shift = self.get_shift(sample) - self.first_shift

        if self.resample_frequency <= 0 or self.resample_length <= 1:
            return None

        resample = [0.0] * self.resample_length
        k = 0
        last_j = 0
        total = t.get_number_of_samples()

        for i in range(total):
            p = i + self.shift
            j = int(i * self.factor)
            if j > last_j and k > 0 and last_j < self.resample_length:
                resample[last_j] /= k
                k = 0
            if j < self.resample_length:
                val = t.get_sample(p % total)
                resample[j] += val
            last_j = j
            k += 1

        if k > 0 and last_j < self.resample_length:
            resample[last_j] /= k

        self.first = False
        return Trace(t.get_title(), t.get_data(), resample, self.resample_frequency * self.samples_per_period)