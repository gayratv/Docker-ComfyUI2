"""
Модуль для импорта данных из JSON-файла в базу данных MySQL.
"""

import json
import os
from typing import Optional, List, Tuple
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from .db_connection import create_db_connection


class OfferImporter:
    """
    Класс для импорта данных из JSON-файла в таблицу offers базы данных.
    """

    def __init__(self, json_file: str, table_name: str = "offers"):
        """
        Инициализация импортера.

        :param json_file: Путь к JSON-файлу с данными.
        :param table_name: Имя таблицы в базе данных (по умолчанию 'offers').
        """
        self.json_file = json_file
        self.table_name = table_name
        self.conn: Optional[MySQLConnection] = None
        self.cursor: Optional[MySQLCursor] = None

    def connect_to_db(self) -> None:
        """
        Подключение к базе данных.
        """
        self.conn = create_db_connection()
        if not self.conn:
            raise ConnectionError("Не удалось подключиться к базе данных.")
        self.cursor = self.conn.cursor()

    def disconnect_from_db(self) -> None:
        """
        Отключение от базы данных.
        """
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def get_new_batch_number(self) -> int:
        """
        Получение нового batch_number.

        :return: Новый batch_number.
        """
        self.cursor.execute("INSERT INTO batches () VALUES ()")
        self.conn.commit()
        self.cursor.execute("SELECT LAST_INSERT_ID()")
        return self.cursor.fetchone()[0]

    def read_json(self) -> List[dict]:
        """
        Чтение данных из JSON-файла.

        :return: Список словарей с данными из JSON.
        """
        if not os.path.exists(self.json_file):
            raise FileNotFoundError(f"Файл {self.json_file} не найден.")

        with open(self.json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get("offers", [])

    def prepare_row(self, offer: dict, batch_number: int) -> dict:
        """
        Подготовка строки для вставки в базу данных.

        :param offer: Данные одного предложения из JSON.
        :param batch_number: Текущий batch_number.
        :return: Словарь с подготовленными данными.
        """
        row = {k: v for k, v in offer.items() if not isinstance(v, (list, dict))}
        row.update({
            "search_gpuCostPerHour": offer.get("search", {}).get("gpuCostPerHour"),
            "search_diskHour": offer.get("search", {}).get("diskHour"),
            "search_totalHour": offer.get("search", {}).get("totalHour"),
            "search_discountTotalHour": offer.get("search", {}).get("discountTotalHour"),
            "search_discountedTotalPerHour": offer.get("search", {}).get("discountedTotalPerHour"),
            "instance_gpuCostPerHour": offer.get("instance", {}).get("gpuCostPerHour"),
            "instance_diskHour": offer.get("instance", {}).get("diskHour"),
            "instance_totalHour": offer.get("instance", {}).get("totalHour"),
            "instance_discountTotalHour": offer.get("instance", {}).get("discountTotalHour"),
            "instance_discountedTotalPerHour": offer.get("instance", {}).get("discountedTotalPerHour"),
            "internet_up_cost_per_tb": offer.get("internet_up_cost_per_tb"),
            "internet_down_cost_per_tb": offer.get("internet_down_cost_per_tb"),
            "batch_number": batch_number
        })
        return row

    def insert_offers(self, batch_num_param: Optional[int] = None) -> Tuple[int, int]:
        """
        Вставка данных из JSON-файла в базу данных.

        :return: Кортеж (количество вставленных записей, batch_number).
        """
        try:
            self.connect_to_db()
            batch_number_insert=None
            if batch_num_param:
                batch_number_insert = batch_num_param
            else:
                batch_number_insert = self.get_new_batch_number()
            print(f"📦 Используемый batch_number: {batch_number_insert}")

            offers = self.read_json()
            if not offers:
                print("❌ JSON-файл пуст.")
                return 0, batch_number_insert

            insert_query = f"""
            INSERT INTO {self.table_name} (
                batch_number, id, ask_contract_id, bundle_id, bw_nvlink, compute_cap, cpu_arch,
                cpu_cores, cpu_cores_effective, cpu_ghz, cpu_name, cpu_ram, credit_discount_max,
                cuda_max_good, direct_port_count, disk_bw, disk_name, disk_space, dlperf,
                dlperf_per_dphtotal, dph_base, dph_total, driver_version, driver_vers,
                duration, end_date, geolocation, geolocode, gpu_arch, gpu_display_active,
                gpu_frac, gpu_lanes, gpu_mem_bw, gpu_name, gpu_ram, gpu_total_ram,
                gpu_max_power, gpu_max_temp, has_avx, host_id, hosting_type, inet_down,
                inet_down_cost, inet_up, inet_up_cost, is_bid, logo, machine_id, min_bid,
                mobo_name, num_gpus, os_version, pci_gen, pcie_bw, public_ipaddr, reliability,
                reliability_mult, rentable, rented, score, start_date, static_ip, storage_cost,
                storage_total_cost, total_flops, verification, vericode, vram_costperhour,
                vms_enabled, expected_reliability, rn, dph_total_adj, reliability2,
                discount_rate, discounted_hourly, discounted_dph_total,
                search_gpuCostPerHour, search_diskHour, search_totalHour,
                search_discountTotalHour, search_discountedTotalPerHour,
                instance_gpuCostPerHour, instance_diskHour, instance_totalHour,
                instance_discountTotalHour, instance_discountedTotalPerHour,
                internet_up_cost_per_tb, internet_down_cost_per_tb
            ) VALUES (
                %(batch_number)s, %(id)s, %(ask_contract_id)s, %(bundle_id)s, %(bw_nvlink)s, %(compute_cap)s, %(cpu_arch)s,
                %(cpu_cores)s, %(cpu_cores_effective)s, %(cpu_ghz)s, %(cpu_name)s, %(cpu_ram)s, %(credit_discount_max)s,
                %(cuda_max_good)s, %(direct_port_count)s, %(disk_bw)s, %(disk_name)s, %(disk_space)s, %(dlperf)s,
                %(dlperf_per_dphtotal)s, %(dph_base)s, %(dph_total)s, %(driver_version)s, %(driver_vers)s,
                %(duration)s, %(end_date)s, %(geolocation)s, %(geolocode)s, %(gpu_arch)s, %(gpu_display_active)s,
                %(gpu_frac)s, %(gpu_lanes)s, %(gpu_mem_bw)s, %(gpu_name)s, %(gpu_ram)s, %(gpu_total_ram)s,
                %(gpu_max_power)s, %(gpu_max_temp)s, %(has_avx)s, %(host_id)s, %(hosting_type)s, %(inet_down)s,
                %(inet_down_cost)s, %(inet_up)s, %(inet_up_cost)s, %(is_bid)s, %(logo)s, %(machine_id)s, %(min_bid)s,
                %(mobo_name)s, %(num_gpus)s, %(os_version)s, %(pci_gen)s, %(pcie_bw)s, %(public_ipaddr)s, %(reliability)s,
                %(reliability_mult)s, %(rentable)s, %(rented)s, %(score)s, %(start_date)s, %(static_ip)s, %(storage_cost)s,
                %(storage_total_cost)s, %(total_flops)s, %(verification)s, %(vericode)s, %(vram_costperhour)s,
                %(vms_enabled)s, %(expected_reliability)s, %(rn)s, %(dph_total_adj)s, %(reliability2)s,
                %(discount_rate)s, %(discounted_hourly)s, %(discounted_dph_total)s,
                %(search_gpuCostPerHour)s, %(search_diskHour)s, %(search_totalHour)s,
                %(search_discountTotalHour)s, %(search_discountedTotalPerHour)s,
                %(instance_gpuCostPerHour)s, %(instance_diskHour)s, %(instance_totalHour)s,
                %(instance_discountTotalHour)s, %(instance_discountedTotalPerHour)s,
                %(internet_up_cost_per_tb)s, %(internet_down_cost_per_tb)s
            )
            """

            inserted = 0
            for offer in offers:
                row = self.prepare_row(offer, batch_number_insert)
                try:
                    self.cursor.execute(insert_query, row)
                    inserted += 1
                except Exception as err:
                    print(f"⚠️ Ошибка вставки: {err} (id: {offer.get('id')})")

            self.conn.commit()
            print(f"✅ Импорт завершён. Всего вставлено: {inserted} записей. Batch: {batch_number_insert}")
            return inserted, batch_number_insert

        finally:
            self.disconnect_from_db()


# Пример использования
if __name__ == "__main__":
    importer = OfferImporter(json_file="../vast-search.json")
    inserted, batch_number = importer.insert_offers()