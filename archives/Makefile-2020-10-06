date        = 2020-10-06
path        = ../plots
theta13     = $(path)/theta13/v4.1-neutrino2020
theta21     = $(path)/theta12/v1.0-neutrino2020
theta23     = $(path)/theta23/v1.0-neutrino2020
dm32        = $(path)/dm32/v4.1-neutrino2020
dm21        = $(path)/dm21/v1.0-neutrino2020
deltaCP     = $(path)/deltaCP/v2.0-neutrino2020
#nmo        =
#nmo_future =

base    = nuosc_comparison_$(date)
archive = $(base).zip

sources = $(theta13) \
		  $(theta12) \
		  $(theta23) \
		  $(dm21) \
		  $(dm32) \
		  $(deltaCP) \
		  $(nmo) \
		  $(nmo_future)

SHELL=fish
.ONESHELL:

$(archive): $(sources)
	set tmp (mktemp -d -p . -t $(base).XXXXXXX)
	pushd $$tmp
	for p in $(sources)
		set -l t (string join '-' (string split -r -m 2 / $$p)[-2..-1])
		ln -s ../$$p $$t
	end
	ls -l 
	apack ../$(archive) *
	popd
	command rm -rf $$tmp


