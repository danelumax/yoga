CCPLUS  =       g++
RM	=	rm -rf

DIR_INC	:=	./include
DIR_SRC	:=	./src
DIR_RELEASE :=	./release
OBJ_SUFFIX	= .o

SOURCES:= $(wildcard $(DIR_SRC)/*.c $(DIR_SRC)/*.cpp)

#C_SOURCES:= $(filter %.c, $(SOURCES))
CPP_SOURCES:= $(filter %.cpp, $(SOURCES))

OBJECTS := $(foreach OBJ,$(CPP_SOURCES:$(DIR_SRC)%.cpp=%$(OBJ_SUFFIX)),$(DIR_RELEASE)$(OBJ))

TARGET = SingletonMultiInstance

BIN_TARGET = ${DIR_RELEASE}/${TARGET}

CFLAGS = -Wall $(foreach DIR,$(DIR_INC),-I "$(DIR)")

LDFLAGS   = -lpthread

# define debug flag
ifdef DEBUG
	LDFLAGS += -g
endif


${BIN_TARGET}:${OBJECTS}
	@[ -d $(DIR_BIN) ] || mkdir $(DIR_BIN)
	$(CCPLUS) $(OBJECTS) $(LDFLAGS) -o $@

${DIR_RELEASE}/%.o:${DIR_SRC}/%.cpp
	@[ -d $(DIR_RELEASE) ] || mkdir $(DIR_RELEASE)
	$(PRE_EXEC) $(CCPLUS) $(LDFLAGS) -c $(CFLAGS) $(foreach DIR,$(INCLUDE_DIRS),-I "$(DIR)") $< -o $@

all:	$(BIN_TARGET)

debug:
	$(MAKE) all "DEBUG=-g"

.PHONY:clean

clean:
	$(RM) $(DIR_RELEASE)
