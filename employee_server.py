import http.server
import socketserver
import os
import csv

PORT = 8080
CSV_FILE = 'employee_data.csv'

class EmployeeDataHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('employee_form.html', 'rb') as file:
                self.wfile.write(file.read())
        elif self.path == '/display':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.display_employee_details()
        else:
            super().do_GET()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        emp_data = self.extract_employee_data(post_data)
        self.save_employee_data(emp_data)

        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

    def extract_employee_data(self, post_data):
        emp_id = emp_name = emp_email = ""
        post_data = post_data.split('&')
        for item in post_data:
            key, value = item.split('=')
            if key == 'emp_id':
                emp_id = value
            elif key == 'emp_name':
                emp_name = value
            elif key == 'emp_email':
                emp_email = value.replace("%40","@")
        return [emp_id, emp_name, emp_email]

    def save_employee_data(self, emp_data):
        with open(CSV_FILE, 'a', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(emp_data)

    def display_employee_details(self):
        self.wfile.write("Employee Details:<br><br>".encode('utf-8'))
        try:
            with open(CSV_FILE, 'r', newline='') as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    self.wfile.write(f"Employee ID: {row[0]}, Employee Name: {row[1]}, Email ID: {row[2]}<br>".encode('utf-8'))
        except FileNotFoundError:
            self.wfile.write("No employee data available.".encode('utf-8'))

with socketserver.TCPServer(("", PORT), EmployeeDataHandler) as httpd:
    print("Serving at port", PORT)
    httpd.serve_forever()
