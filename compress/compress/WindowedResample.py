import math
from typing import List


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
        self.config = {}
        self.number_of_samples = 0

    def set_config(self, key, value):
        self.config[key] = value

    def get_config(self, key):
        return self.config.get(key)


class Trace:
    def __init__(self, title="", data=None, samples=None, sample_freq=1.0):
        self.title = title
        self.data = data
        self.samples = samples if samples is not None else []
        self.sample_freq = sample_freq

    def get_sample(self):
        return self.samples.copy()

    def get_title(self):
        return self.title

    def get_data(self):
        return self.data

    def get_sample_frequency(self):
        return self.sample_freq


module_desc = ModuleDesc(
    pkg_name="Resample",
    name="WindowedResample",
    desc="",
    is_visible=False
)


class WindowedResample(Module):
    COMPRESS_RATIO = "compress.ratio"
    OVERLAP_RATIO = "overlap.ratio"

    MIN_COMPRESS_RATIO = 1
    MIN_OVERLAP_RATIO = 0.0
    MAX_OVERLAP_RATIO = 1.0
    DEFAULT_OVERLAP_RATIO = 0.5

    def __init__(self):
        super().__init__()
        self.overlap_ratio = 0.0
        self.compress_ratio = 1
        self.scale = 0.0

    def init_module(self):
        self.module_title = "WindowedResample"
        self.prefix = "WinRes"
        self.module_description = "Compress traces with fixed window size"
        self.module_version = "1.1"
        self.help_file = "doc/manual/modulesWindowedResample.html"
        self.compress_ratio = 1
        self.overlap_ratio = 0.0
        self.set_config(self.COMPRESS_RATIO, self.compress_ratio)
        self.set_config(self.OVERLAP_RATIO, self.overlap_ratio)

    @staticmethod
    def init_dialog():
        return None

    def set_dialog_values(self):
        pass

    def get_dialog_values(self):
        self.compress_ratio = int(self.get_config(self.COMPRESS_RATIO))
        self.overlap_ratio = float(self.get_config(self.OVERLAP_RATIO))

        if self.compress_ratio < self.MIN_COMPRESS_RATIO:
            print(f"Compress ratio less than minimum, resetting to: {self.MIN_COMPRESS_RATIO}")
            self.compress_ratio = self.MIN_COMPRESS_RATIO

        if not (self.MIN_OVERLAP_RATIO <= self.overlap_ratio < self.MAX_OVERLAP_RATIO):
            print(f"Overlap ratio not within 0..1 range, resetting to: {self.DEFAULT_OVERLAP_RATIO}")
            self.overlap_ratio = self.DEFAULT_OVERLAP_RATIO

        self.scale = self.compress_ratio * (1.0 - self.overlap_ratio)

    def process(self, t: Trace) -> Trace:
        sample = t.get_sample()
        sample_len = len(sample)
        out_len = math.ceil(sample_len / self.scale)
        out_samples = [0.0] * out_len

        for i in range(out_len):
            d = 0.0
            floor_pos = int(i * self.scale)

            j = 0
            k = floor_pos
            while j < self.compress_ratio and k < sample_len:
                if j == 0:
                    weight = (k + 1) - (i * self.scale)
                    d += sample[k] * weight
                else:
                    d += sample[k]
                j += 1
                k += 1

            frac = (i * self.scale) - floor_pos
            if frac > 0 and (floor_pos + self.compress_ratio) < sample_len:
                d += sample[floor_pos + self.compress_ratio] * frac

            out_samples[i] = d / self.compress_ratio

        new_freq = (t.get_sample_frequency() * out_len) / sample_len
        return Trace(t.get_title(), t.get_data(), out_samples, new_freq)