#
#	RiVAI bare Makefile entry...
#

TARGET=$(RISCV_ROOT)/software/host/bin/gcc/bin/riscv32-rivai-elf

PRINT_EN ?= 1
DATA_INIT ?= 1

#-----------------------------------------------------------
GCC             = $(TARGET)-gcc
OBJCOPY = $(TARGET)-objcopy
OBJDUMP = $(TARGET)-objdump
STRIP   = $(TARGET)-strip
ELF2HEX  = elf2hex
AR              = $(TARGET)-ar
RANLIB  = $(TARGET)-ranlib

APP_NAME = $(APP_NAME)

RISCV_TARGET_DIR = $(RISCV_ROOT)/software/target
RISCV_TARGET_COM_DIR = $(RISCV_TARGET_DIR)/common
RISCV_LIB_DIR = $(RISCV_TARGET_COM_DIR)/lib/
RISCV_INC_DIR = $(RISCV_TARGET_COM_DIR)/include
RISCV_BARE_INC_DIR = $(RISCV_INC_DIR)/bare
RISCV_DSP_INC_DIR = $(RISCV_INC_DIR)/dsp
RISCV_TARGET_BARE_DIR = $(RISCV_TARGET_DIR)/bare

SRC_DIR = $(PROJ_ROOT)
SRC_APP_DIR = $(SRC_DIR)/$(APP_TYPE)
OUTPUT_BIN_DIR = $(PROJ_ROOT)/bin
OUTPUT_TEST_BIN_DIR = $(PROJ_ROOT)/bin/$(APP_TYPE)

PROG    = $(OUTPUT_TEST_BIN_DIR)/$(APP_NAME)

#-----------------------------------------------------------
WARNINGS= -Wall -Wextra -Wshadow -Wpointer-arith -Wbad-function-cast -Wcast-align -Wsign-compare \
                -Waggregate-return -Wstrict-prototypes -Wmissing-prototypes -Wmissing-declarations -Wunused

INCLUDES = \
	-I. \
	-I$(RISCV_BARE_INC_DIR) \
	-I$(RISCV_DSP_INC_DIR) \
	-I$(SRC_APP_DIR) \

APP_SRC = $(shell find $(SRC_APP_DIR) -name "*.c")

CFLAGS += \
	$(WARNINGS) $(INCLUDES) \
	-fomit-frame-pointer -fno-strict-aliasing -fno-builtin \
	-D__gracefulExit -mcmodel=medany -g #-fPIC

CFLAGS += -O3 -mcpu=rugrats

#
# Define all object files.
#
OBJS = $(patsubst  %.c, $(OUTPUT_TEST_BIN_DIR)/%.o, $(notdir $(APP_SRC)))
TESTING_APP_OBJ = $(PROG).o

LDFLAGS	 = -T$(RISCV_TARGET_BARE_DIR)/link.ld -nostartfiles -static -nostdlib
LDFLAGS += -L$(RISCV_LIB_DIR)

# dont need -L path due to search them by default actually. Anyway, it is fine to mark here
# -lm should be the first one due to some APIs linking, e.g. floor()
LIBS	 = -ldsp -lbare -lm -lc -lgcc

$(OUTPUT_TEST_BIN_DIR)/%.o: %.c
	@if [ ! -d $(OUTPUT_TEST_BIN_DIR) ]; then mkdir -p $(OUTPUT_TEST_BIN_DIR); fi;
	@echo "    CC $<"
	@$(GCC) -c $(CFLAGS) -o $@ $<

$(OUTPUT_TEST_BIN_DIR)/%.o: %.S
	@if [ ! -d $(OUTPUT_TEST_BIN_DIR) ]; then mkdir -p $(OUTPUT_TEST_BIN_DIR); fi;
	@echo "    CC $<"
	@$(GCC) -c $(CFLAGS) -o $@ $<

all: $(PROG).elf

$(PROG).elf  : $(OBJS) Makefile 
	@echo Linking....
	@if [ ! -d $(OUTPUT_TEST_BIN_DIR) ]; then mkdir -p $(OUTPUT_TEST_BIN_DIR); fi;
	$(GCC) -o $@ $(TESTING_APP_OBJ) $(LDFLAGS) $(LIBS)
	@$(OBJDUMP) -xS $(PROG).elf > $(PROG).asm
	@$(OBJDUMP) -xD $(PROG).elf > $(PROG).dump
#	@$(STRIP) $(PROG).elf
	@echo Completed $@

clean :
	@rm -f $(OBJS)
	@rm -rf $(OUTPUT_BIN_DIR)/



