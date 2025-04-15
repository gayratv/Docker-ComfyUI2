CREATE TABLE hosts (
    host_id INT PRIMARY KEY,
    hosting_type INT,
    hostname VARCHAR(255),
    mobo_name VARCHAR(255),
    os_version VARCHAR(50),
    pci_gen FLOAT,
    pcie_bw FLOAT,
    public_ipaddr VARCHAR(15),
    static_ip BOOLEAN,
    start_date TIMESTAMP,
    reliability FLOAT,
    reliability_mult FLOAT,
    rentable BOOLEAN,
    rented BOOLEAN,
    score FLOAT,
    verification VARCHAR(50),
    vericode INT,
    vms_enabled BOOLEAN,
    expected_reliability FLOAT,
    rn INT
);
CREATE TABLE gpus (
    gpu_id INT AUTO_INCREMENT PRIMARY KEY,
    host_id INT,
    gpu_name VARCHAR(50),
    gpu_ram INT,
    gpu_total_ram INT,
    gpu_max_power FLOAT,
    gpu_max_temp FLOAT,
    gpu_mem_bw FLOAT,
    gpu_lanes INT,
    has_avx BOOLEAN,
    FOREIGN KEY (host_id) REFERENCES hosts(host_id)
);
CREATE TABLE network (
    network_id INT AUTO_INCREMENT PRIMARY KEY,
    host_id INT,
    inet_down FLOAT,
    inet_down_cost FLOAT,
    inet_up FLOAT,
    inet_up_cost FLOAT,
    is_bid BOOLEAN,
    FOREIGN KEY (host_id) REFERENCES hosts(host_id)
);
CREATE TABLE storage (
    storage_id INT AUTO_INCREMENT PRIMARY KEY,
    host_id INT,
    storage_cost FLOAT,
    storage_total_cost FLOAT,
    FOREIGN KEY (host_id) REFERENCES hosts(host_id)
);
CREATE TABLE costs (
    cost_id INT AUTO_INCREMENT PRIMARY KEY,
    host_id INT,
    dph_total_adj FLOAT,
    vram_costperhour FLOAT,
    FOREIGN KEY (host_id) REFERENCES hosts(host_id)
);
CREATE TABLE search (
    search_id INT AUTO_INCREMENT PRIMARY KEY,
    host_id INT,
    gpu_cost_per_hour FLOAT,
    disk_hour FLOAT,
    total_hour FLOAT,
    discount_total_hour FLOAT,
    discounted_total_per_hour FLOAT,
    FOREIGN KEY (host_id) REFERENCES hosts(host_id)
);
CREATE TABLE instance (
    instance_id INT AUTO_INCREMENT PRIMARY KEY,
    host_id INT,
    gpu_cost_per_hour FLOAT,
    disk_hour FLOAT,
    total_hour FLOAT,
    discount_total_hour FLOAT,
    discounted_total_per_hour FLOAT,
    FOREIGN KEY (host_id) REFERENCES hosts(host_id)
);
CREATE TABLE misc (
    misc_id INT AUTO_INCREMENT PRIMARY KEY,
    host_id INT,
    min_bid FLOAT,
    total_flops FLOAT,
    duration FLOAT,
    end_date TIMESTAMP,
    geolocation VARCHAR(255),
    geolocode BIGINT,
    internet_up_cost_per_tb FLOAT,
    internet_down_cost_per_tb FLOAT,
    FOREIGN KEY (host_id) REFERENCES hosts(host_id)
);
