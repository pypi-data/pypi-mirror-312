# gns_helper

`gns_helper` is a Python package offering a suite of utilities for streamlined GNS-related operations. This package includes tools for database operations, barcode management, ZPL label design, WiFi configuration, and user authentication.

## Features
- **Database Operations**: Streamlined handling of database queries and validations.
- **Label Design**: Generate ZPL labels with QR codes and barcodes.
- **Barcode Management**: Compare and validate barcode data with ease.
- **WiFi Configuration**: Automate WiFi setup programmatically.
- **User Authentication**: Includes JWT-based authentication for secure user management.

## Installation
Install the package directly from PyPI:
```bash
pip install gns_helper
```

## How to Use
1. Interacting with API Routes
This package includes utilities for interacting with APIs exposed via Flask. Here's how to make requests to various routes:

Authentication API
Authenticate a user and retrieve a JWT token:

```
from gns_helper.app_routes import AppRoutes

base_url = "http://your-api-server.com"
auth_data = {
    "username": "your_username",
    "password": "your_password"
}
token = AppRoutes.authenticate_user(base_url, auth_data)
print("JWT Token:", token)
```
Get Barcode Data
Fetch barcode details from the server:
```
headers = {"Authorization": f"Bearer {token}"}
barcode_data = AppRoutes.get_barcode_data(base_url, headers)
print(barcode_data)
```
Submit Label Data
Send label data to the API for processing:

```
label_data = {
    "label_id": "12345",
    "content": "Sample Content"
}
response = AppRoutes.submit_label_data(base_url, label_data, headers)
print(response)
```
2. Database Operations
```
from gns_helper.table_operations import DBTableOperations

db_ops = DBTableOperations()
result = db_ops.fetch("SELECT * FROM your_table_name;")
print(result)
```
3. WiFi Configuration
```
from gns_helper.wifi_functions import configure_wifi

configure_wifi("YourSSID", "YourPassword")
```
4. Barcode Validation
```
from gns_helper.table_operations import BarcodeDataModel

barcode_model = BarcodeDataModel()
is_valid = barcode_model.compare("123456789")
print(is_valid)
```
5. Label Design
```
from gns_helper.zpl_label_designer import ZPLLabelDesigner

designer = ZPLLabelDesigner()
label = designer.create_label(data)
print(label)
```

### Changelog 0.4

1. print_thermal_label Enhancements
Enhanced the function to handle requests both:
    - Direct Python calls (backend).
    - HTTP requests (frontend React.js via Flask API).

2. generate_zpl Enhancements
Enable the function to generate a ZPL file with a specified or default name.
    - file_name parameter is optional: Defaults to label.zpl.
    - Allows passing a custom file name for more flexibility.

### License

This package is proprietary software and is distributed under the terms of the Proprietary License. Unauthorized redistribution or modification is prohibited. See the LICENSE file for more information.

### Support
For inquiries or support
contact:
Neudeep Technologies Pvt Ltd

📧 neudeep.tech.pvt.ltd@gmail.com
