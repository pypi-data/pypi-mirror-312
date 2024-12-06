"""
zpl_label_designer

This module provides functionality for designing and printing labels in ZPL (Zebra Programming Language) format. 
It supports dynamic label generation, including text, QR codes, barcodes, and images, and integrates with thermal printers.
"""
from datetime import date
from flask import request, jsonify
from PIL import Image
import shutil
import subprocess
import os
from .table_operations import (
    DBTableOperations
)
from .config import logger
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ZPLLabelDesigner:
    """
    A class to design and print ZPL (Zebra Programming Language) labels.

    Attributes:
        dir_path (str): Directory path where label files are stored.
        printer_name (str): Name of the thermal printer.
    """
    def __init__(self, dir_path, printer_name):
        """
        Initializes the ZPLLabelDesigner with directory path and printer name.

        Args:
            dir_path (str): Directory path where label files are stored.
            printer_name (str): Name of the thermal printer.
        """
        self.dir_path = dir_path
        self.printer_name = printer_name
        self.default_generate_file = "label1.zpl"
        self.default_print_file = "label.zpl"
        
    def generate_zpl(self, file_name=None, input_data=None):
        """
        Generates a ZPL label based on input data from a JSON request or Python input.

        The function dynamically creates a ZPL script, including:
        - Text fields with customizable fonts and sizes.
        - Lines and rectangles with specified coordinates.
        - QR codes with dynamic sizing based on paper dimensions.
        - Barcodes with customizable positioning.
        - Logos resized to fit the label layout.

        The generated ZPL script is saved to a file and returned as a response.

        Args:
            file_name (str): Name of the file to save the ZPL script. Defaults to self.default_generate_file.
            input_data (dict): Data for generating ZPL, passed directly for Flask/Python calls.

        Returns:
            flask.Response or str: JSON response indicating success when called via HTTP,
                                or the file path of the saved ZPL file for Python calls.
        """
        logger.info("---------------------------------generate_zpl called----------------------")
        print("--------------------------------------------------- req method",file_name," req method",request.method)
            
        if not file_name or input_data:
            # Determine data source
            if request.method == "POST":
                data = request.get_json()
                logger.info("Received data for ZPL generation from HTTP request: %s", data)
        
        elif input_data is not None:
            data = input_data
            logger.info("Received data for ZPL generation from Python input: %s", data)
        # else:
        #     error_msg = "No input data provided for ZPL generation."
        #     logger.error(error_msg)
        #     if request.method == "POST":
        #         return jsonify({"success": False, "error": error_msg}), 400
        #     else:
        #         raise ValueError(error_msg)

        # Use default file name if none is provided
        file_name = file_name or self.default_generate_file
        logger.info("---------------- req method: %s",file_name)
        logger.info("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< ----------------- >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> data: %s",data)

        start = "^XA"
        end = "^XZ"
        label_pos = "^FT"
        label_text_tag = "^FD"
        change_font = "^CFA,30"
        start_of_field = "^FO"
        end_of_field = "^FS"

        input_labels = data['input_labels']
        text_values_co_ords = data['text_values_co_ords']
        input_qr_code = data['input_qr_code']
        input_barcode = data['input_barcode']
        barcode_cords = data['barcode_cords']
        qr_code_cords = data['qr_code_cords']
        line_co_ordinates = data['line_co_ordinates']
        rect_co_ordinates = data['rect_co_ordinates']
        font_size = data['font_size']
        font_weight = data['fontweight_array']
        image_data = data['image_data']

        code = [start]

        font_style = ['^CF0' if weight == 'bold' else '^AN' for weight in font_weight]
        for num, label in enumerate(input_labels):
            text_cords = text_values_co_ords[num]
            total_var = f"{font_style[num]},{font_size[num]}{start_of_field}{text_cords['x1']},{text_cords['y1']}{label_text_tag}{label}{end_of_field}"
            code.append(total_var)

        for line in line_co_ordinates:
            if line:
                if 0 < line['angle'] < 175 or 263 < line['angle'] < 280:
                    line_cmd = f"^FO{line['x1']},{line['y1']}^GB1,{line['x2']}^FS"
                else:
                    line_cmd = f"^FO{line['x1']},{line['y1']}^GB{line['x2']},1^FS"
                code.append(line_cmd)

        for rect in rect_co_ordinates:
            if rect:
                rect_cmd = f"^FO{rect['x1']},{rect['y1']}^GB{rect['x2']},{rect['y2']}^FS"
                code.append(rect_cmd)

        if input_barcode and barcode_cords:
            barcode_cmd = f"^FO{barcode_cords[0]['x1']},{barcode_cords[0]['y1']}^BY3^BCN,{barcode_cords[0]['width']},N,N,N^FD{input_barcode}^FS"
            code.append(barcode_cmd)
        # static qrcode size code comemnted
        # elif input_qr_code and qr_code_cords:
        #     qr_code_cmd = f"^FO{qr_code_cords[0]['x1']},{qr_code_cords[0]['y1']}^BQN,2,3^FD00{input_qr_code}^FS"
        #     code.append(qr_code_cmd)
        
        # Dynamic QR Code Sizing Based on Paper Size
        if input_qr_code and qr_code_cords:
            paper_width = data.get('paper_width', 800)  # Default to 800 dots (203 DPI: ~4 inches)
            paper_height = data.get('paper_height', 600)  # Default to 600 dots (203 DPI: ~3 inches)
            margin = int(0.05 * min(paper_width, paper_height))  # 5% margin

            # Calculate available space for the QR code
            max_qr_width = paper_width - qr_code_cords[0]['x1'] - margin
            max_qr_height = paper_height - qr_code_cords[0]['y1'] - margin
            max_qr_size = min(max_qr_width, max_qr_height)

            # Ensure the available space is sufficient for a readable QR code
            if max_qr_size < 50:  # Adjust based on printer readability
                raise ValueError("Insufficient space for QR code on the label.")

            # Determine module size for QR code
            module_size = max(2, max_qr_size // 25)  # Scale QR size proportionally
            qr_scale_factor = min(module_size, 10)  # Cap module size for printer compatibility

            qr_code_cmd = f"^FO{qr_code_cords[0]['x1']},{qr_code_cords[0]['y1']}^BQN,2,{qr_scale_factor}^FD00{input_qr_code}^FS"
            code.append(qr_code_cmd)

        # previous logic to have a fixed size logo image in label start --> 
        # if data.get('logo_flag'):
        #     image = Image.open(data['file_path'])
        #     width, height = 200, 200
        #     image = image.resize((width, height), Image.ANTIALIAS).convert('L').point(lambda x: 0 if x >= 128 else 1, '1')

        #     zpl_command = f"^FO{image_data[0]['x1']},{image_data[0]['y1']}^GFA,{width},{height * 25},{width // 8},"
        #     for y in range(height):
        #         for x in range(width // 8):
        #             byte = 0
        #             for i in range(8):
        #                 pixel = image.getpixel((x * 8 + i, y))
        #                 byte |= (pixel & 1) << (7 - i)
        #             zpl_command += f"{byte:02X}"
        #     zpl_command += "^FS"
        #     code.append(zpl_command)
        # -----end !
        
        if data.get('logo_flag'):
            image = Image.open(data['file_path'])
            original_width, original_height = image.size
            scaled_width, scaled_height = original_width // 4, original_height // 4  # One-fourth size

            image = image.resize((scaled_width, scaled_height), Image.ANTIALIAS).convert('L').point(lambda x: 0 if x >= 128 else 1, '1')

            zpl_command = f"^FO{image_data[0]['x1']},{image_data[0]['y1']}^GFA,{scaled_width},{scaled_height * (scaled_width // 8)},{scaled_width // 8},"
            for y in range(scaled_height):
                for x in range(scaled_width // 8):
                    byte = 0
                    for i in range(8):
                        pixel_x = x * 8 + i
                        if pixel_x < scaled_width:  # Boundary check
                            byte |= (image.getpixel((pixel_x, y)) & 1) << (7 - i)
                    zpl_command += f"{byte:02X}"
            zpl_command += "^FS"
            code.append(zpl_command)

        code.append(end)
        result_string = ','.join(code)
        logger.info("Generated ZPL command: %s", result_string)

        label1_path = os.path.join(self.dir_path, file_name)
        with open(label1_path, "w") as f:
            f.write(result_string)

        return jsonify({"success": True})


    def print_thermal_label(self, source_file=None, destination_file=None, replacement_dict=None):
        """
        Prints the thermal label by preparing a ZPL file and sending it to the printer.

        Args:
            source_file (str): Path to the source label file. Default is 'label1.zpl'.
            destination_file (str): Path to the destination label file. Default is 'label.zpl'.
            replacement_dict (dict): Dictionary containing replacement values for the ZPL label.

        Returns:
            flask.Response: JSON response indicating success or failure.
        """
        # Check if we are dealing with an HTTP request (i.e., from Flask route)
        if not source_file or not destination_file or not replacement_dict:
            # If the parameters are missing, try to retrieve data from the HTTP request
            if request.method == 'POST':
                request_data = request.get_json()
                replacement_dict = request_data  # Replace with the incoming JSON data

        # Default files in case parameters are not provided
        source_file = source_file or "label1.zpl"
        destination_file = destination_file or "label.zpl"

        label_path = os.path.join(self.dir_path, destination_file)

        # Copy the source file to the destination location
        try:
            shutil.copy(os.path.join(self.dir_path, source_file), label_path)
            logger.info(f"File copied from {source_file} to {destination_file}")
        except Exception as e:
            logger.error(f"Error copying file: {e}")
            return jsonify({"success": False, "error": str(e)})

        # Replace variables in the label file with the data in replacement_dict
        self.replace_items_in_file(label_path, list(replacement_dict.keys()), replacement_dict)

        # Send the label to the printer
        subprocess.call(["lp", "-d", self.printer_name, "-o", "raw", label_path])

        return jsonify({"success": True, "message": "Label printed successfully"})

    @staticmethod        
    def replace_items_in_file(file_path, search_list, replacement_dict):
        """
        Replaces placeholders in the label file with corresponding values from a dictionary.

        Args:
            file_path (str): Path to the label file.
            search_list (list): List of placeholder names to search for.
            replacement_dict (dict): Dictionary of placeholder values for replacement.

        Returns:
            None
        """
        with open(file_path, 'r') as file:
            content = file.read()

        for item in search_list:
            # Get the replacement value and default to 0 if it's `None` or missing
            print("replacemnent",replacement_dict)
            replacement_value = replacement_dict.get(item, 0)
            print("replace",replacement_value)        
            # Convert `None` explicitly to 0 if encountered
            if replacement_value is None:
                print(f"Warning: Replacement value for '{item}' is None. Using 0 instead.")
                replacement_value = 0
            
            # Ensure replacement value is a string for `replace()`
            content = content.replace(item, str(replacement_value))

        with open(file_path, 'w') as file:
            file.write(content)

        logger.info("Replacement completed successfully.")