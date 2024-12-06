import requests
import pandas as pd

class Bill:
    def __init__(self, account_token):
        self.account_token = account_token
        self.base_url = "https://api.ready2order.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.account_token}",
            "Content-Type": "application/json"
        }

    def get_all_bills(self, as_dataframe=True, limit=100):
        """
        Fetch and return all bills from the API using pagination.

        :param as_dataframe: bool, whether to return the data as a DataFrame (default is True).
        :param limit: int, the number of records per page (default is 100).
        :return: pd.DataFrame or list, a DataFrame containing all bills data or raw JSON.
        """
        url = f"{self.base_url}/document/invoice"
        offset = 0
        all_bills = []

        while True:
            params = {"limit": limit, "offset": offset}
            response = requests.get(url, headers=self.headers, params=params)

            if response.status_code == 200:
                data = response.json()
                invoices = data.get('invoices', [])
                all_bills.extend(invoices)
                if len(invoices) < limit:  # No more data to fetch
                    break
                offset += limit
            else:
                print(f"Error {response.status_code}: {response.text}")
                return None

        if as_dataframe:
            return pd.DataFrame(all_bills)
        return all_bills

    def get_bill_by_id(self, invoice_id, as_dataframe=True):
        """
        Fetch and return a specific invoice by ID.

        :param invoice_id: int, the ID of the invoice to retrieve.
        :param as_dataframe: bool, whether to return the data as a DataFrame (default is True).
        :return: pd.DataFrame or dict, a DataFrame containing the invoice data or raw JSON.
        """
        url = f"{self.base_url}/document/invoice/{invoice_id}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            invoice_data = response.json()

            if not as_dataframe:
                return invoice_data

            invoice_header = invoice_data.copy()
            del invoice_header['items']

            rows = []
            for item in invoice_data['items']:
                row_data = invoice_header.copy()
                row_data.update(item)
                rows.append(row_data)

            df = pd.DataFrame(rows)
            df['invoice_timestamp'] = pd.to_datetime(df['invoice_timestamp'], format='%Y-%m-%d %H:%M:%S')
            return df
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None

if __name__ == '__main__':
    pass