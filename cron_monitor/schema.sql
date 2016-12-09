drop table if exists job_manager, jobs, job_history;
create table job_manager (
  id integer primary key,
  version char(16) not null,
  base_location varchar(1000) not null);
create table jobs (
  id integer primary key, 
  job_name varchar(1000) unique not null, 
  script_file_path varchar(1000) not null, 
  cron_output_file_path varchar(1000) not null, 
  base_path varchar(1000) not null, 
  log_dir varchar(1000) not null, 
  file_base_name varchar(1000) not null, 
  cron_schedule char(64) not null);
create table job_history ( 
  id integer primary key, 
  status char(64) not null, 
  start_time datetime not null, 
  end_time datetime not null, 
  log_file_path varchar(1000) unique not null);
