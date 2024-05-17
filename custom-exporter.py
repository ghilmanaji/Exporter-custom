from prometheus_client import start_http_server, Gauge
import time
import subprocess

# Membuat metrik baru
CUSTOM_METRIC = Gauge('custom_metric', 'A custom metric from a bash script')

def run_bash_script():
    """Fungsi untuk menjalankan skrip bash dan mendapatkan hasilnya."""
    result = subprocess.run(['./example_script.sh'], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8').strip()
    return output

def update_metrics():
    """Fungsi untuk memperbarui metrik Prometheus."""
    output = run_bash_script()
    for line in output.split('\n'):
        try:
            name, value = line.split()
            if name == "custom_metric":
                CUSTOM_METRIC.set(float(value))
        except ValueError:
            # Tangani jika ada kesalahan dalam parsing
            continue

if __name__ == '__main__':
    # Mulai server HTTP untuk meng-ekspos metrik ke Prometheus
    start_http_server(8100)
    print("Exporter berjalan pada port 8000...")

    # Perbarui metrik setiap 5 detik
    while True:
        update_metrics()
        time.sleep(5)
