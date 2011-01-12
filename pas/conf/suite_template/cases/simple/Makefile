SRCS=simple.ph simple.cc main.cc
EXEC=simple

ARCH=$$(uname -m)-$$(uname -p)-$$(uname -s)

all: bin object cleantemp

$(ARCH):
	mkdir $(ARCH)

dir:
	mkdir -p $(ARCH)

bin: dir
	popcc -noclean -o $(EXEC) $(SRCS)
	mv $(EXEC) $(ARCH)

object: dir
	popcc -noclean -object -o $(EXEC).obj $(SRCS)
	mv $(EXEC).obj $(ARCH)
	./$(ARCH)/$(EXEC).obj -listlong >>obj.map
	sort -u obj.map >obj.map.temp
	mv obj.map.temp obj.map

cleantemp:
	rm -f _paroc* *.o
	
clean: cleantemp
	rm -rf _paroc* *.o $(ARCH)

cleanall: clean
	rm -rf *.obj obj.map

run:
	popcrun obj.map ./$(ARCH)/$(EXEC)
