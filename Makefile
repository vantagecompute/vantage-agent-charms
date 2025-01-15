SHELL:= /bin/bash

qa:
	$(MAKE) -C vantage-agent qa
	$(MAKE) -C jobbergate-agent qa
	$(MAKE) -C license-manager-agent qa

format:
	$(MAKE) -C vantage-agent format
	$(MAKE) -C jobbergate-agent format
	$(MAKE) -C license-manager-agent format

charm:
	$(MAKE) -C vantage-agent charm
	$(MAKE) -C jobbergate-agent charm
	$(MAKE) -C license-manager-agent charm

clean:
	$(MAKE) -C vantage-agent clean
	$(MAKE) -C jobbergate-agent clean
	$(MAKE) -C license-manager-agent clean
