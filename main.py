from IperfLog import IperfLog
from Plotter import Plotter, PlotOptions


if __name__ == '__main__':
    log = IperfLog('log.txt')
    plotter = Plotter(log)
    plotter.create_plot(PlotOptions.BANDWIDTH)
