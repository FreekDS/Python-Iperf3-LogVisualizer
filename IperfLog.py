from typing import List


class LogEntry:
    def __init__(
            self,
            time_interval: List[float],
            transfer_rate: float,
            transfer_unit: str,
            bandwidth: float,
            bandwidth_unit: str,
            dgram_count,
            lost: float = None,
            jitter: float = None
    ):
        self.time_interval: List[float] = time_interval
        self.transfer_rate: float = transfer_rate
        self.transfer_unit: str = transfer_unit
        self.bandwidth: float = bandwidth
        self.bandwidth_unit: str = bandwidth_unit
        self.dgram_count: int = dgram_count

        self.loss: int or None = lost
        self.jitter: float or None = jitter

    @property
    def __is_result_entry(self) -> bool:
        return bool(self.loss and self.jitter)

    @property
    def loss_percentage(self) -> float:
        if self.__is_result_entry:
            return round(self.loss / self.dgram_count * 100, 2)
        else:
            raise AttributeError('Loss percentage only available on final result')

    def __str__(self) -> str:
        base = f'time: {self.time_interval[0]} - {self.time_interval[1]}\n\t' \
               f'Transfer: {self.transfer_rate} {self.transfer_unit}\n\t' \
               f'Bandwidth: {self.bandwidth} {self.bandwidth_unit}\n\t'
        if self.__is_result_entry:
            return f'{base}' \
                   f'Total Datagrams Sent: {self.dgram_count}\n\t' \
                   f'Datagrams Lost: {self.loss} ({self.loss_percentage}%)\n\t' \
                   f'Jitter: {self.jitter} ms\n\t'
        return f'{base}' \
               f'Datagrams Sent: {self.dgram_count}'

    def __repr__(self) -> str:
        return str(self)


class IperfLog:
    def __init__(self, fp):
        self.server_port = 0
        self.server_addr = ''
        self.server_ip = ''

        self.local_port = 0
        self.local_ip = ''

        self.log_entries = []

        self.result: LogEntry

        self.is_tcp = False

        with open(fp, 'r') as f:
            lines = f.readlines()
            connection_info = lines.pop(0)
            local_conn_info = lines.pop(0)
            self.__check_tcp(lines.pop(0))
            self.__parse_conn_info(connection_info)
            self.__parse_local_info(local_conn_info)
            self.__parse_data(lines)

    def __check_tcp(self, header):
        self.is_tcp = 'Datagrams' in header

    @property
    def unit(self):
        return self.log_entries[0].transfer_unit

    def __parse_conn_info(self, line):
        line = line.replace('Connecting to host ', '')
        line = line.replace(', port ', '§')
        conn_tuple = line.split('§')
        self.server_addr = conn_tuple[0]
        self.server_port = int(conn_tuple[1])

    def __parse_local_info(self, line):
        parts = line.split()

        # Throw away useless data
        parts = parts[3:]

        self.local_ip = parts[0]
        self.local_port = parts[2]
        self.server_ip = parts[5]

    @staticmethod
    def __parse_entry(line) -> LogEntry:
        parts = line.split()
        parts = parts[2:]
        timings = [float(x) for x in parts[0].split('-')]
        if len(parts) > 7:  # It is a final log entry when there are more than 7 parts
            lost_and_total = parts[-2].split('/')
            lost = int(lost_and_total[0])
            total = int(lost_and_total[1])
            jitter = float(parts[6])
            return LogEntry(timings, float(parts[2]), parts[3], float(parts[4]), parts[5], total, lost, jitter)
        else:
            while len(parts) < 7:
                parts.append(None)
            if parts[6] in ('sender', 'receiver'):
                parts[6] = None
            dgram_count = None if not parts[6] else int(parts[6])
            return LogEntry(timings, float(parts[2]), parts[3], float(parts[4]), parts[5], dgram_count)

    def __parse_data(self, lines):
        for i, line in enumerate(lines):
            line = line.strip()
            # detect ending
            if '- - - - -' in line:
                self.__parse_result(lines[i + 2:])
                break
            self.log_entries.append(self.__parse_entry(line))

    def __parse_result(self, lines):
        lines = [l.strip() for l in lines]
        self.result = self.__parse_entry(lines[0])

    @property
    def server_connection(self):
        return f'{self.server_addr}:{self.server_port}'

