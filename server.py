import os
# from zipfile import ZipFile
import argparse
import bottle
from bottle import Bottle, run, route, static_file, template, request, redirect, url

from netplot.netplot import plot_to_png
from netplot.helpers import timestamp_string
PLOTS_DIR = 'plots'
UPLOAD_DIR = 'uploads'

bottle.TEMPLATE_PATH.append('templates')

def save_upload(upload):
    upload_path = os.path.join(UPLOAD_DIR, upload.filename)
    with open(upload_path, 'wb') as f:
            f.write(upload.file.read())
    return upload_path

def make_png_plot(csv_path, csv_name, sampling_rate, dpi):
    png_file_name = '{}_{}.png'.format(timestamp_string(), csv_name)
    png_path = os.path.join(PLOTS_DIR, png_file_name)
    plot_to_png(csv_path, png_path, sampling_rate, dpi)
    return png_file_name

@route('/')
def index():
    redirect('/upload')

@route('/upload', name='upload', method='GET')
def upload_form():
    return template('upload')

@route('/upload', method='POST')
def do_upload():
    csv_file = request.files.get('csv-upload')
    csv_name, csv_ext = os.path.splitext(csv_file.filename)
    if csv_ext not in ('.csv','.CSV'):
        redirect('/upload')

    csv_path = save_upload(csv_file)

    sampling_rate = request.forms.get('sampling-rate')
    dpi = int(request.forms.get('dpi'))

    png_file = make_png_plot(csv_path, csv_name, sampling_rate, dpi)
    redirect('/download/{}'.format(png_file))

@route('/download/<png_file>', method='GET')
def download(png_file):
    return template('download.html', png_file=png_file)

@route('/direct-download/<png_file>', method='GET')
def direct_download(png_file):
    return static_file(png_file, root=PLOTS_DIR, download=png_file)

def main():
    parser = argparse.ArgumentParser(description='Web GUI server for netplot.')
    parser.add_argument('-a', '--address',
                 dest='host',
                 default='localhost')
    parser.add_argument('-p', '--port',
                 dest='port',
                 default='12345')
    args = parser.parse_args()
    run(host=args.host, port=args.port, debug=True, reloader=True)

if __name__ == '__main__':
    main()
