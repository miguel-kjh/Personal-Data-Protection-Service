#!/bin/bash
die()
{
	echo "$0:$1" 1>&2
	exit 1
}
if(($#>1)); then
	die "Argument failed"
fi
if(($#==0));then
	option="run"
else
	option=$1
fi
if [ "$option" != "clean" ]; then
	python3 cleanDB.py
	python3 manage.py $option
	exit 0
fi
python3 cleanDB.py
exit 0

