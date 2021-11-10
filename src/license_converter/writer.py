import csv
from license_converter.licenseparser import LicenseParser

columns = ["FILE", "HOST_ID", "PRODUCT", "DESCRIPTION", "VERSION", "QUANTITY", "ISSUE_DATE", "EXPIRATION_DATE"]


class LicenseWriter:
    filepath = None
    output_file = None
    csv_writer = None

    def __init__(self, filepath):
        self.filepath = filepath

    def __enter__(self):
        self.open()
        return self

    def open(self):
        self.output_file = open(self.filepath, "w")
        self.csv_writer = csv.writer(self.output_file)
        self.csv_writer.writerow(columns)

    def write_file(self, lf: LicenseParser):
        for product in lf.features:
            fields = [lf.path, lf.server.host_id, product.feature, product.comment, product.version,
                      product.license_count, product.opt_fields.get("ISSUED", ""), product.exp_date]
            self.csv_writer.writerow(fields)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.output_file.close()
