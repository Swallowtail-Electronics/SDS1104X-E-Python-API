from SDS1104 import SDS1104
import time

def main():
    """
    Program logic main implementation
    """
    os = SDS1104('192.168.1.31')

    print(f"Made by {os.manufacturer}\nModel Number: {os.product_type}\nSeries Number: {os.series_number}\nSoftware Version: {os.software_version}")
    data = os.get_waveform(4, 'DAT2')
    print(data)
    os.close()

if __name__ == '__main__':
    main()