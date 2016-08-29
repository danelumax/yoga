CXXFLAGS =	-O2 -g -Wall -fmessage-length=0

OBJS =		main.o

LIBS =

TARGET =	ListAllData

$(TARGET):	$(OBJS)
	$(CXX) -lmysqlclient -o $(TARGET) $(OBJS) $(LIBS) `mysql_config --cflags --libs`


all:	$(TARGET)

clean:
	rm -f $(OBJS) $(TARGET)
