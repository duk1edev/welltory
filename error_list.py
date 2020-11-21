import os
import json
from jsonschema import Draft7Validator

BASE_DIR = os.path.abspath(os.getcwd())
event_location = os.path.join(BASE_DIR, 'event/')
schema_location = os.path.join(BASE_DIR, 'schema/')


def validate_event(event, schema):
    error_list = []
    validator = Draft7Validator(schema)
    for error in validator.iter_errors(event):
        if 'is a required property' in error.message:
            error_list.append(error.message + ' - You must fill in this field!!!')
        if "is not of type 'null'" in error.message:
            error_list.append(error.message + ' - File is not  be empty!!!')

    if error_list:
        return error_list
    else:
        return 'File is not valid'


def save_to_html(errors, file_name, schema_name):
    with open("error_list.html", "a") as fp:
        html_str = f"""
            <table width="100%" cellspacing="0" cellpadding="0" border='1' style="table-layout: fixed">
              <tr>
                <th>File name</th>
                <th>Schema name</th>
                <th>ERRORS</th>
              </tr>
              <tr>
                <td>{file_name}</td>
                <td>{schema_name}</td>
                <td>{errors}<br></td>
              </tr>
            </table>
        """
        fp.write(html_str)


# read all events from files
for root, dirs, files in os.walk(event_location, topdown=False):
    for file_name in files:
        with open(os.path.join(event_location, file_name), 'r') as file:
            dataEvent = json.loads(file.read())
            for root_inner, dirs_inner, files_inner in os.walk(schema_location, topdown=False):
                for schema_name in files_inner:
                    with open(os.path.join(schema_location, schema_name), 'r') as f:
                        dataSchema = json.loads(f.read())
                        save_to_html(validate_event(dataEvent, dataSchema), file_name, schema_name)