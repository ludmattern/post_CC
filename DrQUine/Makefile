NAME_C = Colleen Grace
NAME_ASM = Colleen Grace

CC = gcc
CFLAGS = -Wall -Wextra -Werror
NASM = nasm
NASMFLAGS = -f elf64

BUILD_DIR = build
OBJ_DIR = $(BUILD_DIR)/obj
BIN_DIR = $(BUILD_DIR)/bin
C_DIR = C
ASM_DIR = ASM

C_BINS = $(addprefix $(BIN_DIR)/$(C_DIR)/, $(NAME_C))
ASM_BINS = $(addprefix $(BIN_DIR)/$(ASM_DIR)/, $(NAME_ASM))

# Colors
BLUE = \033[1;34m
GREEN = \033[1;32m
RED = \033[1;31m
YELLOW = \033[1;33m
RESET = \033[0m
BOLD = \033[1m

# Separator
SEPARATOR = $(BLUE)===========================================$(RESET)

all: $(BUILD_DIR) $(C_BINS) $(ASM_BINS)

$(BUILD_DIR):
	mkdir -p $(OBJ_DIR)/$(C_DIR)
	mkdir -p $(OBJ_DIR)/$(ASM_DIR)
	mkdir -p $(BIN_DIR)/$(C_DIR)
	mkdir -p $(BIN_DIR)/$(ASM_DIR)

$(BIN_DIR)/$(C_DIR)/Colleen: $(C_DIR)/Colleen.c
	$(CC) $(CFLAGS) $< -o $@

$(BIN_DIR)/$(C_DIR)/Grace: $(C_DIR)/Grace.c
	cd $(C_DIR) && $(CC) $(CFLAGS) Grace.c -o ../$(BIN_DIR)/$(C_DIR)/Grace

$(BIN_DIR)/$(ASM_DIR)/Colleen: $(ASM_DIR)/Colleen.s
	$(NASM) $(NASMFLAGS) $< -o $(OBJ_DIR)/$(ASM_DIR)/Colleen.o
	$(CC) -no-pie $(OBJ_DIR)/$(ASM_DIR)/Colleen.o -o $@

$(BIN_DIR)/$(ASM_DIR)/Grace: $(ASM_DIR)/Grace.s
	cd $(ASM_DIR) && $(NASM) $(NASMFLAGS) Grace.s -o ../$(OBJ_DIR)/$(ASM_DIR)/Grace.o
	cd $(ASM_DIR) && $(CC) -no-pie ../$(OBJ_DIR)/$(ASM_DIR)/Grace.o -o ../$(BIN_DIR)/$(ASM_DIR)/Grace

clean:
	rm -f $(OBJ_DIR)/$(ASM_DIR)/*.o $(OBJ_DIR)/$(C_DIR)/*.o $(C_DIR)/Grace_kid.c $(ASM_DIR)/Grace_kid.s

fclean: clean
	rm -rf $(BUILD_DIR)

re: fclean all

test: all
	@echo "\n$(SEPARATOR)"
	@echo "$(BLUE)🔍 TESTING C/COLLEEN$(RESET)"
	@echo "$(SEPARATOR)"
	@echo "$(YELLOW)➤ Running C/Colleen...$(RESET)"
	@cd $(C_DIR) && ../$(BIN_DIR)/$(C_DIR)/Colleen > Colleen_output.txt
	@echo "$(YELLOW)➤ Comparing output with source...$(RESET)"
	@if diff -y --suppress-common-lines $(C_DIR)/Colleen.c $(C_DIR)/Colleen_output.txt > /dev/null; then \
		echo "$(GREEN)✓ Output matches source! Quine successful!$(RESET)"; \
	else \
		echo "$(RED)✗ Output differs from source:$(RESET)"; \
		diff -y --color=always $(C_DIR)/Colleen.c $(C_DIR)/Colleen_output.txt | head -20; \
		echo "$(YELLOW)  (showing first 20 differences only)$(RESET)"; \
	fi
	@rm -f $(C_DIR)/Colleen_output.txt
	
	@echo "\n$(SEPARATOR)"
	@echo "$(BLUE)🔍 TESTING ASM/COLLEEN$(RESET)"
	@echo "$(SEPARATOR)"
	@echo "$(YELLOW)➤ Running ASM/Colleen...$(RESET)"
	@cd $(ASM_DIR) && ../$(BIN_DIR)/$(ASM_DIR)/Colleen > Colleen_output.txt
	@echo "$(YELLOW)➤ Comparing output with source...$(RESET)"
	@if diff -y --suppress-common-lines $(ASM_DIR)/Colleen.s $(ASM_DIR)/Colleen_output.txt > /dev/null; then \
		echo "$(GREEN)✓ Output matches source! Quine successful!$(RESET)"; \
	else \
		echo "$(RED)✗ Output differs from source:$(RESET)"; \
		diff -y --color=always $(ASM_DIR)/Colleen.s $(ASM_DIR)/Colleen_output.txt | head -20; \
		echo "$(YELLOW)  (showing first 20 differences only)$(RESET)"; \
	fi
	@rm -f $(ASM_DIR)/Colleen_output.txt
	
	@echo "\n$(SEPARATOR)"
	@echo "$(BLUE)🔍 TESTING C/GRACE$(RESET)"
	@echo "$(SEPARATOR)"
	@echo "$(YELLOW)➤ Running C/Grace...$(RESET)"
	@cd $(C_DIR) && ../$(BIN_DIR)/$(C_DIR)/Grace
	@echo "$(YELLOW)➤ Checking if Grace_kid.c was created...$(RESET)"
	@if [ -f $(C_DIR)/Grace_kid.c ]; then \
		echo "$(GREEN)✓ Grace_kid.c created successfully!$(RESET)"; \
		echo "$(YELLOW)➤ Comparing with source...$(RESET)"; \
		if diff -y --suppress-common-lines $(C_DIR)/Grace.c $(C_DIR)/Grace_kid.c > /dev/null; then \
			echo "$(GREEN)✓ Grace_kid.c matches source! Self-replication successful!$(RESET)"; \
		else \
			echo "$(RED)✗ Grace_kid.c differs from source:$(RESET)"; \
			diff -y --color=always $(C_DIR)/Grace.c $(C_DIR)/Grace_kid.c | head -20; \
			echo "$(YELLOW)  (showing first 20 differences only)$(RESET)"; \
		fi; \
	else \
		echo "$(RED)✗ Grace_kid.c was not created!$(RESET)"; \
	fi
	
	@echo "\n$(SEPARATOR)"
	@echo "$(BLUE)🔍 TESTING ASM/GRACE$(RESET)"
	@echo "$(SEPARATOR)"
	@echo "$(YELLOW)➤ Running ASM/Grace...$(RESET)"
	@cd $(ASM_DIR) && ../$(BIN_DIR)/$(ASM_DIR)/Grace
	@echo "$(YELLOW)➤ Checking if Grace_kid.s was created...$(RESET)"
	@if [ -f $(ASM_DIR)/Grace_kid.s ]; then \
		echo "$(GREEN)✓ Grace_kid.s created successfully!$(RESET)"; \
		echo "$(YELLOW)➤ Comparing with source...$(RESET)"; \
		if diff -y --suppress-common-lines $(ASM_DIR)/Grace.s $(ASM_DIR)/Grace_kid.s > /dev/null; then \
			echo "$(GREEN)✓ Grace_kid.s matches source! Self-replication successful!$(RESET)"; \
		else \
			echo "$(RED)✗ Grace_kid.s differs from source:$(RESET)"; \
			diff -y --color=always $(ASM_DIR)/Grace.s $(ASM_DIR)/Grace_kid.s | head -20; \
			echo "$(YELLOW)  (showing first 20 differences only)$(RESET)"; \
		fi; \
	else \
		echo "$(RED)✗ Grace_kid.s was not created!$(RESET)"; \
	fi

.PHONY: all clean fclean re test