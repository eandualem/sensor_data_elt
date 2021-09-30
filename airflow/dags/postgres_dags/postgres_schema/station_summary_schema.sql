create table if not exists station_summary (
  id double precision default null,
  flow_99 double precision default null,
  flow_max double precision default null,
  flow_median double precision default null,
  flow_total double precision default null,
  n_obs double precision default null
);