if [ "$1" == production ]
then
	echo 'configuring app for production environment...'
	app_id=your-app-id
elif [ "$1" == serve ]
then
	echo 'configuring app for serve environment...'
	app_id=your-app-id
else
	echo 'bad argument. Allowed arguments are [production, staging, serve].'
	exit 1
fi

echo 'selected app_id is'
echo $app_id

# building app.yaml
cp app.yaml app.yaml.temp 
sed -e "s/\${app_id}/$app_id/" app.yaml.temp > app.yaml


if [[ "$1" == serve  ]]; then
	dev_appserver.py --port=9988 . --log_level=debug # --clear_datastore=yes
else
	echo 'starting deployment'
	appcfg.py update . --no_cookie
fi

echo 'deployment complete.'
echo 'cleaning up...'

rm app.yaml 
mv app.yaml.temp app.yaml

echo 'complete' 
