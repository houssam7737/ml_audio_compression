labels=(bed bird cat dog down eight five four go happy house left marvin nine no off on one stop up wow yes three tree)
quality=(4 8 16)
for q in "${quality[@]}"
do
	for label in "${labels[@]}"
	do
		echo "Transforming audio files in the $label folder"
		mkdir -p ${label}_transformed_${q}
		for i in $(ls -U $label | head -100)
		do
			ffmpeg -i ./$label/$i -qscale:a ${q} "${label}_transformed_${q}/${i::17}_${q}.mp3"
		done
	done
done
