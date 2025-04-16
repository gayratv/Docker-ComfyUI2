CREATE OR REPLACE VIEW view_latest_offers AS
select `id`,
       ROUND(`search_totalHour` + `search_diskHour`, 3) AS `$\H`,
       ROUND(`internet_down_cost_per_tb`, 1)            as i_down_per_tb,
       `inet_down`,
       `cpu_ram`,
       `gpu_name`,
       `geolocation`,
       `search_gpuCostPerHour`,
       `search_diskHour`,
       `cuda_max_good`,
       `disk_space`,
       `gpu_frac`,

       `gpu_ram`,
       `host_id`,

       `machine_id`,
       auto_id,
       CONTRACT_ID

from offers
where batch_number = (SELECT MAX(batch_number) FROM batches)
  and internet_up_cost_per_tb < 8
order by `search_totalHour` + `search_diskHour` + internet_down_cost_per_tb * 40 / 1000 asc;