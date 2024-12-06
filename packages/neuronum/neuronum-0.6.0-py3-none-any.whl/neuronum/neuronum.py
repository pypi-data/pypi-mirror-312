import requests
from typing import Optional


class Cell:
    def __init__(self, host: str, password: str, circuit: str, synapse: str):
        self.host = host
        self.password = password
        self.circuit = circuit
        self.synapse = synapse

    def to_dict(self) -> dict:
        return {
            "host": self.host,
            "password": self.password,
            "synapse": self.synapse
        }

    def __repr__(self) -> str:
        return f"Cell(host={self.host}, password={self.password}, circuit={self.circuit}, synapse={self.synapse})"

    def execute(self, taskID: str, data: dict, base_url: str = "https://{circuit}:443/executeTask"):
        # Format the URL with circuit and include taskID as a query parameter
        full_url = base_url.format(circuit=self.circuit) + f"/{taskID}"

        nt = {
            "data": data,
            "cell": self.to_dict()  # Serialize the Cell instance to a dictionary
        }

        try:
            # Send the POST request without mutual TLS (no cert)
            response = requests.post(
                full_url,
                json=nt,
                verify=True  # Optionally verify the server's SSL certificate (set path to CA bundle if needed)
            )

            # Raise an error for bad status codes
            response.raise_for_status()

            # Print the successful response from the backend (FastAPI server)
            print(f"Response from FastAPI backend: {response.json()}")

        except requests.exceptions.RequestException as e:
            print(f"Error sending request: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")



    def test_connection(self, base_url: str = "https://{circuit}:443/testConnection"):
            # Format the URL with circuit and include taskID as a query parameter
            full_url = base_url.format(circuit=self.circuit)

            nt = {
                "host": self.host,
                "password": self.password,
                "synapse": self.synapse # Serialize the Cell instance to a dictionary
            }

            print(nt)

            try:
                # Send the POST request without mutual TLS (no cert)
                response = requests.post(
                    full_url,
                    json=nt,
                    verify=True  # Optionally verify the server's SSL certificate (set path to CA bundle if needed)
                )

                # Raise an error for bad status codes
                response.raise_for_status()

                # Print the successful response from the backend (FastAPI server)
                print(f"Response from FastAPI backend: {response.json()}")

            except requests.exceptions.RequestException as e:
                print(f"Error sending request: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")



# Now, explicitly expose these components for easy import
__all__ = ['Cell']
