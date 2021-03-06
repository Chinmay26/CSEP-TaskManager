drop table if exists job_manager, job_history, jobs;
create table job_manager (
  id integer primary key auto_increment,
  version char(16) not null,
  base_location varchar(1000) not null);
create table jobs (
  id integer primary key auto_increment, 
  job_name varchar(500) unique not null, 
  script_file_path varchar(500) not null, 
  cron_output_file_path varchar(500) not null, 
  base_path varchar(500) not null, 
  log_dir varchar(500) not null, 
  file_base_name varchar(1000) not null, 
  cron_schedule char(64) not null);
create table job_history ( 
  id integer primary key auto_increment,
  job_id integer not null,
  status char(64) not null, 
  start_time datetime not null, 
  end_time datetime not null, 
  created_at datetime not null default current_timestamp,
  log_file_path varchar(700) unique not null,
  foreign key (job_id) references jobs(id));
