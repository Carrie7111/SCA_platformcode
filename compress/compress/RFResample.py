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
        self.help_file = ""
        self.sample_frequency = 1.0
        self.x_scale = 1.0

    def out(self, msg):
        print(msg)

    def err(self, msg):
        print(msg)


class Trace:
    def __init__(self, title="", data=None, samples=None, sample_freq=1.0):
        self.title = title
        self.data = data
        self.samples = samples if samples is not None else []
        self.sample_frequency = sample_freq

    def get_number_of_samples(self) -> int:
        return len(self.samples)

    def get_sample(self, index: int) -> float:
        return self.samples[index] if 0 <= index < len(self.samples) else 0.0

    def get_title(self):
        return self.title

    def get_data(self):
        return self.data


class DataOperationException(Exception):
    pass


module_desc = ModuleDesc(
    pkg_name="Resample",
    name="RFResample",
    desc="",
    is_visible=False
)


class RFResample(Module):
    RESAMPLE_FREQUENCY = 27.12e6

    def __init__(self):
        super().__init__()
        self.resample_frequency = 0.0
        self.margin = 0.0
        self.factor = 0.0
        self.fft_size = 0
        self.resample_length = 0
        self.org_length = 0
        self.start_partition = -40.0
        self.end_partition = -15.0

    def init_module(self):
        self.module_title = "RFResample"
        self.prefix = "RFResampled "
        self.module_description = "Resamples traces at 27.12 MHz with synchronisation"
        self.help_file = "doc/modulesRFResample.html"

    @staticmethod
    def init_dialog():
        return None

    @staticmethod
    def get_required_memory_size():
        return 0

    def init_process(self) -> bool:
        self.resample_frequency = self.RESAMPLE_FREQUENCY
        self.margin = 0.01
        self.org_length = 0
        self.fft_size = 0

        if self.resample_frequency > self.sample_frequency and self.sample_frequency != 1:
            self.err("WARNING: Resample frequency must be lower than sample frequency")
            return False
        return True

    def get_peak_index(self, t: Trace, offset: int, length: int) -> int:
        total = t.get_number_of_samples()

        if offset < 0:
            offset = 0
        if offset >= total:
            offset = total - 1
        if offset + length >= total:
            length = total - offset - 1

        val = -abs(t.get_sample(offset + 1) - t.get_sample(offset))
        idx = offset
        center = offset + length / 2.0

        for i in range(offset, offset + length):
            diff = t.get_sample(i + 1) - t.get_sample(i)
            dist = abs(i - center)
            weight = 1.0 + (dist / (length / 2.0))
            current = abs(diff) / weight

            if current > val:
                val = current
                idx = i
        return idx

    def compute_frequency(self, t: Trace, initial_resample_freq: float):
        self.org_length = t.get_number_of_samples()
        self.resample_frequency = 0.0
        self.sample_frequency = t.sample_frequency

        if initial_resample_freq > self.sample_frequency:
            self.err(f"ERROR: Resample frequency ({initial_resample_freq}) must be lower than sample frequency ({self.sample_frequency})")
            return

        self.fft_size = 1
        while self.fft_size < t.get_number_of_samples():
            self.fft_size <<= 1

        sample = [0.0] * self.fft_size
        src = t.samples
        copy_len = min(t.get_number_of_samples(), self.fft_size)
        for i in range(copy_len):
            sample[i] = src[i]

        freq = sample
        estimate = round(self.fft_size * initial_resample_freq / self.sample_frequency)
        low = round(estimate * (1 - self.margin))
        high = round(estimate * (1 + self.margin))

        best = estimate
        max_val = freq[estimate]

        for i in range(low, min(high, len(freq))):
            if freq[i] > max_val:
                max_val = freq[i]
                best = i

        if self.margin == 0:
            self.resample_frequency = initial_resample_freq
        else:
            self.resample_frequency = best * self.sample_frequency / self.fft_size

        self.factor = self.resample_frequency / self.sample_frequency
        self.resample_length = math.ceil(t.get_number_of_samples() * self.factor)
        self.out(f"Resample frequency: {self.resample_frequency}")

    def process(self, t: Trace) -> Trace:
        self.factor = self.resample_frequency / self.sample_frequency
        total_samples = t.get_number_of_samples()
        self.resample_length = math.ceil(total_samples * self.factor)

        if self.org_length != total_samples:
            self.compute_frequency(t, self.RESAMPLE_FREQUENCY)

        resample = [0.0] * (self.resample_length + 1)
        float_samples_per_clock = (1.0 / self.resample_frequency) / self.x_scale
        samples_per_clock = round(float_samples_per_clock)

        current_idx = self.get_peak_index(t, samples_per_clock, 3 * samples_per_clock)

        if current_idx > 2 * samples_per_clock:
            current_idx -= samples_per_clock
        if current_idx > 2 * samples_per_clock:
            current_idx -= samples_per_clock

        float_current_idx = float(current_idx)
        k = 0

        while current_idx + samples_per_clock < total_samples and k < len(resample):
            search_start = current_idx - round(float_samples_per_clock / 2)
            peak_idx = self.get_peak_index(t, search_start, samples_per_clock)

            start_idx = peak_idx + round(self.start_partition * samples_per_clock / 100)
            end_idx = peak_idx + round(self.end_partition * samples_per_clock / 100)

            if start_idx < 0:
                start_idx = 0
            if end_idx >= total_samples:
                end_idx = total_samples - 1

            length = end_idx - start_idx
            if length <= 0:
                length = 1

            total = 0.0
            for i in range(start_idx + 1, end_idx - 1):
                total += t.get_sample(i)

            total += t.get_sample(start_idx) / 2.0
            total += t.get_sample(end_idx) / 2.0
            resample[k] = total / length

            float_current_idx += float_samples_per_clock + self.margin * (peak_idx - current_idx)
            current_idx = round(float_current_idx)
            k += 1

        return Trace(t.get_title(), t.get_data(), resample, self.resample_frequency)