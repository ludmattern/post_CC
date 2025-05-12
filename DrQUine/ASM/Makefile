# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: lmattern <lmattern@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/05/12 14:00:00 by lmattern          #+#    #+#              #
#    Updated: 2025/05/12 14:03:57 by lmattern         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAMES = Colleen Grace Sully

NASM = nasm
NASMFLAGS = -f elf64
CC = gcc

BUILD_DIR = build
OBJ_DIR = $(BUILD_DIR)/obj
BIN_DIR = $(BUILD_DIR)/bin

OBJS = $(addprefix $(OBJ_DIR)/, $(NAMES:=.o))
BINS = $(addprefix $(BIN_DIR)/, $(NAMES))

# Colors
BLUE = \033[1;34m
GREEN = \033[1;32m
RED = \033[1;31m
YELLOW = \033[1;33m
RESET = \033[0m
BOLD = \033[1m

# Separator
SEPARATOR = $(BLUE)===========================================$(RESET)

all: $(BUILD_DIR) $(BINS)

$(BUILD_DIR):
	mkdir -p $(OBJ_DIR)
	mkdir -p $(BIN_DIR)

$(OBJ_DIR)/%.o: %.s
	$(NASM) $(NASMFLAGS) $< -o $@

$(BIN_DIR)/Colleen: $(OBJ_DIR)/Colleen.o
	$(CC) -no-pie $< -o $@

$(BIN_DIR)/Grace: $(OBJ_DIR)/Grace.o
	$(CC) -no-pie $< -o $@

$(BIN_DIR)/Sully: $(OBJ_DIR)/Sully.o
	$(CC) -no-pie $< -o $@

clean:
	rm -f $(OBJ_DIR)/*.o Grace_kid.s Sully_*.s Sully_*[0-9] Sully_*.o

fclean: clean
	rm -rf $(BUILD_DIR)

re: fclean all

test: all
	@echo "\n$(SEPARATOR)"
	@echo "$(BLUE)> TESTING COLLEEN$(RESET)"
	@echo "$(SEPARATOR)"
	@echo "$(YELLOW)➤ Running Colleen...$(RESET)"
	@./$(BIN_DIR)/Colleen > Colleen_output.txt
	@echo "$(YELLOW)➤ Comparing output with source...$(RESET)"
	@if diff -y --suppress-common-lines Colleen.s Colleen_output.txt > /dev/null; then \
		echo "$(GREEN)✓ Output matches source! Quine successful!$(RESET)"; \
	else \
		echo "$(RED)✗ Output differs from source:$(RESET)"; \
		diff -y --color=always Colleen.s Colleen_output.txt | head -20; \
		echo "$(YELLOW)  (showing first 20 differences only)$(RESET)"; \
	fi
	@rm -f Colleen_output.txt
	
	@echo "\n$(SEPARATOR)"
	@echo "$(BLUE)> TESTING GRACE$(RESET)"
	@echo "$(SEPARATOR)"
	@echo "$(YELLOW)➤ Running Grace...$(RESET)"
	@./$(BIN_DIR)/Grace
	@echo "$(YELLOW)➤ Checking if Grace_kid.s was created...$(RESET)"
	@if [ -f Grace_kid.s ]; then \
		echo "$(GREEN)✓ Grace_kid.s created successfully!$(RESET)"; \
		echo "$(YELLOW)➤ Comparing with source...$(RESET)"; \
		if diff -y --suppress-common-lines Grace.s Grace_kid.s > /dev/null; then \
			echo "$(GREEN)✓ Grace_kid.s matches source! Self-replication successful!$(RESET)"; \
		else \
			echo "$(RED)✗ Grace_kid.s differs from source:$(RESET)"; \
			diff -y --color=always Grace.s Grace_kid.s | head -20; \
			echo "$(YELLOW)  (showing first 20 differences only)$(RESET)"; \
		fi; \
	else \
		echo "$(RED)✗ Grace_kid.s was not created!$(RESET)"; \
	fi

	@echo "\n$(SEPARATOR)"
	@echo "$(BLUE)> TESTING SULLY$(RESET)"
	@echo "$(SEPARATOR)"
	@echo "$(YELLOW)➤ Running Sully...$(RESET)"
	@./$(BIN_DIR)/Sully
	@echo "$(YELLOW)➤ Checking generated Sully files...$(RESET)"
	@COUNT=$$(ls -l Sully_*.s 2>/dev/null | wc -l); echo "$(GREEN)✓ $$COUNT Sully source files were generated!$(RESET)"
	@echo "$(YELLOW)➤ Looking at the differences between Sully_2.s and Sully_1.s:$(RESET)"
	@if [ -f Sully_2.s ] && [ -f Sully_1.s ]; then \
		diff -y --color=always Sully_2.s Sully_1.s | grep -A1 -B1 "mov r12, " | head -5; \
		echo "$(GREEN)✓ Counter correctly decremented!$(RESET)"; \
	else \
		echo "$(RED)✗ Unable to compare files, they may not exist.$(RESET)"; \
	fi

.PHONY: all clean fclean re test