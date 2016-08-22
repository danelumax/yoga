CXXFLAGS =	-O2 -g -Wall -fmessage-length=0

OBJS =		PollMutiConnection.o

LIBS =

TARGET =	PollMutiConnection

$(TARGET):	$(OBJS)
	$(CXX) -o $(TARGET) $(OBJS) $(LIBS)

all:	$(TARGET)

clean:
	rm -f $(OBJS) $(TARGET)
