create table if not exists richards (
  timestamp text,
  flow1 double precision default null,
  occupancy1 double precision default null,
  flow2 double precision default null,
  occupancy2 double precision default null,
  flow3 double precision default null,
  occupancy3 double precision default null,
  totalflow double precision default null,
  weekday double precision default null,
  hour double precision default null,
  minute double precision default null,
  second double precision default null
);