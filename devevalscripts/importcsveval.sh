#!/bin/sh
#https://medium.com/@rakeshsharma.pr/data-science-on-the-command-line-121fd9922642
#sudo nala install csvkit
#csvclean --enable-all-checks importoptim.csv
csvstat importoptim.csv
#csvsql --query "select * from 'importoptim' limit 10" importoptim.csv 
#csvsql --query "select distinct(Host) from 'importoptim'  limit 10" importoptim.csv
#csvsql --query "select Host,Method,avg(Duration) as 'mean',sqrt(avg(pow(Duration,2))-pow(avg(Duration),2)) as 'stdev' from 'importoptim' where Host='BWN12101' group by Host,Method" importoptim.csv | csvlook
csvsql --query "select Host,Nice,Method,avg(Duration) as 'mean',sqrt(avg(pow(Duration,2))-pow(avg(Duration),2)) as 'stdev' from 'importoptim' where Nice>-10 group by Host,Nice,Method order by Host,Nice,mean" importoptim.csv | csvlook

