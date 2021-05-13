from IperfLog import IperfLog
from PowerLog import PowerLog
from Plotter import Plotter, PowerPlotter

import argparse

parser = argparse.ArgumentParser(description="Visualize log files of iperf or of the power measurement script")
parser.add_argument('input_files', type=str, nargs='+', help='¨Path to log file(s) to visualize')
parser.add_argument('--type', '-t', required=True, choices=['power', 'iperf'], dest='type')
parser.add_argument('--out-dir', '-o', required=False, default='./', dest='out_dir')
parser.add_argument('--power-change', '-pc', required=False, default='channel', choices=['bssid', 'channel', 'none'],
                    dest='pc')
parser.add_argument('--power-yaxis', '-py', required=False, default='signal', choices=['channel', 'signal'], dest='pc')
parser.add_argument('--iperf-yaxis', '-iy', required=False, default='bandwidth',
                    choices=['bandwidth', 'transfer_rate', 'dgram_count'], dest='iy')

if __name__ == '__main__':

    args = parser.parse_args()

    for in_file in args.input_files:

        out_dir = str(args.out_dir)
        if out_dir[-1] != '/':
            out_dir += '/'

        out_path = f"{args.out_dir}out-{in_file}.png"

        if args.type == 'power':
            log = PowerLog(in_file)
            plotter = PowerPlotter(log)
            plotter.create_plot(fname=out_path, change_indicator=args.pc if args.pc != 'none' else None, y_axis=args.py)
        elif args.type == 'iperf':
            log = IperfLog(in_file)
            plotter = Plotter(log)
            plotter.create_plot(fname=out_path, y_axis=args.iy)

    # log = IperfLog('iperf-output.txt')
    # plotter = Plotter(log)
    # plotter.create_plot(PlotOptions.BANDWIDTH)
    #
    # p_log = PowerLog('power-output.txt')
    # plotter = PowerPlotter(p_log)
    # plotter.create_plot(relative_time=True, change_indicator=None, y_axis='channel')
