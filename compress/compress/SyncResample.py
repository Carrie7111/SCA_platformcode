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
        self.aborted = False
        self.config = {}

    def set_config(self, k, v):
        self.config[k] = v

    def get_config(self, k):
        return self.config.get(k)

    def out(self, s):
        print(s)

    def err(self, s):
        print(s)


class Trace:
    def __init__(self, title="", data=None, samples=None, sample_freq=1.0):
        self.title = title
        self.data = data
        self.samples = samples if samples else []
        self.sample_frequency = sample_freq

    def get_number_of_samples(self):
        return len(self.samples)

    def get_sample(self, idx):
        return self.samples[idx] if 0 <= idx < len(self.samples) else 0.0

    def get_title(self):
        return self.title

    def get_data(self):
        return self.data


class DataOperationException(Exception):
    pass


module_desc = ModuleDesc(
    pkg_name="Resample",
    name="SyncResample",
    desc="",
    is_visible=False
)


class SyncResample(Module):
    RESAMPLE = "resample"
    PROCESS = "process"
    PEAK = "peak"
    MARGIN = "margin"
    START_PARTITION = "startPartition"
    END_PARTITION = "endPartition"

    PROC_AVERAGE = 0
    PROC_ABS_AVERAGE = 1
    PROC_INTEGRATE_AVERAGE = 2
    PROC_INTEGRATE_TWICE_AVERAGE = 3
    PROC_RMS = 4

    PEAK_POS = 0
    PEAK_POS_ABS = 1
    PEAK_NEG = 2
    EDGE_POS = 3
    EDGE_NEG = 4

    def __init__(self):
        super().__init__()
        self.initial_resample_frequency = 0.0
        self.resample_frequency = 0.0
        self.margin = 0.1
        self.factor = 1.0
        self.fft_size = 0
        self.resample_length = 0
        self.org_length = 0
        self.processing_type = self.PROC_AVERAGE
        self.synchronization_type = self.PEAK_POS
        self.start_partition = -0.05
        self.end_partition = 0.05

    def init_module(self):
        self.module_title = "SyncResample"
        self.prefix = "Resampled (sync) "
        self.module_description = "Resample traces at another frequency (with synchronisation)"
        self.help_file = "doc/manual/modulesSyncResample.html"

        self.synchronization_type = self.PEAK_POS
        self.start_partition = -0.05
        self.end_partition = 0.05
        self.margin = 0.1
        self.processing_type = self.PROC_AVERAGE

        self.set_config(self.PROCESS, self.processing_type)
        self.set_config(self.PEAK, self.synchronization_type)
        self.set_config(self.RESAMPLE, self.resample_frequency)
        self.set_config(self.MARGIN, self.margin)
        self.set_config(self.START_PARTITION, self.start_partition)
        self.set_config(self.END_PARTITION, self.end_partition)

    @staticmethod
    def init_dialog():
        return None

    def set_dialog_values(self):
        pass

    def get_dialog_values(self):
        self.synchronization_type = self.get_config(self.PEAK)
        self.processing_type = self.get_config(self.PROCESS)
        self.resample_frequency = float(self.get_config(self.RESAMPLE))
        self.margin = float(self.get_config(self.MARGIN))
        self.start_partition = float(self.get_config(self.START_PARTITION)) / 100.0
        self.end_partition = float(self.get_config(self.END_PARTITION)) / 100.0

    @staticmethod
    def get_required_memory_size():
        return 0

    def init_process(self):
        self.initial_resample_frequency = self.resample_frequency
        self.resample_length = 0
        self.org_length = 0
        self.fft_size = 0

        if self.resample_frequency > self.sample_frequency and self.sample_frequency != 1:
            self.err("WARNING: Resample frequency must be lower than sample frequency")
            return False
        if not (0.0 <= self.margin < 1.0):
            self.err("ERROR: margin must be in the range 0..1")
            return False
        return True

    def get_peak_index(self, t: Trace, offset: int, length: int, sync_type: int) -> int:
        total = t.get_number_of_samples()
        if offset < 0:
            offset = 0
        if offset >= total:
            offset = total - 1
        if offset + length >= total:
            length = total - offset

        val = 0.0
        idx = offset
        center = offset + length / 2.0

        for i in range(offset, offset + length):
            if sync_type == self.PEAK_NEG:
                dist = abs(i - center)
                weight = 1.0 + dist / (length / 2.0)
                current = (t.get_sample(i) - t.get_sample(offset)) / weight
                if current < val:
                    val = current
                    idx = i

            elif sync_type == self.PEAK_POS:
                dist = abs(i - center)
                weight = 1.0 + dist / (length / 2.0)
                current = (t.get_sample(i) - t.get_sample(offset)) / weight
                if current > val:
                    val = current
                    idx = i

            elif sync_type == self.PEAK_POS_ABS:
                current = abs(t.get_sample(i))
                if current > val:
                    val = current
                    idx = i

            elif sync_type == self.EDGE_POS:
                if i > 0 and t.get_sample(i - 1) < 0 <= t.get_sample(i):
                    idx = i

            elif sync_type == self.EDGE_NEG:
                if i > 0 and t.get_sample(i - 1) > 0 >= t.get_sample(i):
                    idx = i
        return idx

    def compute_frequency(self, t: Trace, initial: float):
        self.org_length = t.get_number_of_samples()
        self.resample_frequency = 0.0
        self.sample_frequency = t.sample_frequency

        if initial > self.sample_frequency:
            self.err(f"ERROR: Resample frequency ({initial}) must be lower than sample frequency ({self.sample_frequency})")
            return

        self.fft_size = 1
        while self.fft_size < t.get_number_of_samples():
            self.fft_size <<= 1

        sample = [0.0] * self.fft_size
        n = min(t.get_number_of_samples(), self.fft_size)
        for i in range(n):
            sample[i] = t.get_sample(i)

        freq = sample
        estimate = round(self.fft_size * initial / self.sample_frequency)
        low = round(estimate * (1.0 - self.margin))
        high = round(estimate * (1.0 + self.margin))

        best = estimate
        max_val = freq[estimate]
        for i in range(low, min(high, len(freq))):
            if freq[i] > max_val:
                max_val = freq[i]
                best = i

        if self.margin == 0:
            self.resample_frequency = initial
        else:
            self.resample_frequency = best * self.sample_frequency / self.fft_size

        self.factor = self.resample_frequency / self.sample_frequency
        self.resample_length = math.ceil(t.get_number_of_samples() * self.factor)
        self.out(f"Resample frequency: {self.resample_frequency}")

    def process(self, t: Trace) -> Trace | None:
        if self.resample_frequency == 0:
            self.err("ERROR: Enter a valid resample frequency first")
            return None

        total = t.get_number_of_samples()
        integrate = [0.0] * total
        integrate2 = [0.0] * total

        if self.org_length != total:
            self.compute_frequency(t, self.initial_resample_frequency)

        resample = [0.0] * (self.resample_length + 1)
        float_per_clock = (1.0 / self.resample_frequency) / self.x_scale
        samples_per_clock = round(float_per_clock)

        float_current = self.get_peak_index(t, 2 * samples_per_clock, 3 * samples_per_clock, self.synchronization_type)
        current_idx = round(float_current)

        if current_idx > 3 * samples_per_clock:
            current_idx -= samples_per_clock
        if current_idx > 3 * samples_per_clock:
            current_idx -= samples_per_clock

        k = 0
        while current_idx + 2 * samples_per_clock < total and k < len(resample):
            search_start = current_idx - round(float_per_clock / 2)
            peak_idx = self.get_peak_index(t, search_start, samples_per_clock, self.synchronization_type)

            start_idx = peak_idx + round(self.start_partition * samples_per_clock)
            end_idx = peak_idx + round(self.end_partition * samples_per_clock)

            if start_idx < 0:
                start_idx = 0
            if end_idx >= total:
                end_idx = total - 1

            length = end_idx - start_idx
            if length <= 0:
                self.err("ERROR: No samples in partition!")
                self.aborted = True
                return None

            if self.processing_type == self.PROC_AVERAGE:
                for i in range(start_idx + 1, end_idx - 1):
                    resample[k] += t.get_sample(i)
                resample[k] += t.get_sample(start_idx) / 2
                resample[k] += t.get_sample(end_idx) / 2

            elif self.processing_type == self.PROC_ABS_AVERAGE:
                for i in range(start_idx + 1, end_idx - 1):
                    resample[k] += abs(t.get_sample(i))
                resample[k] += abs(t.get_sample(start_idx)) / 2
                resample[k] += abs(t.get_sample(end_idx)) / 2

            elif self.processing_type == self.PROC_INTEGRATE_AVERAGE:
                integrate[0] = 0.0
                for i in range(length):
                    integrate[i + 1] = integrate[i] + t.get_sample(start_idx + i)
                    resample[k] += integrate[i + 1]

            elif self.processing_type == self.PROC_INTEGRATE_TWICE_AVERAGE:
                integrate[0] = 0.0
                integrate2[0] = 0.0
                for i in range(length):
                    integrate[i + 1] = integrate[i] + t.get_sample(start_idx + i)
                    integrate2[i + 1] = integrate2[i] + integrate[i]
                    resample[k] += integrate2[i + 1]

            elif self.processing_type == self.PROC_RMS:
                if end_idx >= start_idx + 3:
                    for i in range(start_idx + 1, end_idx - 1):
                        s = t.get_sample(i)
                        resample[k] += s * s
                resample[k] += (t.get_sample(start_idx) ** 2) / 4.0
                resample[k] += (t.get_sample(end_idx) ** 2) / 4.0
                resample[k] /= length
                resample[k] = math.sqrt(resample[k])
                resample[k] *= length

            resample[k] /= length

            float_current += float_per_clock + self.margin * (peak_idx - current_idx)
            current_idx = round(float_current)
            k += 1

        return Trace(t.get_title(), t.get_data(), resample, self.resample_frequency)