# Log visualizer for iperf3 logs
Read iperf3 log files and generate a simple graph from them.
This tool can also generate graphs based on the output of the `scan-power.bat` script.

## Usage

```python visualizer.py -h/--help```

## Basic Usage Example

Generate iperf graph
```python visualizer.py iperf-log1.txt iperf-log2.txt -t iperf```

<br>
<img src="https://i.imgur.com/yxOsCFC.png" width=400>

Generate power graph
```python visualizer.py power-log1.txt power-log2.txt -t power```

<img src="https://i.imgur.com/9BlJ5Hq.png" width=400>
