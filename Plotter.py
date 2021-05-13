from IperfLog import IperfLog, LogEntry
import matplotlib.pyplot as plt
import enum
from PowerLog import PowerLog, PowerEntry
import datetime


class PlotOptions(enum.Enum):
    BANDWIDTH = 'bandwidth',
    TRANSFER = 'transfer_rate',
    DGRAMS = 'dgram_count'


convert_table = {
    'Bytes': 1,
    'KBytes': 1000,
    'MBytes': pow(10, 6),
    'GBytes': pow(10, 9),

    'bits/sec': 1,
    'Kbits/sec': 1000,
    'Mbits/sec': pow(10, 6),
    'Gbits/sec': pow(10, 9)
}


def convert_multiplier(from_type, to_type):
    return convert_table.get(from_type) / convert_table.get(to_type)


class Plotter:
    def __init__(self, iperf_log: IperfLog):
        self.log = iperf_log

    def create_plot(self, y_axis: PlotOptions or str, fname='output.png',
                    convert_measures=True):
        x_points = list()
        y_points = list()

        x_axis = 'time_interval'

        if isinstance(y_axis, PlotOptions):
            y_axis = y_axis.value[0]

        required_measure = self.log.unit
        if y_axis == 'bandwidth':
            required_measure = self.log.log_entries[0].bandwidth_unit

        log: LogEntry
        for log in self.log.log_entries:
            x_entry = log.__getattribute__(x_axis)
            if x_entry is None:
                raise AttributeError(f"LogEntry has no attribute '{x_axis}'")
            y_entry = log.__getattribute__(y_axis)
            if y_entry is None:
                raise AttributeError(f"LogEntry has no attribute '{y_axis}'")

            if y_axis == 'transfer_rate' and log.transfer_unit != required_measure and convert_measures and \
                    y_axis != 'dgram_count':
                y_entry *= convert_multiplier(log.transfer_unit, required_measure)
            if y_axis == 'bandwidth' and log.bandwidth_unit != required_measure and convert_measures and \
                    y_axis != 'dgram_count':
                y_entry *= convert_multiplier(log.bandwidth_unit, required_measure)

            if x_axis == 'time_interval':
                x_entry = x_entry[0]

            x_points.append(x_entry)
            y_points.append(y_entry)

        assert (len(x_points) == len(y_points))

        if x_axis == 'time_interval':
            x_axis = 'time'
        if y_axis == 'bandwidth':
            y_axis = f"{y_axis} ({required_measure})"

        plt.plot(x_points, y_points)
        plt.xlabel(x_axis.replace('_', ' '))
        plt.ylabel(y_axis.replace('_', ' '))
        plt.title(self.log.server_connection + " trace")
        plt.savefig(fname, format='png')
        plt.show()


class PowerPlotter:
    def __init__(self, power_log: PowerLog):
        self.power_log = power_log

    def create_plot(self, y_axis='signal', relative_time=True, fname='power-output.png',change_indicator='bssid'):
        x_points = list()
        y_points = list()

        bssid_change_points = list()
        channel_change_points = list()
        change_str = str()

        log: PowerEntry
        start_time = datetime.datetime.strptime(self.power_log.log_entries[0].time, '%H:%M:%S')
        current_bssid = self.power_log.log_entries[0].bssid
        current_channel = self.power_log.log_entries[0].channel
        for log in self.power_log.log_entries:
            if relative_time:
                log_time = datetime.datetime.strptime(log.time, '%H:%M:%S')
                x_point = (log_time - start_time).seconds
            else:
                x_point = log.time

            y_point = getattr(log, y_axis)
            y_points.append(y_point)
            x_points.append(x_point)

            if change_indicator == 'bssid':
                if current_bssid != log.bssid:
                    bssid_change_points.append((x_point, y_point))
                    i = len(bssid_change_points)
                    change_str += f"{i}. {current_bssid} -> {log.bssid} ({x_point}s)\n"
                    current_bssid = log.bssid
            elif change_indicator == 'channel':
                if current_channel != log.channel:
                    channel_change_points.append((x_point, y_point))
                    i = len(channel_change_points)
                    change_str += f"{i}. {current_channel} -> {log.channel} ({x_point}s)\n"
                    current_channel = log.channel

        plt.plot(x_points, y_points)

        if change_indicator == 'bssid':
            plt.plot(*zip(*bssid_change_points), 'ro')
            for i, point in enumerate(bssid_change_points):
                plt.annotate(f"{i + 1}",
                             xy=point,
                             xycoords='data',
                             xytext=(-20, -20),
                             textcoords='offset pixels'
                             )
                print(f"Changes in BSSID\n{change_str}")
        elif change_indicator == 'channel':
            plt.plot(*zip(*channel_change_points), 'ro')
            for i, point in enumerate(channel_change_points):
                plt.annotate(f"{i + 1}",
                             xy=point,
                             xycoords='data',
                             xytext=(-20, -20),
                             textcoords='offset pixels'
                             )
            print(f"Changes in channel\n{change_str}")

        plt.xlabel('time (s)')
        if y_axis == 'signal':
            if self.power_log.is_in_dbm:
                y_axis += ' (dbm)'
            else:
                y_axis += ' (%)'
        plt.ylabel(y_axis.replace('-', ''))
        plt.title(y_axis + ' over time (s)')

        plt.savefig(fname, format='png')
        plt.show()


