import json
import mysql.connector

# Подключение к MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='vast',
    port=3307
)
cursor = conn.cursor()

# Чтение JSON
with open('vast-search.json', 'r') as f:
    data = json.load(f)

# Подготовка SQL-запроса
insert_query = """
INSERT INTO offers (
    id, ask_contract_id, bundle_id, bw_nvlink, compute_cap, cpu_arch, cpu_cores,
    cpu_cores_effective, cpu_ghz, cpu_name, cpu_ram, credit_discount_max,
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
    %(id)s, %(ask_contract_id)s, %(bundle_id)s, %(bw_nvlink)s, %(compute_cap)s, %(cpu_arch)s, %(cpu_cores)s,
    %(cpu_cores_effective)s, %(cpu_ghz)s, %(cpu_name)s, %(cpu_ram)s, %(credit_discount_max)s,
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


# Вставка данных
for offer in data["offers"]:

    row = {k: v for k, v in offer.items() if not isinstance(v, (list, dict))}

    # Добавим вложенные поля вручную
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
        "internet_down_cost_per_tb": offer.get("internet_down_cost_per_tb")
    })

    cursor.execute(insert_query, row)

# Финализация
conn.commit()
cursor.close()
conn.close()

print("Импорт завершён успешно.")
