alacconvert: ALAC/convert-utility/alacconvert
	cp ALAC/convert-utility/alacconvert alacconvert

ALAC/convert-utility/Makefile: ALAC/convert-utility/makefile
	sed "s/\$$(CC) \$$(LFLAGS) \$$(OBJS) -o alacconvert/\$$(CC) \$$(OBJS) -o alacconvert \$$(LFLAGS)/" ALAC/convert-utility/makefile > ALAC/convert-utility/Makefile

ALAC/convert-utility/alacconvert: ALAC/convert-utility/Makefile
	cd ALAC/convert-utility && $(MAKE) -f Makefile
