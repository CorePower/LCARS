reinstall-user: uninstall-user install-user

install-user:
	pip install --user .

uninstall-user:
	-(yes | pip uninstall LCARS)

clean:

spotless: clean
	-rm *~
	-rm */*~
	-rm */*/*~
