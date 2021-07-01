SHELL := /bin/sh
BUILD_DIR := $(PWD)/gamer_build_static
export FETK_INCLUDE := $(BUILD_DIR)/include
export FETK_LIBRARY := $(BUILD_DIR)/lib

UNAME := $(shell uname)

CPPFLAGS := -std=c++11

ifeq ($(UNAME), Linux)
	export PYTHON := /usr/bin/python3.9
	export LD_LIBRARY_PATH := $(BUILD_DIR)/lib:$(LD_LIBRARY_PATH)
	LDFLAGS = "-L/usr/local/lib/"
	PYTHON_MODULE_BUILD_DIR = $(BUILD_DIR)/lib/python3.9/site-packages/gamer
	INSTALL_DIR = ..
	PKG_DIR = /Applications/Blender.app/Contents/Resources/2.93  # fixme
else
	# macos
#	export PYTHON := /usr/local/bin/python3.5
	export PYTHON := /Library/Frameworks/Python.framework/Versions/3.9/bin/python3.9
	export DYLD_LIBRARY_PATH := $(BUILD_DIR)/lib:$(DYLD_LIBRARY_PATH)
#	LDFLAGS := -L/usr/local/Cellar/python3/3.5.2_3/Frameworks/Python.framework/Versions/3.5/lib
#	LDFLAGS := -L/opt/local/Library/Frameworks/Python.framework/Versions/3.5/lib
	LDFLAGS := -L/Library/Frameworks/Python.framework/Versions/3.9/lib
	PYTHON_MODULE_BUILD_DIR = $(BUILD_DIR)/lib/python3.9/site-packages/gamer
	INSTALL_DIR := ../
	PKG_DIR = /Applications/Blender.app/Contents/Resources/2.93
endif


all: maloc gamer gamer_swig gamer_tools

.PHONY: maloc gamer gamer_swig upy

maloc:
	@ cd maloc ; CPPFLAGS=-std=c++11 ./configure --enable-static --prefix=$(BUILD_DIR) ; $(MAKE) ; $(MAKE) install

gamer: maloc
	@ cd gamer ; CPPFLAGS=-std=c++11 ./configure --enable-static --prefix=$(BUILD_DIR) ; $(MAKE) ; $(MAKE) install

gamer_swig: gamer
	echo "LDFLAGS is set to:  " $(LDFLAGS)
	echo "LD_LIBRARY_PATH is set to:  " $(LD_LIBRARY_PATH)
	@ cd gamer/swig ; ./configure --enable-static --prefix=$(BUILD_DIR) LDFLAGS=$(LDFLAGS) ; $(MAKE) ; $(MAKE) install

gamer_tools: gamer
	@ cd gamer/tools/ImproveSurfMesh ; ./configure --prefix=$(BUILD_DIR) ; $(MAKE) ; $(MAKE) install
	@ cd gamer/tools/MolecularMesh ; ./configure --prefix=$(BUILD_DIR) ; $(MAKE) ; $(MAKE) install
	@ cd gamer/tools/GenerateMesh ; ./configure --prefix=$(BUILD_DIR) ; $(MAKE) ; $(MAKE) install


install:
	@ mkdir -p $(INSTALL_DIR)/scripts/addons
	@ mkdir -p $(INSTALL_DIR)/scripts/modules
	@ cp -r ./gamer_addon $(INSTALL_DIR)/scripts/addons/
	@ cp -r $(PYTHON_MODULE_BUILD_DIR) $(INSTALL_DIR)/scripts/modules/

pkg:
	@ mkdir -p $(PKG_DIR)/scripts/addons
	@ mkdir -p $(PKG_DIR)/scripts/modules
	@ cp -r ./gamer_addon $(PKG_DIR)/scripts/addons/
	@ cp -r $(PYTHON_MODULE_BUILD_DIR) $(PKG_DIR)/scripts/modules/

clean:
	@ cd maloc; $(MAKE) -k clean
	@ cd gamer; $(MAKE) -k clean
	@ cd gamer/swig; $(MAKE) -k clean
	@ cd gamer/tools/ImproveSurfMesh; $(MAKE) -k clean
	@ cd gamer/tools/MolecularMesh; $(MAKE) -k clean
	@ cd gamer/tools/GenerateMesh; $(MAKE) -k clean

distclean:
	rm -rf $(BUILD_DIR)
	@ $(MAKE) -k clean
