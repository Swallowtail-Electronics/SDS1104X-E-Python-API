from SCPI import SCPI
import datetime

class SDS1104:
    """
    Class for interacting with the SDS110 Siglent Digital Oscilliscope
    """

    class SDSException(Exception):
        '''
        Exception raised when a call returns an error message
        '''
        def __init__(self, code, message):
            self.code = code
            self.message = message
            super().__init__(self.message)

        def __str__(self):
            return f'Error Code: {self.code} -> {self.message}'
            

    scpi = None
    manufacturer = ""
    product_type = ""
    series_number = ""
    software_version = ""

    def __get_product_info(self):
        '''
        Query the manufacturer, product type, series, series no., software version, hardware version
        '''
        self.scpi.send("*IDN?")
        response = self.scpi.recv()
        resp_arr = response.split(",")
        self.manufacturer = resp_arr[0]
        self.product_type = resp_arr[1]
        self.series_number = resp_arr[2]
        self.software_version = resp_arr[3]

    def __send_cmd(self, cmd):
        '''
        Generic call to send command with error checking
        '''
        self.scpi.send(cmd)
        # Check for an error in regards to that command
        self.check_error()

    def xy_display(self, state:bool):
        '''
        The XY_DISPLAY command enables or disables the display the XY format
        '''
        if state:
            self.scpi.send('XY_DISPLAY ON')
        else:
            self.scpi.send('XY_DISPLAY OFF')

    def buzz(self, state:bool):
        '''
        Control the built-in piezo-buzzer.
        '''
        
        temp = ''
        self.scpi.send('BUZZER?')
        temp = self.scpi.recv()
        # TODO Is the buzzer already on?

        if state:
            self.scpi.send('BUZZ ON')
        else:
            self.scpi.send('BUZZ OFF')

    def coupling_mode(self, channel:int, mode):
        '''
        
        '''
        # TODO THIS FUNCTION MAKES THE SCOPE FREEZE
        if mode not in ['A1M', 'D1M', 'D50', 'A50', 'GND', 'AC', 'DC']:
            raise self.SDSException(666, "Invalid Coupling Type must select from ['A1M', 'D1M', 'D50', 'A50', 'GND', 'AC', 'DC']")
        if mode == 'AC':
            mode = 'A1M'
        elif mode == 'DC':
            mode = 'D1M'
        self.scpi.send(f'C{str(channel)}: CPL {mode}')

    def time_div(self, time_div:str):
        '''
        
        '''
        # Convert the time to 
        self.scpi.send(f'TDIV {time_div}')

    def to_csv(self, depth:str='MAX', save:bool=False):
        '''
        
        '''
        if save:
            self.scpi.send(f'CSV_SAVE DD,{depth},SAVE,OFF')
        else:
            self.scpi.send(f'CSV_SAVE DD,{depth},SAVE,ON')

    def display_channel(self, channel:int, state:bool):
        '''
        
        '''
        if state:
            self.scpi.send(f'C{channel}: TRA ON')
        else:
            self.scpi.send(f'C{channel}: TRA OFF')

    def get_waveform(self, channel:int, section:str='ALL'):
        '''
        
        '''
        # TODO Waveform Setup Command needs to be called
        temp = ''
        # self.scpi.send(f'TEMPLATE?')
        # temp = self.scpi.recv(100000)
        # temp += self.scpi.recv(100000)
        # temp += self.scpi.recv(100000)
        print(temp)
        print("-----")
        self.scpi.send(f'C{channel}: WF? {section}')
        return self.scpi.recv()


    def preform_internal_calibration(self):
        '''
        
        '''
        self.scpi.send('*CAL?')

    def get_datetime(self):
        '''
        Query the machine for the datetime

        TODO return datetime object
        '''
        self.scpi.send("DATE?")
        datetime_str = self.scpi.recv()
        return datetime_str

    def change_datetime(self, date):
        '''
        The DATE command changes the date/time of the oscilloscope's internal real-time clock. 
        
        NOTE: The command is only used in the CFL series instrument.
        '''
        month = 'JAN'
        if date.month == 1:
            month = 'JAN'
        elif date.month == 2:
            month = 'FEB'
        elif date.month == 3:
            month = 'MAR'
        elif date.month == 4:
            month = 'APR'
        elif date.month == 5:
            month = 'MAY'
        elif date.month == 6:
            month = 'JUN'
        elif date.month == 7:
            month = 'JUL'
        elif date.month == 8:
            month = 'AUG'
        elif date.month == 9:
            month = 'SEP'
        elif date.month == 10:
            month = 'OCT'
        elif date.month == 11:
            month = 'NOV'
        elif date.month == 12:
            month = 'DEC'

        #self.scpi.send(f'DATE {date.day}, {month}, {date.year}, {date.hour}, {date.minute}, {date.second}')

    def check_error(self):
        '''
        Check for an error on the system
        '''
        self.scpi.send("SYSTem:ERRor?")
        response = self.scpi.recv()
        resp_list = response.split('  ')
        # If error code zero do not raise exception, move along
        if resp_list[0] == '0':
            return False
        # Remove the newline at the end of the message
        resp_list[1] = resp_list[1][:-1]
        # Raise a response with the error code and message
        raise self.SPD3303Exception(resp_list[0], resp_list[1])

    def check_version(self):
        '''
        Query the software version of the equipment
        '''
        self.scpi.send("SYSTem:VERSion?")
        return self.scpi.recv()

    def check_status(self):
        '''
        Return the top level info about the power supply functional status
        '''
        self.scpi.send("SYSTem:STATus?")
        return self.scpi.recv()

    def assign_ip_addr(self, ip):
        '''
        Assign a static Internet Protocol (IP) address for the instrument
        WARING: This command is invalid when DHCP is on
        '''
        self.__send_cmd(f"IPaddr {ip}")

    def query_ip_addr(self):
        '''
        Query the static Internet Protocol (IP) address for the instrument
        '''
        self.scpi.send(f"IPaddr?")
        return self.scpi.recv()

    def assign_subnet_mask(self, subnet_mask):
        '''
        Assign a subnet mask for the instrument
        WARING: This command is invalid when DHCP is on
        '''
        self.__send_cmd(f"MASKaddr {subnet_mask}")

    def query_subnet_mask(self):
        '''
        Query the subnet mask for the instrument
        '''
        self.scpi.send(f"MASKaddr?")
        return self.scpi.recv()

    def assign_gate_address(self, gate_addr):
        '''
        Assign a gate address for the instrument
        WARING: This command is invalid when DHCP is on
        '''
        self.__send_cmd(f"GATEaddr {gate_addr}")

    def query_subnet_mask(self):
        '''
        Query the gate address for the instrument
        WARING: This command is invalid when DHCP is on
        '''
        self.scpi.send(f"GATEaddr?")
        return self.scpi.recv()
    
    def dhcp(self, state:bool):
        '''
        Turn on or off DHCP
        '''
        if state:
            self.scpi.send(f"DHCP ON")
        else:
            self.scpi.send(f"DHCP OFF")

    def query_dhcp(self):
        '''
        Query to see the status of DHCP
        '''
        self.scpi.send(f"DHCP?")
        return self.scpi.recv()

    def close(self):
        '''
        Close the socket connection
        '''
        self.scpi.close()

    def __init__(self, ip):
        '''
        Init the SCPI connection and get the basic product info
        '''
        self.scpi = SCPI(ip, 5025)
        self.__get_product_info()
        self.change_datetime(datetime.datetime.now())
            