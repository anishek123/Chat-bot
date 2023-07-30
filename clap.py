import pyaudio
import struct
import math


INITIAL_TAP_THRESHOLD = 0.1  # Initial value for tap threshold
FORMAT = pyaudio.paInt16
SHORT_NORMALIZE = (1.0 / 32768.0)  # Value for normalizing audio samples
CHANNELS = 2
RATE = 44100
INPUT_BLOCK_TIME = 0.05  # Time for each input block
INPUT_FRAMES_PER_BLOCK = int(RATE * INPUT_BLOCK_TIME)  # Frames per block
OVERSENSITIVE = 15.0 / INPUT_BLOCK_TIME  # Sensitivity for detecting claps
UNDERSENSITIVE = 120.0 / INPUT_BLOCK_TIME  # Threshold for resetting tap threshold
MAX_TAP_BLOCKS = 0.15 / INPUT_BLOCK_TIME  # Maximum number of blocks to count as a clap


class TapTester(object):

    def __init__(self):
        self.pa = pyaudio.PyAudio()
        self.stream = self.open_mic_stream()
        self.tap_threshold = INITIAL_TAP_THRESHOLD
        self.noisy_count = MAX_TAP_BLOCKS + 1
        self.quiet_count = 0
        self.error_count = 0

    def stop(self):
        self.stream.close()

    def find_input_device(self):
        device_index = None
        for i in range(self.pa.get_device_count()):
            devinfo = self.pa.get_device_info_by_index(i)
            for keyword in ["mic", "input"]:
                if keyword in devinfo["name"].lower():
                    device_index = i
                    return device_index

        if device_index is None:
            print("No preferred input found; using default input device.")

        return device_index

    def open_mic_stream(self):
        device_index = self.find_input_device()

        stream = self.pa.open(format=FORMAT,
                              channels=CHANNELS,
                              rate=RATE,
                              input=True,
                              input_device_index=device_index,
                              frames_per_buffer=INPUT_FRAMES_PER_BLOCK)

        return stream

    def listen(self):
        try:
            block = self.stream.read(INPUT_FRAMES_PER_BLOCK)
        except IOError as e:
            self.error_count += 1
            print("(%d) Error recording: %s" % (self.error_count, e))
            self.noisy_count = 1
            return

        amplitude = self.get_rms(block)

        if amplitude > self.tap_threshold:
            self.quiet_count = 0
            self.noisy_count += 1
            if self.noisy_count > OVERSENSITIVE:
                self.tap_threshold *= 1.1
        else:
            if 1 <= self.noisy_count <= MAX_TAP_BLOCKS:
                return "True-Mic"
            self.noisy_count = 0
            self.quiet_count += 1
            if self.quiet_count > UNDERSENSITIVE:
                self.tap_threshold *= 2

    def get_rms(self, block):
        count = len(block) / 2
        format = "%dh" % (count)
        shorts = struct.unpack(format, block)
        sum_squares = 0.0
        for sample in shorts:
            n = sample * SHORT_NORMALIZE
            sum_squares += n * n

        return math.sqrt(sum_squares / count)


def Tester():
    tt = TapTester()

    while True:
        kk = tt.listen()

        if "True-Mic" == kk:
            print("")
            print("> Clap Detected : Starting The Mr.D.")
            print("")
            return "True-Mic"
