# pingscope
Measuring and graphing ping

## Versions

|Version|Summary|
|:--|:--|
|0.1.0|Release pingscope|

## Installation

`pip install pingscope`

## Usage
### pingscope
![](https://github.com/mskz-3110/pingscope/blob/main/images/usage.png)
```python
def test_pingscope_usage():
  dst = os.getenv("PINGSCOPE_DST")
  if dst is not None:
    pingFilePath = "./images/usage.ping"
    ps.Pingscope().save(pingFilePath, dst)
    ps.Pingscope().load(pingFilePath).to_figure_helper().write_image("./images/usage.png")
```
