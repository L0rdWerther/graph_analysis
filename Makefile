CC = gcc
CFLAGS = -std=c11 -O2 -Wall
SRCS = main.c grafo.c
OBJS = $(SRCS:.c=.o)
TARGET = graph

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $(TARGET) $(OBJS)

.c.o:
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) $(TARGET)

.PHONY: all clean
