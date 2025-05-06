# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: lmattern <lmattern@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/05/06 14:01:00 by lmattern          #+#    #+#              #
#    Updated: 2025/05/06 15:56:29 by lmattern         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME    = libasm.a
NASM    = nasm -f elf64
CC      = gcc
CFLAGS  = -Wall -Wextra -Werror
SRCS    = ft_strlen.s ft_strcpy.s ft_strcmp.s ft_write.s ft_read.s ft_strdup.s
OBJS    = $(SRCS:.s=.o)
HEADER  = libasm.h
TEST    = test
TEST_SRC= main.c

.PHONY: all clean fclean re test test_null

all: $(NAME)

%.o: %.s
	$(NASM) $< -o $@

$(NAME): $(OBJS)
	ar rcs $@ $^

test: $(NAME) $(TEST_SRC) $(HEADER)
	$(CC) $(CFLAGS) $(TEST_SRC) -L. -lasm -o $(TEST) && valgrind --leak-check=full ./$(TEST)

test_null: $(NAME) $(TEST_SRC) $(HEADER)
	$(CC) $(CFLAGS) -DTEST_NULL $(TEST_SRC) -L. -lasm -o $(TEST) && valgrind --leak-check=full ./$(TEST)

clean:
	rm -f $(OBJS)

fclean: clean
	rm -f $(NAME) $(TEST)

re: fclean all
