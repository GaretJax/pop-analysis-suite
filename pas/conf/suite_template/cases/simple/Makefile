MEASURE_NAME=$(EXEC)

run:
	$(call header,Running measure)

	@echo "\n 1. Starting measures and services"
	@pas measure start $(INDENT)
	@pas jobmgr start $(INDENT)
	@echo "    OK."

	@echo "\n 2. Running test case"
	@pas execute $(EXEC) $(INDENT)
	@echo "    OK."

	@echo "\n 3. Stopping measures and services"
	@pas jobmgr stop $(INDENT)
	@pas measure stop $(INDENT)
	@echo "    OK."

	@echo "\n 4. Collecting results"
	@pas measure collect $(MEASURE_NAME) $(INDENT)
	@echo "    OK."

	$(call done)


report:
	$(call header,Reporting measure)
	
	@echo "\n 1. Converting measures to xml"
	@pas report toxml $(MEASURE_NAME) $(INDENT)
	@echo "    OK."
	
	@echo "\n 2. Simplifying measures"
	@pas report simplify $(MEASURE_NAME) $(INDENT)
	@echo "    OK."

	@echo "\n 3. Decoding measures"
	@pas report decode $(MEASURE_NAME) $(INDENT)
	@echo "    OK."

	@echo "\n 4. Generating report"
	@pas report report $(MEASURE_NAME) $(INDENT)
	@echo "    OK."

include $(ENV_BASE)/conf/Makefile.base