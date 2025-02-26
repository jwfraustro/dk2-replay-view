import struct


class TimeRecorded:
    """Time the replay was recorded."""

    def __init__(self, data):
        self.year, self.month, self.day, self.hour, self.minute = struct.unpack("<HBBBB", data)

    def __repr__(self):
        return f"{self.year}-{self.month:02}-{self.day:02} {self.hour:02}:{self.minute:02}"


class RandomMapSettings:
    """Random map settings data structure"""

    def __init__(self, data):
        (
            self.seed,
            self.seedMapHash,
            self.mapScenarioFlags,
            self.oppositionDensity,
            self.oppositionFilter,
            self.locationNameStrId,
        ) = struct.unpack("<IIIIII", data)

    def __repr__(self):
        return (
            f"seed: 0x{self.seed:08X}\n"
            f"seedMapHash: {self.seedMapHash}\n"
            f"mapScenarioFlags: {self.mapScenarioFlags}\n"
            f"oppositionDensity: {self.oppositionDensity}\n"
            f"oppositionFilter: {self.oppositionFilter}\n"
            f"locationNameStrId: {self.locationNameStrId}"
        )


class ReplayHeader:
    """Game replay header data structure."""

    def __init__(self, data):
        self.gameVersion = struct.unpack_from("<I", data, 0x00)[0]
        self.version = struct.unpack_from("<B", data, 0x04)[0]
        self.numStars = struct.unpack_from("<B", data, 0x05)[0]
        self.completedChallenges = struct.unpack_from("<B", data, 0x06)[0]
        self.availableChallenges = struct.unpack_from("<B", data, 0x07)[0]
        self.scenarioType = struct.unpack_from("<B", data, 0x08)[0]
        self.playTime = struct.unpack_from("<i", data, 0x09)[0]
        self.mapName = struct.unpack_from("64s", data, 0x0D)[0].decode("utf-8").strip("\x00")
        self.mapFileHash = struct.unpack_from("<I", data, 0x4D)[0]
        self.date = TimeRecorded(data[0x51:0x57])
        self.mapRngInfo = RandomMapSettings(data[0x57:0x6F])
        self.downloaded = struct.unpack_from("<?", data, 0x6F)[0]
        self.clientIndex = struct.unpack_from("<i", data, 0x70)[0]
        self.clientNames = [
            struct.unpack_from("32s", data, 0x74 + i * 32)[0].decode("utf-8").strip("\x00") for i in range(4)
        ]
        self.modsHash = struct.unpack_from("<I", data, 0xF4)[0]

    def format_play_time(self):
        """Convert milliseconds to minutes:seconds.milliseconds"""
        total_seconds = self.playTime / 1000
        minutes = int(total_seconds // 60)
        seconds = int(total_seconds % 60)
        milliseconds = int(self.playTime % 1000)
        return f"{minutes}m:{seconds:02}s.{milliseconds:03}ms"

    def __repr__(self):
        return (
            f"gameVersion: {self.gameVersion}\n"
            f"version: {self.version}\n"
            f"numStars: {self.numStars}\n"
            f"completedChallenges: {self.completedChallenges}\n"
            f"availableChallenges: {self.availableChallenges}\n"
            f"scenarioType: {self.scenarioType}\n"
            f"playTime: {self.format_play_time()}\n"
            f"mapName: {self.mapName}\n"
            f"mapFileHash: {self.mapFileHash}\n"
            f"date: {self.date}\n"
            f"mapRngInfo:\n{self.mapRngInfo}\n"
            f"downloaded: {self.downloaded}\n"
            f"clientIndex: {self.clientIndex}\n"
            f"clientNames: {self.clientNames}\n"
            f"modsHash: {self.modsHash}"
        )


def read_replay_header(file_path):
    """
    Reads the header of a replay file.

    Args:
        file_path (str): The path to the replay file.

    Returns:
        ReplayHeader: An instance of ReplayHeader containing the header data.
    """
    with open(file_path, "rb") as f:
        data = f.read(0xF8)  # Read only the header size
        return ReplayHeader(data)


# # Example usage
# if __name__ == "__main__":
#     replay_header = read_replay_header()
#     print(replay_header)
