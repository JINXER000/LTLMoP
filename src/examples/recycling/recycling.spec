# This is a specification definition file for the LTLMoP toolkit.
# Format details are described at the beginning of each section below.


======== SETTINGS ========

Actions: # List of action propositions and their state (enabled = 1, disabled = 0)
pickup, 1
drop, 1
light, 1

CompileOptions:
convexify: True
parser: slurp
fastslow: False
decompose: True
use_region_bit_encoding: True

CurrentConfigName:
Nao

Customs: # List of custom propositions

RegionFile: # Relative path of region description file
recycling.regions

Sensors: # List of sensor propositions and their state (enabled = 1, disabled = 0)


======== SPECIFICATION ========

RegionMapping: # Mapping between region names and their decomposed counterparts
bedroom = p3
hall = p2
office = p1
others = 

Spec: # Specification in structured English
Start in the hall with light.
The paper is in the hall.
Activate your light in the hall.
#Don't go in the bedroom.
Don't activate your light in the bedroom.
Carry the paper to the office.

