import xml.dom.minidom as dom
import xml.sax as sax
import xml.sax.handler as sax_handler
from typing import List, Dict
from model import Client, ClientCollection


class ClientSAXHandler(sax_handler.ContentHandler):

    def __init__(self):
        super().__init__()
        self._clients: List[Client] = []
        self._current_element = ""
        self._current_client_data: Dict[str, str] = {}

    def startElement(self, name: str, attrs):

        self._current_element = name

        if name == "client":

            self._current_client_data = {
                'full_name': '',
                'account_number': '',
                'registration_address': '',
                'phone_mobile': '',
                'phone_landline': ''
            }

    def endElement(self, name: str):

        if name == "client":
            client = Client.from_dict(self._current_client_data)
            self._clients.append(client)
            self._current_client_data = {}

        self._current_element = ""

    def characters(self, content: str):
        content = content.strip()
        if not content:
            return

        # Сохраняем данные в зависимости от того, в каком мы теге
        if self._current_element == "full_name":
            self._current_client_data['full_name'] = content
        elif self._current_element == "account_number":
            self._current_client_data['account_number'] = content
        elif self._current_element == "registration_address":
            self._current_client_data['registration_address'] = content
        elif self._current_element == "phone_mobile":
            self._current_client_data['phone_mobile'] = content
        elif self._current_element == "phone_landline":
            self._current_client_data['phone_landline'] = content

    def get_clients(self) -> List[Client]:
        return self._clients


class XMLHandler:


    @staticmethod
    def save_to_xml(collection: ClientCollection, filepath: str) -> bool:

        try:

            doc = dom.Document()

            root = doc.createElement("clients")# Создание корневого элемента
            doc.appendChild(root)

            for client in collection.get_all_clients():
                client_elem = doc.createElement("client")
                root.appendChild(client_elem) # добавляется дочерний элемент к корню

                full_name_elem = doc.createElement("full_name")
                full_name_text = doc.createTextNode(client.full_name)
                full_name_elem.appendChild(full_name_text)
                client_elem.appendChild(full_name_elem)

                account_elem = doc.createElement("account_number")
                account_text = doc.createTextNode(client.account_number)
                account_elem.appendChild(account_text)
                client_elem.appendChild(account_elem)

                address_elem = doc.createElement("registration_address")
                address_text = doc.createTextNode(client.registration_address)
                address_elem.appendChild(address_text)
                client_elem.appendChild(address_elem)

                mobile_elem = doc.createElement("phone_mobile")
                mobile_text = doc.createTextNode(client.phone_mobile)
                mobile_elem.appendChild(mobile_text)
                client_elem.appendChild(mobile_elem)

                landline_elem = doc.createElement("phone_landline")
                landline_text = doc.createTextNode(client.phone_landline)
                landline_elem.appendChild(landline_text)
                client_elem.appendChild(landline_elem)

            with open(filepath, 'w', encoding='utf-8') as f:
                doc.writexml(f, indent='  ', addindent='  ', newl='\n', encoding='UTF-8')

            return True

        except Exception as e:
            print(f"Ошибка при сохранении XML: {e}")
            return False

    @staticmethod
    def load_from_xml(filepath: str) -> ClientCollection:

        collection = ClientCollection()

        try:
            parser = sax.make_parser()

            handler = ClientSAXHandler()
            parser.setContentHandler(handler)

            parser.parse(filepath)

            for client in handler.get_clients():
                collection.add_client(client)

            return collection

        except Exception as e:
            print(f"Ошибка при загрузке XML: {e}")
            return collection

    @staticmethod
    def append_client_to_xml(client: Client, filepath: str) -> bool:

        try:
            doc = dom.parse(filepath)
            root = doc.documentElement

            client_elem = doc.createElement("client")

            full_name_elem = doc.createElement("full_name")
            full_name_text = doc.createTextNode(client.full_name)
            full_name_elem.appendChild(full_name_text)
            client_elem.appendChild(full_name_elem)

            account_elem = doc.createElement("account_number")
            account_text = doc.createTextNode(client.account_number)
            account_elem.appendChild(account_text)
            client_elem.appendChild(account_elem)

            address_elem = doc.createElement("registration_address")
            address_text = doc.createTextNode(client.registration_address)
            address_elem.appendChild(address_text)
            client_elem.appendChild(address_elem)

            mobile_elem = doc.createElement("phone_mobile")
            mobile_text = doc.createTextNode(client.phone_mobile)
            mobile_elem.appendChild(mobile_text)
            client_elem.appendChild(mobile_elem)

            landline_elem = doc.createElement("phone_landline")
            landline_text = doc.createTextNode(client.phone_landline)
            landline_elem.appendChild(landline_text)
            client_elem.appendChild(landline_elem)

            root.appendChild(client_elem)

            with open(filepath, 'w', encoding='utf-8') as f:
                doc.writexml(f, indent='  ', addindent='  ', newl='\n', encoding='UTF-8')

            return True

        except Exception as e:
            print(f"Ошибка при добавлении клиента в XML: {e}")
            return False