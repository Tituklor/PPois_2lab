from datetime import date
from typing import List, Optional, Dict, Any
import re


class Client:
    """Модель клиента"""

    def __init__(self, full_name: str = "", account_number: str = "",
                 registration_address: str = "", phone_mobile: str = "",
                 phone_landline: str = ""):
        """
        Инициализация клиента
        """
        self.full_name = full_name
        self.account_number = account_number
        self.registration_address = registration_address
        self.phone_mobile = phone_mobile
        self.phone_landline = phone_landline

    def to_dict(self) -> Dict[str, str]:
        return {
            'full_name': self.full_name,
            'account_number': self.account_number,
            'registration_address': self.registration_address,
            'phone_mobile': self.phone_mobile,
            'phone_landline': self.phone_landline
        }

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'Client':
        """Создание клиента из словаря"""
        return cls(
            full_name=data.get('full_name', ''),
            account_number=data.get('account_number', ''),
            registration_address=data.get('registration_address', ''),
            phone_mobile=data.get('phone_mobile', ''),
            phone_landline=data.get('phone_landline', '')
        )

    def __str__(self) -> str:
        """Строковое представление клиента"""
        return f"{self.full_name} | {self.account_number} | {self.registration_address}"

    def matches_search(self, **kwargs) -> bool:
        """
        Проверка соответствия клиента условиям поиска/удаления.
        """
        if 'surname' in kwargs and kwargs['surname']:
            search_value = kwargs['surname'].strip().lower()
            if search_value:
                surname = self.full_name.split()[0].lower() if self.full_name else ""
                if search_value not in surname:
                    return False

        if 'address' in kwargs and kwargs['address']:
            search_value = kwargs['address'].strip().lower()
            if search_value:
                if search_value not in self.registration_address.lower():
                    return False

        if 'account' in kwargs and kwargs['account']:
            search_value = kwargs['account'].strip()
            if search_value:
                if search_value not in self.account_number:
                    return False

        if 'mobile_phone' in kwargs and kwargs['mobile_phone']:
            #import re
            search_value = kwargs['mobile_phone'].strip()
            if search_value:
                search_digits = re.sub(r'\D', '', search_value)
                client_digits = re.sub(r'\D', '', self.phone_mobile)
                if search_digits not in client_digits:
                    return False


        if 'phone_or_surname' in kwargs and kwargs['phone_or_surname']:
            search_value = kwargs['phone_or_surname'].strip().lower()
            if search_value:
                surname = self.full_name.split()[0].lower() if self.full_name else ""
                if search_value in surname: return True
                if search_value in self.phone_mobile or search_value in self.phone_landline: return True
                return False


        if 'account_or_address' in kwargs and kwargs['account_or_address']:
            search_value = kwargs['account_or_address'].strip().lower()
            if search_value:
                if search_value in self.account_number.lower() or search_value in self.registration_address.lower():
                    return True
                return False


        if 'name_and_digits' in kwargs and kwargs['name_and_digits']:
            search_value = kwargs['name_and_digits'].strip().lower()
            if search_value:
                if search_value not in self.full_name.lower():
                    return False
                phone_digits = re.sub(r'\D', '', self.phone_mobile + self.phone_landline)
                if not phone_digits:
                    return False
                return True

        return True
class ClientCollection:


    def __init__(self):
        self._clients: List[Client] = []

    def add_client(self, client: Client) -> None:

        self._clients.append(client) #метод списка, добавляет элемент в конец

    def remove_client(self, index: int) -> bool:

        if 0 <= index < len(self._clients):
            del self._clients[index]
            return True
        return False

    def get_all_clients(self) -> List[Client]:

        return self._clients.copy()

    def get_client(self, index: int) -> Optional[Client]:

        if 0 <= index < len(self._clients):
            return self._clients[index]
        return None

    def search_clients(self, **conditions) -> List[Client]:

        result = []
        for client in self._clients:
            if client.matches_search(**conditions):
                result.append(client)
        return result

    def delete_by_conditions(self, **conditions) -> int:

        clients_to_delete = self.search_clients(**conditions)
        count = len(clients_to_delete)

        for client in clients_to_delete:
            if client in self._clients:
                self._clients.remove(client)

        return count

    def clear(self) -> None:

        self._clients.clear()

    def __len__(self) -> int:

        return len(self._clients)

    def __str__(self) -> str:

        return f"ClientCollection: {len(self._clients)} клиентов"