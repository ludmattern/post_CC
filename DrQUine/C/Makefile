# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: lmattern <lmattern@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/05/12 14:00:00 by lmattern          #+#    #+#              #
#    Updated: 2025/05/12 14:04:03 by lmattern         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAMES = Colleen Grace Sully

CC = gcc
CFLAGS = -Wall -Wextra -Werror

BUILD_DIR = build
OBJ_DIR = $(BUILD_DIR)/obj
BIN_DIR = $(BUILD_DIR)/bin

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

$(BIN_DIR)/Colleen: Colleen.c
	$(CC) $(CFLAGS) $< -o $@

$(BIN_DIR)/Grace: Grace.c
	$(CC) $(CFLAGS) $< -o $@

$(BIN_DIR)/Sully: Sully.c
	$(CC) $(CFLAGS) $< -o $@

clean:
	rm -f Grace_kid.c Sully_*.c Sully_*[0-9]

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
	@if diff -y --suppress-common-lines Colleen.c Colleen_output.txt > /dev/null; then \
		echo "$(GREEN)✓ Output matches source! Quine successful!$(RESET)"; \
	else \
		echo "$(RED)✗ Output differs from source:$(RESET)"; \
		diff -y --color=always Colleen.c Colleen_output.txt | head -20; \
		echo "$(YELLOW)  (showing first 20 differences only)$(RESET)"; \
	fi
	@rm -f Colleen_output.txt
	
	@echo "\n$(SEPARATOR)"
	@echo "$(BLUE)> TESTING GRACE$(RESET)"
	@echo "$(SEPARATOR)"
	@echo "$(YELLOW)➤ Running Grace...$(RESET)"
	@./$(BIN_DIR)/Grace
	@echo "$(YELLOW)➤ Checking if Grace_kid.c was created...$(RESET)"
	@if [ -f Grace_kid.c ]; then \
		echo "$(GREEN)✓ Grace_kid.c created successfully!$(RESET)"; \
		echo "$(YELLOW)➤ Comparing with source...$(RESET)"; \
		if diff -y --suppress-common-lines Grace.c Grace_kid.c > /dev/null; then \
			echo "$(GREEN)✓ Grace_kid.c matches source! Self-replication successful!$(RESET)"; \
		else \
			echo "$(RED)✗ Grace_kid.c differs from source:$(RESET)"; \
			diff -y --color=always Grace.c Grace_kid.c | head -20; \
			echo "$(YELLOW)  (showing first 20 differences only)$(RESET)"; \
		fi; \
	else \
		echo "$(RED)✗ Grace_kid.c was not created!$(RESET)"; \
	fi

	@echo "\n$(SEPARATOR)"
	@echo "$(BLUE)> TESTING SULLY$(RESET)"
	@echo "$(SEPARATOR)"
	@echo "$(YELLOW)➤ Running Sully...$(RESET)"
	@./$(BIN_DIR)/Sully
	@echo "$(YELLOW)➤ Checking generated Sully files...$(RESET)"
	@COUNT=$$(ls -l Sully_*.c 2>/dev/null | wc -l); echo "$(GREEN)✓ $$COUNT Sully source files were generated!$(RESET)"
	@echo "$(YELLOW)➤ Looking at the differences between Sully_2.c and Sully_1.c:$(RESET)"
	@if [ -f Sully_2.c ] && [ -f Sully_1.c ]; then \
		diff -y --color=always Sully_2.c Sully_1.c | grep -A1 -B1 "int i =" | head -5; \
		echo "$(GREEN)✓ Counter correctly decremented!$(RESET)"; \
	else \
		echo "$(RED)✗ Unable to compare files, they may not exist.$(RESET)"; \
	fi

.PHONY: all clean fclean re test