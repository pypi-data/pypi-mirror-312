# 🤖 Botable
> Record and play keyboard and mouse clicks

[![Actions Status](https://github.com/ebonnal/botable/workflows/unittest/badge.svg)](https://github.com/ebonnal/botable/actions)
[![Actions Status](https://github.com/ebonnal/botable/workflows/PyPI/badge.svg)](https://github.com/ebonnal/botable/actions)

# install
```bash
pip install botable
```

# use
## as a lib
1. launch the recording:
```python
from botable import record, play

events = list(record())
```

2. then press some keys and do some clicks
3. press f1 to stop recording
4. play the recorded events:

```python
play(events, loops=10, rate=1.5)
```

## as a cli

1. launch the recording:
```bash
python -m botable record > ./events.py
```

2. then press some keys and do some clicks
3. press f1 to stop recording
4. play the recorded events:

```bash
cat ./events.py | python -m botable play --playback-loops 10 --playback-rate 1.5
```
