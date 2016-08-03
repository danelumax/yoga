CXXFLAGS =	-O2 -g -Wall -fmessage-length=0

OBJS =		tokenizer.o

LIBS =

TARGET =	tokenizer

$(TARGET):	$(OBJS)
	$(CXX) -o $(TARGET) $(OBJS) $(LIBS)

all:	$(TARGET)

clean:
	rm -f $(OBJS) $(TARGET)
