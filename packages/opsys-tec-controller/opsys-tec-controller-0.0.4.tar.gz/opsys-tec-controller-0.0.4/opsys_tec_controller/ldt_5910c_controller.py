from opsys_tec_controller.tec_abstract import TecAbstract
import pyvisa
import pandas as pd
import time
import numpy as np


class Idt5910cController(TecAbstract):
    """
    IDT-5910C Device Interface 
    --------------------------
    Thermoelectric Temperature Controllers
    ______________________________________
    
    This class provides an interface to interact with the IDT-5910C device.
    It extends the TecAbstract class and implements methods to control and 
    monitor the device's operations.
    """

    _sleep_time = 0.3

    def __init__(self, device_address, lut_filepath):
        """
        Constructor

        Args:
            device_address (str): Device address
            lut_filepath (str): Resistance to temperature LUT
        """
        self._device_address = device_address
        self._resistance_to_temp_db = None
        self._filepath = lut_filepath
        self.device = None

        self.rm = pyvisa.ResourceManager()

    def _send_command(self, command):
        """
        Send command to device

        Args:
            command (str): Input command
        """
        self.device.write(command)

    def _query(self, command):
        """
        Get query result from device

        Args:
            command (str): Query command

        Returns:
            str: Query result
        """
        self.device.write(command)
        response = self.device.read()
        return response.strip()

    def load_lut(self, lut_filepath=None):
        """
        Loads the temperature to resistance lookup table (LUT) from a CSV file.

        Args:
            lut_filepath (str, optional): The file path to the resistance to temperature LUT CSV file.
                                        If None, the default file path stored in self._filepath is used.
                                        Defaults to None.

        Notes:
            The CSV file should have columns "Nom" and "Temp" where "Nom" represents nominal resistances
            and "Temp" represents corresponding temperatures.

        Example:
            >>> device.load_lut("path/to/lut.csv")
            # Loads the LUT from the specified file path
        """
        self._filepath = self._filepath if lut_filepath is None else lut_filepath
        self._resistance_to_temp_db = pd.read_csv(self._filepath)

        self.nom_resistances = list(
            self._resistance_to_temp_db["Nom"][1:].astype("float")
        )
        self.temps = list(self._resistance_to_temp_db["Temp"][1:].astype("float"))

    def connect(self):
        """
        Connect to device

        Returns:
            bool: Connection status.
                  True if connected, else False.
        """
        # Load temp/resistance conversion table
        if self._resistance_to_temp_db is None:
            self.load_lut()

        try:
            self.device = self.rm.open_resource(self._device_address)
            print(f"Connected to device: {self.device}")
            return True
        except Exception as e:
            print(f"Failed to connect to device: {self._device_address}. {e}")
            return False

    def disconnect(self):
        """
        Disconnect from device
        """
        self.device.close()

    def device_on(self):
        """
        Turns on the instrument's output.

        This method sends a command to the device to enable the output. It sets the output state to `ON` (or `1`), allowing the
        instrument to begin or resume its output functionality.

        Notes:
            - Ensure that the device is properly configured and ready before enabling the output.
            - If there are any error conditions, the output may not turn on as expected. Use the `is_on()` method to confirm the
            output state.

        Example:
            >>> device.device_on()
            # Sends the command to turn on the output
        """
        self._send_command(":OUTPut 1")

    def device_off(self):
        """
        Turns off the instrument's output.

        This method sends a command to the device to disable the output. It sets the output state to `OFF` (or `0`), ensuring the
        instrument's output is no longer active.

        Notes:
            - This method does not verify whether the output has successfully turned off. Use the `is_on()` method to confirm the
            output state if needed.
            - Disabling the output can be necessary during error conditions or when the device is not actively in use.

        Example:
            >>> device.device_off()
            # Sends the command to turn off the output
        """
        self._send_command(":OUTPut 0")

    def device_reset(self):
        """
        Reset TEC

        This method turns off the device, waits for a predefined sleep time, and then turns the device back on.
        """
        self.device_off()
        time.sleep(self._sleep_time)
        self.device_on()

    def set_temperature(self, temperature):
        """
        Set temperature value, using corresponding resistance value

        Args:
            temperature (int): Temperature setpoint.
        """
        try:
            resistance = np.interp(temperature, self.temps, self.nom_resistances)
            self.set_sensor_value(resistance * 1000)
        except Exception as e:
            print(f"Input value is out of defined range - {temperature}. {e}")

    def get_temperature(self):
        """
        Get the current temperature from the device.

        Returns:
            float: The current temperature in degrees Celsius.
        """
        try:
            resistance = float(self.get_sensor_value()) / 1000
            temperature = np.interp(
                resistance, self.nom_resistances[::-1], self.temps[::-1]
            )

        except Exception as e:
            print(f"Error reading temperature for R={resistance} (ohm)!. {e}")
            temperature = -999

        return temperature

    def scan_temperature(self, scan_time):
        """
        Scan temperature value

        Args:
            scan_time (float): Scanning time in sec.

        Returns:
            list: temperature samples list
        """
        samples = []
        start_time = time.time()
        while time.time() - start_time < scan_time:
            samples.append(self.get_temperature())
            time.sleep(self._sleep_time)
        return samples

    def get_device_id(self):
        """
        Retrieves the instrument's identification string.

        This method sends a query to the instrument to request its identification information. The response typically includes
        details such as the manufacturer, model number, serial number, and firmware version in a comma-separated format.

        Returns:
            str: A string containing the instrument's identification information.
                The format is typically: "Manufacturer,Model Number,Serial Number,Firmware Revision".

        Notes:
            - This method does not require any parameters to be passed.
            - Ensure the device is properly connected before invoking this method.

        Example:
            >>> device_id = device.get_device_id()
            >>> print(device_id)
            "ILX Lightwave,LDT-5910C,59101111,1.00-1.00"
        """
        return self._query("*IDN?")

    def clear_status(self):
        """
        Clears all status event registers and the error queue.

        This method sends the *CLS command to the device to clear all status event registers and the error queue.

        Example:
            >>> device.clear_status()
            # Sends the command to clear status
        """
        self._send_command("*CLS")

    def set_standard_event_status_enable(self, value):
        """
        Sets the bits in the standard event status enable register.

        Args:
            value (int): The value must be between 0 and 255.

        Example:
            >>> device.set_standard_event_status_enable(40)
            # Sets the standard event status enable register to enable bit 5 of the status byte register
        """
        self._send_command(f"*ESE {value}")

    def get_standard_event_status_enable(self):
        """
        Determines the contents of the standard event status enable register.

        Returns:
            int: The value between 0 and 255 representing the bits of the standard event status enable register.

        Example:
            >>> status_enable = device.get_standard_event_status_enable()
            >>> print(status_enable)
            68
        """
        return self._query("*ESE?")

    def get_standard_event_status_register(self):
        """
        Determines the contents of the standard event status register.

        Returns:
            int: The value between 0 and 255 representing the bits of the standard event status register.

        Example:
            >>> status_register = device.get_standard_event_status_register()
            >>> print(status_register)
            32
        """
        return self._query("*ESR?")

    def get_identification(self):
        """
        Requests the instrument to identify itself.

        Returns:
            str: A string containing the instrument's identification information.

        Example:
            >>> identification = device.get_identification()
            >>> print(identification)
            "ILX Lightwave,LDT-5910C,59101111,1.00-1.00"
        """
        return self._query("*IDN?")

    def set_operation_complete(self):
        """
        Sets the operation complete bit (bit 0) in the standard event status register when all pending overlapped commands have been completed.

        Example:
            >>> device.set_operation_complete()
            # Sets the operation complete bit
        """
        self._send_command("*OPC")

    def get_operation_complete(self):
        """
        Places an ASCII character 1 into the instrument’s output queue when all pending operations have been finished.

        Returns:
            str: The ASCII character "1" when all overlapped commands are complete.

        Example:
            >>> operation_complete = device.get_operation_complete()
            >>> print(operation_complete)
            "1"
        """
        return self._query("*OPC?")

    def set_power_on_status_clear(self, value):
        """
        Sets automatic power-on clearing of the enable registers.

        Args:
            value (int): A number that rounds to the integer zero disables the power-on clearing of enable register while any other number enables the power-on clearing of enable registers.

        Example:
            >>> device.set_power_on_status_clear(1)
            # Enables automatic power-on clearing of the enable registers
        """
        self._send_command(f"*PSC {value}")

    def get_power_on_status_clear(self):
        """
        Requests the status of the power-on status clear flag.

        Returns:
            int: 0 if the enable registers are saved through power off/on, 1 if the enable registers are cleared during power on.

        Example:
            >>> power_on_status_clear = device.get_power_on_status_clear()
            >>> print(power_on_status_clear)
            1
        """
        return self._query("*PSC?")

    def recall(self, bin_value):
        """
        Recalls a stored setup configuration from memory.

        Args:
            bin_value (int): A value from 0 to 10.

        Example:
            >>> device.recall(0)
            # Recalls the factory-set default configuration
        """
        self._send_command(f"*RCL {bin_value}")

    def reset(self):
        """
        Performs a device reset.

        This method sends the *RST command to the device to reset it.

        Notes:
            1. Clears *OPC or *OPC? device requirements.
            2. Stops operation of overlapped commands.
            3. Sets all device specific functions to a known state (*RST Value).
            The reset command does NOT affect the following:
            1. Output Queue.
            2. Enable Registers.
            3. Event Registers.
            4. *PSC state.
            5. Memory contents associated with *SAV.

        Example:
            >>> device.reset()
            # Sends the command to reset the device
        """
        self._send_command("*RST")

    def save(self, bin_value):
        """
        Saves the current instrument configuration to non-volatile memory.

        Parameters:
            bin_value (int): A value from 1 to 10.

        Notes:
            The *SAV operation saves the contents of everything affected by the *RST command.
            It is not necessary to save the current setup for next power-on. The current setup is automatically stored and recalled at next power-on.
            Use *RCL <bin> to restore the saved configuration.

        Example:
            >>> device.save(3)
            # The current instrument configuration is stored in memory bin 3
        """
        self._send_command(f"*SAV {bin_value}")

    def set_service_request_enable(self, value):
        """
        Sets the service request enable register bits.

        Parameters:
            value (int): A value in the range of 0 to 255.

        Notes:
            The integer sent as a parameter when expressed in binary format, each bit represents a bit in the service request enable register.
            A bit value of one indicates an enabled condition. A bit value of zero indicates a disabled condition. Bit 6 will be ignored.
            Setting the service request enable register allows the programmer to select which summary messages in the status byte register may cause service requests.
            Each bit in the service request enable register corresponds to a bit in the status byte register.
            A service request is generated when a bit in either the service request enable register or the status byte register transitions from zero to one and the corresponding bit in the other register is either set to one or transitions from zero to one at the same time.

        Example:
            >>> device.set_service_request_enable(16)
            # Enables the service request enable register to generate a service request when a query generating message is available to read from the output queue.
        """
        self._send_command(f"*SRE {value}")

    def get_service_request_enable(self):
        """
        Returns the enabled bits in the service request enable register.

        Returns:
            int: The response is a value between 0 and 255, representing the bits of the standard event status enable register when expressed in base 2 binary format.

        Example:
            >>> device.get_service_request_enable()
            # A response of 16 signifies that the message available summary bit is enabled
        """
        return self._query("*SRE?")

    def get_status_byte(self):
        """
        Returns the value of the status byte register.

        Returns:
            int: The response is the sum of the enabled bits and must be a value between 0 and 255.

        Example:
            >>> device.get_status_byte()
            # A response of 200 specifies that the TEC condition summary, master status summary and error available bits are enabled
        """
        return self._query("*STB?")

    def self_test(self):
        """
        Performs an internal self-test and then reports results.

        Returns:
            int: Response 0 = test completed with no errors, Response 1 = test completed with errors.

        Notes:
            This is a synchronous command and will block other commands from execution until it has completed.

        Example:
            >>> device.self_test()
            # A response of 0 means tests completed without errors
        """
        return self._query("*TST?")

    def wait_to_continue(self):
        """
        Prevents the instrument from executing any further commands until all pending operations are complete.

        Notes:
            This command can be used to make the instrument wait until an operation is complete before continuing.
            Care should be taken to set the time-out appropriately for use with the *WAI command. After this command is sent, the instrument may block subsequent commands waiting for the input queue to empty.

        Example:
            >>> device.wait_to_continue()
            # The temperature measurement will occur after the output is on
        """
        self._send_command("*WAI")

    def set_analog_input(self, value):
        """
        Enables the analog input rear panel BNC to be used for temperature modulation.

        Parameters:
            value (str): ON/1 – Temperature Modulation ON, OFF/0 – Temperature Modulation OFF.

        Example:
            >>> device.set_analog_input("ON")
            # Enables the analog input for temperature modulation
        """
        self._send_command(f":ANAloginput {value}")

    def get_analog_input(self):
        """
        Determines if the analog input rear panel BNC is used for temperature modulation.

        Returns:
            str: ON/1 – Temperature Modulation ON, OFF/0 – Temperature Modulation OFF.

        Example:
            >>> device.get_analog_input()
            # Returns the current state of the analog input
        """
        return self._query(":ANAloginput?")

    def set_cable_resistance(self, ohms):
        """
        Sets the output cable resistance used to improve the accuracy of the MEASure:VTE? command.

        Parameters:
            ohms (float): Cable resistance.

        Notes:
            Voltage measurement subtracts this resistance multiplied by output current to get actual voltage.

        Example:
            >>> device.set_cable_resistance(0.02)
            # Sets the cable resistance to 0.02 ohms
        """
        self._send_command(f":CABLER {ohms}")

    def get_cable_resistance(self):
        """
        Gets the output cable resistance value.

        Returns:
            float: The current cable resistance value.

        Example:
            >>> resistance = device.get_cable_resistance()
            >>> print(resistance)
            0.02
        """
        return self._query(":CABLER?")

    def set_ici_constants(self, slope, offset):
        """
        Sets the slope and offset compensation for a temperature to current transducer.

        Args:
            slope (float): The µA/K response of the temperature to current transducer.
            offset (float): The sensor offset in µA.

        Example:
            >>> device.set_ici_constants(1.0, 0.0)
            # Sets the slope to 1.0 µA/K and offset to 0.0 µA
        """
        self._send_command(f":CONST:ICI {slope},{offset}")

    def get_ici_constants(self):
        """
        Gets the slope and offset compensation for a temperature to current transducer.

        Returns:
            tuple: The slope and offset values.

        Example:
            >>> slope, offset = device.get_ici_constants()
            >>> print(slope, offset)
            1.0, 0.0
        """
        return self._query(":CONST:ICI?")

    def set_ici_slope(self, slope):
        """
        Sets the slope compensation for a temperature to current transducer.

        Args:
            slope (float): The µA/K response of the temperature to current transducer.

        Example:
            >>> device.set_ici_slope(1.0)
            # Sets the slope to 1.0 µA/K
        """
        self._send_command(f":CONST:ICI:SLOPe {slope}")

    def get_ici_slope(self):
        """
        Gets the slope compensation for a temperature to current transducer.

        Returns:
            float: The slope value.

        Example:
            >>> slope = device.get_ici_slope()
            >>> print(slope)
            1.0
        """
        return self._query(":CONST:ICI:SLOPe?")

    def set_ici_offset(self, offset):
        """
        Sets the offset compensation for a temperature to current transducer.

        Args:
            offset (float): The sensor offset in µA.

        Example:
            >>> device.set_ici_offset(0.0)
            # Sets the offset to 0.0 µA
        """
        self._send_command(f":CONST:ICI:OFFSet {offset}")

    def get_ici_offset(self):
        """
        Gets the offset compensation for a temperature to current transducer.

        Returns:
            float: The offset value.

        Example:
            >>> offset = device.get_ici_offset()
            >>> print(offset)
            0.0
        """
        return self._query(":CONST:ICI:OFFSet?")

    def set_icv_constants(self, slope, offset):
        """
        Sets the slope and offset compensation for a temperature to voltage transducer.

        Args:
            slope (float): The mV/K response of the temperature to voltage transducer.
            offset (float): The sensor offset in mV.

        Example:
            >>> device.set_icv_constants(10.0, 0.0)
            # Sets the slope to 10.0 mV/K and offset to 0.0 mV
        """
        self._send_command(f":CONST:ICV {slope},{offset}")

    def get_icv_constants(self):
        """
        Gets the slope and offset compensation for a temperature to voltage transducer.

        Returns:
            tuple: The slope and offset values.

        Example:
            >>> slope, offset = device.get_icv_constants()
            >>> print(slope, offset)
            10.0, 0.0
        """
        return self._query(":CONST:ICV?")

    def set_icv_slope(self, slope):
        """
        Sets the slope compensation for a temperature to voltage transducer.

        Args:
            slope (float): The mV/K response of the temperature to voltage transducer.

        Example:
            >>> device.set_icv_slope(10.0)
            # Sets the slope to 10.0 mV/K
        """
        self._send_command(f":CONST:ICV:SLOPe {slope}")

    def get_icv_slope(self):
        """
        Gets the slope compensation for a temperature to voltage transducer.

        Returns:
            float: The slope value.

        Example:
            >>> slope = device.get_icv_slope()
            >>> print(slope)
            10.0
        """
        return self._query(":CONST:ICV:SLOPe?")

    def set_icv_offset(self, offset):
        """
        Sets the offset compensation for a temperature to voltage transducer.

        Args:
            offset (float): The sensor offset in mV.

        Example:
            >>> device.set_icv_offset(0.0)
            # Sets the offset to 0.0 mV
        """
        self._send_command(f":CONST:ICV:OFFSet {offset}")

    def get_icv_offset(self):
        """
        Gets the offset compensation for a temperature to voltage transducer.

        Returns:
            float: The offset value.

        Example:
            >>> offset = device.get_icv_offset()
            >>> print(offset)
            0.0
        """
        return self._query(":CONST:ICV:OFFSet?")

    def set_rtd_constants(self, a, b, c, r0):
        """
        Sets the Callendar-Van Dusen coefficients for an RTD temperature transducer.

        Args:
            a (float): The first coefficient of the Callendar-Van Dusen equation multiplied by 10^-3 °C^-1.
            b (float): The second coefficient of the Callendar-Van Dusen equation multiplied by 10^-7 °C^-2.
            c (float): The third coefficient of the Callendar-Van Dusen equation multiplied by 10^-12 °C^-3.
            r0 (float): The resistance of the transducer at 0 °C, adjustable from 0 to 9999.9 Ohm.

        Example:
            >>> device.set_rtd_constants(3.908, -5.775, -4.183, 100.0)
            # Sets the RTD coefficients
        """
        self._send_command(f":CONST:RTD {a},{b},{c},{r0}")

    def get_rtd_constants(self):
        """
        Gets the Callendar-Van Dusen coefficients for an RTD temperature transducer.

        Returns:
            tuple: The coefficients a, b, c, and r0.

        Example:
            >>> a, b, c, r0 = device.get_rtd_constants()
            >>> print(a, b, c, r0)
            3.908, -5.775, -4.183, 100.0
        """
        return self._query(":CONST:RTD?")

    def set_thermistor_constants(self, c1, c2, c3):
        """
        Sets the Steinhart-Hart parameters for a thermistor temperature transducer.

        Args:
            c1 (float): The first parameter of the Steinhart-Hart equation multiplied by 10^-3.
            c2 (float): The second parameter of the Steinhart-Hart equation multiplied by 10^-4.
            c3 (float): The third parameter of the Steinhart-Hart equation multiplied by 10^-7.

        Example:
            >>> device.set_thermistor_constants(1.125, 2.347, 0.855)
            # Sets the Steinhart-Hart coefficients
        """
        self._send_command(f":CONST:THERMistor {c1},{c2},{c3}")

    def get_thermistor_constants(self):
        """
        Gets the Steinhart-Hart parameters for a thermistor temperature transducer.

        Returns:
            tuple: The coefficients c1, c2, and c3.

        Example:
            >>> c1, c2, c3 = device.get_thermistor_constants()
            >>> print(c1, c2, c3)
            1.125, 2.347, 0.855
        """
        return self._query(":CONST:THERMistor?")

    def set_enable_condition(self, value):
        """
        Sets the device condition status enable register.

        Args:
            value (int): The value to set the condition status enable register.

        Example:
            >>> device.set_enable_condition(1)
            # Sets the condition status enable register
        """
        self._send_command(f":ENABle:COND {value}")

    def get_enable_condition(self):
        """
        Gets the device condition status enable register.

        Returns:
            int: The value of the condition status enable register.

        Example:
            >>> condition = device.get_enable_condition()
            >>> print(condition)
            1
        """
        return self._query(":ENABle:COND?")

    def set_enable_event(self, value):
        """
        Sets the device event status enable register.

        Args:
            value (int): The value to set the event status enable register.

        Example:
            >>> device.set_enable_event(1)
            # Sets the event status enable register
        """
        self._send_command(f":ENABle:EVEnt {value}")

    def get_enable_event(self):
        """
        Gets the device event status enable register.

        Returns:
            int: The value of the event status enable register.

        Example:
            >>> event = device.get_enable_event()
            >>> print(event)
            1
        """
        return self._query(":ENABle:EVEnt?")

    def set_enable_output_off(self, value):
        """
        Sets the device output off enable register.

        Args:
            value (int): The value to set the output off enable register.

        Example:
            >>> device.set_enable_output_off(1)
            # Sets the output off enable register
        """
        self._send_command(f":ENABle:OUTOFF {value}")

    def get_enable_output_off(self):
        """
        Gets the device output off enable register.

        Returns:
            int: The value of the output off enable register.

        Example:
            >>> output_off = device.get_enable_output_off()
            >>> print(output_off)
            1
        """
        return self._query(":ENABle:OUTOFF?")

    def get_errors(self):
        """
        Gets the list of errors which have occurred since the last ERR? request.

        Returns:
            str: ASCII character string: list of error numbers, separated by commas.

        Example:
            >>> errors = device.get_errors()
            >>> print(errors)
            "0"
        """
        return self._query(":ERRors?")

    def get_event(self):
        """
        Gets the value in the device event status register.

        Returns:
            int: The value of the event status register.

        Example:
            >>> event = device.get_event()
            >>> print(event)
            2048
        """
        return self._query(":EVEnt?")

    def set_fan(self, value):
        """
        Controls the external fan.

        Args:
            value (str): ON/1 to turn the fan on, OFF/0 to turn the fan off.

        Example:
            >>> device.set_fan("ON")
            # Turns the fan on
        """
        self._send_command(f":FAN {value}")

    def get_fan(self):
        """
        Gets the external fan state.

        Returns:
            str: ON/1 if the fan is on, OFF/0 if the fan is off.

        Example:
            >>> fan_state = device.get_fan()
            >>> print(fan_state)
            "ON"
        """
        return self._query(":FAN?")

    def set_fan_voltage(self, voltage):
        """
        Sets the external fan voltage.

        Args:
            voltage (float): The voltage to set for the external fan.

        Example:
            >>> device.set_fan_voltage(12.0)
            # Sets the fan voltage to 12.0 volts
        """
        self._send_command(f":FAN:VOLTage {voltage}")

    def get_fan_voltage(self):
        """
        Gets the external fan voltage.

        Returns:
            float: The voltage of the external fan.

        Example:
            >>> fan_voltage = device.get_fan_voltage()
            >>> print(fan_voltage)
            12.0
        """
        return self._query(":FAN:VOLTage?")

    def set_ite_high_limit(self, amps):
        """
        Sets the upper TEC current limit.

        Args:
            amps (float): The upper current limit in amps.

        Example:
            >>> device.set_ite_high_limit(2.5)
            # Sets the upper current limit to 2.5 amps
        """
        self._send_command(f":LIMit:ITE:HIgh {amps}")

    def get_ite_high_limit(self):
        """
        Gets the upper TEC current limit.

        Returns:
            float: The upper current limit in amps.

        Example:
            >>> high_limit = device.get_ite_high_limit()
            >>> print(high_limit)
            2.5
        """
        return self._query(":LIMit:ITE:HIgh?")

    def set_ite_low_limit(self, amps):
        """
        Sets the lower TEC current limit.

        Args:
            amps (float): The lower current limit in amps.

        Example:
            >>> device.set_ite_low_limit(-2.5)
            # Sets the lower current limit to -2.5 amps
        """
        self._send_command(f":LIMit:ITE:LOw {amps}")

    def get_ite_low_limit(self):
        """
        Gets the lower TEC current limit.

        Returns:
            float: The lower current limit in amps.

        Example:
            >>> low_limit = device.get_ite_low_limit()
            >>> print(low_limit)
            -2.5
        """
        return self._query(":LIMit:ITE:LOw?")

    def set_display(self, value):
        """
        Sets the display state.

        Args:
            value (str): ON/1 to turn the display on, OFF/0 to turn the display off.

        Example:
            >>> device.set_display("ON")
            # Turns the display on
        """
        self._send_command(f":DISPLay {value}")

    def get_display(self):
        """
        Gets the display state.

        Returns:
            str: ON/1 if the display is on, OFF/0 if the display is off.

        Example:
            >>> display_state = device.get_display()
            >>> print(display_state)
            "ON"
        """
        return self._query(":DISPLay?")

    def set_display_brightness(self, brightness):
        """
        Sets the display brightness.

        Args:
            brightness (int): The brightness level from 1 to 10.

        Example:
            >>> device.set_display_brightness(5)
            # Sets the display brightness to 5
        """
        self._send_command(f":DISPLay:BRIGHTness {brightness}")

    def get_display_brightness(self):
        """
        Gets the display brightness.

        Returns:
            int: The brightness level from 1 to 10.

        Example:
            >>> brightness = device.get_display_brightness()
            >>> print(brightness)
            5
        """
        return self._query(":DISPLay:BRIGHTness?")

    def set_sensor_high_limit(self, value):
        """
        Sets the more positive sensor measurement limit.

        Args:
            value (float): The sensor measurement limit.

        Example:
            >>> device.set_sensor_high_limit(4501.0)
            # Sets the sensor upper limit to 4501.0
        """
        self._send_command(f":LIMit:SENsor:HIgh {value}")

    def get_sensor_high_limit(self):
        """
        Gets the more positive sensor measurement limit.

        Returns:
            float: The sensor measurement limit.

        Example:
            >>> high_limit = device.get_sensor_high_limit()
            >>> print(high_limit)
            4501.0
        """
        return self._query(":LIMit:SENsor:HIgh?")

    def set_sensor_low_limit(self, value):
        """
        Sets the more negative sensor measurement limit.

        Args:
            value (float): The sensor measurement limit.

        Example:
            >>> device.set_sensor_low_limit(450.0)
            # Sets the sensor lower limit to 450.0
        """
        self._send_command(f":LIMit:SENsor:LOw {value}")

    def get_sensor_low_limit(self):
        """
        Gets the more negative sensor measurement limit.

        Returns:
            float: The sensor measurement limit.

        Example:
            >>> low_limit = device.get_sensor_low_limit()
            >>> print(low_limit)
            450.0
        """
        return self._query(":LIMit:SENsor:LOw?")

    def set_temp_high_limit(self, degrees):
        """
        Sets the more positive temperature limit at which the temperature controller will turn off.

        Args:
            degrees (float): The maximum temperature in degrees Celsius.

        Example:
            >>> device.set_temp_high_limit(105.0)
            # Sets the high temperature limit to 105.0 ºC
        """
        self._send_command(f":LIMit:Temp:HIgh {degrees}")

    def get_temp_high_limit(self):
        """
        Gets the more positive temperature limit at which the temperature controller will turn off.

        Returns:
            float: The maximum temperature in degrees Celsius.

        Example:
            >>> high_limit = device.get_temp_high_limit()
            >>> print(high_limit)
            105.0
        """
        return self._query(":LIMit:Temp:HIgh?")

    def set_temp_low_limit(self, degrees):
        """
        Sets the more negative temperature limit at which the temperature controller will turn off.

        Args:
            degrees (float): The minimum temperature in degrees Celsius.

        Example:
            >>> device.set_temp_low_limit(-20.0)
            # Sets the lower temperature limit to -20.0 ºC
        """
        self._send_command(f":LIMit:Temp:LOw {degrees}")

    def get_temp_low_limit(self):
        """
        Gets the more negative temperature limit at which the temperature controller will turn off.

        Returns:
            float: The minimum temperature in degrees Celsius.

        Example:
            >>> low_limit = device.get_temp_low_limit()
            >>> print(low_limit)
            -20.0
        """
        return self._query(":LIMit:Temp:LOw?")

    def set_tolerance(self, value):
        """
        Sets the settling tolerance for determining when *OPC is complete or an :EVENT? is set.

        Args:
            value (float): The settling value dependent on mode.

        Example:
            >>> device.set_tolerance(0.3)
            # Sets the tolerance window to +0.3 ºC
        """
        self._send_command(f":LIMit:TOLerance {value}")

    def get_measured_ite(self):
        """
        Measures the TEC current.

        Returns:
            float: The measured TEC current in Amps.

        Example:
            >>> current = device.get_measured_ite()
            >>> print(current)
            2.2
        """
        return self._query(":MEASure:ITE?")

    def get_measured_sensor(self):
        """
        Measures the sensor value.

        Returns:
            float: The measured sensor value in Ohms, µA, or Volts depending on the sensor type.

        Example:
            >>> sensor_value = device.get_measured_sensor()
            >>> print(sensor_value)
            0.0001323
        """
        return self._query(":MEASure:SENsor?")

    def get_measured_temp(self):
        """
        Measures the sensor temperature.

        Returns:
            float: The measured temperature in °C.

        Example:
            >>> temperature = device.get_measured_temp()
            >>> print(temperature)
            45.6
        """
        return self._query(":MEASure:Temp?")

    def get_measured_vte(self):
        """
        Measures the TEC voltage.

        Returns:
            float: The measured TEC voltage in Volts.

        Example:
            >>> voltage = device.get_measured_vte()
            >>> print(voltage)
            4.2
        """
        return self._query(":MEASure:VTE?")

    def set_mode(self, mode):
        """
        Configures the control mode of operation.

        Args:
            mode (str): The control mode (T, SENSOR, ITE).

        Example:
            >>> device.set_mode("T")
            # Sets the control mode to Temperature control mode
        """
        self._send_command(f":MODE {mode}")

    def get_mode(self):
        """
        Gets the current control mode of operation.

        Returns:
            str: The current control mode.

        Example:
            >>> mode = device.get_mode()
            >>> print(mode)
            "T"
        """
        return self._query(":MODE?")

    def set_output(self, value):
        """
        Controls whether the output is enabled or not.

        Args:
            value (str): ON/1 to turn the output on, OFF/0 to turn the output off.

        Example:
            >>> device.set_output("ON")
            # Turns the output on
        """
        self._send_command(f":OUTPut {value}")

    def get_output(self):
        """
        Gets the current state of the output.

        Returns:
            str: ON/1 if the output is on, OFF/0 if the output is off.

        Example:
            >>> output_state = device.get_output()
            >>> print(output_state)
            "ON"
        """
        return self._query(":OUTPut?")

    def set_pid(self, p, i, d):
        """
        Sets the PID control loop constants.

        Args:
            p (float): Proportional term.
            i (float): Integral term.
            d (float): Derivative term.

        Example:
            >>> device.set_pid(24.0, 5.6, 8.0)
            # Sets the PID constants
        """
        self._send_command(f":PID {p},{i},{d}")

    def get_pid(self):
        """
        Gets the PID control loop constants.

        Returns:
            tuple: The PID constants (P, I, D).

        Example:
            >>> p, i, d = device.get_pid()
            >>> print(p, i, d)
            24.0, 5.6, 8.0
        """
        return self._query(":PID?")

    def set_pid_autotune(self, value):
        """
        Controls the PID auto-tune functionality.

        Args:
            value (str): RUN to start auto-tuning, STOP to halt auto-tuning.

        Example:
            >>> device.set_pid_autotune("RUN")
            # Starts the PID auto-tuning
        """
        self._send_command(f":PID:ATUNE {value}")

    def get_pid_autotune(self):
        """
        Gets the status of the PID auto-tune functionality.

        Returns:
            str: The status of the PID auto-tune (IDLE, RUNNING, PASS, FAIL).

        Example:
            >>> status = device.get_pid_autotune()
            >>> print(status)
            "RUNNING"
        """
        return self._query(":PID:ATUNE?")

    def set_pid_preset(self, name):
        """
        Restores preset PID constants.

        Args:
            name (str): The name of the preset (e.g., DEFAULT, GAIN1, LDM4405).

        Example:
            >>> device.set_pid_preset("LDM4405")
            # Restores the PID constants for the LDM4405 mount
        """
        self._send_command(f":PID:PRESET {name}")

    def get_pid_preset(self):
        """
        Gets the current PID preset.

        Returns:
            str: The name of the current PID preset.

        Example:
            >>> preset = device.get_pid_preset()
            >>> print(preset)
            "LDM4405"
        """
        return self._query(":PID:PRESET?")

    def set_radix(self, value):
        """
        Sets the response data format for the status, event, and enable registers.

        Args:
            value (str): The data format (BINary, DECimal, HEXadecimal, OCTal).

        Example:
            >>> device.set_radix("DECimal")
            # Sets the data format to decimal
        """
        self._send_command(f":RADIX {value}")

    def get_radix(self):
        """
        Gets the current response data format for the status, event, and enable registers.

        Returns:
            str: The current data format.

        Example:
            >>> radix = device.get_radix()
            >>> print(radix)
            "DECimal"
        """
        return self._query(":RADIX?")

    def set_sensor(self, name):
        """
        Selects the sensor for temperature conversion and sensor mode.

        Args:
            name (str): The name of the sensor (e.g., ICI, ICV, THERM100UA).

        Example:
            >>> device.set_sensor("THERM100UA")
            # Sets the sensor to thermistor with 100 µA current source
        """
        self._send_command(f":SENsor {name}")

    def get_sensor(self):
        """
        Gets the current sensor selection.

        Returns:
            str: The name of the current sensor.

        Example:
            >>> sensor = device.get_sensor()
            >>> print(sensor)
            "THERM100UA"
        """
        return self._query(":SENsor?")

    def set_ite(self, amps):
        """
        Sets the constant current setpoint for use in ITE mode.

        Args:
            amps (float): The constant current setpoint in Amps.

        Example:
            >>> device.set_ite(2.5)
            # Sets the constant current setpoint to 2.5 A
        """
        self._send_command(f":SET:ITE {amps}")

    def get_ite(self):
        """
        Gets the constant current setpoint for use in ITE mode.

        Returns:
            float: The constant current setpoint in Amps.

        Example:
            >>> current_setpoint = device.get_ite()
            >>> print(current_setpoint)
            2.5
        """
        return self._query(":SET:ITE?")

    def set_sensor_value(self, value):
        """
        Sets the control setpoint for use in sensor mode.

        Args:
            value (float): The sensor-dependent value for the control point.

        Example:
            >>> device.set_sensor_value(0.002932)
            # Sets the control setpoint for the ICV sensor to 2.93 mV
        """
        self._send_command(f":SET:SENsor {value}")

    def get_sensor_value(self):
        """
        Gets the control setpoint for use in sensor mode.

        Returns:
            float: The sensor-dependent value for the control point.

        Example:
            >>> sensor_setpoint = device.get_sensor_value()
            >>> print(sensor_setpoint)
            0.002932
        """
        return self._query(":SET:SENsor?")

    def set_temp(self, degrees):
        """
        Sets the temperature setpoint for use in temperature mode.

        Args:
            degrees (float): The temperature setpoint in °C.

        Example:
            >>> device.set_temp(75.43)
            # Sets the temperature setpoint to 75.43 °C
        """
        self._send_command(f":SET:Temp {degrees}")

    def get_temp(self):
        """
        Gets the temperature setpoint for use in temperature mode.

        Returns:
            float: The temperature setpoint in °C.

        Example:
            >>> temp_setpoint = device.get_temp()
            >>> print(temp_setpoint)
            75.43
        """
        return self._query(":SET:Temp?")

    def get_condition_status(self):
        """
        Gets the contents of the device condition status register.

        Returns:
            int: The value of the condition status register.

        Example:
            >>> condition_status = device.get_condition_status()
            >>> print(condition_status)
            1
        """
        return self._query(":COND?")

    def get_status(self):
        """
        Gets the contents of the device status register.

        Returns:
            int: The value of the status register.

        Example:
            >>> status = device.get_status()
            >>> print(status)
            0x600
        """
        return self._query(":STATus?")

    def set_syntax(self, value):
        """
        Sets the unit for compatibility with LDT-5910B.

        Args:
            value (int): 0 for LDT-5910B compatibility, 1 for LDT-5910C and LDT-5940C default operation.

        Example:
            >>> device.set_syntax(0)
            # Sets the unit for LDT-5910B compatibility
        """
        self._send_command(f":SYNTAX {value}")

    def get_syntax(self):
        """
        Gets the current syntax setting.

        Returns:
            int: The current syntax setting.

        Example:
            >>> syntax = device.get_syntax()
            >>> print(syntax)
            0
        """
        return self._query(":SYNTAX?")
