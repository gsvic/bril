inputs := $(wildcard ./*.json)

.PHONY: test
test: $(inputs)
#	echo $^
#	for f in $^ do
#		turnt $f
#	done
	for f in $^ ; do	\
		turnt --save $$f ;	\
	done