# lhereader
[![PyPI version](https://badge.fury.io/py/lhereader.svg)](https://badge.fury.io/py/lhereader)

A Python module to read LHE files. Originally by [diptaparna](https://github.com/diptaparna/lhereader), significantly rewritten by me. No dependency on ROOT, requires python version >= 3.6.

Usage example:

```python
import numpy as np
from lhereader import LHEReader


reader = LHEReader('path/to/file.lhe')

# Mediator mass in each event
mmed = []
counter = 0
for iev, event in enumerate(reader):
    # Find DM particles
    dm = filter(lambda x: abs(x.pdgid)== 52, event.particles)

    # Sum over all DM four-momenta in the event
    combined_p4 = None
    for p4 in map(lambda x: x.p4(), dm):
        if combined_p4:
            combined_p4 += p4
        else:
            combined_p4 = p4
    mmed.append(combined_p4.mass)

print(f'Mean mediator mass: {np.mean(mmed)}')
print(f'Median mediator mass: {np.median(mmed)}')
```