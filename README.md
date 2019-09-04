# Snail

Snail is a QGIS plugin allowing to monitor performances:

- CPU and RAM monitoring with or without a dedicated graphic
- RAM warning when a specified amount is exceeded

More functionalities will come in time.

<p align="center">
  <img width="400" src="https://github.com/pblottiere/snail/blob/master/docs/snail.png">
</p>


## Installation

Once you have installed `Snail` with the Plugin Manager tool in QGIS, a last
step is necessary to have a fully operational plugin. Indeed, some Python
modules are necessary and have to be installed.

Of course, the dependency may be installed manually with `pip`, `apt-get`,
`pacman` or others, but Snail provides an embedded solution too. Actually, if
a package is missing, then the next window will be opened:

<p align="center">
  <img width="400" src="https://github.com/pblottiere/snail/blob/master/docs/deps.png">
</p>

If you click on `Yes`, the `pip install -user` command will be runned to
install lacking dependencies. It has been tested on Windows and Archlinux. Once
dependencies have been installed, you have to restart QGIS to use Snail.


## Settings

You can open a settings window through the `Snail` menu. It allows you to
customize some colors as well as defining an amount of RAM above which a
warning message is displayed periodically.

<p align="center">
  <img width="400" src="https://github.com/pblottiere/snail/blob/master/docs/settings.png">
</p>
