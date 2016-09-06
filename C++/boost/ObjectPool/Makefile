CXXFLAGS =	-O2 -g -Wall -fmessage-length=0

OBJS =		main.o

LIBS =

TARGET =	ObjectPool

$(TARGET):	$(OBJS)
	$(CXX) -o $(TARGET) $(OBJS) $(LIBS) -lboost_system

all:	$(TARGET)

clean:
	rm -f $(OBJS) $(TARGET)
