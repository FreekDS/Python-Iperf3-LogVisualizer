from IperfLog import IperfLog
from PowerLog import PowerLog
from Plotter import Plotter, PowerPlotter, PlotOptions


if __name__ == '__main__':
    log = IperfLog('iperf-client.txt')
    plotter = Plotter(log)
    plotter.create_plot(PlotOptions.BANDWIDTH)

    p_log = PowerLog('power-output.txt')
    plotter = PowerPlotter(p_log)
    plotter.create_plot(relative_time=True)
