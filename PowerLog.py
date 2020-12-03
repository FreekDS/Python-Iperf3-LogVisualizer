class PowerEntry:
    def __init__(self, time, signal, channel, bssid):
        self.time = time
        self.channel = channel
        self.signal = signal
        self.bssid = bssid

        self.in_percentage = True

    @property
    def in_dbm(self):
        return not self.in_percentage

    def convert_to_dbm(self):
        """
        https://stackoverflow.com/questions/15797920/how-to-convert-wifi-signal-strength-from-quality-percent-to-rssi-dbm
        """
        if self.in_percentage:
            self.signal = (self.signal / 2) - 100
            self.in_percentage = False

    def convert_to_percentage(self):
        """
        https://stackoverflow.com/questions/15797920/how-to-convert-wifi-signal-strength-from-quality-percent-to-rssi-dbm
        """
        if self.in_dbm:
            self.signal = (self.signal + 100) * 2
            self.in_percentage = True


class PowerLog:
    def __init__(self, fp):
        self.log_entries = list()
        with open(fp, 'r') as file:
            lines = file.readlines()
            lines.pop(0)
            for line in lines:
                if line:
                    self.__proc_line(line)

    def __proc_line(self, line):
        ' '.join(line.split())
        parts = line.split()
        signal = int(parts[1].replace('%', ''))
        self.log_entries.append(PowerEntry(parts[0], signal, parts[2], parts[3]))

    def to_percentages(self):
        log: PowerEntry
        for log in self.log_entries:
            log.convert_to_percentage()

    def to_dbm(self):
        log: PowerEntry
        for log in self.log_entries:
            log.convert_to_dbm()

    @property
    def is_in_dbm(self):
        return self.log_entries[0].in_dbm

    @property
    def is_in_percentage(self):
        return self.log_entries[0].in_percentage
