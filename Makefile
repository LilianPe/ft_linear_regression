TARGET=values.json

all: init

init: $(TARGET)

$(TARGET):
	echo '{"theta0": 0, "theta1": 0, "min": 0, "rangeKm": 0}' > $(TARGET)

fclean:
	rm -rf $(TARGET)

re: fclean all
