import os
import glob
import csv
import locale
import argparse
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

COLS = {'timestamp': 0,
     'interface name': 1,
     'bytes out/s': 2,
     'bytes in/s': 3,
     'bytes total/s': 4,
     'bytes in': 5,
     'bytes out': 6,
     'packets out/s': 7,
     'packets in/s': 8,
     'packets total/s': 9,
     'packets in': 10,
     'packets out': 11,
     'error out/s': 12,
     'errors in/s': 13,
     'errors in': 14,
     'errors out': 15}

def smart_bps(y, pos):
  """Formatter for Y axis, values are in bps/kbps/mbps/gbps"""
  if y < 1024:
    return "bps {:,.2f}".format(y)
  elif y < 1048576:
    return "Kbps {:,.2f}".format(y / 1024)
  elif y < 1073741824:
    return "Mbps {:,.2f}".format(y / (1024 * 1024))
  return "Gbps {:,.2f}".format(y / (1024 * 1024 * 1024))

def smart_bits(y, pos):
  """Formatter for Y axis, values are in bits/kb/mb/gb"""
  if y < 1024:
    return "b {:,.2f}".format(y)
  elif y < 1048576:
    return "Kb {:,.2f}".format(y / 1024)
  elif y < 1073741824:
    return "Mb {:,.2f}".format(y / (1024 * 1024))
  return "Gb {:,.2f}".format(y / (1024 * 1024 * 1024))


def plot(csv_file, sampling_rate='10ms'):
    print('Processing %s' % csv_file)
    with open(csv_file) as csvfile:
        csvrd = csv.reader(csvfile, delimiter=';')
        data = [(float(row[COLS['bytes out/s']]), int(row[COLS['bytes out']])) for row in csvrd]
        speed_data = [datum[0] for datum in data]
        volume_data = [datum[1] for datum in data]

    fig = plt.figure()

    ax1 = plt.subplot(211)
    ax1.set_title('Network out usage during "%s"' % os.path.basename(csv_file)[:-4])
    ax1.set_xlabel('{} sampling'.format(sampling_rate))
    ax1.yaxis.set_major_formatter(FuncFormatter(smart_bps))
    ax1.plot(speed_data, 'g')

    ax2 = plt.subplot(212)
    ax2.set_xlabel('{} sampling'.format(sampling_rate))
    ax2.yaxis.set_major_formatter(FuncFormatter(smart_bits))
    ax2.plot(volume_data, 'b')

    fig.text(0.97, 0.01, 'Thales Signaling Solutions',
          fontsize=10, color='gray',
          ha='right', va='bottom', alpha=0.5)

    plt.tight_layout()
    return fig

def plot_to_png(csv_file, png_file, sampling_rate='10ms', dpi=100):
    fig = plot(csv_file, sampling_rate)
    fig.savefig(png_file, dpi=dpi)

def main():
    parser = argparse.ArgumentParser(description='An outbound network traffic plotter.')
    parser.add_argument('-f', '--folder',
                 dest='folder',
                 default=None,
                 help='The data folder')
    parser.add_argument('-r', '--rate',
                 dest='sampling_rate',
                 default=None,
                 help='The bwm-ng sampling rate')
    parser.add_argument('-d', '--dpi',
                 dest='dpi',
                 default=None,
                 help='The PNG DPI')
    args = parser.parse_args()

    locale.setlocale(locale.LC_ALL, 'en_US.utf8')

    for f in glob.glob('{}/*.csv'.format(args.folder)):
        plot_to_png(f, '%s.png' % f[:-4], sampling_rate=args.sampling_rate, dpi=int(args.dpi))

if __name__ == '__main__':
    main()
