# CSEP-TaskManager
This cron monitor web app parses CSEP cron log files to detect success/failure. This is based on Flask + MySQL


### App Structure
```
/CSEP-TaskManager
	/cron_monitor
		/data
			csep_job_metadata.csv
				[Contains the metadata used to create Cron Jobs(used in jobs mysql table)]
		/templates
			show_job_entries.html
				[HTML view file which renders the job history]
		config.py
			[Has configuration parameters for the web app]
		create_log_entries.py
			[python cron script to create log entries on daily basis]
		cron_monitor.py
			[Base application startup file. Contains web app initialization, setting up DB]
		db_client.py
			[Mysql database client to interact with DB]
		log_parser.py
			[Application code which parser log files. Brains of the web app]
		schema.sql
			[Msql schema used to create the web app]
		/setup
			/database
				[Scripts to initialise and setup Mysql database]
```
