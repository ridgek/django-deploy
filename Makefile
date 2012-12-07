VENV := venv
REQS := requirements.txt
PKGS := packages.txt

DEBIAN := $(shell test -f '/etc/debian_version' && echo true)

$(VENV): $(VENV)/bin/activate
$(VENV)/bin/activate: $(REQS) .packages
	test -d $(VENV) || virtualenv $(VENV)
	. $(VENV)/bin/activate; pip install -Ur $(REQS)
	touch $(VENV)/bin/activate

.packages: $(PKGS)
    ifeq ($(DEBIAN),true)
	dpkg -s `xargs < $(PKGS)` > /dev/null || \
	    (sudo apt-get -q update; \
	     sudo apt-get -q install `xargs < $(PKGS)`)
	touch .packages
    else
	mkdir -p $(VENV)
	@echo "---------------------------------------------------------"
	@echo "Only Debian derivatives are supported."
	@echo "You must install the equivalent of the following packages"
	@echo "and 'touch .packages' before running make again."
	@echo "---------------------------------------------------------"
	@cat  $(PKGS)
	@echo "---------------------------------------------------------"
	@false
    endif

.PHONY: clean
clean:
	rm -rf $(VENV)
	rm .packages

