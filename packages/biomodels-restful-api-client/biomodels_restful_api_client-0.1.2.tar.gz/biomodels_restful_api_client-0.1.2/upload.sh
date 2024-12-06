python -m build
python -m twine upload -u __token__ \
  -p pypi-AgEIcHlwaS5vcmcCJGUyNGEyNWI4LTJhZTQtNDg1OC05ZGZkLTNlNTJlMTliMjEzZQACKlszLCJhZDM0NzZhMC0wNWU5LTQ2YzgtOWFkMC0xYTJhYzJkN2E1ZWIiXQAABiCLAuhtHfy9BivALGsa9zKbUwzAOUi2smE-A3k_zmaFQw \
  --repository pypi dist/* --verbose
